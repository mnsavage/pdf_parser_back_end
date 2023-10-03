import base64
from unittest.mock import patch
from api.upload.post import handler
from api.upload.post import ensure_base64_padding
@patch("api.upload.post.extract_text")
def test_post_handler_success(mock_extract_text):
    encoded_pdf = base64.b64encode(b"dummy PDF content").decode()
    event = {
        "isBase64Encoded": True,
        "body": encoded_pdf
    }
    mock_extract_text.return_value = "Extracted text from PDF."
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    assert "PDF processed successfully." in response['body']
    assert "Extracted text from PDF." in response['body']

def test_post_handler_no_base64():
    event = {
        "isBase64Encoded": False,
        "body": "not encoded data"
    }

    response = handler(event, None)

    assert response['statusCode'] == 400
    assert "Expected the body to be base64 encoded." in response['body']
    
def test_no_padding_needed():
    assert ensure_base64_padding("YW55IGNhcm5hbCBwbGVhc3VyZQ==") == "YW55IGNhcm5hbCBwbGVhc3VyZQ=="

def test_padding_needed():
    assert ensure_base64_padding("YW55IGNhcm5hbCBwbGVhc3VyZQ") == "YW55IGNhcm5hbCBwbGVhc3VyZQ=="

def test_empty_string():
    assert ensure_base64_padding("") == ""