import pulumi
import pulumi_gcp as gcp


def create_network(region, app_name):
    # Get GCP project from config
    gcp_config = pulumi.Config("gcp")
    project = gcp_config.get("project")

    # Get existing VPC network instead of creating a new one
    # This avoids the "already exists" error
    network = gcp.compute.get_network(
        name=f"{app_name}-vpc",
        project=project
    )

    # Get existing subnet instead of creating a new one
    subnet = gcp.compute.get_subnetwork(
        name=f"{app_name}-subnet",
        project=project,
        region=region
    )

    # Get existing Cloud Router instead of creating a new one
    router = gcp.compute.get_router(
        name=f"{app_name}-router",
        network=network.name,
        project=project,
        region=region
    )

    # Get existing Cloud NAT instead of creating a new one
    nat = gcp.compute.get_router_nat(
        name=f"{app_name}-nat",
        router=router.name,
        project=project,
        region=region
    )

    return network, subnet, router, nat
