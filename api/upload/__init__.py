import json
import base64
from io import BytesIO
from pdfminer.high_level import extract_text


def lambda_handler(event, context):
    # Check if the body is base64 encoded
    if not event.get("isBase64Encoded"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Expected the body to be base64 encoded."}),
            "headers": {"Content-Type": "application/json"},
        }

    pdf_content = base64.b64decode(event["body"])

    text = extract_text(BytesIO(pdf_content))

    response = {"message": "PDF processed successfully.", "content": text}

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": {"Content-Type": "application/json"},
    }
