import hashlib
import logging
import os

import boto3
import smart_open
from memory_profiler import memory_usage

from implementations.process_pool_multipart import main as process_pool_multipart
from implementations.sequential_boto3 import main as seq_boto3
from implementations.sequential_multipart_boto3 import main as seq_multipart_boto3
from implementations.sequential_multipart_smart_boto3 import (
    main as seq_multipart_smart_boto3,
)
from implementations.sequential_smart_open import main as seq_smart_open
from implementations.thread_pool_multipart import main as thread_pool_multipart
from implementations.thread_pool_multipart_smart_boto import (
    main as thread_pool_multipart_smart_boto,
)
from timer import Timer

logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)


def main():
    bucket = "testing-bucket"
    manifest = [f"test_{i + 1}.txt" for i in range(10_000)]

    with Timer("sequential smart_open") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((seq_smart_open, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("sequential boto3") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((seq_boto3, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("sequential multipart boto3") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((seq_multipart_boto3, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("sequential multipart smart boto3") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((seq_multipart_smart_boto3, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("boto3 thread pool multipart") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((thread_pool_multipart, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("boto3 process pool multipart") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((process_pool_multipart, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()

    with Timer("thread pool multipart smart_open boto3 ") as t:
        print(t.name)
        print(
            f"Peak memory used: {max(memory_usage((thread_pool_multipart_smart_boto, (bucket, manifest), {}), multiprocess=True, include_children=True))}MiB"
        )
    check_integrity()


def hash_file(filename, block_size=65536):
    sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def check_integrity():
    first_file = "downloaded.txt"
    second_file = "downloaded2.txt"
    client = boto3.client("s3", endpoint_url="http://localhost:4566")
    with smart_open.open(
        f"s3://testing-bucket/output.txt", "rb", transport_params={"client": client}
    ) as output_file:
        with open("downloaded2.txt", "wb") as f:
            f.write(output_file.read())

    result = hash_file(first_file) == hash_file(second_file)
    os.remove(second_file)
    FAIL = "\033[91m"
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"
    print(f"Integrity check: {f'{OKGREEN}Passed' if result else f'{FAIL}Failed'}{ENDC}")


if __name__ == "__main__":
    main()
