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


def handler(event, context):
    UUID = str(uuid.uuid4())
    encoded_pdf = event.get("body")

    # store pdf
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("STORAGE"))

    item = {
        "uuid": UUID,
        "job_status": "submitted",  # what is the status of the batch job
        "encoded_pdf": encoded_pdf,
        "job_output": None,  # this is where the batch job will put its pdf parser output later
    }

    table.put_item(Item=item)

    # submit batch job
    batch_client = boto3.client("batch")
    batch_client.submit_job(
        jobName="pdf parser",
        jobQueue=os.environ.get("JOB_QUEUE"),
        jobDefinition=os.environ.get("JOB_DEFINITION"),
        containerOverrides={
            "environment": [
                {"name": "S3_BUCKET_NAME", "value": os.environ.get("STORAGE")},
                {"name": "S3_KEY", "value": UUID},
            ]
        },
    )

    # Prepare the body
    body = {"message": "PDF parser job successfully submitted.", "UUID": UUID}

    return make_response(
        status_code=200,
        access_control_allow_origin=os.environ.get("CLOUDFRONT_URL"),
        body=body,
    )
