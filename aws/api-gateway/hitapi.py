# https://github.com/DavidMuller/aws-requests-auth

import requests, os
from aws_requests_auth.aws_auth import AWSRequestsAuth

# let's talk to our AWS Elasticsearch cluster
auth = AWSRequestsAuth(aws_access_key=os.environ.get('access'),
                       aws_secret_access_key=os.environ.get('secret'),
                       aws_host='pish6mpnr0.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

response = requests.post('https://pish6mpnr0.execute-api.us-east-1.amazonaws.com/alpha-2/vm_stand_up',
                        auth=auth)
print(response.content)

