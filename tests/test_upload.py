import base64
import json
from unittest.mock import patch
from api.upload.post import handler as post_handler
from api.upload.get import handler as get_handler
from api.upload.post import ensure_base64_padding

@patch("api.upload.post.extract_text")
def test_post_handler_success(mock_extract_text):
    encoded_pdf = base64.b64encode(b"dummy PDF content").decode()
    event = {
        "body": encoded_pdf
    }
    mock_extract_text.return_value = "Extracted text from PDF."
    
    response = post_handler(event, None)
    
    assert response['statusCode'] == 200
    assert "PDF processed successfully." in response['body']
    assert "Extracted text from PDF." in response['body']
    
def test_no_padding_needed():
    assert ensure_base64_padding("YW55IGNhcm5hbCBwbGVhc3VyZQ==") == "YW55IGNhcm5hbCBwbGVhc3VyZQ=="

def test_padding_needed():
    assert ensure_base64_padding("YW55IGNhcm5hbCBwbGVhc3VyZQ") == "YW55IGNhcm5hbCBwbGVhc3VyZQ=="

def test_empty_string():
    assert ensure_base64_padding("") == ""
    
def test_get_handler_success():
    body_header = [
        {
            "title": "Page Formatting & Font",
            "requirements": [
                "Font: Use a standard 12-point font consistently throughout the document, including headings and subheadings, and must be black font including URLs",
                'No Blank pages in the documents'
                ],
        },
        {
            "title": "Page Order & Section Formatting",
            "requirements": [
                "2 double spaces beneath title"
            ]
        }
    ]
    
    response = get_handler(None, None)
    body_dict = json.loads(response['body'])

    assert response['statusCode'] == 200
    assert "Retrieve PDF requirements successfully." in response['body']
    assert body_dict["header"] == body_header