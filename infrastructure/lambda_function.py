""""Script to identify the Expensive Resources"""

import json
import logging
import os
import datetime
import re
import boto3

#Get Env Variable Values
if os.environ.get("EC2_ESTIMATION") is not None:
    ec2_estimation = os.environ["EC2_ESTIMATION"]
    ec2_estimation = float(ec2_estimation)
else:
    raise Exception("EC2_ESTIMATION parameter is required")
    
if os.environ.get("RDS_ESTIMATION") is not None:
    rds_estimation = os.environ["RDS_ESTIMATION"]
    rds_estimation = float(rds_estimation)
else:
    raise Exception("RDS_ESTIMATION parameter is required")
    
if os.environ.get("SNS_TOPIC_ARN") is not None:
    sns_topic_arn = os.environ["SNS_TOPIC_ARN"]
else:
    raise Exception("SNS_TOPIC_ARN parameter is required")

#Calculate the Cost Usage and Output
def usage_calculation(service,billing_client,your_estimation):
    
    # getting dates (yyyy-MM-dd) and converting to string
    today = datetime.date.today()
    weekback = today - datetime.timedelta(days=7)
    str_today = str(today)
    str_weekback = str(weekback)
    
    response = billing_client.get_cost_and_usage( 
       TimePeriod={ 
         'Start': str_weekback, 
         'End': str_today },
       Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': [
                service,
            ],
       }
       },
       Granularity='DAILY', 
       Metrics=[ 'UnblendedCost'],
       GroupBy=[
            {
                'Type': 'TAG',
                'Key': 'Name'
            },
        ]
    )
    
    cost_usage = []
    for Name in response["ResultsByTime"][0]["Groups"]:
        namestring = Name['Keys'][0]
        name = re.search("\$(.*)", namestring).group(1)
        if name is None or name == "":
            name = "Other"

        amount = Name['Metrics']['UnblendedCost']['Amount']
        amount = float(amount)
        
        if amount > your_estimation:
        
            line = "{} : ${:,.2f}".format(name, amount)
            cost_usage.append(line)
        
    return cost_usage
    
def send_sns_email(sns_messege,sns,sns_topic_arn):
    response = sns.publish(
    TopicArn=sns_topic_arn,
    Message=sns_messege
    )
    
    print(response)

def lambda_handler(event, context):
    ########### Getting the Amount spent in AWS ########### 
    # opening connection with cost explorer 
    billing_client = boto3.client("ce")
    
    # Create an SNS client
    sns = boto3.client('sns')
    
    # Get EC2 Expensive
    ec2_usage_msg = usage_calculation('Amazon Elastic Compute Cloud - Compute',billing_client,ec2_estimation)
    
    # Get RDS Expensive
    rds_usage_msg = usage_calculation('Relational Database Service (RDS)',billing_client,rds_estimation)

    # Generate the Warning Messege
    sns_messege = f"Following EC2s have exceeded the Cost threshold, {ec2_usage_msg}\n\n Following RDSs have exceeded the Cost threshold, {rds_usage_msg}"
        
    # Publish a warning message to the specified SNS topic
    send_sns_email(sns_messege,sns,sns_topic_arn)