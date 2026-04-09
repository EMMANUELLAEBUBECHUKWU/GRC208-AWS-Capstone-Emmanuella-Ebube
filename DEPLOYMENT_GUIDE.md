# Deployment Guide

## GRC208 AWS Integrated GRC Platform

|                       |                                                                 |
|-----------------------|-----------------------------------------------------------------|
|**Name**               |Emmanuella Ebubechukwu                                           |
|**Student ID**         |2025/GRC/10041                                                   |
|**Course**             |GRC208 - Governance, Risk, and Compliance                        |
|**Institution**        |International Cybersecurity and Digital Forensics Academy (ICDFA)|
|**Date Deployed**      |April 9, 2026                                                    |
|**Environment**        |AWS Free Tier Personal Account                                   |
|**AWS Account ID**     |562923011251                                                     |
|**Region**             |us-east-1 (N. Virginia)                                          |
|**IAM User**           |emmanuella-admin                                                 |

This document is a record of how I deployed the AWS Integrated GRC Platform for my GRC208 capstone. It covers every command I ran, every error I encountered, and exactly how I resolved each one. Anyone following this guide on a personal AWS Free Tier account should be able to replicate the same deployment without running into the same issues I did.

-----

## Environment Setup

Before starting the deployment, I confirmed the following were ready:

- AWS Free Tier account active with a $10 budget alert configured
- IAM user `emmanuella-admin` created with AdministratorAccess
- MFA enabled on the IAM user
- Region set to us-east-1 (N. Virginia) throughout
- AWS CloudShell opened directly from the AWS Management Console

I verified my identity first to confirm I was working in the correct account:

```bash
aws sts get-caller-identity
```

Output:

```json
{
    "UserId": "AIDAYGEGTPSZ7LDAERXFA",
    "Account": "562923011251",
    "Arn": "arn:aws:iam::562923011251:user/emmanuella-admin"
}
```

Then I cloned the instructor’s project files into CloudShell:

```bash
git clone https://github.com/icdfa/GRC208-AWS-Capstone-Project.git
cd GRC208-AWS-Capstone-Project
```

-----

## Phase 1: Network Infrastructure

This phase deploys the VPC, public and private subnets across two availability zones, security groups, internet gateway, NAT gateway, and an application load balancer.

```bash
aws cloudformation create-stack \
  --stack-name grc-capstone-network-stack \
  --template-body file://cloudformation-network-stack.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
  --region us-east-1
```

I checked the status until it returned CREATE_COMPLETE:

```bash
aws cloudformation describe-stacks \
  --stack-name grc-capstone-network-stack \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```

Then I retrieved the stack outputs to confirm all resources were created:

```bash
aws cloudformation describe-stacks \
  --stack-name grc-capstone-network-stack \
  --region us-east-1 \
  --query 'Stacks[0].Outputs' \
  --output table
```

Resources created:

|Resource          |ID                      |
|------------------|------------------------|
|VPC               |vpc-00204003995d48e34   |
|Public Subnet 1   |subnet-0e6c4823316500b67|
|Public Subnet 2   |subnet-0f1683e183304d7ee|
|Private Subnet 1  |subnet-0bb3889421244130e|
|Private Subnet 2  |subnet-0c79c9a2301e854e2|
|RDS Security Group|sg-064802794fa337415    |
|ECS Security Group|sg-0771599d1db672c25    |

Phase 1 completed with no errors.

-----

## Phase 2: Database Infrastructure

This phase deploys the RDS MySQL instance, two S3 buckets for evidence and compliance reports, and three DynamoDB tables.

### Issue Encountered: ROLLBACK_COMPLETE on First Attempt

The first deployment attempt failed immediately. I checked the failure reason:

```bash
aws cloudformation describe-stack-events \
  --stack-name grc-capstone-database-stack \
  --region us-east-1 \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`].[ResourceType,ResourceStatusReason]' \
  --output table
```

The error returned was:

```
Properties validation failed for resource EvidenceBucket with message:
#: extraneous key [ServerSideEncryptionConfiguration] is not permitted

Properties validation failed for resource ComplianceReportsBucket with message:
#: extraneous key [ServerSideEncryptionConfiguration] is not permitted
```

The S3 bucket encryption property in the original template was placed at the wrong level. I deleted the failed stack and fixed the template using sed:

```bash
aws cloudformation delete-stack \
  --stack-name grc-capstone-database-stack \
  --region us-east-1

