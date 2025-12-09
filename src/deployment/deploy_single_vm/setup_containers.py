import pulumi
from pulumi import ResourceOptions
from pulumi_command import remote
import pulumi_docker as docker


def setup_containers(connection, configure_docker, project, instance_ip, ssh_user):
    """
    Setup and deploy all application containers:
    - Copy GCP secrets to the VM
    - Create Docker network
    - Create persistent directories
    - Deploy frontend container
    - Deploy API service container

    Args:
        connection: SSH connection configuration
        configure_docker: The Docker configuration command (dependency)
        project: GCP project ID

    Returns:
        remote.Command: The last container deployment command (for dependency chaining)
    """
    # Get image references from deploy_images stack
    images_stack = pulumi.StackReference("organization/deploy-images/dev")
    # Get the image tags (these are arrays, so we take the first element)
    api_service_tag = images_stack.get_output("tummyai-app-api-service-tags")
    frontend_tag = images_stack.get_output("tummyai-app-frontend-react-tags")

    # Setup GCP secrets for containers
    copy_secrets = remote.Command(
        "copy-gcp-secrets",
        connection=connection,
        create="""
            sudo mkdir -p /srv/secrets
            sudo chmod 0755 /srv/secrets
        """,
        opts=ResourceOptions(depends_on=[configure_docker]),
    )

    upload_service_account = remote.CopyToRemote(
        "upload-service-account-key",
        connection=connection,
        source=pulumi.FileAsset("/secrets/gcp-service.json"),
        remote_path="/tmp/gcp-service.json",
        opts=ResourceOptions(depends_on=[copy_secrets]),
    )

    move_secrets = remote.Command(
        "move-secrets-to-srv",
        connection=connection,
        create="""
            sudo mv /tmp/gcp-service.json /srv/secrets/gcp-service.json
            sudo chmod 0644 /srv/secrets/gcp-service.json
            sudo chown root:root /srv/secrets/gcp-service.json
            gcloud auth activate-service-account --key-file /srv/secrets/gcp-service.json
            gcloud auth configure-docker us-docker.pkg.dev --quiet
        """,
        opts=ResourceOptions(depends_on=[upload_service_account]),
    )

    # Create directories on persistent disk
    create_dirs = remote.Command(
        "create-persistent-directories",
        connection=connection,
        create="""
            sudo mkdir -p /mnt/disk-1/persistent
            sudo mkdir -p /mnt/disk-1/chromadb
            sudo chmod 0777 /mnt/disk-1/persistent
            sudo chmod 0777 /mnt/disk-1/chromadb
        """,
        opts=ResourceOptions(depends_on=[move_secrets]),
    )

    # Set up Docker provider with SSH credentials for remote access
    docker_provider = docker.Provider(
        "docker-provider",
        host=instance_ip.apply(lambda ip: f"ssh://{ssh_user}@{ip}"),
        # SSH options to handle key-based authentication and suppress host checking
        ssh_opts=[
            "-i",
            "/secrets/ssh-key-deployment",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
        ],
        # Authentication for Google Container Registry / Artifact Registry
        registry_auth=[
            {
                "address": "us-docker.pkg.dev",
            }
        ],
        opts=ResourceOptions(depends_on=[create_dirs]),
    )

    # Create Docker network
    docker_network = docker.Network(
        "docker-network",
        name="appnetwork",
        driver="bridge",
        opts=ResourceOptions(provider=docker_provider),
    )

    # Deploy containers
    # Frontend
    deploy_frontend = docker.Container(  # noqa: F841
        "deploy-frontend-container",
        image=frontend_tag.apply(lambda tags: tags[0]),
        name="frontend",
        ports=[
            docker.ContainerPortArgs(
                internal=3000,  # Container port
                external=3000,  # Host port
            )
        ],
        networks_advanced=[
            docker.ContainerNetworksAdvancedArgs(
                name=docker_network.name,
            ),
        ],
        opts=ResourceOptions(
            provider=docker_provider,
            depends_on=[docker_network, create_dirs],
        ),
    )

    # API Service
    deploy_api_service = docker.Container(  # noqa: F841
        "deploy-api-service-container",
        image=api_service_tag.apply(lambda tags: tags[0]),
        name="api-service",
        restart="always",
        ports=[
            docker.ContainerPortArgs(
                internal=9000,
                external=9000,
            )
        ],
        envs=[
            "GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json",
            f"GCP_PROJECT={project}",
            "GCS_BUCKET_NAME=tummyai-app-models",
        ],
        volumes=[
            docker.ContainerVolumeArgs(
                host_path="/mnt/disk-1/persistent",
                container_path="/persistent",
                read_only=False,
            ),
            docker.ContainerVolumeArgs(
                host_path="/srv/secrets",
                container_path="/secrets",
                read_only=False,
            ),
        ],
        networks_advanced=[
            docker.ContainerNetworksAdvancedArgs(
                name=docker_network.name,
            )
        ],
        opts=ResourceOptions(
            provider=docker_provider,
        ),
    )

    return docker_provider, docker_network
