import logging
import os
from concurrent.futures import ThreadPoolExecutor

import boto3

from implementations.multipart import multipart_setup, process_chunk

logging.basicConfig(level=logging.INFO)

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def main(bucket, manifest):
    client, chunks, upload_id = multipart_setup(bucket, manifest)

    with ThreadPoolExecutor() as executor:
        results = []
        for i, chunk in enumerate(chunks):
            results.append(
                executor.submit(process_chunk, client, bucket, chunk, upload_id, i + 1)
            )
        parts = [result.result() for result in results]

    logging.info("Completing upload...")
    client.complete_multipart_upload(
        Bucket=bucket,
        Key="output.txt",
        UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )

    logging.info("Done!")


def task(bucket, chunk, upload_id, part_number):
    client = boto3.client("s3", endpoint_url="http://localhost:4566")
    return process_chunk(client, bucket, chunk, upload_id, part_number)


if __name__ == "__main__":
    main("testing-bucket", [f"test_{i + 1}.txt" for i in range(10)])
