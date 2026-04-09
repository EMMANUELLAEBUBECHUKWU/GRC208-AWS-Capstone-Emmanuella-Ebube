# Project Manifest

## GRC208 AWS Integrated GRC Platform

|                       |                                                                 |
|-----------------------|-----------------------------------------------------------------|
|**Name**               |Emmanuella Ebubechukwu                                           |
|**Student ID**         |2025/GRC/10041                                                   |
|**Course**             |GRC208 - Governance, Risk, and Compliance                        |
|**Institution**        |International Cybersecurity and Digital Forensics Academy (ICDFA)|
|**Instructor**         |Aminu Idris                                                      |
|**Date Deployed**      |April 9, 2026                                                    |
|**Submission Deadline**|April 21, 2026                                                   |
|**Environment**        |AWS Free Tier Personal Account                                   |
|**AWS Account ID**     |562923011251                                                     |
|**Region**             |us-east-1 (N. Virginia)                                          |
|**IAM User**           |emmanuella-admin                                                 |

-----

## Repository Overview

This repository contains the complete submission for the GRC208 capstone project. It includes all infrastructure templates, application code, documentation, test cases, sample data, architecture diagrams, and deployment screenshots. Everything needed to understand, evaluate, and replicate this deployment is contained here.

-----

## File Inventory

### Infrastructure Files

|File                                |Description                                                                                                                                                                  |Lines|
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|`cloudformation-network-stack.yaml` |Deploys the VPC, public and private subnets across two availability zones, internet gateway, NAT gateway, application load balancer, and all associated security groups      |174  |
|`cloudformation-database-stack.yaml`|Deploys the RDS MySQL instance, two S3 buckets for evidence and reports, and three DynamoDB tables. This is the Free Tier compatible version that was fixed during deployment|143  |

### Application Code

|File                          |Description                                                                                                                                                                                                                                                       |Lines|
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|`lambda_compliance_monitor.py`|AWS Lambda function that monitors compliance status, calculates compliance percentages, counts non-compliant rules, and returns a structured JSON response                                                                                                        |250  |
|`grc-dashboard.jsx`           |React component for the GRC platform frontend dashboard. Displays compliance status, risk register, and control implementation tracking. Included in the repository as a deliverable but frontend deployment requires ECS Fargate which is outside Free Tier scope|299  |
|`grc-dashboard.css`           |Stylesheet for the GRC dashboard component. Included alongside grc-dashboard.jsx as a complete frontend deliverable                                                                                                                                               |275  |

### Testing

|File           |Description                                                                                                                                                                                           |Lines|
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|`test_cases.py`|22 test cases covering compliance monitoring, risk assessment, data validation, database operations, framework mapping, audit logging, report generation, and integration workflows. All 22 tests pass|341  |

### Data and Configuration

|File              |Description                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`sample_data.sql` |SQL script containing sample GRC data for loading into the RDS MySQL database including frameworks, controls, risks, assets, and compliance snapshots. The file is included in the repository as a deliverable. Direct loading into RDS was not possible from CloudShell because the RDS instance sits in a private subnet with no route to the internet gateway. Sample data was loaded into DynamoDB directly instead and all 22 tests passed successfully|
|`requirements.txt`|Python dependencies required for the Lambda function and test suite                                                                                                                                                                                                                                                                                                                                                                                         |
|`deploy.sh`       |Shell script for automated deployment of all five phases. Included in the repository as a reference deliverable. Manual deployment through CloudShell was used instead since the script assumes an environment with direct RDS access which was not available on this Free Tier account                                                                                                                                                                     |

### Documentation

