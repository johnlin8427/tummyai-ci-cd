import pulumi
import pulumi_gcp as gcp  # noqa: F401
from pulumi import StackReference, ResourceOptions, Output  # noqa: F401
import pulumi_kubernetes as k8s


def setup_containers(project, namespace, k8s_provider, ksa_name, app_name):
    # Get image references from deploy_images stack
    # For local backend, use: "organization/project/stack"
    images_stack = pulumi.StackReference("organization/deploy-images/dev")
    # Get the image tags (these are arrays, so we take the first element)
    api_service_tag = images_stack.get_output("tummyai-app-api-service-tags")
    frontend_tag = images_stack.get_output("tummyai-app-frontend-react-tags")

    # General persistent storage for application data (5Gi)
    persistent_pvc = k8s.core.v1.PersistentVolumeClaim(
        "persistent-pvc",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="persistent-pvc",
            namespace=namespace.metadata.name,
        ),
        spec=k8s.core.v1.PersistentVolumeClaimSpecArgs(
            access_modes=["ReadWriteOnce"],  # Single pod read/write access
            resources=k8s.core.v1.VolumeResourceRequirementsArgs(
                requests={"storage": "5Gi"},  # Request 5GB of persistent storage
            ),
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider, depends_on=[namespace]),
    )

    # --- Frontend Deployment ---
    # Creates pods running the frontend container on port 3000
    # ram 1.7 gb
    frontend_deployment = k8s.apps.v1.Deployment(
        "frontend",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="frontend",
            namespace=namespace.metadata.name,
        ),
        spec=k8s.apps.v1.DeploymentSpecArgs(
            selector=k8s.meta.v1.LabelSelectorArgs(
                match_labels={"run": "frontend"},  # Select pods with this label
            ),
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(
                    labels={"run": "frontend"},  # Label assigned to pods
                ),
                spec=k8s.core.v1.PodSpecArgs(
                    containers=[
                        k8s.core.v1.ContainerArgs(
                            name="frontend",
                            image=frontend_tag.apply(
                                lambda tags: tags[0]
                            ),  # Container image (placeholder - needs to be filled)
                            image_pull_policy="IfNotPresent",  # Use cached image if available
                            ports=[
                                k8s.core.v1.ContainerPortArgs(
                                    container_port=3000,  # Frontend app listens on port 3000
                                    protocol="TCP",
                                )
                            ],
                            resources=k8s.core.v1.ResourceRequirementsArgs(
                                requests={"cpu": "250m", "memory": "2Gi"},
                                limits={"cpu": "500m", "memory": "3Gi"},
                            ),
                        ),
                    ],
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider, depends_on=[namespace]),
    )

    frontend_service = k8s.core.v1.Service(
        "frontend-service",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="frontend",
            namespace=namespace.metadata.name,
        ),
        spec=k8s.core.v1.ServiceSpecArgs(
            type="ClusterIP",  # Internal only - not exposed outside cluster
            ports=[
                k8s.core.v1.ServicePortArgs(
                    port=3000,  # Service port
                    target_port=3000,  # Container port to forward to
                    protocol="TCP",
                )
            ],
            selector={"run": "frontend"},  # Route traffic to pods with this label
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider, depends_on=[frontend_deployment]),
    )

    # api_service Deployment
    api_deployment = k8s.apps.v1.Deployment(
        "api",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="api",
            namespace=namespace.metadata.name,
        ),
        spec=k8s.apps.v1.DeploymentSpecArgs(
            selector=k8s.meta.v1.LabelSelectorArgs(
                match_labels={"run": "api"},
            ),
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(
                    labels={"run": "api"},
                ),
                spec=k8s.core.v1.PodSpecArgs(
                    service_account_name=ksa_name,  # Use KSA for Workload Identity (GCP access)
                    security_context=k8s.core.v1.PodSecurityContextArgs(
                        fs_group=1000,
                    ),
                    volumes=[
                        k8s.core.v1.VolumeArgs(
                            name="persistent-vol",
                            persistent_volume_claim=k8s.core.v1.PersistentVolumeClaimVolumeSourceArgs(
                                claim_name=persistent_pvc.metadata.name,  # Temporary storage (lost on restart)
                            ),
                        )
                    ],
                    containers=[
                        k8s.core.v1.ContainerArgs(
                            name="api",
                            image=api_service_tag.apply(
                                lambda tags: tags[0]
                            ),  # API container image (placeholder - needs to be filled)
                            image_pull_policy="IfNotPresent",
                            ports=[
                                k8s.core.v1.ContainerPortArgs(
                                    container_port=9000,  # API server port
                                    protocol="TCP",
                                )
                            ],
                            volume_mounts=[
                                k8s.core.v1.VolumeMountArgs(
                                    name="persistent-vol",
                                    mount_path="/persistent",  # Temporary file storage
                                )
                            ],
                            env=[
                                k8s.core.v1.EnvVarArgs(
                                    name="GCS_BUCKET_NAME",
                                    value="tummyai-app-models",  # GCS bucket for ML models
                                ),
                                k8s.core.v1.EnvVarArgs(
                                    name="GCP_PROJECT",
                                    value=project,
                                ),
                                k8s.core.v1.EnvVarArgs(
                                    name="ROOT_PATH",
                                    value="/api-service",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(
            provider=k8s_provider,
        ),
    )

    # api_service Service
    api_service = k8s.core.v1.Service(
        "api-service",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name="api",
            namespace=namespace.metadata.name,
        ),
        spec=k8s.core.v1.ServiceSpecArgs(
            type="ClusterIP",  # Internal only
            ports=[
                k8s.core.v1.ServicePortArgs(
                    port=9000,
                    target_port=9000,
                    protocol="TCP",
                )
            ],
            selector={"run": "api"},
        ),
        opts=pulumi.ResourceOptions(provider=k8s_provider, depends_on=[api_deployment]),
    )

    return frontend_service, api_service
