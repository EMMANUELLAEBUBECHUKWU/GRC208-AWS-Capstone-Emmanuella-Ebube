# Best Practices

## GRC208 AWS Integrated GRC Platform

### Emmanuella Ebubechukwu | 2025/GRC/10041

This document captures the AWS and GRC best practices I observed and applied during the deployment of this capstone project. Some of these came from prior knowledge, some from the course material, and some I learned the hard way when things did not work as expected.

-----

## AWS Best Practices

### 1. Never Use the Root Account for Day-to-Day Work

The root account has unrestricted access to everything in an AWS account and cannot be limited by IAM policies. I created a dedicated IAM user called `emmanuella-admin` with AdministratorAccess and used that for the entire deployment. The root account was only used during the initial account setup.

This is not just a recommendation, it is a basic access control principle. If the root account credentials were ever compromised, the damage would be total and irreversible.

### 2. Enable MFA Before Doing Anything Else

I enabled Multi-Factor Authentication on the `emmanuella-admin` IAM user before starting the deployment. This adds a second layer of verification beyond a password and is one of the simplest controls you can put in place against unauthorized account access.

In a real GRC context, MFA on privileged accounts is a control requirement under ISO 27001, NIST, and most other frameworks. Enabling it on a test account costs nothing and takes less than five minutes.

### 3. Set a Billing Alert Before Deploying Infrastructure

I set a $10 budget alert before running any CloudFormation stacks. AWS charges begin the moment certain resources are created, and it is easy to lose track of what is running especially with RDS instances which continue billing as long as they are active.

Setting the alert first meant I would be notified before costs got out of hand. On a Free Tier account, this is mandatory. On a production account, it is still good practice because unexpected costs are often the first sign that something has gone wrong.

### 4. Use Infrastructure as Code for Everything

All network and database infrastructure in this project was deployed using AWS CloudFormation templates. This means the entire environment can be torn down and rebuilt from scratch using the same files, with consistent results every time.

Manually clicking through the AWS Console to create resources is fine for learning but it creates environments that are impossible to reproduce exactly, difficult to audit, and hard to version control. CloudFormation solves all three of those problems.

### 5. Use Least Privilege for IAM Roles

Each AWS service in this project got its own dedicated IAM role with only the permissions it needed. The Lambda function got the basic execution role and Config access. The Config recorder got the AWS managed Config role. CloudTrail got its own S3 bucket policy.

I learned this the hard way during Phase 4. When I tried to use the Lambda role for the Config recorder, it failed with an InsufficientDeliveryPolicyException. The fix was to create a dedicated role for Config with the correct trust policy pointing to config.amazonaws.com. Least privilege is not just a security principle, it is also what makes services actually work correctly.

### 6. Always Verify Stack Outputs Before Moving to the Next Phase

After each CloudFormation stack completed, I ran a describe-stacks command with the Outputs query to confirm the expected resources had been created and their IDs were available for the next phase. The database stack imports subnet and security group IDs from the network stack using ImportValue, so if Phase 1 had not completed correctly, Phase 2 would have failed immediately.

Checking outputs at each stage catches problems early before they cascade into harder-to-diagnose failures later.

### 7. Use Separate S3 Buckets for Separate Purposes

This project uses three S3 buckets: one for compliance evidence, one for compliance reports, and one for CloudTrail logs. Each bucket has its own access policy scoped to the specific service that needs it.

Mixing audit logs, evidence files, and application data in a single bucket creates access control complexity and makes it harder to enforce retention policies or respond to audit requests. Separating them by purpose is cleaner and easier to manage.

### 8. Encrypt Data at Rest

All S3 buckets in this project use AES256 server-side encryption. While the original template included KMS encryption, that configuration was not compatible with a Free Tier account. AES256 encryption through S3-managed keys still provides encryption at rest without the additional cost of KMS.

On a production account, KMS would be the right choice because it provides key rotation, usage auditing, and finer access control. For a Free Tier deployment, AES256 is a reasonable and still compliant approach.

### 9. Validate CloudFormation Templates Before Deploying

One of the lessons from Phase 2 was that the original database template had a structural error in the S3 encryption configuration that only surfaced at deployment time. Running aws cloudformation validate-template before deploying can catch syntax and structural errors before they cause a rollback.

It does not catch every error, but it eliminates the simple ones and saves time.

### 10. Always Test After Deployment

