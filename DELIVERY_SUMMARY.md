# Delivery Summary

## GRC208 AWS Integrated GRC Platform

|                       |                                                                             |
|-----------------------|-----------------------------------------------------------------------------|
|**Name**               |Emmanuella Ebubechukwu                                                       |
|**Student ID**         |2025/GRC/10041                                                               |
|**Course**             |GRC208 - Governance, Risk, and Compliance                                    |
|**Institution**        |International Cybersecurity and Digital Forensics Academy (ICDFA)            |
|**Date Deployed**      |April 9, 2026                                                                |
|**Environment**        |AWS Free Tier Personal Account                                               |
|**AWS Account ID**     |562923011251                                                                 |
|**Region**             |us-east-1 (N. Virginia)                                                      |
|**GitHub Repository**  |https://github.com/EMMANUELLAEBUBECHUKWU/GRC208-AWS-Capstone-Emmanuella-Ebube|

-----

## Completion Status

The AWS Integrated GRC Platform has been fully deployed, tested, and documented on a personal AWS Free Tier account. All five deployment phases were completed successfully and verified. The platform is live and all services are actively running.

-----

## Deployment Phases

|Phase  |Description                                                       |Status  |
|-------|------------------------------------------------------------------|--------|
|Phase 1|Network Infrastructure — VPC, subnets, security groups, routing   |Complete|
|Phase 2|Database Infrastructure — RDS MySQL, S3 buckets, DynamoDB tables  |Complete|
|Phase 3|Lambda Function — compliance monitoring deployed and tested       |Complete|
|Phase 4|AWS Config and CloudTrail — continuous recording and audit logging|Complete|
|Phase 5|Sample Data Loading — DynamoDB tables populated and verified      |Complete|

-----

## Deliverables

### Infrastructure

|Deliverable                       |Status  |Notes                                                                                                |
|----------------------------------|--------|-----------------------------------------------------------------------------------------------------|
|cloudformation-network-stack.yaml |Deployed|CREATE_COMPLETE                                                                                      |
|cloudformation-database-stack.yaml|Deployed|Free Tier compatible version. Original template replaced due to KMS and S3 encryption incompatibility|

### Application Code

|Deliverable                 |Status                |Notes                                                                    |
|----------------------------|----------------------|-------------------------------------------------------------------------|
|lambda_compliance_monitor.py|Deployed and tested   |Returns StatusCode 200                                                   |
|grc-dashboard.jsx           |Included in repository|Frontend deployment requires ECS Fargate which is outside Free Tier scope|
|grc-dashboard.css           |Included in repository|Submitted alongside grc-dashboard.jsx as a complete frontend deliverable |

### Testing

|Deliverable  |Status              |Notes         |
|-------------|--------------------|--------------|
|test_cases.py|All 22 tests passing|100% pass rate|

### Data and Configuration

|Deliverable     |Status                |Notes                                                                                                                |
|----------------|----------------------|---------------------------------------------------------------------------------------------------------------------|
|sample_data.sql |Included in repository|Direct RDS loading was not possible due to private subnet architecture. DynamoDB used for sample data loading instead|
|requirements.txt|Included              |All dependencies listed                                                                                              |
|deploy.sh       |Included in repository|Manual deployment through CloudShell was used. Script included as reference deliverable                              |

### Documentation

|Deliverable            |Status  |
|-----------------------|--------|
|README.md              |Complete|
|DEPLOYMENT_GUIDE.md    |Complete|
|BEST_PRACTICES.md      |Complete|
|AWS_SERVICES_GUIDE.md  |Complete|
|PROJECT_MANIFEST.md    |Complete|
|DELIVERY_SUMMARY.md    |Complete|
|architecture_design.md |Complete|
|architecture-diagram.md|Complete|

-----

## AWS Resources Deployed and Verified

|Service       |Resource                          |Status                |
|--------------|----------------------------------|----------------------|
|CloudFormation|grc-capstone-network-stack        |CREATE_COMPLETE       |
|CloudFormation|grc-capstone-database-stack       |CREATE_COMPLETE       |
|VPC           |vpc-00204003995d48e34             |Active                |
|RDS MySQL     |grc-capstone-db                   |Available             |
|S3            |grc-capstone-evidence-562923011251|Active                |
|S3            |grc-capstone-reports-562923011251 |Active                |
|S3            |grc-cloudtrail-logs-562923011251  |Active                |
|DynamoDB      |grc-compliance-status             |Active                |
|DynamoDB      |grc-risk-register                 |Active                |
|DynamoDB      |grc-controls                      |Active                |
|Lambda        |grc-compliance-monitor            |Active                |
|IAM           |grc-lambda-role                   |Active                |
|IAM           |grc-config-role                   |Active                |
|AWS Config    |grc-recorder                      |Recording (Continuous)|
|CloudTrail    |grc-trail                         |Logging               |

-----

## Test Results

```
Ran 22 tests in 0.001s
OK
```

|Module               |Tests |Result        |
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

## Adjustments Made During Deployment

Three issues were encountered during deployment and resolved. One limitation was documented transparently.

|Item                       |What Happened                                                                                                             |How It Was Handled                                                                                              |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
|Database stack template    |Original template failed with ROLLBACK_COMPLETE due to invalid S3 encryption property and KMS incompatibility on Free Tier|Template replaced with a Free Tier compatible version using AES256 encryption and db.t3.micro RDS instance      |
|AWS Config delivery channel|Failed when using the Lambda IAM role                                                                                     |Dedicated grc-config-role created with AWS_ConfigRole policy and explicit S3 bucket policy applied              |
|CloudTrail S3 bucket       |Failed without a bucket policy                                                                                            |Explicit bucket policy applied allowing cloudtrail.amazonaws.com to write to the logs bucket                    |
|sample_data.sql RDS loading|RDS sits in a private subnet with no internet gateway route. Direct connection from CloudShell was not possible           |Sample data loaded into DynamoDB directly. RDS instance is deployed and running. SQL file included in repository|

-----

## Screenshots

23 deployment screenshots are included in the `screenshots/` folder covering every phase of the deployment from identity verification through to final service confirmation across both AWS CloudShell and the AWS Management Console.

-----

## Security Controls Applied

|Control                         |Implementation                                                               |
|--------------------------------|-----------------------------------------------------------------------------|
|No root account usage           |Dedicated IAM user emmanuella-admin used throughout                          |
|MFA                             |Enabled on emmanuella-admin before deployment                                |
|Least privilege IAM             |Separate roles created for Lambda, Config, and CloudTrail                    |
|Encryption at rest              |AES256 server-side encryption on all S3 buckets                              |
|Private networking              |RDS deployed in private subnets with no direct internet access               |
|Audit logging                   |CloudTrail enabled and verified logging before deployment considered complete|
|Continuous compliance monitoring|AWS Config running with continuous recording across all resource types       |
|Budget alert                    |$10 budget alert set before any resources were deployed                      |

-----

## Final Verification

All services confirmed active on April 9, 2026:

```
=== GRC Platform Final Verification ===
Network Stack:    "CREATE_COMPLETE"
Database Stack:   "CREATE_COMPLETE"
Lambda Function:  "Active"
Config Recorder:  true
CloudTrail:       true
```

-----

## Submission

|Item             |Detail                                                                       |
|-----------------|-----------------------------------------------------------------------------|
|GitHub Repository|https://github.com/EMMANUELLAEBUBECHUKWU/GRC208-AWS-Capstone-Emmanuella-Ebube|
|Student          |Emmanuella Ebubechukwu                                                       |
|Student ID       |2025/GRC/10041                                                               |
