
echo "plos"
aws s3api --profile odl-lpa2a list-objects --bucket 2017-2018-capstone-plos --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "dlt"
aws s3api --profile odl-lpa2a list-objects --bucket 846033058400-dlt-utilization --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'

echo "bamc"
aws s3api --profile odl-lpa2a list-objects --bucket odl-bamc --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "mabc scratch"
aws s3api --profile odl-lpa2a list-objects --bucket odl-bamc-scratch --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "cbwc"
aws s3api --profile odl-lpa2a list-objects --bucket odl-cbwc --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "domi"
aws s3api --profile odl-lpa2a list-objects --bucket odl-domi --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "hmtt"
aws s3api --profile odl-lpa2a list-objects --bucket odl-hmtt --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "hmtt-scratch"
aws s3api --profile odl-lpa2a list-objects --bucket odl-hmtt-scratch --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "nept"
aws s3api --profile odl-lpa2a list-objects --bucket odl-nept --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "orci"
aws s3api --profile odl-lpa2a list-objects --bucket odl-orci --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "pmis"
aws s3api --profile odl-lpa2a list-objects --bucket odl-pmis --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "podc"
aws s3api --profile odl-lpa2a list-objects --bucket odl-podc --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "projects-test"
aws s3api --profile odl-lpa2a list-objects --bucket odl-projects-test --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "readonly-test"
aws s3api --profile odl-lpa2a list-objects --bucket odl-readonly-test --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "odl scratch test"
aws s3api --profile odl-lpa2a list-objects --bucket odl-scratch-test --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "sp19sys6016"
aws s3api --profile odl-lpa2a list-objects --bucket odl-sp19-sys6016 --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "spark-education"
aws s3api --profile odl-lpa2a list-objects --bucket odl-spark-education --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "spark19sp"
aws s3api --profile odl-lpa2a list-objects --bucket odl-spark19spds6003-001 --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "odl-watr"
aws s3api --profile odl-lpa2a list-objects --bucket odl-watr --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "watr-scratch"
aws s3api --profile odl-lpa2a list-objects --bucket odl-watr-scratch --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "wiki"
aws s3api --profile odl-lpa2a list-objects --bucket odl-wiki --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
echo "uva-bucket"
aws s3api --profile odl-lpa2a list-objects --bucket uva-bucket --output json --query "[sum(Contents[].Size), length(Contents[])]" | awk 'NR!=2 {print $0;next} NR==2 {print $0/1024/1024/1024" GB"}'
