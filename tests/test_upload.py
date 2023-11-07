import json
import unittest
from unittest.mock import patch
from api.upload.post import handler as post_handler
from api.upload.get import handler as get_handler


class TestLambdaFunction(unittest.TestCase):
    @patch("api.upload.post.boto3.client")
    @patch("api.upload.post.uuid.uuid4")
    def test_post_handler_success(self, mock_uuid, mock_boto_client):
        # Mock the UUID generated in the handler
        expected_uuid = 12345
        mock_uuid.return_value = expected_uuid

        # Mock the S3 and Batch client (same mock for simplicity)
        mock_s3 = mock_boto_client.return_value
        mock_batch = mock_boto_client.return_value

        # Input for the Lambda function
        encoded_pdf = "fake-base64-pdf-content"
        event = {"body": encoded_pdf}

        # Expected make_response output
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
        mock_s3.put_object.assert_called_once_with(
            Bucket=None, Key=f"{expected_uuid}-encodedPDF", Body=encoded_pdf
        )
        mock_batch.submit_job.assert_called_once_with(
            jobName="pdf parser",
            jobQueue=None,
            jobDefinition=None,
            containerOverrides={
                "environment": [
                    {"name": "S3_BUCKET_NAME", "value": None},
                    {"name": "S3_KEY", "value": str(expected_uuid)},
                ]
            },
        )

        assert response == expected_response

    def test_get_handler_success(self):
        body_header = [
            {
                "title": "Page Formatting & Font",
                "requirements": [
                    "Font: Use a standard 12-point font consistently throughout the document, including headings and subheadings, and must be black font including URLs",
                    "No Blank pages in the documents",
                ],
            },
            {
                "title": "Page Order & Section Formatting",
                "requirements": ["2 double spaces beneath title"],
            },
        ]

        response = get_handler(None, None)
        body_dict = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert "Retrieve PDF requirements successfully." in response["body"]
        assert body_dict["header"] == body_header
