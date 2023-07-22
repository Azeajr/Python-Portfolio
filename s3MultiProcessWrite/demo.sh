time mprof run python boto3/sequential.py
#real    0m27.792s
#user    0m9.713s
#sys     0m4.331s
#3134891871 output.txt
#Memory usage: 15_000.00 MiB
time mprof run python smart_open/sequetial.py
#real    0m26.482s
#user    0m8.201s
#sys     0m1.986s
#3134891772 output.txt
#Memory usage: 242.00 MiB
time mprof run python boto3/s3_process_pool.py
#real    0m15.886s
#user    0m17.065s
#sys     0m4.757s
#3134891772 output.txt
#3134891784 output.txt
#Memory usage: 1620.00 MiB
time mprof run python boto3/sequential_multipart.py
#real    0m31.908s
#user    0m11.634s
#sys     0m3.974s
#3134891772 output.txt
#3134891784 output.txt
#Memory usage: 340.00 MiB
