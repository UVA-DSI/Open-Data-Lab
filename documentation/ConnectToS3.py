
# coding: utf-8

# In[ ]:


# from http://boto.cloudhackers.com/en/latest/s3_tut.html


# In[7]:


# You have permission to list the contents of any open data lab bucket


import boto3
s3 = boto3.resource('s3')

my_bucket = s3.Bucket('odl-projects-test')

for awsfile in my_bucket.objects.all():
    print(awsfile)


# In[9]:


# However you do not have permission to read the contents of every bucket.

import boto3
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
my_bucket = resource.Bucket('odl-projects-test') #subsitute this for your s3 bucket name. obj = client.get_object(Bucket='my-bucket', Key='path/to/my/table.csv')
obj = client.get_object(Bucket='odl-projects-test', Key='open-data-lab.json')


# In[17]:


# An example showing how to print the content of a text file
# This is long and verbose, some steps are not necessary.


import boto3
client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
my_bucket = resource.Bucket('odl-bamc')
obj = client.get_object(Bucket='odl-bamc', Key='foo.txt')
print(type(obj))
print(obj)
print(obj['Body'])

import pandas as pd
body = pd.read_csv(obj['Body'])
body