|File                     |Description                                                                                                                             |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
|`README.md`              |Main project overview including deployment summary, AWS resources deployed, test results, challenges and fixes, and repository structure|
|`DEPLOYMENT_GUIDE.md`    |Full record of the deployment process including every command run, every error encountered, and every fix applied                       |
|`BEST_PRACTICES.md`      |AWS and GRC best practices observed and applied during this deployment                                                                  |
|`AWS_SERVICES_GUIDE.md`  |Explanation of each AWS service used in this project and its role in the GRC platform                                                   |
|`PROJECT_MANIFEST.md`    |This file. Complete inventory of all project files, deployed resources, and submission details                                          |
|`DELIVERY_SUMMARY.md`    |Project completion summary covering all deliverables and their status                                                                   |
|`architecture_design.md` |System architecture documentation covering design decisions, component interactions, and data flow                                      |
|`architecture-diagram.md`|Mermaid diagrams illustrating the system architecture                                                                                   |

### Diagrams Folder

|File                                   |Description                                                              |
|---------------------------------------|-------------------------------------------------------------------------|
|`diagrams/01_system_architecture.png`  |Full system architecture showing all AWS services and their relationships|
|`diagrams/02_data_flow.png`            |Data flow diagram showing how information moves through the platform     |
|`diagrams/03_risk_assessment.png`      |Risk assessment process diagram                                          |
|`diagrams/04_security_architecture.png`|Security architecture showing network segmentation and access controls   |
|`diagrams/05_deployment_pipeline.png`  |Deployment pipeline diagram showing the five phases                      |
|`diagrams/06_compliance_dashboard.png` |Compliance dashboard layout and data sources                             |
|`diagrams/07_aws_access_options.png`   |AWS access options diagram                                               |

### Screenshots Folder

All 23 deployment screenshots are stored in the `screenshots/` folder. They cover the full deployment from identity verification through to final service confirmation.

|Screenshot                                      |What It Shows                                                                    |
|------------------------------------------------|---------------------------------------------------------------------------------|
|`01_identity_verified`                          |AWS account identity confirmed via aws sts get-caller-identity                   |
|`02_repo_cloned`                                |Instructor repository cloned and all project files listed                        |
|`03_network_stack_create_complete`              |Phase 1 network stack showing CREATE_COMPLETE status                             |
|`04_network_stack_outputs`                      |Network stack outputs table showing VPC, subnet, and security group IDs          |
|`05_database_stack_create_complete`             |Phase 2 database stack showing CREATE_COMPLETE status                            |
|`06_database_stack_outputs`                     |Database stack outputs showing RDS endpoint, S3 buckets, and DynamoDB tables     |
|`07_lambda_function_created`                    |Phase 3 Lambda function creation output showing function ARN and configuration   |
|`08_lambda_invocation_test`                     |Lambda test invocation returning StatusCode 200 and compliance monitoring message|
|`09_config_recorder_running`                    |Phase 4 AWS Config recorder status showing CONTINUOUS recording                  |
|`10_cloudtrail_created`                         |CloudTrail trail creation output showing trail name and S3 bucket                |
|`11_cloudtrail_logging`                         |CloudTrail status showing IsLogging: True                                        |
|`12_dynamodb_data_loaded`                       |Phase 5 DynamoDB table scans showing all three tables populated with sample data |
|`13_tests_passing`                              |Test suite output showing 22 tests run and all passing                           |
|`14_console_cloudformation_both_stacks_complete`|AWS Console CloudFormation page showing both stacks with CREATE_COMPLETE         |
|`15_console_database_stack_outputs`             |AWS Console database stack Outputs tab                                           |
|`16_console_network_stack_outputs`              |AWS Console network stack Outputs tab                                            |
|`17_console_lambda_function`                    |AWS Console Lambda functions page showing grc-compliance-monitor                 |
|`18_console_config_recording`                   |AWS Console Config Settings page showing Recording is on                         |
|`19_console_cloudtrail_logging`                 |AWS Console CloudTrail Trails page showing grc-trail with logging enabled        |
|`20_console_s3_buckets`                         |AWS Console S3 buckets list showing all three GRC buckets                        |
|`21_console_dynamodb_tables`                    |AWS Console DynamoDB tables list showing all three GRC tables                    |
|`22_console_iam_user`                           |AWS Console IAM Users page showing emmanuella-admin                              |
|`23_final_verification`                         |CloudShell final verification showing all five services confirmed active         |

-----

## Deployed AWS Resources

### Network Stack: grc-capstone-network-stack

