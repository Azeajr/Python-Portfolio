awslocal s3api create-bucket --bucket testing-bucket
awslocal s3 sync  temp/processing2 s3://testing-bucket
# awslocal s3 rm s3://testing-bucket --recursive