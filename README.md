## Streamlit on GCP Cloud Run

This is a demo app for running Steamlit on Cloud Run.
It runs a [rembg](https://github.com/danielgatis/rembg) that removes the background from an image as a sample.

Note that:

This is just a test application.
Cloudrun distributes its requests to multiple instances by default. Because of that, Streamlit's FileUploader may cause a 404.
To avoid this, set max-instance to 1.

## Try it
https://streamlit-on-cloudrun-wnj6lnxzja-an.a.run.app/

(If my GCP bills go up, I might just delete it🤔)

## Prepare mdoel file

Download `u2netp.onnx` file from [here](https://drive.google.com/uc?id=1tNuFmLv0TSNDjYIkjEdeH1IWKQdUA4HR) and put it in `model_files/`.

## Run in a local environment

```
docker-compose up
```

## Build & Deploy on GCP

- Build docker image and register to GCR

```
gcloud builds submit --project ${GCP_PROJECT} --tag gcr.io/${GCP_PROJECT}/streamlit-on-cloudrun
```

- Deploy app

```
gcloud beta run deploy streamlit-on-cloudrun --project ${GCP_PROJECT} --region asia-northeast1 --image gcr.io/${GCP_PROJECT}/streamlit-on-cloudrun --memory 2G --max-instances 1
```
