# GRC208 AWS Integrated GRC Platform

## Capstone Project — Emmanuella Ebubechukwu

|                   |                                                                 |
|-------------------|-----------------------------------------------------------------|
|**Student**        |Emmanuella Ebubechukwu                                           |
|**Student ID**     |2025/GRC/10041                                                   |
|**Programme**      |GRC Engineering (CGRCE)                                          |
|**Institution**    |International Cybersecurity and Digital Forensics Academy (ICDFA)|
|**Course**         |GRC208 — Governance, Risk, and Compliance Capstone               |
|**Submission Date**|April 21, 2026                                                   |

-----

## Project Overview

This repository contains my capstone submission for GRC208. The project involved designing and deploying a fully functional AWS Integrated GRC Platform from scratch on a personal AWS Free Tier account. The platform demonstrates practical, hands-on implementation of governance, risk, and compliance management using AWS native services.

Governance, Risk, and Compliance (GRC) is a critical function in any organisation that handles sensitive data or operates under regulatory requirements. This project translates GRC principles into a real cloud architecture — moving beyond theory to show how compliance monitoring, risk tracking, audit logging, and access control work together in a live environment.

The deployment was carried out entirely through AWS CloudShell using Infrastructure as Code (CloudFormation). All five phases were completed successfully, verified, and documented with screenshots. The platform supports six major compliance frameworks: ISO 27001, NIST Cybersecurity Framework, PCI DSS, HIPAA, GDPR, and SOC 2.

-----

## AWS Account Details

|Attribute      |Value                  |
|---------------|-----------------------|
|Account ID     |562923011251           |
|Region         |us-east-1 (N. Virginia)|
|IAM User       |emmanuella-admin       |
|Deployment Date|April 9, 2026          |

-----

## Prerequisites

The following were in place before deployment began:

- Active AWS Free Tier account with a budget alert set at $10
- IAM user `emmanuella-admin` created with AdministratorAccess
- MFA enabled on the `emmanuella-admin` IAM user as a GRC security requirement
- AWS CloudShell accessed directly from the AWS Management Console
- GitHub repository created for submission
- Personal Access Token generated for GitHub authentication
- Instructor’s project files cloned from the ICDFA GitHub repository

-----

## Deployment Summary

All five phases were deployed successfully in sequence:

|Phase  |Description                                            |Status  |
|-------|-------------------------------------------------------|--------|
|Phase 1|Network Infrastructure — VPC, subnets, security groups |Complete|
|Phase 2|Database Infrastructure — RDS MySQL, S3, DynamoDB      |Complete|
|Phase 3|Lambda Function — compliance monitoring                |Complete|
|Phase 4|AWS Config and CloudTrail — audit logging and recording|Complete|
|Phase 5|Sample Data Loading — DynamoDB tables populated        |Complete|

Each phase was deployed using AWS CloudFormation and verified before proceeding to the next. Status checks were run after each stack creation to confirm `CREATE_COMPLETE` before moving forward.

-----

## How to Deploy

Follow these steps to replicate this deployment in your own AWS account:

**Step 1 — Clone the project files**

```bash
git clone https://github.com/icdfa/GRC208-AWS-Capstone-Project.git
cd GRC208-AWS-Capstone-Project
```

**Step 2 — Deploy the network stack**

```bash
aws cloudformation create-stack \
  --stack-name grc-capstone-network-stack \
  --template-body file://cloudformation-network-stack.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
  --region us-east-1
```

**Step 3 — Deploy the database stack**

```bash
aws cloudformation create-stack \
  --stack-name grc-capstone-database-stack \
  --template-body file://cloudformation-database-stack.yaml \
  --parameters \
    ParameterKey=EnvironmentName,ParameterValue=grc-capstone \
    ParameterKey=DBUsername,ParameterValue=grcadmin \
    ParameterKey=DBPassword,ParameterValue=YourSecurePassword123! \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

Note: The cloudformation-database-stack.yaml in this repository has been updated 
to resolve Free Tier compatibility issues encountered during deployment. 
See Challenges and Fixes for full details.

**Step 4 — Deploy the Lambda function**

```bash
zip -r lambda_compliance_monitor.zip lambda_compliance_monitor.py
aws lambda create-function \
  --function-name grc-compliance-monitor \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/grc-lambda-role \
  --handler lambda_compliance_monitor.lambda_handler \
  --zip-file fileb://lambda_compliance_monitor.zip \
  --timeout 60 \
  --memory-size 256 \
  --region us-east-1
