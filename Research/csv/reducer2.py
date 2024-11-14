# Opening the product file in append mode
import os
from glob import glob
from functools import reduce

from memory_profiler import profile

@profile
def reducer(num=None):
    output_file = "cumulative.csv"
    received_csv_files = [file for file in glob("*.csv") if file != output_file]

    if not num or 0 > num > len(received_csv_files):
        num = len(received_csv_files)
        
    received_csv_files = received_csv_files[:num]
    
    with open(output_file, "ab") as outfile:
        def combine_files(out_file, in_file_path:str):
            with open(in_file_path, "rb") as in_file:
                if out_file.tell() !=0:
                    next(in_file)
                out_file.writelines(in_file)
                return out_file
        
        reduce(combine_files, received_csv_files, outfile)

if __name__ == "__main__":
    reducer()
