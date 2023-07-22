import logging

import boto3


def multipart_setup(
    bucket,
    manifest,
):
    client = boto3.client("s3", endpoint_url="http://localhost:4566")

    logging.info("Getting files sizes...")
    files = [
        (file_name, client.head_object(Bucket=bucket, Key=file_name)["ContentLength"])
        for file_name in manifest
    ]
    chunks = get_chunks(files)

    logging.info("Starting upload...")
    response = client.create_multipart_upload(Bucket=bucket, Key="output.txt")
    upload_id = response["UploadId"]

    return client, chunks, upload_id


def process_chunk(
    client, bucket: str, chunk: list[str], upload_id: str, part_number: int
):
    output = []
    for j, file_name in enumerate(chunk):
        logging.debug(f"Processing file {j + 1} of {len(chunk)}")
        response = (
            client.get_object(Bucket=bucket, Key=file_name)["Body"]
            .read()
            .decode("utf-8")
        )
        output.append(response)
    logging.debug(f"Uploading chunk {part_number} of {len(chunk)}")
    response = client.upload_part(
        Bucket=bucket,
        Key="output.txt",
        UploadId=upload_id,
        PartNumber=part_number,
        Body="".join(output),
    )
    return {"PartNumber": part_number, "ETag": response["ETag"]}


def get_chunks(files: list, max_size: int = 50 * 1024 * 1024) -> list[list]:
    logging.info("Breaking into chunks...")
    chunks: list[list[str]] = []
    current_chunk = []
    current_size = 0
    for file_name, size in files:
        if current_size + size > max_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
        current_chunk.append(file_name)
        current_size += size
    chunks.append(current_chunk)
    return chunks
