# Data_Engineering_Projects
# Redhsift IaC (Infrastructure as Code) Utility
This utility automates the Infrastructure deployement and configuration for Redshift cluster along with the pre-requisites to spin up the cluster. 

The code performs 3 setups:

 - Create or delete an IAM role and apply appropriate policy to allow access to other AWS services 
 - Create or delete a VPC security group, with appropriate Indound rules to allow connection to the cluster.
 - Finally, spin up a cluster using the Hardware configurations defined in config file, set-up master DB configs, apply cluster permission's with the IAM role and set VPC security groups as created above.

### Setup Configurations File - cluster.config

    [AWS]
    KEY=<Your Access Key>
    SECRET=<Your Secret Access Key>
    
    [DWH] 
    DWH_CLUSTER_TYPE=<single or multi node cluster>
    DWH_NUM_NODES=<number of nodes>
    DWH_NODE_TYPE=<Node type e.g. dc2.large>
    DWH_CLUSTER_IDENTIFIER=<cluster identifier>
    DWH_DB=<db name>
    DWH_DB_USER=<db user>
    DWH_DB_PASSWORD=<db password>
    DWH_PORT=<db port. default - 5439>
    
    
    [IAM_ROLE]
    NAME=<role-name>
    DESCRIPTION=<role-description>
    POLICY_ARN=<policy-arn e.g - arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess>
    
    [SECURITY_GROUP]
    NAME=<redshift-security-group-name>
    DESCRIPTION=<security-group-description>
    
    [INBOUND_RULE]
    TYPE=<Redshift>
    PROTOCOL=<protocol e.g - TCP>
    PORT_RANGE=<port>
    CIDRIP=<Specify a single IP address, or an IP address range in CIDR notation>
    DESCRIPTION=<description>

 ### Usage 
 

    > python Redshift_Cluster_IaC.py -h
    
    usage: Redshift_Cluster_IaC.py [-h] -c  -d  [-v]
    
    A Redshift cluster IaC (Infrastructure as Code). It creates IAM role for the
    Redshift, creates security group and sets up ingress parameters. Finally spin-
    up a redshift cluster.
    
    required arguments:
      -c , --create      True or False. Create IAM roles, security group and
                         redshift cluster if ie does not exist.
      -d , --delete      True or False. Delete the roles, securitygroup and
                         cluster. WARNING: Deletes the Redshift cluster, IAM role
                         and security group.
    
    optional arguments:
      -v , --verbosity   Increase output verbosity. Default set to DEBUG. 
    
### How to run
Create a new cluster: 

    python Redshift_Cluster_IaC.py --create TRUE --delete FALSE --verbosity TRUE

Delete cluster:

    python Redshift_Cluster_IaC.py --create FALSE --delete TRUE --verbosity TRUE



</br>
</br>

# Project 1:  Data Modeling with Postgres
## Overview 
In this project, we apply Data Modeling with Postgres and build an ETL pipeline using Python. A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Currently, they are collecting data in json format and the analytics team is particularly interested in understanding what songs users are listening to.

Project Link - [Data_Modeling_with_Postgres](https://github.com/san089/Data_Engineering_Projects/tree/master/Data_Modeling_with_Postgres)

</br>

# Project 2:  Data Modeling with Apache Cassandra
## Overview 
In this project, we apply Data Modeling with Cassandra and build an ETL pipeline using Python. A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Currently, they are collecting data in json format and the analytics team is particularly interested in understanding what songs users are listening to.
Data is modeled in the table and the sequence and order in which data is partitioned, inserted and retrieved from the table is optimized for certain queries to be run on the Cassandra DB.

Project Link - [Data_Modeling_with_Apache_Cassandra](https://github.com/san089/Data_Engineering_Projects/tree/master/Data_Modeling_with_Apache_Cassandra)


