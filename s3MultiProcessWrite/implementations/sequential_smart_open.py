import logging
import os

import boto3
import smart_open

logging.basicConfig(level=logging.INFO)

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def main(bucket, manifest):
    client = boto3.client("s3", endpoint_url="http://localhost:4566")
    logging.info("Starting upload...")
    with smart_open.open(
        f"s3://{bucket}/output.txt", "wb", transport_params={"client": client}
    ) as output_file:
        for file_name in manifest:
            logging.debug(f"Processing file {file_name}")
            with smart_open.open(
                f"s3://{bucket}/{file_name}", "rb", transport_params={"client": client}
            ) as input_file:
                output_file.write(input_file.read())
    logging.info("Done!")


if __name__ == "__main__":
    main("testing-bucket", [f"test_{i + 1}.txt" for i in range(10_000)])
