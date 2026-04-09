# Best Practices

## GRC208 AWS Integrated GRC Platform

### Emmanuella Ebubechukwu | 2025/GRC/10041

|                 |                                                                 |
|-----------------|-----------------------------------------------------------------|
|**Name**         |Emmanuella Ebubechukwu                                           |
|**Student ID**   |2025/GRC/10041                                                   |
|**Course**       |GRC208 - Governance, Risk, and Compliance                        |
|**Institution**  |International Cybersecurity and Digital Forensics Academy (ICDFA)|
|**Date Deployed**|April 9, 2026                                                    |
|**Environment**  |AWS Free Tier Personal Account                                   |
|**Region**       |us-east-1 (N. Virginia)                                          |

-----

## AWS Best Practices

### Define Your Infrastructure Before You Deploy It

Before this project, I understood Infrastructure as Code as a concept. After watching a CloudFormation stack fail twice and having to fix the template each time, I understood it as a discipline.

When the database stack rolled back the first time, I fixed the S3 encryption property. When it rolled back again, I replaced the entire template with a version that actually worked on Free Tier. Both fixes went into the file, not into the console. That meant when the stack finally deployed successfully, what was running in AWS matched exactly what was written in the code. That kind of certainty is only possible when everything lives in a template.

If you find yourself making changes directly in the AWS Console to get something working, stop and ask yourself why you are not making that change in the template instead.

### A Budget Alert Is Not Optional

I set a $10 billing alert before I ran a single CloudFormation command. This was not just a precaution. It was a deliberate decision made after understanding that an RDS instance does not know when you have forgotten about it. It keeps running and it keeps charging.

On a Free Tier account, unexpected costs almost always mean something is running that should not be. On a production account, unexpected costs can mean something far more serious. Either way, you want to know the moment it happens, not at the end of the month when the bill arrives.

Set the alert first. Then deploy.

### Never Work as Root

I created the `emmanuella-admin` IAM user and worked through that account for everything. The root account has no guardrails. There is no policy you can attach to it, no permission boundary that constrains it, and no easy way to recover from a mistake made under it.

Working as a named IAM user also means every action is attributed to `emmanuella-admin` in CloudTrail. That is useful during an audit and it is useful if something goes wrong and you need to trace what happened.

### Enable MFA and Do Not Skip It

I enabled MFA on `emmanuella-admin` before starting the deployment. It feels like an extra step when you are in a hurry to get things running but it is the kind of control you are glad you put in place before something goes wrong, not after.

A password alone is one stolen credential away from a full account compromise. MFA makes that significantly harder. Under ISO 27001 and NIST it is also a documented control requirement, which means skipping it is not just a security gap but a compliance gap.

### Give Each Service Only What It Needs

This was a lesson Phase 4 made very clear. I tried to use the Lambda IAM role for the AWS Config recorder and got back an InsufficientDeliveryPolicyException. The fix required understanding why it failed.

Config needs to assume a role with `config.amazonaws.com` as the trusted principal. Lambda needs `lambda.amazonaws.com`. These are different services with different trust relationships and they need different roles. When you blur those boundaries, things break in ways that are hard to diagnose if you do not understand why the boundary exists.

Create a dedicated role for each service. Scope it to exactly what that service needs.

### Verify Every Phase Before Moving to the Next

After each stack deployment I ran a status check and pulled the outputs before starting the next phase. The database stack imports subnet and security group IDs from the network stack. If I had started Phase 2 without confirming Phase 1 outputs were available, Phase 2 would have failed immediately with a cross-stack reference error.

Checking outputs at each stage catches problems early before they cascade into harder failures later.

### Read the Error Before You Fix It

Both times the database stack rolled back, I ran the describe-stack-events command before touching anything:

```bash
aws cloudformation describe-stack-events \
  --stack-name grc-capstone-database-stack \
  --region us-east-1 \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`].[ResourceType,ResourceStatusReason]' \
  --output table
