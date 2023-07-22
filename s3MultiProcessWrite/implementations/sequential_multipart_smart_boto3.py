import io
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
    response = client.create_multipart_upload(Bucket=bucket, Key="output.txt")
    upload_id = response["UploadId"]

    parts = []
    buffer = io.BytesIO()
    part_num = 0
    for i, file_name in enumerate(manifest):
        with smart_open.open(
            f"s3://{bucket}/{file_name}",
            "rb",
            transport_params={"client": client},
        ) as f:
            for line in f:
                buffer.write(line)
                if buffer.tell() > 50 * 1024**2:
                    buffer.seek(0)
                    part_num += 1
                    logging.info(f"Uploading part {part_num}...")
                    response = client.upload_part(
                        Bucket=bucket,
                        Key="output.txt",
                        PartNumber=part_num,
                        UploadId=upload_id,
                        Body=buffer,
                    )
                    buffer.seek(0)
                    buffer.truncate(0)
                    parts.append({"ETag": response["ETag"], "PartNumber": part_num})

    if buffer.tell() > 0:
        buffer.seek(0)
        part_num += 1
        logging.info(f"Uploading part {part_num}...")
        response = client.upload_part(
            Bucket=bucket,
            Key="output.txt",
            PartNumber=part_num,
            UploadId=upload_id,
            Body=buffer,
        )
        buffer.seek(0)
        buffer.truncate(0)
        parts.append({"ETag": response["ETag"], "PartNumber": part_num})
    logging.info("Completing upload...")
    client.complete_multipart_upload(
        Bucket=bucket,
        Key="output.txt",
        UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
    logging.info("Done!")


if __name__ == "__main__":
    main("testing-bucket", [f"test_{i + 1}.txt" for i in range(10_000)])
