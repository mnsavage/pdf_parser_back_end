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
    job_name = f"pdf_parser_{UUID}"
    encoded_pdf = event.get("body")
    print(f"job name: {job_name}")

    # store encoded pdf in s3 bucket
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=os.environ.get("S3"), Key=UUID, Body=encoded_pdf)

    # submit batch job
    batch_client = boto3.client("batch")
    batch_client.submit_job(
        jobName=job_name,
        jobQueue=os.environ.get("JOB_QUEUE"),
        jobDefinition=os.environ.get("JOB_DEFINITION"),
        containerOverrides={
            "environment": [
                {"name": "DYNAMODB_NAME", "value": os.environ.get("DYNAMODB")},
                {"name": "DYNAMODB_KEY", "value": UUID},
            ]
        },
    )

    # store batch job information
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("DYNAMODB"))

    item = {
        "uuid": UUID,
        "job_status": "submitted",  # what is the status of the batch job
        "job_output": None,  # this is where the batch job will put its pdf parser output later
    }

    table.put_item(Item=item)

    # Prepare the body
    body = {"message": "PDF parser job successfully submitted.", "UUID": UUID}

    return make_response(
        status_code=200,
        access_control_allow_origin=os.environ.get("CLOUDFRONT_URL"),
        body=body,
    )
