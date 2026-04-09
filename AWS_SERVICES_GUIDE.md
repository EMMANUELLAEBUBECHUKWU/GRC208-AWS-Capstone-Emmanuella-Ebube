# AWS Services Guide for GRC Platform

## Overview

This guide explains each AWS service used in the GRC platform and how it contributes to the overall system.

## Core Services

### 1. Amazon VPC (Virtual Private Cloud)

**Purpose**: Provides isolated network environment for all resources.

**Key Components**:
- **Subnets**: Logical divisions of the VPC
  - Public subnets: For resources needing internet access (ALB, NAT Gateway)
  - Private subnets: For resources not needing direct internet access (RDS, ECS)
- **Internet Gateway**: Enables communication between VPC and internet
- **NAT Gateway**: Allows private resources to access internet without exposing them
- **Route Tables**: Define traffic routing rules
- **Security Groups**: Act as virtual firewalls

**GRC Platform Usage**:
```
Internet
    ↓
Internet Gateway
    ↓
ALB (Public Subnet)
    ↓
ECS (Private Subnet)
    ↓
RDS (Private Subnet)
```

**Best Practice**: Keep databases in private subnets, only expose load balancers publicly.

### 2. AWS CloudFormation

**Purpose**: Infrastructure as Code service for provisioning AWS resources.

**Key Concepts**:
- **Templates**: JSON/YAML files defining resources
- **Stacks**: Collections of resources created from templates
- **Parameters**: Input values for templates
- **Outputs**: Values returned after stack creation

**GRC Platform Usage**:
```
CloudFormation Template
    ↓
Defines VPC, Subnets, Security Groups
    ↓
Creates Stack
    ↓
All resources provisioned automatically
```

**Benefits**:
- Reproducible deployments
- Version control for infrastructure
- Easy rollback and updates
- Consistent environments

### 3. Amazon RDS (Relational Database Service)

**Purpose**: Managed MySQL database for storing GRC data.

**Key Features**:
- **Automated Backups**: Daily backups with 30-day retention
- **Multi-AZ**: Automatic failover to standby instance
- **Encryption**: Data encrypted at rest and in transit
- **Enhanced Monitoring**: Detailed performance metrics
- **Read Replicas**: Scale read operations

**GRC Platform Usage**:
- Stores frameworks, controls, risks, assets
- Maintains audit logs
- Tracks compliance status

**Data Structure**:
```
Frameworks
├── Controls
├── Risks
├── Assets
└── Audit Logs
```

**Performance Considerations**:
- Use appropriate instance type (db.t3.micro for dev, db.r6i for prod)
- Create indexes on frequently queried columns
- Monitor slow query logs
- Use read replicas for reporting

### 4. Amazon S3 (Simple Storage Service)

**Purpose**: Object storage for evidence, reports, and backups.

**Key Features**:
- **Versioning**: Keep multiple versions of objects
- **Encryption**: Server-side encryption with KMS
- **Lifecycle Policies**: Automatically transition or delete old objects
- **Access Control**: Fine-grained permissions

**GRC Platform Usage**:
- Evidence bucket: Stores audit evidence and documentation
- Reports bucket: Stores compliance reports
- Backup bucket: Stores database backups

**Lifecycle Policy Example**:
```yaml
Rules:
  - Id: ArchiveOldReports
    Transitions:
      - Days: 90
        StorageClass: GLACIER
  - Id: DeleteVeryOldReports
    ExpirationInDays: 365
```

### 5. Amazon DynamoDB

**Purpose**: NoSQL database for high-performance data access.

**Key Features**:
- **On-Demand Billing**: Pay per request
- **TTL**: Automatically delete expired items
- **Streams**: Capture changes for real-time processing
- **Global Tables**: Multi-region replication

**GRC Platform Usage**:
- Compliance Status Table: Real-time compliance snapshots
- Risk Register Table: Risk assessments and scores
- Controls Table: Control implementation status

**Table Structure**:
```
grc-compliance-status
├── timestamp (Partition Key)
├── compliance_percentage
├── total_rules
└── rules_detail

grc-risk-register
├── risk_id (Partition Key)
├── assessment_date (Sort Key)
├── risk_level
└── details
```

### 6. AWS Lambda

**Purpose**: Serverless compute for compliance automation.

**Key Features**:
- **Event-Driven**: Triggered by events (schedule, S3, API)
- **Automatic Scaling**: Scales automatically based on demand
- **No Server Management**: AWS manages infrastructure
- **Pay Per Use**: Only pay for execution time

