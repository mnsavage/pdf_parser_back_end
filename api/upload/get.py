import json


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

    # Prepare the response
    response = {
        "message": "Retrieve PDF requirements successfully.",
        "header": pdf_requirements,
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": {"Content-Type": "application/json"},
    }
