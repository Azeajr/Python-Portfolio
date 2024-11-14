import os
from glob import glob
from functools import reduce

# from memory_profiler import profile

# @profile
def reducer(num=None):
    output_file = "cumulative.csv"
    received_csv_files = [file for file in glob("*.csv") if file != output_file]

    if not num or 0 > num > len(received_csv_files):
        num = len(received_csv_files)
        
    received_csv_files = received_csv_files[:num]
    
    with open(output_file, "wb") as outfile:
        with open(received_csv_files[0],"rb") as one:
            with open(received_csv_files[1],"rb") as two:
                with open(received_csv_files[2],"rb") as three:
                    with open(received_csv_files[3],"rb") as four:
                        with open(received_csv_files[4],"rb") as five:
                            with open(received_csv_files[5],"rb") as six:
                                with open(received_csv_files[6],"rb") as seven:
                                    with open(received_csv_files[7],"rb") as eight:
                                        with open(received_csv_files[8],"rb") as nine:
                                            with open(received_csv_files[9],"rb") as ten:
                                                outfile.writelines(one)
                                                outfile.writelines(two)
                                                outfile.writelines(three)
                                                outfile.writelines(four)
                                                outfile.writelines(five)
                                                outfile.writelines(six)
                                                outfile.writelines(seven)
                                                outfile.writelines(eight)
                                                outfile.writelines(nine)
                                                outfile.writelines(ten)
                                
                    
if __name__ == "__main__":
    reducer()
