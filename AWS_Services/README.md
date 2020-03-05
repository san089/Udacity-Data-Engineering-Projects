# Launching EMR cluster from command line
### Below example creates a 3 Node EMR cluster with 1 master and 2 slave Nodes. 

    aws emr create-cluster \
    --applications Name=Ganglia Name=Spark Name=Zeppelin \
    --ebs-root-volume-size 10 \
    --ec2-attributes \ 
    '{"KeyName":<cluster-name>,"InstanceProfile":<IAMROLE>,"SubnetId":<subnet-id>,"EmrManagedSlaveSecurityGroup":<slave-security-group-id>,"EmrManagedMasterSecurityGroup":<master-security-group-id>}' \
    --service-role IAMROLE \
    --enable-debugging \ 
    --release-label <emr release version e.g emr-5.29.0> \ 
    --log-uri <s3-bucket-path-for-logging> \ 
    --name <cluster-name> \ 
    --instance-groups \
    '[ \ 
    {"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"MASTER","InstanceType":"m5.xlarge","Name":"Master Instance Group"}, \
    {"InstanceCount":2,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"CORE","InstanceType":"m5.xlarge","Name":"Core Instance Group"}\ 
    ]' \ 
    --scale-down-behavior TERMINATE_AT_TASK_COMPLETION \ 
    --region us-east-1


# AWS s3 CLI Cheat Sheet
![s3 cli cheat sheet](https://github.com/san089/Data_Engineering_Projects/blob/master/AWS_Services/aws-s3-cheat-sheet.png)