**GRC Platform Usage**:
- Compliance Monitoring: Runs hourly to check AWS Config compliance
- Risk Assessment: Calculates risk scores based on compliance
- Report Generation: Creates compliance reports
- Alert Handling: Sends SNS notifications

**Execution Flow**:
```
EventBridge Rule (hourly)
    ↓
Triggers Lambda Function
    ↓
Retrieves AWS Config data
    ↓
Analyzes compliance
    ↓
Stores in DynamoDB
    ↓
Sends alerts if needed
```

**Performance Optimization**:
- Memory: 256-512 MB for GRC functions
- Timeout: 60 seconds for compliance checks
- Concurrency: Set reserved concurrency for critical functions

### 7. AWS Application Load Balancer (ALB)

**Purpose**: Distributes incoming traffic across multiple targets.

**Key Features**:
- **Path-Based Routing**: Route based on URL path
- **Host-Based Routing**: Route based on hostname
- **Health Checks**: Automatically remove unhealthy targets
- **SSL/TLS**: Terminate HTTPS connections

**GRC Platform Usage**:
- Routes HTTP/HTTPS traffic to ECS tasks
- Performs health checks on application
- Distributes load across availability zones

**Configuration**:
```
Internet
    ↓
ALB (Port 80/443)
    ↓
Target Group
    ├── ECS Task 1 (Port 8000)
    ├── ECS Task 2 (Port 8000)
    └── ECS Task 3 (Port 8000)
```

### 8. Amazon ECS (Elastic Container Service)

**Purpose**: Container orchestration for running the GRC application.

**Key Features**:
- **Fargate**: Serverless container execution
- **Task Definitions**: Define container configuration
- **Services**: Maintain desired number of running tasks
- **Auto Scaling**: Scale based on metrics

**GRC Platform Usage**:
- Runs OpenGRC application in containers
- Manages application lifecycle
- Scales based on demand

**Task Configuration**:
```yaml
ContainerDefinitions:
  - Name: grc-app
    Image: opengrc:latest
    Memory: 512
    Cpu: 256
    PortMappings:
      - ContainerPort: 8000
```

## Security & Compliance Services

### 9. AWS Config

**Purpose**: Continuous monitoring of AWS resource configurations.

**Key Features**:
- **Config Rules**: Evaluate resource compliance
- **Conformance Packs**: Collections of rules for frameworks
- **Remediation Actions**: Automatically fix non-compliant resources
- **Configuration History**: Track changes over time

**GRC Platform Usage**:
- Monitors EC2, RDS, S3, IAM configurations
- Checks compliance with security policies
- Provides compliance data to Lambda functions

**Example Config Rule**:
```
Rule: encrypted-volumes
Evaluates: All EBS volumes have encryption enabled
Remediation: Enable encryption on non-compliant volumes
```

**Integration with GRC**:
```
AWS Config Rules
    ↓
Compliance Status
    ↓
Lambda Function
    ↓
GRC Platform
    ↓
Compliance Dashboard
```

### 10. AWS Security Hub

**Purpose**: Centralized security findings and compliance dashboard.

**Key Features**:
- **Compliance Standards**: Built-in support for frameworks
- **Security Score**: Overall security posture
- **Integrated Insights**: Correlate findings across services
- **Custom Insights**: Create custom views

**GRC Platform Usage**:
- Aggregates security findings
- Provides compliance status for frameworks
- Generates security reports

**Supported Standards**:
- CIS AWS Foundations Benchmark
- PCI DSS
- AWS Foundational Security Best Practices
- NIST Cybersecurity Framework

### 11. AWS CloudTrail

**Purpose**: Audit logging for all API calls and user activity.

**Key Features**:
- **Event History**: 90-day history in console
- **Trails**: Long-term logging to S3
- **Multi-Region**: Log all regions to single bucket
- **Log File Validation**: Ensure log integrity

**GRC Platform Usage**:
- Logs all API calls for audit trail
- Tracks user and service actions
- Provides evidence for compliance audits

**Logged Events**:
```
User Actions:
- Console login/logout
- Resource creation/modification
- Permission changes

Service Actions:
- Lambda function invocations
- Database modifications
- S3 object uploads
```

### 12. AWS IAM (Identity and Access Management)

**Purpose**: Manage user and service access to AWS resources.

**Key Concepts**:
- **Users**: Individual accounts
- **Roles**: Temporary credentials for services
- **Policies**: Permission documents
- **Groups**: Collections of users with same permissions

**GRC Platform Usage**:
- Lambda execution role: Permissions for Lambda functions
- ECS task role: Permissions for container tasks
- User roles: Different access levels for GRC users

