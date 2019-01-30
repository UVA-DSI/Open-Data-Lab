#!/bin/bash

HelpMessage="""\n
   Stand Up CLI to launch and terminate OpenDataLab connected EC2 Projects.\n
   \n 
   Usage:\n
      \t./odl.sh standup -id (projectId)\n
      \t./odl.sh standup --project-id (projectId)\n
      \t./odl.sh standdown -id (projectId)\n
      \t./odl.sh standdown --project-id (projectId)\n
      \t./odl.sh -h | --help\n
   Arguments:\n
      \t-id | --project-id   Project Id\n
   Options:\n
      \t-h --help   Show this screen.\n
"""

command=$1

# Parse Arguments 
POSITIONAL=()
while [ "$1" != "" ]; do
   case $1 in
      -h| --help )   shift
                     HELP=true
                     ;;
      -id| --project-id )  ID=$1
                     ;;
   esac
   shift
done


# If help is true then display the help message
if [[ "$HELP" = true ]] || [[ -z $ID ]] || [[ -z $command ]] ; then
   echo -e ${HelpMessage}
   exit 
fi

# grabs credentials from file
API_KEY=`cat api_key.txt`
if [[ -z $API_KEY ]] ; then
   echo "Please place Open Data Lab API key in api_key.txt"
   exit 
fi


# TODO assign URLs
standUpLink=''
standDownLink=''

stand_up(){
   # Stand up an instance 
   curl -X POST \
      -H "host: apigateway.us-east-1.amazonaws.com" \
      -H "x-amz-date: `date -u +'%Y%m%dT%H%M%SZ'`" \
      -H "content-type: application/x-amz-json-1.0"
      -H "Authorization: " \
      ${standUpLink} > connect.sh
   chmod +x connect.sh
   ./connect.sh
}

stand_down(){
   # Shut down an instance
   curl -X POST ${standDownLink}
}


