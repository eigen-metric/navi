import boto3
import click
from .database import db_query
from .tag import tag_by_uuid


def organize_aws_keys(aws_ec2):
    '''Collect All Ids to reduce calls to the T.io API'''
    aws = {}
    aws_keys = {}
    for tags in aws_ec2['Tags']:
        if tags['ResourceType'] == 'instance':
            aws_key = tags['Key']
            aws_value = tags['Value']
            resource_id = tags['ResourceId']

            # Tenable IO Requires a Key and a Value; AWS does not.  In this case we just use the key as both
            if aws_value == '':
                aws_value = aws_key

            try:
                aws[aws_value].append(resource_id)
            except KeyError:
                aws[aws_value] = [resource_id]

            aws_keys[aws_key] = {aws_value: aws[aws_value]}

    return aws_keys


@click.command(help="Migrate AWS Tags to T.io tags by Instance ID")
@click.option("--region", default="", required=True, help="AWS Region")
@click.option("--a", default="", required=True, help="AWS Region")
@click.option("--s", default="", required=True, help="AWS Region")
def migrate(region, a, s):
    # Authentication
    ec2client = boto3.client('ec2', region_name=region, aws_access_key_id=a, aws_secret_access_key=s)

    # Grab All of the tags in the Account
    aws_ec2 = ec2client.describe_tags()

    # Send the data to get organized into a neat dictionary of Lists
    aws_organized_tags = organize_aws_keys(aws_ec2)

    # Grab the Key, value and the new list out of the dict to send to the tagging function
    for key, value in aws_organized_tags.items():
        for z, w in value.items():
            uuid_list = []
            for instance in w:
                # Look up the UUID of the asset
                db = db_query("select uuid from assets where aws_id='{}';".format(instance))
                for record in db:
                    uuid_list.append(record[0])
            description = "AWS Tag by Navi"

            print("Creating a Tag named - {} : {} - with the following ids {}".format(z, key, w))

            tag_by_uuid(uuid_list,key, z, description)
