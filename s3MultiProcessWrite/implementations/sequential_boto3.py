import logging
import os

import boto3

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def main(bucket, manifest):
    client = boto3.client("s3", endpoint_url="http://localhost:4566")
    logging.info("Starting upload...")
    output = []
    for file_name in manifest:
        logging.debug(f"Processing file {file_name}")
        response = client.get_object(Bucket=bucket, Key=file_name)["Body"].read()
        output.append(response.decode("utf-8"))
    client.put_object(Bucket=bucket, Key="output.txt", Body="".join(output))
    logging.info("Done!")


if __name__ == "__main__":
    main("testing-bucket", [f"test_{i + 1}.txt" for i in range(10)])
