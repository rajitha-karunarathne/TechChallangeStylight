# Stylight Technical Challenge. #

Have implemented and tested out the following solution for this technical challenge.

Since this is more over scheduled event-based application and in order to void certain unnecessary idle time cost and all decided to use AWS Lambda function Service. Additionally, to keep history of findings for later audits , store the details in a DynamoDB table.

## 1.	Tech Stack Used for the Solution:

•	Cloud Service Provider: AWS
•	Serverless Service: Lambda
•	Data Base: DynamoDB 
•	Event Scheduler: Event Bridge
•	IaC : AWS CloudFormation
•	Version Control and Source Code Management + CI/CD : github.com
•	Repository URL: https://github.com/rajitha-karunarathne/TechChallengeStylight

## 2.	CFT Template Sequence:

Following CFTs have been used to deploy the above Infrastructure Setup into an AWS Account, which can be founded in the above-mentioned repository path -> https://github.com/rajitha-karunarathne/TechChallengeStylight/tree/master/infrastructure

I.	Stylight-DB.yml : To Deploy the DynamoDB to later audit the findings.
II.	Stylight-IAM.yml : To Deploy the necessary policy permission to run the solution.
III.Stylight-Lambda.yml : To Deploy the Lambda Function , SNS Topic , Event Scheduler for the solution.


## 3.	Deployment Steps:

## Prerequisite: 

•	Github account access.
•	Fork or clone the repo -> https://github.com/rajitha-karunarathne/TechChallengeApp
•	AWS account with Administrator / root user access (Recommended).

## Steps:

1.	Create an IAM User (Preferably with Admin access), by allowing only the AWS programmatic access and download the credential file. (Do not share this with anyone else).

2.	Add the Access key ID and Secret access key to the Github secrets of the above repository settings. 
 Use the naming as, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

3.	Select the Github Actions and then “Deploy Stylight Application Infrastructure” and Run the Workflow as follows, give some time to Deploy the full infrastructure setup.

4. If all goes well and the build will be successful and please Confirm the SNS subscription once you have received the mail as below for the above entered email in order to receive the SNS notifications.



 

