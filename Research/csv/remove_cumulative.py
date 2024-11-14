import os 

def remove_cumulative():
    output_file = "cumulative.csv"
    if os.path.exists(output_file):
        os.remove(output_file)
    #     print("Done")
    # else:
    #     print("Nothing to delete")

if __name__ == "__main__":
    remove_cumulative()
