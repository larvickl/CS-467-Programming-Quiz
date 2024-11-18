# Instructions

## Prerequisites
Must have the following:
* Google Cloud account with billing enabled.
* Installed Docker and Git locally.
* Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

## Enable Google Cloud Services:
Enable the following services for your project:
* Billing
* IAM Admin
* Compute Engine
* Cloud Storage
* Cloud Run
* SQL

## IAM Setup
1. Navigate to IAM & Admin in the Google Cloud Console.
2. Add project principals by email.
3. Assign appropriate roles (e.g., Viewer, Editor, or Owner).
4. Notify principals separately about their addition and include the project name.

## Compute Engine Setup
Create a VM instance:
* Set the region and zone as appropriate for your project.
* Configure VM instance settings (e.g., machine type, disk size).

## Cloud Storage Setup
Create a bucket for data storage:
* Assign a unique name to the bucket.
* Choose appropriate storage class and location settings.

## SQL
Create a new SQL instance:
* Database type: MySQL.
* SQL Edition: Choose based on your project requirements.
* Instance ID: Follow these naming conventions:
    * Use only lowercase alphanumeric characters and dashes (-).
    * Cannot begin or end with a dash.
    * Maximum length: 63 characters.
* Password: Set a root password or leave it empty.
* Configuration: Assign a Public IP as needed.

## Cloud Run
Install Google Cloud SDK
Follow [these instructions](https://cloud.google.com/sdk/docs/install) to install the Google Cloud SDK.

Run: `gcloud init`
Set default project:
`gcloud config set project PROJECT_ID`
where PROJECT_ID should be replaced with the ID of your project.

Enable the Cloud Run Admin API and the Cloud Build API:
`gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com`

Create an Artifact Registry repository:
  `gcloud artifacts repositories create quiz_image \
        --repository-format=docker \
        --location=REGION \
        --immutable-tags \
        --async`

## To use Google Cloud SDK Locally:
Run `gcloud init` to initialize Google Cloud SDK.
Authenticate to the project using `gcloud auth login`.
(Optional) To set the default project, use the command: `gcloud config set project PROJECT_ID`.

To make sure that Docker congifuration and functionality is enabled for the project, use the following command:
`gcloud auth configure-docker`

## Using Google SDK Locally
Build locally:
`docker build -t gcr.io/PROJECT_ID/IMAGE_ID`
where IMAGE_ID should be replaced with the desired name of the image.
For MacOS: 
`docker build --platform linux/amd64 -t gcr.io/PROJECT_ID/IMAGE_ID .`
Test locally:
`docker run -p PORT:PORT gcr.io/PROJECT_ID/IMAGE_ID`
Push to Google Cloud:
`docker push gcr.io/PROJECT_ID/IMAGE_ID`

## Deploy to Cloud Run
In Google Cloud CLI:
`gcloud run deploy CONTAINER_ID \
  --image gcr.io/PROJECT_ID/IMAGE_ID \
  --platform managed \
  --region REGION \
  --allow-unauthenticated`

Replace placeholders:
* CONTAINER_ID: Name of the Cloud Run service.
* PROJECT_ID: Google Cloud project ID.
* IMAGE_ID: Docker image name.
* REGION: Deployment region (e.g., us-central1).

Follow these naming conventions:
* Use only lowercase alphanumeric characters and dashes (-).
* Cannot begin or end with a dash.
* Maximum length: 63 characters.

## Checking Logs
To check Cloud Run logs:
`gcloud logs read --project=PROJECT_ID --service=IMAGE_ID`