```

**Step 5 — Set up AWS Config and CloudTrail**

Create dedicated IAM roles for both services, apply S3 bucket policies, then start recording. Full commands are documented in `DEPLOYMENT_GUIDE.md`.

**Step 6 — Load sample data and run tests**

```bash
python3 test_cases.py
```

-----

## AWS Resources Deployed

**Network Stack**

- VPC: `vpc-00204003995d48e34`
- Public Subnet 1: `subnet-0e6c4823316500b67`
- Public Subnet 2: `subnet-0f1683e183304d7ee`
- Private Subnet 1: `subnet-0bb3889421244130e`
- Private Subnet 2: `subnet-0c79c9a2301e854e2`
- RDS Security Group: `sg-064802794fa337415`
- ECS Security Group: `sg-0771599d1db672c25`

**Database Stack**

- RDS MySQL Endpoint: `grc-capstone-db.cyrou02g6leq.us-east-1.rds.amazonaws.com`
- Evidence S3 Bucket: `grc-capstone-evidence-562923011251`
- Reports S3 Bucket: `grc-capstone-reports-562923011251`
- DynamoDB Tables: `grc-compliance-status`, `grc-risk-register`, `grc-controls`

**Lambda**

- Function: `grc-compliance-monitor`
- Runtime: Python 3.11
- Status: Active

**Monitoring and Audit**

**Monitoring and Audit**

- AWS Config Recorder: `grc-recorder` — Recording (Continuous)
- AWS Config Rules: `cloudtrail-enabled` (COMPLIANT), `s3-bucket-server-side-encryption-enabled` (COMPLIANT), `iam-password-policy` (NON_COMPLIANT)
- Compliance Percentage: 66.67% — 2 of 3 rules compliant
- Non-compliant rule: `iam-password-policy` — no custom IAM password policy set on Free Tier account
- CloudTrail: `grc-trail` — Logging enabled, last delivery 2026-04-12
- CloudTrail S3 Bucket: `grc-cloudtrail-logs-562923011251`
- Lambda invocation result: compliance_percentage 66.67, non_compliant_rules 1, StatusCode 200
-----

## Test Results

```
Ran 22 tests in 0.001s
OK
```

All 22 test cases passed across the following modules:

|Module               |Tests|Result|
|---------------------|-----|------|
|Compliance Monitoring|3    |Passed|
|Risk Assessment      |3    |Passed|
|Data Validation      |4    |Passed|
|Database Operations  |3    |Passed|
|Framework Mapping    |2    |Passed|
|Audit Logging        |3    |Passed|
|Report Generation    |2    |Passed|
|Integration Workflows|2    |Passed|

-----

## Challenges and Fixes

Three real-world issues were encountered and resolved during deployment:

**1. Database Stack Rollback — S3 Encryption and KMS Incompatibility**

The original `cloudformation-database-stack.yaml` failed with `ROLLBACK_COMPLETE` because the S3 bucket resource used an invalid encryption property and the KMS key configuration was not compatible with the Free Tier account. The template was replaced with a simplified Free Tier compatible version using AES256 server-side encryption, a `db.t3.micro` RDS instance class, no KMS key, and `BackupRetentionPeriod` set to 0. This resolved the issue and the stack deployed successfully on the next attempt.

**2. AWS Config and CloudTrail Delivery Channel Errors**

Both AWS Config and CloudTrail returned permission errors when trying to write to S3 using the Lambda IAM role. The fix involved creating a dedicated `grc-config-role` with the `AWS_ConfigRole` managed policy attached and `config.amazonaws.com` as the trusted service. A separate S3 bucket policy was also applied to explicitly allow `config.amazonaws.com` and `cloudtrail.amazonaws.com` to perform `s3:GetBucketAcl` and `s3:PutObject`. Once both roles and policies were in place, the delivery channels were created and recording started successfully.

**3. GitHub Push Rejected — Divergent Branch History**

When pushing the project files to GitHub, the push was initially rejected because the remote repository already contained an initial commit with a README file. This created divergent branch histories. The fix involved deleting the remote README and running a force push with `--force`, which successfully pushed all 34 project files to the repository.

-----

## Compliance Frameworks Covered

|Framework                   |Description                                        |
|----------------------------|---------------------------------------------------|
|ISO 27001                   |Information Security Management System             |
|NIST Cybersecurity Framework|Risk management and security controls              |
|PCI DSS                     |Payment Card Industry Data Security Standard       |
|HIPAA                       |Health Insurance Portability and Accountability Act|
|GDPR                        |General Data Protection Regulation                 |
|SOC 2                       |Service Organization Control Framework             |

-----

## Learning Outcomes

Through this capstone deployment, I gained practical experience in the following areas:

- Deploying cloud infrastructure using Infrastructure as Code with AWS CloudFormation
- Understanding how network segmentation works in practice through VPC design with public and private subnets
- Configuring serverless compliance monitoring using AWS Lambda
- Setting up continuous compliance recording with AWS Config and audit logging with CloudTrail
- Implementing MFA and least-privilege IAM policies as foundational GRC security controls
- Troubleshooting real CloudFormation deployment failures and applying targeted fixes
- Managing IAM roles and S3 bucket policies to meet least-privilege access requirements
- Mapping technical cloud controls to established compliance frameworks
- Using Git and GitHub for version-controlled project submission

This project reinforced that GRC in cloud environments is not just a documentation exercise. It requires practical understanding of how services interact, what permissions are needed, and how to diagnose and fix failures when they occur.

-----

## Repository Structure

```
GRC208-AWS-Capstone-Emmanuella-Ebube/
├── cloudformation-network-stack.yaml
├── cloudformation-database-stack.yaml
├── lambda_compliance_monitor.py
├── grc-dashboard.jsx
├── grc-dashboard.css
├── test_cases.py
├── sample_data.sql
├── requirements.txt
├── deploy.sh
├── README.md
├── DEPLOYMENT_GUIDE.md
├── BEST_PRACTICES.md
├── AWS_SERVICES_GUIDE.md
├── PROJECT_MANIFEST.md
├── DELIVERY_SUMMARY.md
├── architecture_design.md
├── architecture-diagram.md
├── diagrams/
└── screenshots/
```

-----

## Screenshots

All 24 deployment screenshots are available in the `screenshots/` folder. They cover every phase from identity verification through to final service verification, documented across both AWS CloudShell and the AWS Management Console.

-----

## Additional Documentation

Full details for each section of this project are available in the following files:

- `DEPLOYMENT_GUIDE.md` — step-by-step deployment instructions including all fixes applied
- `BEST_PRACTICES.md` — AWS and GRC implementation best practices observed
- `AWS_SERVICES_GUIDE.md` — detailed explanation of each AWS service used
- `PROJECT_MANIFEST.md` — complete file inventory and project organisation
- `DELIVERY_SUMMARY.md` — project completion summary and metadata
- `architecture_design.md` — system architecture and design decisions
- `architecture-diagram.md` — Mermaid architecture diagrams
