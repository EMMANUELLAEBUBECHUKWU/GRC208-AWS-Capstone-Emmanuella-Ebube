# GRC208 AWS Integrated GRC Platform

## Capstone Project — Emmanuella Ebubechukwu

**Student:** Emmanuella Ebubechukwu
**Student ID:** 2025/GRC/10041
**Programme:** GRC Engineering (CGRCE)
**Institution:** International Cybersecurity and Digital Forensics Academy (ICDFA)
**Course:** GRC208 — Governance, Risk, and Compliance Capstone
**Submission Date:** April 21, 2026

-----

## Project Overview

This repository contains my capstone submission for GRC208. The project involved deploying a fully functional AWS Integrated GRC Platform from scratch on a personal AWS Free Tier account. The platform demonstrates practical implementation of governance, risk, and compliance management using AWS native services.

The deployment was carried out entirely through AWS CloudShell using Infrastructure as Code (CloudFormation), with all five phases completed successfully and verified.

-----

## AWS Account Details

|Attribute      |Value                  |
|---------------|-----------------------|
|Account ID     |562923011251           |
|Region         |us-east-1 (N. Virginia)|
|IAM User       |emmanuella-admin       |
|Deployment Date|April 9, 2026          |

-----

## Deployment Summary

All five phases were deployed successfully:

|Phase  |Description                                            |Status  |
|-------|-------------------------------------------------------|--------|
|Phase 1|Network Infrastructure — VPC, subnets, security groups |Complete|
|Phase 2|Database Infrastructure — RDS MySQL, S3, DynamoDB      |Complete|
|Phase 3|Lambda Function — compliance monitoring                |Complete|
|Phase 4|AWS Config and CloudTrail — audit logging and recording|Complete|
|Phase 5|Sample Data Loading — DynamoDB tables populated        |Complete|

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

- AWS Config Recorder: `grc-recorder` — Recording (Continuous)
- CloudTrail: `grc-trail` — Logging enabled
- CloudTrail S3 Bucket: `grc-cloudtrail-logs-562923011251`

-----

## Test Results

```
Ran 22 tests in 0.001s
OK
```

All 22 test cases passed across the following modules: Compliance Monitoring, Risk Assessment, Data Validation, Database Operations, Framework Mapping, Audit Logging, Report Generation, and Integration Workflows.

-----

## Challenges and Fixes

During deployment, two issues were encountered and resolved:

**1. Database Stack Rollback**
The original `cloudformation-database-stack.yaml` failed due to an invalid S3 encryption property and KMS incompatibility on Free Tier. The template was replaced with a simplified Free Tier compatible version using AES256 encryption, `db.t3.micro` RDS instance, and no KMS key.

**2. AWS Config and CloudTrail Delivery Channel**
Both services required dedicated IAM roles and explicit S3 bucket policies before the delivery channels could be created. A `grc-config-role` was created for AWS Config and a separate bucket policy was applied to the CloudTrail S3 bucket.

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

## Compliance Frameworks Covered

ISO 27001, NIST Cybersecurity Framework, PCI DSS, HIPAA, GDPR, SOC 2

-----

## Screenshots

All deployment screenshots are available in the `screenshots/` folder. They cover every phase from identity verification through to final service verification across both CloudShell and the AWS Console.
