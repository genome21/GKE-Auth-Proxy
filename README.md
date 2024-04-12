# GKE Auth Proxy Setup Guide

## Introduction

Securing access to Google Kubernetes Engine (GKE) clusters is a critical aspect of cloud infrastructure management. Organizations often choose private GKE clusters for their security advantages, but this limits their direct accessibility from the internet, posing a challenge for remote management.

The need for a secure communication pathway is clear. While using a bastion host as an intermediary is common, the complexity of setting up and maintaining a secure tunnel to the GKE cluster can be overwhelming.

So, how can we simplify secure access to private GKE clusters? The aim is to enable seamless `kubectl` command execution as if the clusters were directly accessible, without compromising on security.

Enter the GKE Auth Proxy. This tool streamlines the creation of a secure tunnel from your local machine to a remote GKE cluster through a bastion host. It makes the setup process straightforward and ensures secure cluster management.

## Prerequisites

Before using the GKE Auth Proxy, ensure that you have the following:

1. **Google Cloud Platform (GCP) account:** A valid account with access to GKE and Compute Engine services.
2. **GKE cluster:** A GKE cluster set up in your GCP account. This can be a private cluster that is not directly accessible from the internet.
3. **Bastion host:** A Compute Engine instance with either an external IP address or internal access via VPN, Shared VPC, or Interconnect. This instance will act as the intermediary for secure communication.

## Setup Instructions

There are two methods to set up the GKE Auth Proxy: using a bash script or a Python script. Choose the method that best fits your workflow.

### Bash Script Method

1. **Download the script:** Obtain the bash script from the repository and make it executable:

    ```bash
    wget https://raw.githubusercontent.com/genome21/GKE-Auth-Proxy/main/gke_auth_proxy.sh
    chmod +x gke_auth_proxy.sh
    ```

2. **Run the script:** Execute the script and provide the required information when prompted:

    ```bash
    ./gke_auth_proxy.sh
    ```

    - **GKE Cluster Name (CLUSTER_NAME):** The name of your GKE cluster.
    - **GCP Zone (ZONE):** The zone where your GKE cluster is located.
    - **GCP Project ID (PROJECT_ID):** The ID of your GCP project.
    - **Local Port (LOCAL_PORT):** A local port on your machine for the secure tunnel (e.g., 8080).
    - **Remote Port (REMOTE_PORT):** The remote port on the GKE control plane (usually 443).
    - **Username (USERNAME):** The username for SSH access to the bastion host.
    - **Bastion Host IP (BASTION_HOST):** The external IP address of the bastion host.

### Python Script Method (Streamlit App)

1. **Clone the repository:** Get the Python script and related files:

    ```bash
    git clone https://github.com/genome21/GKE-Auth-Proxy.git
    cd GKE-Auth-Proxy
    ```

2. **Install dependencies:** Use the provided `requirements.txt` to install necessary packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app:** Start the app and follow the interactive prompts:

    ```bash
    streamlit run deploy.py
    ```

    The app will guide you through selecting your GKE cluster, VPC, subnet, and region. It will then generate the commands you need to run on your bastion host to set up the GKE Auth Proxy.

## Security Considerations

- **Bastion Host Security:** Ensure that your bastion host is secured with appropriate firewall rules and access controls. Limit access to the bastion host to trusted individuals and follow best practices for system security.
- **Credential Management:** Handle GCP credentials and service account keys with care. Use IAM roles and permissions to grant the least privilege necessary for the tasks.

## Conclusion

The GKE Auth Proxy simplifies the process of securely accessing a private GKE cluster through a bastion host. By following the setup instructions provided in this guide, you can establish a secure tunnel to manage your GKE cluster remotely without exposing it to potential threats.