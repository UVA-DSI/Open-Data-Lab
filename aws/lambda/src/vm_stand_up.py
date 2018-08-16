import boto3
from botocore.exceptions import ClientError
import datetime
import time
import json
import os



ec2_resource = boto3.resource('ec2')
subnet = ec2_resource.Subnet('subnet-6fbabc40')


def lambda_handler(event, context):
    # TODO implement
    print('Hello from Lambda')

# generate a new key pair for EC2 instance
    key_name = 'key_'+str(int(datetime.datetime.timestamp(datetime.datetime.now())))
    
    key_pair = ec2_resource.create_key_pair(
        KeyName = key_name
    )
    
    # read details from event passed
    projectId = '1' #str(event.get('1'))
    projectKey = '1.json' #str(event.get('1'))+'.json'
    if projectId is None or projectId=="None":
        return "Please Provide a Project Id"

    print(projectKey)

    s3_client = boto3.client('s3')
#    s3_access_key = os.environ.get('AWS_ACCESS_KEY')
#    s3_secret_key = os.environ.get('AWS_SECRET_KEY')
#    s3_access_key = os.getenv('AWS_ACCESS_KEY')
#    s3_secret_key = os.getenv('AWS_SECRET_KEY')
#    s3_access_key = os.environ('AWS_ACCESS_KEY')
#    s3_secret_key = os.environ('AWS_SECRET_KEY')
#    print('access key: ',s3_access_key)
#    print('secret key: ',s3_secret_key)
    
    try:
        projectS3 = s3_client.get_object(Bucket='odl-projects-test', Key=projectKey).get('Body').read()
        projectDetails = json.loads(projectS3.decode('utf-8'))
        assert projectS3 is not None
        assert projectDetails is not None
    except AssertionError:
        return "Project Datails not found for project:{}".format(projectKey)

 
    # template UserData bash script to auto fusemount
    init_script = """#!/bin/bash
                     sudo yum install -y gcc libstdc++-devel gcc-c++ fuse fuse-devel curl-devel libxml2-devel mailcap automake openssl-devel git
                     chmod u+x ~/.bash_profile
                     echo ''

                     mkdir /home/ec2-user/data
                     mkdir /home/ec2-user/scratch
                     sudo git clone https://github.com/s3fs-fuse/s3fs-fuse
                     cd s3fs-fuse/
                     sudo ./autogen.sh
                     sudo ./configure --prefix=/usr --with-openssl
                     sudo make
                     sudo make install
                     touch /etc/passwd-s3fs
                     echo {}:{} | tee /etc/passwd-s3fs
                     chmod 400 /etc/passwd-s3fs
                     s3fs {} /home/ec2-user/data -o use_cache=/tmp &> /home/ec2-user/mount1.log
                     s3fs {} /home/ed2-user/scratch -o use_cache=/tmp &> /home/ec2-user/mount2.log
                     
                     echo 'git clone {}' >> /home/ec2-user/.bash_profile
                     """.format(os.environ.get('ACCESS'), os.environ.get('SECRET'), projectDetails.get('data'), projectDetails.get('scratch'), 'https://github.com/UVA-DSI/Open-Data-Lab.git')
    
                     
                     
                     
                     
    instance = subnet.create_instances(
        ImageId = 'ami-b70554c8',
        InstanceType = 't2.nano',
        MaxCount = 1,
        MinCount = 1,
        KeyName = key_pair.name,
        UserData = init_script
    )
    
    
    try:
        assert type(instance) == list
        assert len(instance) != 0
        launched_instance = instance[0]
    except AssertionError:
        print("Couldn't Launch Instance")
    
    print('instance launched')
    
    #print(type(instance)) --> list


    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Open Data Lab <uva-dsi-opendatalab-request@virginia.edu>"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "lpa2a@virginia.edu" #"uva-dsi-opendatalab-request@virginia.edu"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    SUBJECT = "Your VM is ready"

    # add tags to describe the 
    launched_instance.create_tags(
        Tags = [
            {
                'Key': 'test',
                'Value': 'TEST',
            }
            ]
        )

    time.sleep(2)

    eni_list = None
    publicIp = None

    launched_instance.load()
    network_interface = launched_instance.network_interfaces[0]      
    network_interface.load()
    eni_list =launched_instance.network_interfaces_attribute
    publicIp = eni_list[0].get('Association',{}).get('PublicIp')
    print("ip check",publicIp)
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Open Data Lab VM for project TEST is ready.\r\n"
                 "Step 1. Copy the contents below mark\r\n"
                 "Step 2. Paste into terminal and execute\r\n"
                 "Step 3. Execute connect.sh\r\n"
                 "#//....oooOO0OOooo........oooOO0OOooo....START....oooOO0OOooo........oooOO0OOooo......\r\n"
                 "echo '{0}' > {1} && chmod 400 {1}  && echo 'ssh -i {1} ec2-user@{2}' > connect.sh && chmod u+x connect.sh\r\n".format(key_pair.key_material, key_pair.name+'.pem', publicIp)
                )

    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
    return 0

