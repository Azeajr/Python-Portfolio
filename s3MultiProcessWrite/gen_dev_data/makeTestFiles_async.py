import asyncio
import os
import pathlib

import aiohttp


async def fetch(session, url, file_name, retries=3, backoff_factor=2):
    attempt = 0
    while attempt <= retries:
        try:
            async with session.get(url) as response:
                text = await response.text()
                if "Too many requests" in text:
                    raise aiohttp.ClientError("Too many requests")
                await asyncio.to_thread(write_file, file_name, text)
                return  # Successful response, exit the loop
        except aiohttp.ClientError as e:
            print(f"Error occurred: {e}")
            if attempt == retries:
                print(f"All retry attempts exhausted. Skipping {url}")
                return
            delay = backoff_factor**attempt
            await asyncio.sleep(delay)
            attempt += 1


def write_file(file_name, text):
    with open(file_name, "w") as f:
        f.write(text)


async def main():
    urls = ["https://loripsum.net/api/1/verylong/plaintext" for _ in range(0, 10)]
    directory = "processing"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
            file_name = os.path.join(directory, f"test_{i + 1}.txt")
            task = fetch(session, url, file_name)
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
