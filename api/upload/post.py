import os
import sys
import boto3
import uuid

# Check if NOT running on AWS Lambda
if "AWS_EXECUTION_ENV" not in os.environ:
    from ..utilities.response_maker import make_response
else:
    sys.path.append("/opt/")
    from response_maker import make_response


cloudfront_url = os.environ.get("CLOUDFRONT_URL")
job_queue = os.environ.get("JOB_QUEUE")
job_definition = os.environ.get("JOB_DEFINITION")
storage_name = os.environ.get("STORAGE")


def handler(event, context):
    UUID = str(uuid.uuid4())
    encoded_pdf = event.get("body")

    # store pdf
    storage_client = boto3.client("s3")
    storage_client.put_object(Bucket=storage_name, Key=UUID, Body=encoded_pdf)

    # submit batch job
    batch_client = boto3.client("batch")
    batch_client.submit_job(
        jobName="pdf parser",
        jobQueue=job_queue,
        jobDefinition=job_definition,
        containerOverrides={
            "environment": [
                {"name": "S3_BUCKET_NAME", "value": storage_name},
                {"name": "S3_KEY", "value": UUID},
            ]
        },
    )

    # Prepare the body
    body = {"message": "PDF parser job successfully submitted.", "UUID": UUID}

    return make_response(
        status_code=200, access_control_allow_origin=cloudfront_url, body=body
    )