sed -i 's/ServerSideEncryptionConfiguration/BucketEncryption/g' cloudformation-database-stack.yaml
```

### Issue Encountered: Second ROLLBACK_COMPLETE

The second attempt also failed. The new error was:

```
#/BucketEncryption: expected type: JSONObject, found: JSONArray
```

The sed replacement fixed the property name but the structure was still invalid. Rather than patching the original template further, I replaced it entirely with a clean Free Tier compatible version. I used the following to write the new template directly in CloudShell:

```bash
cat > cloudformation-database-stack.yaml << 'EOF'
...
EOF
```

The fixed template used:

- RDS MySQL EngineVersion 8.0.40
- DBInstanceClass db.t3.micro
- AllocatedStorage 20
- StorageEncrypted false
- BackupRetentionPeriod 0
- DeletionProtection false
- No KMS key
- S3 buckets with AES256 server-side encryption
- Subnets and security group imported from the network stack using ImportValue
- DynamoDB tables for grc-compliance-status, grc-risk-register, and grc-controls

### Successful Deployment

```bash
aws cloudformation create-stack \
  --stack-name grc-capstone-database-stack \
  --template-body file://cloudformation-database-stack.yaml \
  --parameters \
    ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
    ParameterKey=DBUsername,ParameterValue=grcadmin \
    ParameterKey=DBPassword,ParameterValue=GrcAdmin2025! \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

The stack took approximately 12 minutes to complete. I confirmed outputs with:

```bash
aws cloudformation describe-stacks \
  --stack-name grc-capstone-database-stack \
  --region us-east-1 \
  --query 'Stacks[0].Outputs' \
  --output table
```

Resources created:

|Resource        |Value                                                   |
|----------------|--------------------------------------------------------|
|RDS Endpoint    |grc-capstone-db.cyrou02g6leq.us-east-1.rds.amazonaws.com|
|Evidence Bucket |grc-capstone-evidence-562923011251                      |
|Reports Bucket  |grc-capstone-reports-562923011251                       |
|Compliance Table|grc-compliance-status                                   |
|Risk Table      |grc-risk-register                                       |
|Controls Table  |grc-controls                                            |

-----

## Phase 3: Lambda Function

This phase creates the IAM role for Lambda, attaches the required policies, packages the compliance monitor function, and deploys it.

### Create the IAM Role

```bash
aws iam create-role \
  --role-name grc-lambda-role \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
```

### Attach Policies

```bash
aws iam attach-role-policy \
  --role-name grc-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name grc-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AWSConfigUserAccess
```

### Package and Deploy

```bash
zip -r lambda_compliance_monitor.zip lambda_compliance_monitor.py

aws lambda create-function \
  --function-name grc-compliance-monitor \
  --runtime python3.11 \
  --role arn:aws:iam::562923011251:role/grc-lambda-role \
  --handler lambda_compliance_monitor.lambda_handler \
  --zip-file fileb://lambda_compliance_monitor.zip \
  --timeout 60 \
  --memory-size 256 \
  --region us-east-1
```

### Test the Function

```bash
aws lambda invoke \
  --function-name grc-compliance-monitor \
  --region us-east-1 \
  response.json && cat response.json
```

Response:

```json
{"statusCode": 200, "body": "{\"message\": \"Compliance monitoring completed\", \"compliance_percentage\": 0, \"non_compliant_rules\": 0}"}
```

Phase 3 completed successfully.

-----

## Phase 4: AWS Config and CloudTrail

This phase sets up continuous compliance recording with AWS Config and full audit logging with AWS CloudTrail.

### AWS Config Setup

#### Issue Encountered: Insufficient Delivery Policy

Using the Lambda role for the Config recorder caused this error:

```
An error occurred (NoAvailableDeliveryChannelException):
Delivery channel is not available to start configuration recorder.

An error occurred (InsufficientDeliveryPolicyException):
Insufficient delivery policy to s3 bucket: grc-capstone-evidence-562923011251,
unable to assume role: arn:aws:iam::562923011251:role/grc-lambda-role
```

