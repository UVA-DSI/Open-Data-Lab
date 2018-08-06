import os
import boto3
import json
import datetime

s3_client = boto3.client('s3')
ec2_resource = boto3.resource('ec2')
subnet = ec2_resource.Subnet('subnet-1025015b')

# access the sys environment secret keys 
access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')


def standUp(event, context):
    ''' Lambda Handler for Standing Up ODL Projects
    '''
    
    # read details from event passed
    projectId = str(event.get('projectId'))
    projectKey = str(event.get('projectId'))+'.json'
    
    
    if projectKey is None:
        return "Please Provide a Project Id"
    
    # load project details from s3
    try:
        projectS3 = s3_client.get_object(Bucket='odltest-projects', Key=projectKey).get('Body').read()
        assert projectS3 is not None
        projectDetails = json.loads(projectS3.decode('utf-8'))
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
sudo touch /etc/passwd-s3fs
sudo echo {}:{} | sudo tee /etc/passwd-s3fs
sudo chmod 400 /etc/passwd-s3fs
sudo mkdir ~/data
sudo s3fs odltest-mal ~/data -o use_cache=/tmp
cd ~/
sudo git clone {}
    """.format(access_key, secret_key, projectDetails.get('data'), projectDetails.get('github'))
    
    instance = subnet.create_instances(
        ImageId = 'ami-b70554c8',
        InstanceType = 't2.small',
        MaxCount = 1,
        MinCount = 1,
        KeyName = key_pair.name,
        UserData = init_script
    )
    
    try:
        assert type(instance) == list
        assert len(instance) != 0
    except AssertionError:
        return "Couldn't Launch Instance"
    
    # add tags to describe the 
    instance[0].create_tags(
        Tags = [
            {
                'Key': 'ProjectId',
                'Value': projectId,
            }
            ]
        )
    
    publicIp = instance[0].network_interfaces_attribute[0].get('Association', {}).get('PublicDnsName')
    
    return "echo '{0}' > {1} && chmod 400 {1}  && ssh -i {1} ec2-user@{2}".format(key_pair.key_material, key_pair.name+'.pem', publicIp)
