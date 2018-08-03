import boto3
import botocore
import logging
import datetime
import json

logs = loggin.getLogger('standUp')
logs.setLevel(loggin.INFO)

ec2_resource = boto3.resource('ec2', region_name='us-east-1')
subnet = ec2_resource.Subnet('subnet-6fbabc40')

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')

def standUp(event, context):
    ''' Start up an EC2 Instance Fusemounted to Open Data Lab Bucket 
    '''

    projectId = event.get('projectId')
    if projectId is None:
        return "Please Specify a projectId"

    try:
        projectData = json.loads(
                s3_client.get_object(Bucket='odltest-projects', Key=str(projectId)+'.json').get('Body').read()
                )

        # Grab User Credentials from Event
        access_key = projectData.get('accessKey')
        secret_key = projectData.get('secretKey')
        bucket = projectData.get('data')
        github = projectData.get('github')

    except:
        return "Unable to Find Project Data"


    # Generate SHH Credentials
    key_pair = KeyPair('AutoKey:'+str(datetime.datetime.now()))


    # Template the Bash Script
    init_script = """#!/bin/bash
    sudo su
    yum install -y gcc libstdc++-devel gcc-c++ fuse fuse-devel curl-devel libxml2-devel mailcap automake openssl-devel git
    git clone https://github.com/s3fs-fuse/s3fs-fuse
    cd s3fs-fuse/
    ./autogen.sh
    ./configure --prefix=/usr --with-openssl
    make
    make install
    touch /etc/passwd-s3fs
    echo {}:{} | tee /etc/passwd-s3fs
    chmod 400 /etc/passwd-s3fs
    mkdir ~/data
    s3fs odltest-mal ~/data -o use_cache=/tmp
    cd ~/
    git clone {}
    """.format(access_key, secret_key, bucket_name, github)


    # create a new instance
    instance = subnet.create_instances(
            ImageId = 'ami-b70554c8',
            InstanceType = 't2.small',
            MaxCount = 1,
            MinCount = 1,
            KeyName = key_pair.name,
            UserData= init_script
            )

    try:
        assert type(instance) == list
        assert len(instance) != 0
    except AssertionErroro:
        return "Couldn't Launch Instance"

    publicIp = instance[0].network_interfaces_attribute[0].get('Association', {}).get('PublicIp') 

    return "cat '{0}' > {1} && chmod 400 {1}  && ssh -i {1} ubuntu@{}".format(key_pair.key_material, key_pair.name+'.pem', publicIp)


