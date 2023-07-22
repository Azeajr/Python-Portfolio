import itertools
import json
import logging
import os
import pathlib
import random

import numpy
import numpy as np
import requests


def write_file(file_name, text):
    with open(file_name, "w") as f:
        f.write(text)


def main():
    directory = "processing"
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    for i in range(3000):
        logging.info(f"requesting {i + 1}")
        file_name = os.path.join(directory, f"test_{i + 1}.txt")
        logging.info(f"requesting {file_name}")
        numpy_random(file_name, 1000, 100)
        logging.info(f"writing {file_name}")


def numpy_random(file_name: str, num_lines: int = 100, max_length: int = 100):
    letters = np.array(list(chr(ord("a") + i) for i in range(26)))
    lengths = np.random.randint(1, max_length, num_lines)
    arrays = [np.random.choice(letters, length) for length in lengths]
    strings = ["".join(array) + "\n" for array in arrays]
    result = "".join(strings)
    with open(file_name, "w") as f:
        f.write(result)


def uniform_letters(n: int = 10):
    directory = "temp/processing2/"
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    letters = [chr(ord("a") + i) for i in range(26)]
    n_grams = itertools.chain(
        *[itertools.permutations(letters, i + 1) for i in range(26)]
    )
    for index, n_gram in enumerate(n_grams):
        if index >= n:
            break
        file_name = os.path.join(directory, f"test_{index + 1}.txt")
        with open(file_name, "w") as f:
            f.write(("".join(n_gram) * 100 + "\n") * 100)


def shuffle_grow():
    directory = "temp/processing"
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory)]

    directory = "temp/processing2"
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    for i in range(3000):
        file_name = os.path.join(directory, f"test_{i + 1}.txt")
        with open(file_name, "w") as f:
            for file_path in random.sample(
                file_paths, random.randint(len(file_paths) // 2, len(file_paths))
            ):
                with open(file_path, "r") as f2:
                    f.write(f2.read())


if __name__ == "__main__":
    # numpy.savetxt("test.txt", numpy_random(1024**2), fmt="%s")
    # print(type(numpy_random(1024**2)))
    # with open("test.txt", "w") as f:
    #     f.write(json.dumps(numpy_random(1024**2)))
    # main()
    uniform_letters(10_000)
    # shuffle_grow()
