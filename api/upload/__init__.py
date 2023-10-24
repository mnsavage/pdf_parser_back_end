import sys
import os

# Check if NOT running on AWS Lambda
if "AWS_EXECUTION_ENV" not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
