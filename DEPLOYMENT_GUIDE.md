# GRC Platform - Complete Deployment Guide

## Table of Contents
1. Prerequisites
2. Architecture Overview
3. Step-by-Step Deployment
4. Configuration
5. Testing and Validation
6. Troubleshooting
7. Post-Deployment Steps

## 1. Prerequisites

### Required Software
- AWS CLI v2 or higher
- Docker (for local testing)
- Python 3.8+
- Git
- MySQL Client (for database management)

### AWS Account Requirements
- Active AWS account with appropriate permissions
- IAM user with the following permissions:
  - CloudFormation
  - EC2
  - RDS
  - Lambda
  - S3
  - DynamoDB
  - CloudTrail
  - Config
  - Security Hub
  - IAM

### Installation Steps

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (us-east-1)
# Enter your default output format (json)

# Verify installation
aws sts get-caller-identity
```

## 2. Architecture Overview

### System Components

The GRC platform consists of the following AWS services:

**Network Layer**
- VPC with public and private subnets across 2 availability zones
- Internet Gateway for public internet access
- NAT Gateway for private subnet internet access
- Application Load Balancer for traffic distribution

**Data Layer**
- Amazon RDS MySQL 8.0 for relational data
- Amazon S3 for evidence and report storage
- Amazon DynamoDB for compliance status and risk register
- AWS KMS for encryption

**Application Layer**
- Amazon ECS Fargate for containerized GRC application
- AWS Lambda for compliance monitoring and automation
- AWS API Gateway for REST API endpoints

**Security & Compliance Layer**
- AWS Config for resource compliance monitoring
- AWS CloudTrail for audit logging
- AWS Security Hub for security posture
- AWS IAM for access control

**Monitoring & Alerting**
- CloudWatch for metrics and logs
- SNS for alert notifications
- EventBridge for event routing

## 3. Step-by-Step Deployment

### Phase 1: Network Infrastructure

```bash
# Navigate to project directory
cd /home/ubuntu/grc-capstone-project

# Deploy network stack
aws cloudformation create-stack \
  --stack-name grc-capstone-network-stack \
  --template-body file://cloudformation-network-stack.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
  --region us-east-1

# Monitor stack creation
aws cloudformation describe-stacks \
  --stack-name grc-capstone-network-stack \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'

# Wait for stack to complete (typically 5-10 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name grc-capstone-network-stack \
  --region us-east-1
```

### Phase 2: Database Infrastructure

```bash
# Deploy database stack
# Note: You will be prompted for database credentials
aws cloudformation create-stack \
  --stack-name grc-capstone-database-stack \
  --template-body file://cloudformation-database-stack.yaml \
  --parameters \
    ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
    ParameterKey=DBUsername,ParameterValue=grcadmin \
    ParameterKey=DBPassword,ParameterValue=YourSecurePassword123! \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

# Wait for stack completion
aws cloudformation wait stack-create-complete \
  --stack-name grc-capstone-database-stack \
  --region us-east-1

# Get database endpoint
aws cloudformation describe-stacks \
  --stack-name grc-capstone-database-stack \
  --region us-east-1 \
  --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
  --output text
```

### Phase 3: Lambda Functions

```bash
# Create IAM role for Lambda
aws iam create-role \
  --role-name grc-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policies to role
aws iam attach-role-policy \
  --role-name grc-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name grc-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/ConfigUserAccess

# Package Lambda function
cd /home/ubuntu/grc-capstone-project
zip -r lambda_compliance_monitor.zip lambda_compliance_monitor.py

# Create Lambda function
aws lambda create-function \
  --function-name grc-compliance-monitor \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/grc-lambda-role \
  --handler lambda_compliance_monitor.lambda_handler \
  --zip-file fileb://lambda_compliance_monitor.zip \
  --timeout 60 \
  --memory-size 256 \
  --region us-east-1
```

### Phase 4: AWS Config Setup

```bash
# Enable AWS Config
aws configservice put-config-recorder \
  --config-recorder name=grc-recorder,roleARN=arn:aws:iam::ACCOUNT_ID:role/grc-config-role \
  --region us-east-1

# Start recording
aws configservice start-config-recorder \
  --config-recorder-names grc-recorder \
  --region us-east-1

# Create delivery channel
aws configservice put-delivery-channel \
  --delivery-channel name=grc-channel,s3BucketName=grc-config-bucket \
  --region us-east-1
```

### Phase 5: Database Initialization

```bash
# Get database endpoint
DB_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name grc-capstone-database-stack \
  --region us-east-1 \
  --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
  --output text)

# Connect to database and load sample data
mysql -h $DB_ENDPOINT -u grcadmin -p < sample_data.sql

# Verify data loaded
mysql -h $DB_ENDPOINT -u grcadmin -p -e "USE grcdb; SELECT * FROM compliance_summary;"
```

## 4. Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012

# Database Configuration
DB_HOST=grc-capstone-db.xxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306
DB_NAME=grcdb
DB_USER=grcadmin
DB_PASSWORD=YourSecurePassword123!

# S3 Configuration
EVIDENCE_BUCKET=grc-capstone-evidence-bucket-123456789012
COMPLIANCE_REPORTS_BUCKET=grc-capstone-compliance-reports-123456789012

# Lambda Configuration
LAMBDA_FUNCTION_NAME=grc-compliance-monitor
LAMBDA_ROLE_ARN=arn:aws:iam::123456789012:role/grc-lambda-role

# SNS Configuration
ALERT_SNS_TOPIC=arn:aws:sns:us-east-1:123456789012:grc-compliance-alerts
```