The fix required three things: a dedicated IAM role for Config, the AWS managed Config policy attached to that role, and an explicit S3 bucket policy allowing Config to write to the evidence bucket.

#### Create the Config Role

```bash
aws iam create-role \
  --role-name grc-config-role \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"config.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

aws iam attach-role-policy \
  --role-name grc-config-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWS_ConfigRole
```

#### Apply S3 Bucket Policy for Config

```bash
aws s3api put-bucket-policy \
  --bucket grc-capstone-evidence-562923011251 \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AWSConfigBucketPermissionsCheck",
        "Effect": "Allow",
        "Principal": {"Service": "config.amazonaws.com"},
        "Action": "s3:GetBucketAcl",
        "Resource": "arn:aws:s3:::grc-capstone-evidence-562923011251"
      },
      {
        "Sid": "AWSConfigBucketDelivery",
        "Effect": "Allow",
        "Principal": {"Service": "config.amazonaws.com"},
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::grc-capstone-evidence-562923011251/AWSLogs/562923011251/Config/*",
        "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
      }
    ]
  }'
```

#### Configure and Start the Recorder

```bash
aws configservice put-configuration-recorder \
  --configuration-recorder name=grc-recorder,roleARN=arn:aws:iam::562923011251:role/grc-config-role \
  --recording-group allSupported=true,includeGlobalResourceTypes=true \
  --region us-east-1

aws configservice put-delivery-channel \
  --delivery-channel name=grc-channel,s3BucketName=grc-capstone-evidence-562923011251 \
  --region us-east-1

aws configservice start-configuration-recorder \
  --configuration-recorder-name grc-recorder \
  --region us-east-1
```

I verified the recorder was running:

```bash
aws configservice describe-configuration-recorders \
  --region us-east-1 \
  --output table
```

The output confirmed recording frequency as CONTINUOUS and all supported resource types being recorded.

### CloudTrail Setup

#### Create the S3 Bucket for CloudTrail Logs

```bash
aws s3 mb s3://grc-cloudtrail-logs-562923011251 --region us-east-1
```

#### Issue Encountered: Insufficient S3 Bucket Policy

The first attempt to create the trail returned:

```
An error occurred (InsufficientS3BucketPolicyException):
Incorrect S3 bucket policy is detected for bucket: grc-cloudtrail-logs-562923011251
```

I applied the required bucket policy before creating the trail:

```bash
aws s3api put-bucket-policy \
  --bucket grc-cloudtrail-logs-562923011251 \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AWSCloudTrailAclCheck",
        "Effect": "Allow",
        "Principal": {"Service": "cloudtrail.amazonaws.com"},
        "Action": "s3:GetBucketAcl",
        "Resource": "arn:aws:s3:::grc-cloudtrail-logs-562923011251"
      },
      {
        "Sid": "AWSCloudTrailWrite",
        "Effect": "Allow",
        "Principal": {"Service": "cloudtrail.amazonaws.com"},
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::grc-cloudtrail-logs-562923011251/AWSLogs/562923011251/*",
        "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
      }
    ]
  }'
```

#### Create and Start the Trail

```bash
aws cloudtrail create-trail \
  --name grc-trail \
  --s3-bucket-name grc-cloudtrail-logs-562923011251 \
  --region us-east-1

aws cloudtrail start-logging \
  --name grc-trail \
  --region us-east-1
```

I verified logging was active:

```bash
aws cloudtrail get-trail-status \
  --name grc-trail \
  --region us-east-1 \
  --query '[IsLogging]' \
  --output table
```

Output confirmed IsLogging: True.

-----

## Phase 5: Sample Data Loading

### Attempted: Loading sample_data.sql into RDS

The deployment guide specifies loading sample data into the RDS MySQL database using:

```bash
mysql -h $DB_ENDPOINT -u grcadmin -p < sample_data.sql
```

I attempted this after confirming the RDS endpoint was available. The connection failed with:

```
ERROR 2002 (HY000): Can't connect to MySQL server on
'grc-capstone-db.cyrou02g6leq.us-east-1.rds.amazonaws.com' (115)
```

To investigate, I temporarily added an inbound rule to the RDS security group allowing port 3306 from the CloudShell IP address and modified the RDS instance to be publicly accessible:

