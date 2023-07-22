import io
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor

import boto3
import smart_open

logging.basicConfig(level=logging.INFO)

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def task(
    task_contents,
    task_upload_id,
    task_part_num,
    task_client,
    task_bucket,
):
    task_response = task_client.upload_part(
        Bucket=task_bucket,
        Key="output.txt",
        PartNumber=task_part_num,
        UploadId=task_upload_id,
        Body=task_contents,
    )
    logging.debug(f"Uploaded part {task_part_num} size {len(task_contents)}")
    return {"ETag": task_response["ETag"], "PartNumber": task_part_num}


def main(bucket, manifest):
    client = boto3.client("s3", endpoint_url="http://localhost:4566")

    logging.info("Starting upload...")
    response = client.create_multipart_upload(Bucket=bucket, Key="output.txt")
    upload_id = response["UploadId"]

    futures = []
    buffer = io.BytesIO()
    part_num = 0
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=1) as executor:
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
                        contents = buffer.read()
                        part_num += 1
                        futures.append(
                            executor.submit(
                                task,
                                task_contents=contents,
                                task_upload_id=upload_id,
                                task_part_num=part_num,
                                task_client=client,
                                task_bucket=bucket,
                            )
                        )
                        buffer.seek(0)
                        buffer.truncate(0)
        if buffer.tell() > 0:
            buffer.seek(0)
            contents = buffer.read()
            part_num += 1
            futures.append(
                executor.submit(
                    task,
                    task_contents=contents,
                    task_upload_id=upload_id,
                    task_part_num=part_num,
                    task_client=client,
                    task_bucket=bucket,
                )
            )
            buffer.seek(0)
            buffer.truncate(0)
    parts = [f.result() for f in futures]
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
