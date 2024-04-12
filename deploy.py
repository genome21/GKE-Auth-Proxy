import streamlit as st
from google.cloud import container_v1, compute_v1
from google.api_core.exceptions import PermissionDenied

# Initialize the GKE and Compute clients
gke_client = container_v1.ClusterManagerClient()
compute_client = compute_v1.NetworksClient()
subnetworks_client = compute_v1.SubnetworksClient()

# Create a Streamlit app
st.title("GKE Auth Proxy Setup")

# Create a text input for the project ID
project_id = st.text_input("GCP Project ID")

# Function to list VPCs
def list_vpcs(project_id):
    if not project_id:
        return []
    try:
        vpcs = compute_client.list(project=project_id)
        return [vpc.name for vpc in vpcs]
    except PermissionDenied:
        return []

# Function to list regions
def list_regions(project_id):
    if not project_id:
        return []
    try:
        regions = compute_v1.RegionsClient().list(project=project_id)
        return [region.name for region in regions]
    except PermissionDenied:
        return []

# Function to list subnets for a given region and VPC
def list_subnets(project_id, region, vpc_name):
    if not project_id or not region or not vpc_name:
        return []
    try:
        subnets = subnetworks_client.list(project=project_id, region=region)
        return [subnet.name for subnet in subnets if subnet.network.endswith(f"/{vpc_name}")]
    except PermissionDenied:
        return []

# Function to list GKE clusters in a given region
def list_gke_clusters(project_id, region):
    if not project_id or not region:
        return []
    try:
        parent = f"projects/{project_id}/locations/{region}"
        clusters = gke_client.list_clusters(parent=parent).clusters
        return [cluster.name for cluster in clusters]
    except PermissionDenied:
        return []

# Check if the user has access to the project and list VPCs
vpc_names = list_vpcs(project_id)

if vpc_names:
    # User has access to the project, show the rest of the form
    selected_vpc = st.selectbox("Select a VPC", vpc_names)
    region_names = list_regions(project_id)
    selected_region = st.selectbox("Select a Region", region_names)
    subnet_names = list_subnets(project_id, selected_region, selected_vpc)
    selected_subnet = st.selectbox("Select a Subnet", subnet_names)

    # List GKE clusters in the selected region
    cluster_names = list_gke_clusters(project_id, selected_region)
    if cluster_names:
        selected_cluster = st.selectbox("Select a GKE Cluster", cluster_names)
    else:
        st.error("No GKE clusters found in the selected region.")

    # Check if the bastion host exists
    bastion_host_exists = st.checkbox("Bastion Host Created")

    if not bastion_host_exists:
        # Prompt the user to create a bastion host on their own
        st.write("Please create a GCP-native compute instance to be used as the bastion host on your own. This app will not create one for you at this time.")
    else:
        # Prompt for ports and username once the bastion host exists
        local_port = st.text_input("Local Port for Secure Tunnel", "8080")
        remote_port = st.text_input("Remote Port for Secure Tunnel", "443")

        # If the user has submitted the form, provide instructions and code to run on the bastion host
        if st.button("Submit"):
            st.write("Please run the following commands on your bastion host to set up the GKE Auth Proxy:")
            code = f"""
            # Set the project
            gcloud config set project {project_id}

            # Get the credentials for the GKE cluster
            gcloud container clusters get-credentials {selected_cluster} --region {selected_region}

            # Start the kubectl proxy as a background process
            nohup kubectl proxy --port={remote_port} > /dev/null 2>&1 &
            """
            st.code(code, language='bash')
            st.write("Once you have run these commands on your bastion host, the GKE Auth Proxy should be set up and ready to use.")
else:
    # User does not have access to the project
    st.error("You do not have access to the specified project or it does not exist.")