**Example Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "config:GetComplianceDetailsByConfigRule",
        "dynamodb:PutItem"
      ],
      "Resource": "*"
    }
  ]
}
```

### 13. AWS KMS (Key Management Service)

**Purpose**: Manage encryption keys for data protection.

**Key Features**:
- **Customer Master Keys**: Keys you control
- **Automatic Rotation**: Rotate keys annually
- **Audit Trail**: Track key usage
- **Multi-Region**: Replicate keys across regions

**GRC Platform Usage**:
- Encrypts RDS database
- Encrypts S3 objects
- Encrypts DynamoDB tables

**Encryption Flow**:
```
Data
    ↓
KMS Key
    ↓
Encrypted Data
    ↓
Storage (RDS/S3/DynamoDB)
```

## Monitoring & Alerting Services

### 14. Amazon CloudWatch

**Purpose**: Monitoring, logging, and alerting service.

**Key Features**:
- **Metrics**: Monitor resource performance
- **Logs**: Centralize application and system logs
- **Alarms**: Alert on metric thresholds
- **Dashboards**: Visualize metrics

**GRC Platform Usage**:
- Monitor Lambda execution metrics
- Track RDS performance
- Collect application logs
- Alert on compliance violations

**Example Metrics**:
```
Lambda:
- Duration
- Errors
- Throttles
- Concurrent Executions

RDS:
- CPU Utilization
- Database Connections
- Read Latency
- Storage Space
```

### 15. Amazon SNS (Simple Notification Service)

**Purpose**: Send notifications and alerts.

**Key Features**:
- **Topics**: Channels for messages
- **Subscriptions**: Receive messages (email, SMS, Lambda)
- **Message Filtering**: Route based on attributes
- **Fanout**: Send to multiple subscribers

**GRC Platform Usage**:
- Send compliance alerts
- Notify on risk changes
- Alert on security findings

**Example Flow**:
```
Compliance Check
    ↓
Non-Compliance Detected
    ↓
SNS Topic
    ↓
Email Notification
SMS Notification
Lambda Function
```

### 16. Amazon EventBridge

**Purpose**: Route events between AWS services.

**Key Features**:
- **Rules**: Define event patterns
- **Targets**: Services to invoke
- **Schedules**: Cron expressions for timing
- **Transformations**: Modify event data

**GRC Platform Usage**:
- Schedule hourly compliance checks
- Route compliance events to Lambda
- Trigger reports on schedule

**Example Rule**:
```yaml
Name: grc-compliance-check
ScheduleExpression: "rate(1 hour)"
Targets:
  - Arn: arn:aws:lambda:us-east-1:ACCOUNT_ID:function:grc-compliance-monitor
    RoleArn: arn:aws:iam::ACCOUNT_ID:role/eventbridge-role
```

## Service Interactions

### Data Flow Diagram

```
AWS Config (Compliance Data)
    ↓
EventBridge (Hourly Trigger)
    ↓
Lambda Function (Compliance Monitor)
    ├─→ Retrieves Config data
    ├─→ Calculates compliance
    ├─→ Assesses risks
    └─→ Stores results
    ↓
DynamoDB (Compliance Status)
    ↓
RDS Database (GRC Platform)
    ↓
S3 (Reports & Evidence)
    ↓
CloudWatch (Metrics & Logs)
    ↓
SNS (Alerts)
    ↓
Email/SMS Notifications
```

### Security Flow

```
User
    ↓
ALB (HTTPS)
    ↓
ECS Task (IAM Role)
    ↓
RDS (Encrypted)
    ↓
S3 (Encrypted)
    ↓
CloudTrail (Audit)
```

## Cost Optimization

### Service Costs

| Service | Pricing Model | Optimization |
|---------|--------------|--------------|
| RDS | Per hour | Use t3 for dev, schedule downtime |
| S3 | Per GB stored | Lifecycle policies to Glacier |
| Lambda | Per invocation | Optimize function duration |
| DynamoDB | Per request | Use on-demand for variable load |
| CloudTrail | Per 100K events | Filter unnecessary events |
| CloudWatch | Per metric/log | Remove unused metrics |

### Cost Reduction Strategies

1. **Use Serverless**: Lambda and DynamoDB scale automatically
2. **Lifecycle Policies**: Archive old data to Glacier
3. **Reserved Instances**: For predictable workloads
4. **Spot Instances**: For non-critical batch jobs
5. **Consolidation**: Combine resources where possible

## Conclusion

The GRC platform leverages AWS services to create a secure, scalable, and compliant system. Each service plays a specific role in the architecture, and together they provide a comprehensive solution for governance, risk, and compliance management.

For more information on each service, refer to the official AWS documentation at https://docs.aws.amazon.com/
