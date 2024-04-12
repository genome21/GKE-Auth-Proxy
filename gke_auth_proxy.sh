#!/bin/bash

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "gcloud could not be found, installing..."
    # Download and install Google Cloud SDK
    curl https://sdk.cloud.google.com | bash
    # Initialize the Google Cloud SDK
    exec -l $SHELL
    gcloud init
else
    echo "gcloud is installed"
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl could not be found, installing..."
    # Install kubectl
    gcloud components install kubectl
else
    echo "kubectl is installed"
fi

# Prompt for variable values if they're not already set
if [ -z ${GKE_CLUSTER_NAME+x} ]; then read -p "Enter your GKE cluster name: " GKE_CLUSTER_NAME; fi
if [ -z ${ZONE+x} ]; then read -p "Enter your GKE zone: " ZONE; fi
if [ -z ${PROJECT_ID+x} ]; then read -p "Enter your GCP project ID: " PROJECT_ID; fi
if [ -z ${LOCAL_PORT+x} ]; then read -p "Enter the local port for the secure tunnel: " LOCAL_PORT; fi
if [ -z ${REMOTE_PORT+x} ]; then REMOTE_PORT="443"; fi
if [ -z ${USERNAME+x} ]; then read -p "Enter the username for the bastion host: " USERNAME; fi
if [ -z ${BASTION_HOST+x} ]; then read -p "Enter the external IP of the bastion host: " BASTION_HOST; fi

# Write the variables to gke_auth_proxy_vars.sh
cat > /etc/profile.d/gke_auth_proxy_vars.sh <<EOF
#!/bin/bash

export GKE_CLUSTER_NAME="$GKE_CLUSTER_NAME"
export ZONE="$ZONE"
export PROJECT_ID="$PROJECT_ID"
export LOCAL_PORT="$LOCAL_PORT"
export REMOTE_PORT="$REMOTE_PORT"
export USERNAME="$USERNAME"
export BASTION_HOST="$BASTION_HOST"
EOF

chmod +x /etc/profile.d/gke_auth_proxy_vars.sh

# Authenticate with gcloud
gcloud auth login

# Set the project in gcloud
gcloud config set project $PROJECT_ID

# Get the credentials for the GKE cluster
gcloud container clusters get-credentials $GKE_CLUSTER_NAME --zone $ZONE

# Start the proxy
kubectl proxy --port=8080 &
sleep 5

# Set up the secure tunnel
nohup ssh -N -L ${LOCAL_PORT}:localhost:${REMOTE_PORT} ${USERNAME}@${BASTION_HOST} &
