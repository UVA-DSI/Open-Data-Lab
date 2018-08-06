import os
import boto3
import json
import datetime

s3_client = boto3.client('s3')
ec2_resource = boto3.resource('ec2')
subnet = ec2_resource.Subnet('subnet-1025015b')

def standDown(event, context):
    ''' Terminate a Project by a Project ID
    '''
 
    # read details from event passed
    projectId = str(event.get('projectId'))
    
    
    if projectId is None:
        return "Please Provide a Project Id"

    filters = [{
        'Name': 'tag:ProjectId',
        'Values': [projectId]
        }]

    instance_descriptions = ec2.describe_instance(Filters=filers)

    # grab the instance id of all 
    instance_ids = []
    for elem in instances_descriptions.get('Reservations'):
        for instance in elem.get('Instances'):
            instance_ids.appned(
                    instance.get('InstanceId')
                    )


    response = ec2_client.terminate_instances(
            InstanceIds = instance_ids,
            )

    message = {
            "projectId": projectId,
            "instances": instance_ids,
            "awsResponse": response
            }

    return json.dumps(message)

