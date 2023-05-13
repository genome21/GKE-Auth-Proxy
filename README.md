# GKE Auth Proxy

The `gke_auth_proxy.sh` script creates a secure tunnel from your local machine to a remote Google Kubernetes Engine (GKE) cluster through a bastion host. It allows you to run `kubectl` commands on the GKE cluster as if you were running them locally. 

This script is particularly useful when you want to access a private GKE cluster that isn't directly accessible from the internet. By connecting through a bastion host, you can securely manage your GKE cluster without exposing it to potential threats.

## Prerequisites

Before running the script, you need to have the following:

1. A Google Cloud Platform (GCP) account.
2. A GKE cluster set up in your GCP account.
3. A bastion host with an external IP address.
4. `gcloud` and `kubectl` installed on the bastion host.

## Usage

1. Download the script to your bastion host:

    ```bash
    wget https://raw.githubusercontent.com/genome21/GKE-Auth-Proxy/main/gke_auth_proxy.sh
    ```

2. Make the script executable:

    ```bash
    chmod +x gke_auth_proxy.sh
    ```

3. Run the script:

    ```bash
    ./gke_auth_proxy.sh
    ```

    The script will prompt you to enter the following information:

    - Your GKE cluster name
    - Your GKE zone
    - Your GCP project ID
    - The local port for the secure tunnel
    - The remote port for the secure tunnel
    - The username for the bastion host
    - The external IP of the bastion host

    If you want to run the script as a startup script on the bastion host, add it to your `/etc/rc.local` or similar file depending on your system's initialization system.

## Note

The script will check if `gcloud` and `kubectl` are installed on your bastion host. If not, it will install them for you. 

If the script is run for the first time or the required variables are not set, it will prompt you to enter them. These variables will then be set globally for all users and will persist through system reboots.

## Caution

Keep the security of your bastion host in mind. Anyone with access to the bastion host will have access to the GKE cluster. Therefore, only give access to trusted individuals and always follow best practices for securing your systems.
