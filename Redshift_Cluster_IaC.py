import boto3
import configparser
from botocore.exceptions import ClientError
import json
import logging
import logging.config
from pathlib import Path

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
    except Exception as e:
        logger.error(f"Error occured while creating role : {e}")
        return False


    try:
        # Attaching policy using ARN's( Amazon Resource Names )
        policy_response = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=role_policy_arn
        )
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

    try:
        detach_response = iam_client.detach_role_policy(RoleName=config.get('IAM_ROLE', 'NAME'), PolicyArn=config.get('IAM_ROLE','POLICY_ARN'))
        delete_response = iam_client.delete_role(RoleName=config.get('IAM_ROLE', 'NAME'))
    except Exception as e:
        logger.error(f"Exception occured while deleting role : {e}")

    return True if( (detach_response['ResponseMetadata']['HTTPStatusCode'] == 200) and  (delete_response['ResponseMetadata']['HTTPStatusCode'] == 200) ) else False


if __name__ == "__main__":

    # print(boto3._get_default_session().get_available_services() ) # Getting aws services list

    # Creating low-level service clients

    ec2 = boto3.client(service_name = 'ec2', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    s3 = boto3.client(service_name = 's3', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    iam = boto3.client(service_name = 'iam', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    redshift = boto3.client(service_name = 'redshift', region_name = 'us-east-1', aws_access_key_id=config.get('AWS', 'Key'), aws_secret_access_key=config.get('AWS', 'SECRET'))

    if(create_IAM_role(iam)):
        logger.info("Role created and policy applied !!")

    if(delete_IAM_role(iam)):
        logger.info("Deleted IAM role !!")

