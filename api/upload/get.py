import os
import sys


# Check if NOT running on AWS Lambda
if "AWS_EXECUTION_ENV" not in os.environ:
    from ..utilities.response_maker import make_response
else:
    sys.path.append("/opt/")
    from response_maker import make_response


cloudfront_url = os.environ.get("CLOUDFRONT_URL")


def handler(event, context):
    # list of pdf requirements
    pdf_requirements = [
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

    # Prepare the body
    body = {
        "message": "Retrieve PDF requirements successfully.",
        "header": pdf_requirements,
    }

    return make_response(
        status_code=200, access_control_allow_origin=cloudfront_url, body=body
    )
