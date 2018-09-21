# https://github.com/DavidMuller/aws-requests-auth

print("usage: bash$ python hitapi.py <<projectID>>")

import requests, os, sys
from aws_requests_auth.aws_auth import AWSRequestsAuth

# let's talk to our AWS Elasticsearch cluster
auth = AWSRequestsAuth(aws_access_key=os.environ.get('access'),
                       aws_secret_access_key=os.environ.get('secret'),
                       aws_host='pish6mpnr0.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

response = requests.post('https://pish6mpnr0.execute-api.us-east-1.amazonaws.com/alpha-2/vm_stand_up',
                        auth=auth,
                        params={'projectID':sys.argv[1]})

#print(response.content)
#print("status code: {}".format(response.status_code))

print("Please check your email for connection information.")
print("It may take a minute before your VM is ready for use.")
