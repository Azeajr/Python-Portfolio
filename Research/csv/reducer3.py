from glob import glob
import shutil

from memory_profiler import profile

@profile
def reducer(num=None):
    output_file = "cumulative.csv"
    received_csv_files = [file for file in glob("*.csv") if file != output_file]
    with open(output_file, 'wb') as outfile:
        for i, filename in enumerate(received_csv_files):
            if filename == output_file:
                continue
            with open(filename, 'rb') as readfile:
                if i != 0:
                    readfile.readline()
                shutil.copyfileobj(readfile, outfile)
                
if __name__ == "__main__":
    reducer()