|Resource          |Type          |ID                      |
|------------------|--------------|------------------------|
|GRC VPC           |VPC           |vpc-00204003995d48e34   |
|Public Subnet 1   |Subnet        |subnet-0e6c4823316500b67|
|Public Subnet 2   |Subnet        |subnet-0f1683e183304d7ee|
|Private Subnet 1  |Subnet        |subnet-0bb3889421244130e|
|Private Subnet 2  |Subnet        |subnet-0c79c9a2301e854e2|
|RDS Security Group|Security Group|sg-064802794fa337415    |
|ECS Security Group|Security Group|sg-0771599d1db672c25    |

### Database Stack: grc-capstone-database-stack

|Resource               |Type            |Value                                                   |
|-----------------------|----------------|--------------------------------------------------------|
|GRC Database           |RDS MySQL 8.0.40|grc-capstone-db.cyrou02g6leq.us-east-1.rds.amazonaws.com|
|Evidence Bucket        |S3              |grc-capstone-evidence-562923011251                      |
|Reports Bucket         |S3              |grc-capstone-reports-562923011251                       |
|Compliance Status Table|DynamoDB        |grc-compliance-status                                   |
|Risk Register Table    |DynamoDB        |grc-risk-register                                       |
|Controls Table         |DynamoDB        |grc-controls                                            |

### Lambda

|Resource          |Type           |Value                 |
|------------------|---------------|----------------------|
|Compliance Monitor|Lambda Function|grc-compliance-monitor|
|Lambda Role       |IAM Role       |grc-lambda-role       |
|Runtime           |Python         |3.11                  |

### Monitoring and Audit

|Resource               |Type      |Value                           |
|-----------------------|----------|--------------------------------|
|Config Recorder        |AWS Config|grc-recorder                    |
|Config Role            |IAM Role  |grc-config-role                 |
|Config Delivery Channel|AWS Config|grc-channel                     |
|Audit Trail            |CloudTrail|grc-trail                       |
|CloudTrail Bucket      |S3        |grc-cloudtrail-logs-562923011251|

-----

## Test Summary

|Category             |Tests |Result        |
|---------------------|------|--------------|
|Compliance Monitoring|3     |Passed        |
|Risk Assessment      |3     |Passed        |
|Data Validation      |4     |Passed        |
|Database Operations  |3     |Passed        |
|Framework Mapping    |2     |Passed        |
|Audit Logging        |3     |Passed        |
|Report Generation    |2     |Passed        |
|Integration Workflows|2     |Passed        |
|**Total**            |**22**|**All Passed**|

-----

## Compliance Frameworks Supported

|Framework                   |Standard                                           |
|----------------------------|---------------------------------------------------|
|ISO 27001                   |Information Security Management System             |
|NIST Cybersecurity Framework|Risk management and security controls              |
|PCI DSS                     |Payment Card Industry Data Security Standard       |
|HIPAA                       |Health Insurance Portability and Accountability Act|
|GDPR                        |General Data Protection Regulation                 |
|SOC 2                       |Service Organization Control Framework             |

-----

## Deployment Issues Resolved

|Issue                                                                 |Resolution                                                                                                                                                               |
|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Database stack ROLLBACK_COMPLETE due to invalid S3 encryption property|Fixed the property name using sed, then replaced the full template with a Free Tier compatible version                                                                   |
|AWS Config InsufficientDeliveryPolicyException                        |Created dedicated grc-config-role with AWS_ConfigRole policy and applied explicit S3 bucket policy for config.amazonaws.com                                              |
|CloudTrail InsufficientS3BucketPolicyException                        |Applied explicit S3 bucket policy allowing cloudtrail.amazonaws.com to write to the logs bucket                                                                          |
|GitHub push rejected due to divergent branch history                  |Deleted the remote README and force pushed using git push –force                                                                                                         |
|RDS direct connection not possible from CloudShell                    |RDS sits in a private subnet with no internet gateway route. Sample data was loaded into DynamoDB directly instead. All 22 tests passed confirming platform functionality|