```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-064802794fa337415 \
  --protocol tcp \
  --port 3306 \
  --cidr 3.94.196.117/32 \
  --region us-east-1

aws rds modify-db-instance \
  --db-instance-identifier grc-capstone-db \
  --publicly-accessible \
  --apply-immediately \
  --region us-east-1
```

The connection still failed. The root cause is that the RDS instance sits in a private subnet that has no route to the internet gateway. Even with the instance set to publicly accessible, the subnet routing prevents external connections from reaching it. This is the private subnet architecture working as designed.

Both temporary changes were immediately reverted after the investigation:

```bash
aws rds modify-db-instance \
  --db-instance-identifier grc-capstone-db \
  --no-publicly-accessible \
  --apply-immediately \
  --region us-east-1

aws ec2 revoke-security-group-ingress \
  --group-id sg-064802794fa337415 \
  --protocol tcp \
  --port 3306 \
  --cidr 3.94.196.117/32 \
  --region us-east-1
```

### Alternative: Loading Sample Data into DynamoDB

Since direct RDS access was not possible from CloudShell on this Free Tier account, sample data was loaded directly into the three DynamoDB tables instead:

```bash
aws dynamodb put-item \
  --table-name grc-compliance-status \
  --item '{"complianceId": {"S": "COMP-001"}, "framework": {"S": "ISO27001"}, "status": {"S": "COMPLIANT"}, "lastChecked": {"S": "2026-04-09"}, "controlCount": {"N": "30"}}' \
  --region us-east-1

aws dynamodb put-item \
  --table-name grc-risk-register \
  --item '{"riskId": {"S": "RISK-001"}, "riskName": {"S": "Unauthorized Access"}, "likelihood": {"N": "4"}, "impact": {"N": "5"}, "riskScore": {"N": "20"}, "status": {"S": "OPEN"}}' \
  --region us-east-1

aws dynamodb put-item \
  --table-name grc-controls \
  --item '{"controlId": {"S": "CTRL-001"}, "controlName": {"S": "Access Control Policy"}, "framework": {"S": "ISO27001"}, "status": {"S": "IMPLEMENTED"}, "owner": {"S": "Security Team"}}' \
  --region us-east-1
```

I verified each table had data:

```bash
aws dynamodb scan --table-name grc-compliance-status --region us-east-1 --output table
aws dynamodb scan --table-name grc-risk-register --region us-east-1 --output table
aws dynamodb scan --table-name grc-controls --region us-east-1 --output table
```

All three tables returned their records correctly. The sample_data.sql file is included in the repository as a deliverable and would work as intended in an environment with direct database access such as through a bastion host or VPN connection into the VPC.

-----

## Test Suite

With all five phases complete, I ran the full test suite to validate the deployment:

```bash
python3 test_cases.py
```

Result:

```
Ran 22 tests in 0.001s
OK
```

All 22 tests passed across Compliance Monitoring, Risk Assessment, Data Validation, Database Operations, Framework Mapping, Audit Logging, Report Generation, and Integration Workflows.

-----

## Final Verification

I ran a combined verification to confirm all services were active at the same time:

```bash
echo "=== GRC Platform Final Verification ===" && \
echo "Network Stack:" && \
aws cloudformation describe-stacks --stack-name grc-capstone-network-stack --region us-east-1 --query 'Stacks[0].StackStatus' && \
echo "Database Stack:" && \
aws cloudformation describe-stacks --stack-name grc-capstone-database-stack --region us-east-1 --query 'Stacks[0].StackStatus' && \
echo "Lambda Function:" && \
aws lambda get-function --function-name grc-compliance-monitor --region us-east-1 --query 'Configuration.State' && \
echo "Config Recorder:" && \
aws configservice describe-configuration-recorder-status --region us-east-1 --query 'ConfigurationRecordersStatus[0].recording' && \
echo "CloudTrail:" && \
aws cloudtrail get-trail-status --name grc-trail --region us-east-1 --query 'IsLogging'
```

Result:

```
=== GRC Platform Final Verification ===
Network Stack:
"CREATE_COMPLETE"
Database Stack:
"CREATE_COMPLETE"
Lambda Function:
"Active"
Config Recorder:
true
CloudTrail:
true
```

All services confirmed running. Deployment complete.
