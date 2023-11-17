import os
import sys
import boto3

# Check if NOT running on AWS Lambda
if "AWS_EXECUTION_ENV" not in os.environ:
    from ..utilities.response_maker import make_response
else:
    sys.path.append("/opt/")
    from response_maker import make_response


cloudfront_url = os.environ.get("CLOUDFRONT_URL")


def handler(event, context):
    # Get uuid from in path (EX: upload/uuid)
    UUID = str(event.get("pathParameters", {}).get("uuid"))

    # Get item from database using uuid
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("DYNAMODB"))

    response = table.get_item(Key={"uuid": UUID})

    # Prepare the body
    body = {
        "message": "Batch job status and output",
        "job_status": response.get("Item", {}).get("job_status"),
        "job_output": response.get("Item", {}).get("job_output"),
    }

    status_code = None
    if body["job_status"] == "completed":
        status_code = 200
        table.delete_item(Key={"uuid": UUID})
    elif body["job_status"] == "submitted":
        status_code = 202
    else:
        status_code = 404
        table.delete_item(Key={"uuid": UUID})

    return make_response(
        status_code=status_code, access_control_allow_origin=cloudfront_url, body=body
    )
