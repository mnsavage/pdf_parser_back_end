import json
from api.utilities.response_maker import make_response


def test_make_response():
    status_code = 200
    access_control_allow_origin = "domain.cloudfront.net"
    body = "hello world"
    expected_response = {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": access_control_allow_origin,
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST,DELETE",
        },
    }

    response = make_response(
        status_code=200,
        access_control_allow_origin=access_control_allow_origin,
        body=body,
    )

    assert response == expected_response