### CloudWatch Alarms

```bash
# Create alarm for high non-compliance
aws cloudwatch put-metric-alarm \
  --alarm-name grc-high-non-compliance \
  --alarm-description "Alert when compliance drops below 80%" \
  --metric-name CompliancePercentage \
  --namespace GRC \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT_ID:grc-compliance-alerts
```

## 5. Testing and Validation

### Run Test Suite

```bash
# Run all tests
python3 test_cases.py

# Run specific test class
python3 -m unittest test_cases.TestComplianceMonitoring

# Run with verbose output
python3 -m unittest test_cases -v
```

### Manual Testing

```bash
# Test Lambda function
aws lambda invoke \
  --function-name grc-compliance-monitor \
  --region us-east-1 \
  response.json

cat response.json

# Test database connectivity
mysql -h $DB_ENDPOINT -u grcadmin -p -e "SELECT VERSION();"

# Test S3 access
aws s3 ls s3://grc-capstone-evidence-bucket-ACCOUNT_ID/

# Test DynamoDB tables
aws dynamodb scan \
  --table-name grc-compliance-status \
  --region us-east-1
```

## 6. Troubleshooting

### Common Issues

**Issue: CloudFormation Stack Creation Failed**
```bash
# Check stack events
aws cloudformation describe-stack-events \
  --stack-name grc-capstone-network-stack \
  --region us-east-1 \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'

# Rollback failed stack
aws cloudformation delete-stack \
  --stack-name grc-capstone-network-stack \
  --region us-east-1
```

**Issue: Database Connection Timeout**
```bash
# Verify security group allows traffic
aws ec2 describe-security-groups \
  --group-ids sg-xxxxxxxx \
  --region us-east-1

# Check RDS instance status
aws rds describe-db-instances \
  --db-instance-identifier grc-capstone-db \
  --region us-east-1 \
  --query 'DBInstances[0].DBInstanceStatus'
```

**Issue: Lambda Function Execution Error**
```bash
# Check Lambda logs
aws logs tail /aws/lambda/grc-compliance-monitor --follow

# Check Lambda IAM role permissions
aws iam get-role-policy \
  --role-name grc-lambda-role \
  --policy-name grc-lambda-policy
```

## 7. Post-Deployment Steps

### 1. Configure Monitoring Dashboard

```bash
# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name GRC-Platform \
  --dashboard-body file://cloudwatch-dashboard.json
```

### 2. Set Up Automated Compliance Checks

```bash
# Create EventBridge rule for hourly compliance checks
aws events put-rule \
  --name grc-compliance-check \
  --schedule-expression "rate(1 hour)" \
  --state ENABLED

# Add Lambda as target
aws events put-targets \
  --rule grc-compliance-check \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:ACCOUNT_ID:function:grc-compliance-monitor"
```

### 3. Enable CloudTrail Logging

```bash
# Create S3 bucket for CloudTrail
aws s3 mb s3://grc-cloudtrail-logs-ACCOUNT_ID --region us-east-1

# Create CloudTrail
aws cloudtrail create-trail \
  --name grc-trail \
  --s3-bucket-name grc-cloudtrail-logs-ACCOUNT_ID \
  --region us-east-1

# Start logging
aws cloudtrail start-logging \
  --trail-name grc-trail \
  --region us-east-1
```

### 4. Configure Backup and Disaster Recovery

```bash
# Enable RDS automated backups (already configured in template)
# Verify backup retention
aws rds describe-db-instances \
  --db-instance-identifier grc-capstone-db \
  --region us-east-1 \
  --query 'DBInstances[0].BackupRetentionPeriod'

# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier grc-capstone-db \
  --db-snapshot-identifier grc-initial-snapshot \
  --region us-east-1
```

### 5. Set Up Access Control

```bash
# Create IAM policy for GRC administrators
aws iam create-policy \
  --policy-name GRC-Admin-Policy \
  --policy-document file://grc-admin-policy.json

# Create IAM group for GRC users
aws iam create-group --group-name grc-users

# Attach policy to group
aws iam attach-group-policy \
  --group-name grc-users \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/GRC-Admin-Policy
```

## Deployment Checklist

- [ ] AWS CLI installed and configured
- [ ] Network stack deployed successfully
- [ ] Database stack deployed successfully
- [ ] Database initialized with sample data
- [ ] Lambda functions created and tested
- [ ] AWS Config enabled and recording
- [ ] CloudTrail enabled for audit logging
- [ ] Security groups configured correctly
- [ ] IAM roles and policies in place
- [ ] CloudWatch alarms configured
- [ ] Test suite passes all tests
- [ ] Monitoring dashboard created
- [ ] Backup strategy implemented
- [ ] Documentation reviewed

## Support and Maintenance

### Regular Maintenance Tasks

- Monitor CloudWatch metrics daily
- Review compliance reports weekly
- Update AWS Config rules monthly
- Audit IAM permissions quarterly
- Test disaster recovery procedures annually

### Backup and Recovery

- Daily automated RDS backups (30-day retention)
- Weekly manual snapshots
- Test recovery procedures monthly

### Security Updates

- Apply AWS security patches automatically
- Review AWS security advisories monthly
- Update Lambda function dependencies quarterly

## Additional Resources

- AWS GRC Documentation: https://docs.aws.amazon.com/grc/
- AWS Security Best Practices: https://aws.amazon.com/security/best-practices/
- AWS Config User Guide: https://docs.aws.amazon.com/config/
- AWS Lambda Developer Guide: https://docs.aws.amazon.com/lambda/