After completing all five phases, I ran the full test suite with python3 test_cases.py. All 22 tests passed. Running tests after deployment confirms that the platform is functioning as expected and gives a documented record that the system was verified.

Deploying without testing is not a deployment — it is just a hope.

-----

## GRC Best Practices

### 1. Separate the Three Pillars: Governance, Risk, and Compliance

Governance, risk management, and compliance are related but distinct functions. Governance sets the policies and frameworks. Risk management identifies and responds to threats. Compliance monitors adherence to those frameworks and policies.

In this platform, these are reflected in separate DynamoDB tables: grc-controls for governance, grc-risk-register for risk, and grc-compliance-status for compliance. Keeping them separate makes it easier to query, report on, and update each function independently.

### 2. Map Controls to Frameworks Explicitly

A control that cannot be traced back to a specific framework requirement is difficult to defend during an audit. This platform supports six frameworks: ISO 27001, NIST Cybersecurity Framework, PCI DSS, HIPAA, GDPR, and SOC 2. Every control in the grc-controls table carries a framework field that links it to the relevant standard.

During a real audit, the question is not just whether a control exists but whether it satisfies a specific requirement. Explicit mapping makes that answer easy to provide.

### 3. Automate Compliance Monitoring Where Possible

Manual compliance checks are slow, inconsistent, and easy to forget. AWS Config with continuous recording means resource configurations are monitored automatically and any drift from the expected state is detected without human intervention.

The Lambda compliance monitor adds another layer by running automated checks and reporting on compliance percentages. Automation does not replace human judgment but it removes the dependency on someone remembering to check.

### 4. Maintain an Audit Trail for Everything

CloudTrail is enabled in this deployment and logs every API call made in the account. This means every CloudFormation stack creation, every IAM role change, every S3 bucket policy update — all of it is logged with a timestamp, the identity that made the call, and the source IP address.

In a GRC context, an audit trail is not optional. It is the evidence that controls are being applied and that access is being monitored. Without it, compliance claims are unverifiable.

### 5. Treat Evidence Collection as a Continuous Process

The S3 evidence bucket in this project is not just a storage location. It is the repository for everything that would be needed to demonstrate compliance during an assessment: configuration snapshots from AWS Config, CloudTrail logs, compliance reports, and test results.

Evidence should be collected continuously and organised systematically, not pulled together at the last minute before an audit. This project establishes that habit from the start.

### 6. Apply the Principle of Least Privilege as a GRC Control

Least privilege is both a security principle and a compliance requirement. Under ISO 27001 control A.9.2.3 and NIST AC-6, users and systems should have only the access they need to perform their function and nothing more.

Every IAM role in this project was created with a specific purpose and a specific trust policy. No role was given broader permissions than necessary. This is not just good security practice — it is a documented control that can be shown to an auditor.

### 7. Risk Assessment Should Be Quantitative

The grc-risk-register table stores likelihood and impact as numeric values and calculates a risk score as likelihood multiplied by impact. This is a standard risk matrix approach and it makes risks comparable and prioritisable.

A risk with a score of 20 (likelihood 4, impact 5) should be addressed before a risk with a score of 6 (likelihood 2, impact 3). Quantifying risk removes subjectivity and makes it easier to justify resource allocation decisions to leadership.

### 8. Document Everything, Including What Went Wrong

Three deployment issues were encountered during this project and all three are documented in the deployment guide with the exact error messages and the steps taken to resolve them. This kind of documentation has real value in a GRC context.

When something fails in a production environment, the team needs to know what happened, why it happened, and what was done to fix it. A culture of honest documentation is part of what makes a GRC programme credible.

### 9. Review Access Regularly

Enabling MFA was a starting point but access control is not a one-time task. IAM permissions should be reviewed regularly to ensure that roles and users still have only what they need. Users who no longer need access should be removed. Roles that were created for a specific task and are no longer needed should be deleted.

This project set up the roles needed for deployment. In a production environment, those roles would be reviewed after go-live to determine which ones are still needed and which can be removed.

### 10. Compliance Is Not a Destination

Completing this deployment and passing 22 tests does not mean the platform is permanently compliant. AWS Config is set to continuous recording precisely because compliance is an ongoing state, not a one-time achievement. Configurations change, new resources are added, and requirements evolve.

The value of this platform is that it monitors continuously and provides the data needed to make informed decisions about the organisation’s compliance posture at any point in time.