'''
import os
import boto3
import json
import datetime

s3_client = boto3.client('s3')
ec2_resource = boto3.resource('ec2')
subnet = ec2_resource.Subnet('subnet-6fbabc40')

# access the sys environment secret keys 
import os
access_key = os.environ.get('ACCESS')
secret_key = os.environ.get('SECRET')

def standUp(event, context):
    #Lambda Handler for Standing Up ODL Projects
    
    
    # read details from event passed
    projectId = str(event.get('projectId'))
    projectKey = str(event.get('projectId'))+'.json'
    
    
    if projectId is None or projectId=="None":
        return "Please Provide a Project Id"
    
    
    # load project details from s3
    s3_client = boto3.client('s3')
    try:
        projectS3 = s3_client.get_object(Bucket='odl-projects-test', Key=projectKey).get('Body').read()
        projectDetails = json.loads(projectS3.decode('utf-8'))
        assert projectS3 is not None
        assert projectDetails is not None
    except AssertionError:
        return "Project Datails not found for project:{}".format(projectKey)
    
    # generate a new key pair for EC2 instance
    key_name = 'key_'+str(int(datetime.datetime.timestamp(datetime.datetime.now())))
    
    key_pair = ec2_resource.create_key_pair(
        KeyName = key_name
    )
    
    
    # template UserData bash script to auto fusemount
    init_script = """#!/bin/bash
sudo yum install -y gcc libstdc++-devel gcc-c++ fuse fuse-devel curl-devel libxml2-devel mailcap automake openssl-devel git
sudo git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
sudo ./autogen.sh
sudo ./configure --prefix=/usr --with-openssl
sudo make
sudo make install
echo 'touch .passwd-s3fs' >> /home/ec2-user/.bash_profile
echo 'echo {}:{} | tee /home/ec2-user/.passwd-s3fs' >> /home/ec2-user/.bash_profile
echo 'chmod 400 /home/ec2-user/.passwd-s3fs' >> /home/ec2-user/.bash_profile
echo 'mkdir ~/data/' >> /home/ec2-user/.bash_profile
echo 's3fs {} ~/data -o use_cache=/tmp' >> /home/ec2-user/.bash_profile
echo 'mkdir ~/scratch' >> /home/ec2-user/.bash_profile
echo 's3fs {} ~/scratch -o use_cache=/tmp' >> ~/.bash_profile
echo 'git clone {}' >> ~/.bash_profile
    """.format(access_key, secret_key, projectDetails.get('data'), projectDetails.get('scratch'), projectDetails.get('github'))
    
    instance = subnet.create_instances(
        ImageId = 'ami-b70554c8',
        InstanceType = 't2.nano',
        MaxCount = 1,
        MinCount = 1,
        KeyName = key_pair.name,
        UserData = init_script
    )
    
    
    try:
        assert type(instance) == list
        assert len(instance) != 0
        launched_instance = instance[0]
    except AssertionError:
        return "Couldn't Launch Instance"
    
    # add tags to describe the 
    launched_instance.create_tags(
        Tags = [
            {
                'Key': 'ProjectId',
                'Value': projectId,
            }
            ]
        )
    
    eni_list = None
    publicIp = None

    launched_instance.load()
    network_interface = launched_instance.network_interfaces[0]      
    network_interface.load()
    eni_list =launched_instance.network_interfaces_attribute
    # assert eni_list != None
    publicIp = eni_list[0].get('Association',{}).get('PublicIp')
      
    
    #publicIp = network_interface.association_attribute.get('PublicIp')        
    return "echo '{0}' > {1} && chmod 400 {1}  && sudo ssh -i {1} ec2-user@{2}".format(key_pair.key_material, key_pair.name+'.pem', publicIp)

'''

'''
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Sender Name <sender@example.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "recipient@example.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"

# The subject line for the email.
SUBJECT = "Amazon SES Test (SDK for Python)"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """            

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])
    
'''