```

The first error pointed to exactly which property was wrong. The second showed the structure itself was invalid. Both times, reading the error pointed directly to the fix. The error message is not the problem. It is the answer.

-----

## Security Best Practices

### Keep Credentials Out of Your Code

The database password was passed as a CloudFormation parameter at deployment time and exists nowhere in any file in this repository. A single password accidentally committed to a public GitHub repository can result in full account compromise within minutes. Automated bots scan public repositories continuously looking for exactly this kind of exposure.

If you are ever unsure whether a file contains credentials before pushing, check it manually. That few minutes of caution is worth it.

### Encrypt Storage Even When It Feels Unnecessary

The original database template used KMS encryption which was not compatible with a Free Tier account. Rather than deploying without encryption, I switched to AES256 server-side encryption for the S3 buckets. The data is still encrypted at rest. The mechanism is different but the protection is real.

Encryption at rest is not just a compliance checkbox. If the underlying storage were ever accessed without going through the application layer, encrypted data is unreadable without the key.

### Apply Bucket Policies That Actually Restrict Access

Both the evidence bucket and the CloudTrail logs bucket have explicit bucket policies that only allow the specific services that need them. Config can write to the evidence bucket. CloudTrail can write to the logs bucket. Nothing else has permission to write to either.

Both services failed until those policies were in place. That failure confirmed that the default state of these buckets is restrictive, which is exactly what you want. Permissions should be granted explicitly, not inherited by default.

-----

## Compliance Best Practices

### Continuous Monitoring Beats Scheduled Scanning

AWS Config is running with continuous recording across all supported resource types. The moment any resource configuration changes, Config evaluates it. There is no gap between when a change happens and when it is detected.

Compliance checked only once a week is a snapshot, not a posture. In a cloud environment where a misconfigured resource can be created and deleted in minutes, a weekly scan would miss it entirely. Continuous monitoring is the only approach that gives you an accurate picture at any given moment.

### Link Every Control to a Framework

The grc-controls DynamoDB table stores a framework field with every control record. This is not just an organisational choice. It is the difference between answering an auditor’s question in thirty seconds and spending hours searching for the answer.

When you can query your controls table and immediately retrieve every control mapped to a specific framework, that is operationally useful. Controls that have no framework reference are hard to audit and hard to defend.

### Build Your Audit Trail Before You Need It

CloudTrail was configured and verified as part of the deployment. Every API call made in the account since then is logged and stored. This means there is already a record of the deployment itself including every CloudFormation action, every IAM change, and every S3 bucket policy update.

You cannot reconstruct an audit trail after the fact. By the time you realise you need one, the events you needed to capture have already happened without being recorded.

### Document What Broke and How You Fixed It

Three things went wrong during this deployment. All three are documented in the deployment guide with the exact error messages and the exact commands used to resolve them.

In a real GRC programme, honest documentation is what makes an organisation trustworthy during an audit. A gap that is documented with a clear resolution is a defensible position. A gap that is hidden is a liability.

### Compliance Requires Ongoing Attention

Completing this deployment does not mean this environment is permanently compliant. Resources change, configurations drift, and requirements evolve. AWS Config is running continuously precisely because compliance is not something you achieve once and set aside.

Think of it less like passing a test and more like maintaining a standard.

-----

## Operational Best Practices

### Test After Every Significant Change

The test suite runs in under a second. There is no justification for not running it:

```bash
python3 test_cases.py
```

All 22 tests passing after deployment confirmed the platform was functioning as expected. Automated tests are not a formality. They are how you know the thing you built actually works.

### Understand Your Environment Before You Deploy Into It

Free Tier has boundaries. KMS encryption adds cost. RDS on anything larger than db.t3.micro exceeds Free Tier. Some AWS Config rules carry a per-rule monthly charge. Knowing your environment means you can design for it rather than discovering its constraints through failures.

### Know When to Replace Instead of Patch

After the second database stack failure I made a decision to stop trying to fix the original template and replace it entirely. The original had structural issues that went beyond a single property fix. Patching it further would have produced a harder to read template even if it eventually worked.

Sometimes the cleanest solution is a fresh start. Knowing when you have crossed that line is a judgement call but it is worth making deliberately rather than spending another hour on a template that is working against you.
