import boto3
import configparser
from botocore.exceptions import ClientError
import json
import logging
import logging.config
from pathlib import Path
import argparse

# Setting up logger, Logger properties are defined in logging.ini file
logging.config.fileConfig(f"{Path(__file__).parents[0]}/logging.ini")
logger = logging.getLogger(__name__)

# Loading cluster configurations from cluster.config
config = configparser.ConfigParser()
config.read_file(open('cluster.config'))


def create_IAM_role(iam_client):
    """
    Create and IAM_role, Define configuration in cluster.config
    :param iam_client: an IAM service client instance
    :return: True if IAM role created and policy applied successfully.
    """

    role_name = config.get('IAM_ROLE', 'NAME')
    role_description = config.get('IAM_ROLE', 'DESCRIPTION')
    role_policy_arn = config.get('IAM_ROLE','POLICY_ARN')

    logging.info(f"Creating IAM role with name : {role_name}, description : {role_description} and policy : {role_arn}")

    # Creating Role.
    # Policy Documentation reference - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples
    role_policy_document = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": { "Service": [ "redshift.amazonaws.com" ] },
                    "Action": [ "sts:AssumeRole" ]
                }
            ]
        }
    )

    try:
        create_response = iam_client.create_role(
                    Path='/',
                    RoleName=role_name,
                    Description=role_description,
                    AssumeRolePolicyDocument = role_policy_document
        )
        logger.info(f"Got response from IAM client for creating role : {create_response}")
        logger.debug(f"Role create response code : {create_response['ResponseMetadata']['HTTPStatusCode']}")
    except Exception as e:
        logger.error(f"Error occured while creating role : {e}")
        return False


    try:
        # Attaching policy using ARN's( Amazon Resource Names )
        policy_response = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=role_policy_arn
        )
        logger.info(f"Got response from IAM client for applying policy to role : {policy_response}")
        logger.debug(f"Attach policy response code : {policy_response['ResponseMetadata']['HTTPStatusCode']}")
    except Exception as e:
        logger.error(f"Error occured while applying policy : {e}")
        return False

    return True if( (create_response['ResponseMetadata']['HTTPStatusCode'] == 200) and  (policy_response['ResponseMetadata']['HTTPStatusCode'] == 200) ) else False


def delete_IAM_role(iam_client):
    """
    Delete and IAM role
    Make sure that you do not have any Amazon EC2 instances running with the role you are about to delete.
    Deleting a role or instance profile that is associated with a running instance will break any applications running on the instance.
    :param iam_client: an IAM service client instance
    :return: True if role deleted successfully.
    """

    role_name = config.get('IAM_ROLE', 'NAME')
    logger.info(f"Processing deleting IAM role : {role_name}")
    try:
        detach_response = iam_client.detach_role_policy(RoleName=role_name, PolicyArn=config.get('IAM_ROLE','POLICY_ARN'))
        logger.info(f"Response for policy detach from IAM role : {detach_response}")
        logger.debug(f"Detach policy response code : {detach_response['ResponseMetadata']['HTTPStatusCode']}")
        delete_response = iam_client.delete_role(RoleName=role_name)
        logger.info(f"Response for deleting IAM role : {delete_response}")
        logger.debug(f"Delete role response code : {delete_response['ResponseMetadata']['HTTPStatusCode']}")
    except Exception as e:
        logger.error(f"Exception occured while deleting role : {e}")

    return True if( (detach_response['ResponseMetadata']['HTTPStatusCode'] == 200) and  (delete_response['ResponseMetadata']['HTTPStatusCode'] == 200) ) else False



def create_cluster(redshift_client, iam_role_arn, vpc_security_group_id):

    # Cluster Hardware config
    cluster_type = config.get('DWH','DWH_CLUSTER_TYPE')
    node_type =  config.get('DWH', 'DWH_NODE_TYPE')
    num_nodes = int(config.get('DWH', 'DWH_NUM_NODES'))

    # Cluster identifiers and credentials
    cluster_identifier = config.get('DWH','DWH_CLUSTER_IDENTIFIER')
    db_name = config.get('DWH', 'DWH_DB')
    database_port=int(config.get('DWH','DWH_PORT'))
    master_username = config.get('DWH', 'DWH_DB_USER')
    master_user_password = config.get('DWH', 'DWH_DB_PASSWORD')

    # Cluster adding IAM role
    iam_role = None

    # Security settings
    security_group = config.get('SECURITY_GROUP', 'NAME')

    # Documentation - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html?highlight=create_cluster#Redshift.Client.create_cluster
    try:
        response = redshift_client.create_cluster(
            DBName=db_name,
            ClusterIdentifier=cluster_identifier,
            ClusterType=cluster_type,
            NodeType=node_type,
            NumberOfNodes=num_nodes,
            MasterUsername=master_username,
            MasterUserPassword=master_user_password,
            VpcSecurityGroupIds=vpc_security_group_id,
            IamRoles = [iam_role_arn]
        )
        logger.info(f"Response for creating cluster : {response}")
    except Exception as e:
        logger.error(f"Exception occured while creating cluster : {e}")


