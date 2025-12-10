import pulumi
import pulumi_gcp as gcp
from pulumi import ResourceOptions, Output
import pulumi_kubernetes as k8s
import pulumi_command as command
import yaml

base_config = pulumi.Config()
service_account_email = pulumi.Config("security").get("gcp_service_account_email")
ksa_service_account_email = pulumi.Config("security").get("gcp_ksa_service_account_email")
initial_node_count = 1
machine_type = "n2d-standard-2"
machine_disk_size = 50


def create_cluster(project, zone, network, subnet, app_name):
    # Get existing GKE cluster instead of creating a new one
    cluster = gcp.container.get_cluster(
        name=f"{app_name}-cluster",
        location=zone,
        project=project
    )

    # Note: We don't need to manage the node pool separately when using get_cluster
    # The cluster data already includes node pool information
    node_pool = None  # Not needed when referencing existing cluster

    # -----------------------------
    # Kubeconfig for k8s provider
    # -----------------------------
    k8s_info = pulumi.Output.all(cluster.name, cluster.endpoint, cluster.master_auths)

    def make_kubeconfig(info):
        cluster_name, endpoint, master_auths = info
        # Get the first master_auth from the list
        master_auth = master_auths[0] if master_auths else {}
        context_name = f"{project}_{zone}_{cluster_name}"

        kubeconfig = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": context_name,
                    "cluster": {
                        "certificate-authority-data": master_auth["cluster_ca_certificate"],
                        "server": f"https://{endpoint}",
                    },
                }
            ],
            "contexts": [
                {
                    "name": context_name,
                    "context": {"cluster": context_name, "user": context_name},
                }
            ],
            "current-context": context_name,
            "users": [
                {
                    "name": context_name,
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1beta1",
                            "command": "gke-gcloud-auth-plugin",
                            "installHint": "Install gke-gcloud-auth-plugin for use with kubectl",
                            "provideClusterInfo": True,
                            "interactiveMode": "Never",
                        }
                    },
                }
            ],
        }

        # Generate YAML
        result = yaml.dump(kubeconfig, default_flow_style=False)

        # Debug
        # print("=" * 80)
        # print("Generated kubeconfig:")
        # print(result)
        # print("=" * 80)

        return result

    cluster_kubeconfig = k8s_info.apply(make_kubeconfig)

    # Create Kubernetes provider using GKE cluster credentials to deploy K8s resources
    k8s_provider = k8s.Provider(
        "gke_k8s_v2",
        kubeconfig=cluster_kubeconfig,  # Use the kubeconfig generated from the GKE cluster
    )

    # Create Kubernetes namespace for application deployments
    namespace = k8s.core.v1.Namespace(
        f"{app_name}-namespace",
        metadata={"name": f"{app_name}-namespace"},
        opts=ResourceOptions(provider=k8s_provider),
    )

    # --- Kubernetes Service Account (KSA) with Workload Identity annotation ---
    # KSA = Kubernetes Service Account - an identity used by pods running in K8s to authenticate
    # This allows pods to securely access GCP services without embedding credentials
    ksa_name = "api-ksa"
    api_ksa = k8s.core.v1.ServiceAccount(  # noqa: F841
        "api-ksa",
        metadata=k8s.meta.v1.ObjectMetaArgs(
            name=ksa_name,
            namespace=namespace.metadata["name"],
            annotations={
                # Critical: map KSA → GSA (Google Service Account) for Workload Identity
                "iam.gke.io/gcp-service-account": f"{ksa_service_account_email}",
            },
        ),
        opts=ResourceOptions(provider=k8s_provider),
    )

    # --- Bind KSA identity to the GSA (Workload Identity user) ---
    # This IAM binding allows the KSA to impersonate the GSA and use its GCP permissions
    # member format: serviceAccount:<PROJECT_ID>.svc.id.goog[<namespace>/<ksa_name>]
    project_id = gcp.config.project
    wi_member = Output.concat(  # Build the Workload Identity member string
        "serviceAccount:",
        project_id,
        ".svc.id.goog[",
        namespace.metadata["name"],
        "/",
        ksa_name,
        "]",
    )

    # Construct the full GSA resource ID
    gsa_full_id = pulumi.Output.concat("projects/", project_id, "/serviceAccounts/", f"{ksa_service_account_email}")

    # Grant the KSA permission to act as the GSA
    gsa_wi_binding_strict = gcp.serviceaccount.IAMMember(  # noqa: F841
        "api-gsa-wi-user",
        service_account_id=gsa_full_id,
        role="roles/iam.workloadIdentityUser",  # Required role for Workload Identity
        member=wi_member,  # The KSA that will impersonate this GSA
    )

    # Connect to the cluster
    connect_k8s_command = command.local.Command(  # noqa: F841
        "connect-k8s-command",
        create=Output.concat(
            "gcloud container clusters get-credentials ", cluster.name, f" --zone {zone} --project {project}"
        ),
    )

    return cluster, namespace, k8s_provider, ksa_name
