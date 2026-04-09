# AWS Integrated GRC Platform - Architecture Design

## Project Overview
The AWS Integrated GRC Platform is a comprehensive capstone project designed for GRC208 students. It demonstrates how to build, deploy, and manage a Governance, Risk, and Compliance platform using modern cloud architecture and AWS native services.

## Architecture Approach
This project uses a **Hybrid Architecture** that combines a robust open-source GRC application (OpenGRC) with native AWS security and compliance services. This approach provides students with a realistic, production-grade system while teaching practical AWS skills.

## Core Components

### 1. The GRC Application Layer
- **Application**: OpenGRC (PHP/Laravel based)
- **Compute**: AWS Elastic Container Service (ECS) with AWS Fargate for serverless container execution
- **Database**: Amazon Relational Database Service (RDS) for MySQL
- **Storage**: Amazon S3 for document and evidence storage
- **Load Balancing**: Application Load Balancer (ALB) for traffic distribution

### 2. AWS Native Compliance Integration
- **AWS Config**: Continuous monitoring of AWS resource configurations
- **AWS Security Hub**: Centralized security posture management
- **AWS CloudTrail**: Comprehensive API and user activity logging
- **Amazon EventBridge**: Event routing for compliance alerts

### 3. Automation & Remediation Layer
- **AWS Lambda**: Serverless functions written in Python to handle:
  - Automated compliance checks
  - Log parsing and formatting
  - Alert generation
  - Auto-remediation of non-compliant resources

### 4. Security & Governance
- **AWS IAM**: Role-based access control (RBAC) and least privilege policies
- **AWS KMS**: Key Management Service for data encryption at rest
- **AWS WAF**: Web Application Firewall protecting the GRC application
- **Amazon VPC**: Isolated network environment with public/private subnets

## System Modules

### Module 1: Risk Management
- Risk register and assessment matrix
- Threat modeling integration
- Risk scoring and mitigation tracking

### Module 2: Compliance Tracking
- Framework mapping (ISO 27001, NIST, PCI DSS)
- Control implementation tracking
- Automated AWS compliance status ingestion

### Module 3: Audit & Evidence
- Centralized evidence repository (S3)
- Audit trail logging (CloudTrail)
- Assessment reporting

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | HTML/CSS/JS (Filament) | User Interface |
| Backend | PHP 8.x (Laravel) | Application Logic |
| Database | MySQL 8.0 (Amazon RDS) | Relational Data Storage |
| Infrastructure | AWS CloudFormation | Infrastructure as Code (IaC) |
| Automation | Python 3.11 (AWS Lambda) | Serverless Scripts |
| Containers | Docker | Application Packaging |

## Deployment Strategy
The project will be deployed using AWS CloudFormation templates, allowing students to provision the entire infrastructure with a single click. The deployment is broken down into logical stacks:
1. **Network Stack**: VPC, Subnets, Security Groups
2. **Data Stack**: RDS, S3, KMS
3. **Application Stack**: ECS, ALB, IAM Roles
4. **Security Stack**: Config, Security Hub, CloudTrail, Lambda

## Learning Objectives for Students
By completing this capstone, students will learn to:
1. Deploy a multi-tier application on AWS
2. Configure AWS native security services (Config, Security Hub)
3. Implement Infrastructure as Code (IaC)
4. Map technical controls to compliance frameworks
5. Automate compliance monitoring using serverless functions
