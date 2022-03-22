import boto3 #Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python
import pandas #pandas is a software library written for the Python programming language for data manipulation and analysis

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id='AKIA46SFIWN5AMWMDQVB',
    aws_secret_access_key='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',
    region_name='ap-south-1'
)

# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id='AKIA46SFIWN5AMWMDQVB',
    aws_secret_access_key='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',
    region_name='ap-south-1'
)

# Fetch the list of existing buckets
clientResponse = client.list_buckets()

# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')

# Creating a bucket in AWS S3
location = {'LocationConstraint': 'ap-south-1'}
client.create_bucket(
    Bucket='sql-server-shack-demo-3',
    CreateBucketConfiguration=location
)

# Create the S3 object
obj = client.get_object(
    Bucket='sql-server-shack-demo-1',
    Key='sql-shack-demo.csv'
)

# Read data from the S3 object
data = pandas.read_csv(obj['Body'])

# Print the data frame
print('Printing the data frame...')
print(data)