import json
import pytest
from unittest.mock import patch
from api.upload.post import handler as post_handler
from api.upload.get import handler as get_handler


@patch("api.upload.post.boto3.client")
@patch("api.upload.post.boto3.resource")
@patch("api.upload.post.uuid.uuid4")
def test_post_handler_success(mock_uuid, mock_boto_resource, mock_boto_client):
    # Mock the UUID generated in the handler
    expected_uuid = 12345
    mock_uuid.return_value = expected_uuid

    # Mock the S3 and Batch client (same mock for simplicity)
    mock_s3 = mock_boto_resource.return_value
    mock_dynamo = mock_boto_resource.return_value
    mock_table = mock_dynamo.Table.return_value
    mock_batch = mock_boto_client.return_value

    # Input for the Lambda function
    encoded_pdf = "fake-base64-pdf-content"
    event = {"body": encoded_pdf}

    # Expected make_response output
    expected_item = {
        "uuid": str(expected_uuid),
        "job_status": "submitted",
        "job_output": None,
    }
    expected_response = {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "PDF parser job successfully submitted.",
                "UUID": str(expected_uuid),
            }
        ),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": None,
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST,DELETE",
        },
    }

    # call post handler
    response = post_handler(event, None)

    # Assertions
    mock_s3.put_object(Bucket=None, Key=str(mock_uuid), Body=encoded_pdf)
    mock_table.put_item.assert_called_once_with(Item=expected_item)
    mock_batch.submit_job.assert_called_once_with(
        jobName=f"pdf_parser_{expected_uuid}",
        jobQueue=None,
        jobDefinition=None,
        containerOverrides={
            "environment": [
                {"name": "DYNAMODB_NAME", "value": None},
                {"name": "DYNAMODB_KEY", "value": str(expected_uuid)},
            ]
        },
    )

    assert response == expected_response


@patch("api.upload.get.boto3.resource")
@pytest.mark.parametrize(
    "expected_status_code, expected_job_status, expected_job_output",
    [
        (200, "completed", "output from batch job"),
        (202, "submitted", None),
        (404, "error", None),
    ],
)
def test_get_handler(
    mock_resource, expected_job_status, expected_status_code, expected_job_output
):
    UUID = "123"
    event = {"pathParameters": {"uuid": UUID}}
    expected_body = {
        "message": "Batch job status and output",
        "job_status": expected_job_status,
        "job_output": expected_job_output,
    }
    expected__response = {
        "statusCode": expected_status_code,
        "body": json.dumps(expected_body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": None,
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST,DELETE",
        },
    }

    # Mock database
    expected_item = {
        "Item": {
            "uuid": "123",
            "encoded_pdf": "fake-base64-pdf-content",
            "job_status": expected_job_status,
            "job_output": expected_job_output,
        }
    }
    mock_dynamo = mock_resource.return_value
    mock_table = mock_dynamo.Table.return_value
    mock_table.get_item.return_value = expected_item

    # Get handler
    response = get_handler(event, None)

    # Assertions
    mock_resource.assert_called_once_with("dynamodb")
    mock_dynamo.Table.assert_called_once_with(None)
    mock_table.get_item.assert_called_once_with(Key={"uuid": UUID})
    if expected_status_code == 200 or expected_status_code == 404:
        mock_table.delete_item.assert_called_once_with(Key={"uuid": UUID})
    assert response == expected__response
