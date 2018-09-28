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
#    print(event["queryStringParameters"]['projectID'])
    
# generate a new key pair for EC2 instance
    key_name = 'key_'+str(int(datetime.datetime.timestamp(datetime.datetime.now())))

    key_pair = ec2_resource.create_key_pair(
        KeyName = key_name
    )
    
    # read details from event passed
    #projectId = '1' #str(event.get('1'))
    #projectKey = '1.json' #str(event.get('1'))+'.json'
    #if projectId is None or projectId=="None":
    #    return "Please Provide a Project Id"

    if 'projectID' in event:    
        projectKey = str(event["queryStringParameters"]['projectID'])+'.json'
    else:
        projectKey = 'open-data-lab.json'

    print(projectKey)

    s3_client = boto3.client('s3')

    try:
        projectS3 = s3_client.get_object(Bucket='odl-projects-test', Key=projectKey).get('Body').read()
        projectDetails = json.loads(projectS3.decode('utf-8'))
        assert projectS3 is not None
        assert projectDetails is not None
    except AssertionError:
        return "Project Datails not found for project:{}".format(projectKey)
        
    print(projectDetails['github'])
 
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
                     s3fs {} /home/ec2-user/data -o allow_other,use_cache=/tmp &> /home/ec2-user/mount1.log
                     sudo chmod -R 444 /home/ec2-user/data/*
                     s3fs {} /home/ec2-user/scratch -o allow_other,use_cache=/tmp &> /home/ec2-user/mount2.log
                     sudo chmod -R 777 /home/ec2-user/scratch/*
                     
                     echo 'git clone {}' >> /home/ec2-user/.bash_profile
                     
                     echo ''
                     echo 'Welcome to your EC2 Instance'
                     echo 'Your data lives in /home/ec2-user/data'
                     echo 'Your scratch space is /home/ec2-user/scratch'
                     echo 'Your code repo is << repo name >>'
                     echo 'Only your scratch data and space will persist'
                     echo 'When you shutdown this instance all other disk space will be recycled.'
                     echo ''
                     """.format(os.environ.get('ACCESS'), os.environ.get('SECRET'), projectDetails['data-bucket'], projectDetails['scratch-bucket'], projectDetails['github'])
    
                     
                     
                     
                     
    instance = subnet.create_instances(
        ImageId = projectDetails['ImageId'],#'ami-b70554c8',
        InstanceType = projectDetails['InstanceType'],#'t2.nano',
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
    RECIPIENT = projectDetails['email'] #"lpa2a@virginia.edu" #"uva-dsi-opendatalab-request@virginia.edu"

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
        
    return 'beta-test: '+str(int(datetime.datetime.timestamp(datetime.datetime.now())))
