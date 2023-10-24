import base64
import os
from io import BytesIO
from pdfminer.high_level import extract_text

from ..utilities.response_maker import make_response


cloudfront_url = os.environ.get("CLOUDFRONT_URL")


def handler(event, context):
    # Decode the PDF from the base64 encoded request body

    encoded_str = ensure_base64_padding(event["body"])

    pdf_content = base64.b64decode(encoded_str)

    # Use pdfminer.six to extract text from the PDF
    text = extract_text(BytesIO(pdf_content))

    # Prepare the body
    body = {"message": "PDF processed successfully.", "content": text}

    return make_response(
        status_code=200, access_control_allow_origin=cloudfront_url, body=body
    )


def ensure_base64_padding(encoded_str):
    """
    Description: checks for incorrect base64 padding and if exist fixes it
    encoded_str(str): the encoded string to check for incorrect padding
    """
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += "=" * (4 - missing_padding)

    return encoded_str
