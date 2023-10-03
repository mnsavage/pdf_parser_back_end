import json
import base64
from io import BytesIO
from pdfminer.high_level import extract_text


def handler(event, context):
    # Check if the body is base64 encoded
    if not event.get("isBase64Encoded"):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Expected the body to be base64 encoded."}),
            "headers": {"Content-Type": "application/json"},
        }

    # Decode the PDF from the base64 encoded request body
    
    encoded_str = ensure_base64_padding(event["body"])

    pdf_content = base64.b64decode(encoded_str)
    
    # Use pdfminer.six to extract text from the PDF
    text = extract_text(BytesIO(pdf_content))

    # Prepare the response
    response = {"message": "PDF processed successfully.", "content": text}

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": {"Content-Type": "application/json"},
    }

def ensure_base64_padding(encoded_str):
    '''
    Description: checks for incorrect base64 padding and if exist fixes it
    encoded_str(str): the encoded string to check for incorrect padding
    '''
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += '=' * (4 - missing_padding)

    return encoded_str