def delete_cluster(redshift_client):

    try:
        response = \
            redshift_client.delete_cluster(ClusterIdentifier=config.get('DWH','DWH_CLUSTER_IDENTIFIER'), SkipFinalClusterSnapshot=True)
        logger.info(f"Cluster deleted response code : {response['ResponseMetadata']['HTTPStatusCode']}")
    except Exception as e:
        logger.info(f"Exception occured while deleting cluster : {e}")

    return response['ResponseMetadata']['HTTPStatusCode']

def get_group(ec2_client, group_name):
    groups = \
    ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [group_name]}])[
        'SecurityGroups']
    return None if(len(groups) == 0) else groups[0]


def create_ec2_security_group(ec2_client):

    if(get_group(ec2_client, config.get('SECURITY_GROUP','NAME')) is not None):
        logger.info("Group already exists!!")
        return True

    # Fetch VPC ID
    vpc_id = ec2_client.describe_security_groups()['SecurityGroups'][0]['VpcId']

    response = ec2_client.create_security_group(
        Description=config.get('SECURITY_GROUP','DESCRIPTION'),
        GroupName=config.get('SECURITY_GROUP','NAME'),
        VpcId=vpc_id,
        DryRun=False # Checks whether you have the required permissions for the action, without actually making the request, and provides an error response
    )
    logger.info(f"Group created!! Response code {response['ResponseMetadata']['HTTPStatusCode']}")


    logger.info("Authorizing security group ingress")
    ec2_client.authorize_security_group_ingress(
                GroupId=response['GroupId'],
                GroupName=config.get('SECURITY_GROUP','NAME'),
                FromPort=int(config.get('INBOUND_RULE','PORT_RANGE')),
                ToPort=int(config.get('INBOUND_RULE', 'PORT_RANGE')),
                CidrIp=config.get('INBOUND_RULE','CIDRIP'),
                IpProtocol=config.get('INBOUND_RULE','PROTOCOL'),
                DryRun=False
    )

    return (response['ResponseMetadata']['HTTPStatusCode'] == 200)


def delete_ec2_security_group(ec2_client):
    """
    Delete a security group
    :param ec2_client: ec2 client instance
    :return: True if security group deleted successfully
    """

    group_name = config.get('SECURITY_GROUP','NAME')
    group = get_group(ec2_client, group_name)

    if(group is None):
        logger.info("Group does not exist")
        return True

    response = ec2_client.delete_security_group(
        GroupId=group['GroupId'],
        GroupName=group_name,
        DryRun=False
    )

    logger.info(f"Delete response {response['ResponseMetadata']['HTTPStatusCode']}")
    return (response['ResponseMetadata']['HTTPStatusCode'] == 200)



if __name__ == "__main__":

    # Parsing arguments
    parser = argparse.ArgumentParser(description="A Redshift cluster IaC (Infrastructure as Code). It creates IAM role for the Redshift, creates security group and sets up ingress parameters."
                                                 " Finally spin-up a redshift cluster.")
    parser.add_argument("-c", "--cleanup", type=bool, metavar='', required=True, help="cleanup the roles, securitygroup and cluster.")
    parser.add_argument("-v", "--verbosity", type=bool, required=False, default=False, help="increase output verbosity")
    args = parser.parse_args()

    if(args.verbosity):
        logger.setLevel(logging.INFO)
    else:
        logging.setLoggerClass(logging.DEBUG)

    # print(boto3._get_default_session().get_available_services() ) # Getting aws services list
    # Creating low-level service clients

    ec2 = boto3.client(service_name = 'ec2', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    s3 = boto3.client(service_name = 's3', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    iam = boto3.client(service_name = 'iam', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    redshift = boto3.client(service_name = 'redshift', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    logger.info("Clients setup for all services.")

    # Setting up IAM Role, security group and cluster
    if(create_IAM_role(iam)):
        if(create_ec2_security_group(ec2)):
            role_arn = iam.get_role(RoleName = config.get('IAM_ROLE', 'NAME'))['Role']['Arn']
            vpc_security_group_id = get_group(ec2, config.get('SECURITY_GROUP', 'NAME'))['GroupId']
            create_cluster(redshift, role_arn, [vpc_security_group_id])
        else:
            logger.error("Failed to create security group")
    else:
        logger.error("Failed to create IAM role")


    # cleanup
    if(args.cleanup):
        delete_cluster(redshift)
        delete_ec2_security_group(ec2)
        delete_IAM_role(iam)
