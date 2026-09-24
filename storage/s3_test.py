import boto3


s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password123",
)

s3.put_object(
    Bucket="ai-telemetry",
    Key="test.txt",
    Body=b"Hello S3",
)

print("Upload complete")
