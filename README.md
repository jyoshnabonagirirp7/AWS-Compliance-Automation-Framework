# AWS-Compliance-Automation-Framework

This project demonstrates automated compliance monitoring and remediation in AWS.

It enforces compliance for EC2 and S3 resources using AWS-native services:

AWS Config

AWS Lambda (custom rules)

AWS Systems Manager (SSM) Automation

Amazon EventBridge

Amazon SNS

Amazon CloudWatch

The framework continuously evaluates resources, detects violations, and automatically remediates them.

**Objectives**

Continuously monitor AWS resources for compliance.

Detect and remediate:

EC2 instances with public IP.

Security Groups allowing SSH (22) from 0.0.0.0/0.

EC2 instances with detailed monitoring disabled.

S3 buckets missing required tags.

Notify administrators of compliance changes

**Services Used**

**AWS Config**: Detects configuration changes and evaluates rules.

**AWS Lambda**: Custom compliance logic for:

    EC2 detailed monitoring
    
    S3 bucket tagging
    
**AWS Systems Manager Automation**: Executes remediation steps automatically.

**Amazon EventBridge**: Routes non-compliance events to remediation or SNS.

**Amazon SNS**: Sends email notifications.

**Amazon CloudWatch**: Stores Lambda and SSM logs for auditing


**Implemented Compliance Rules**

1. **EC2 Instance With Public IP**
   
Resource: AWS::EC2::Instance

Remediation: Stops the EC2 instance using SSM Automation.

2. **Security Group SSH (Port 22) Open to 0.0.0.0/0**
   
Resource: AWS::EC2::SecurityGroup

Remediation: SSM Automation removes the offending ingress rule.

3. **EC2 Instances Without Detailed Monitoring**
   
Resource: AWS::EC2::Instance

Logic:

Custom Lambda evaluates Monitoring State.

Non-compliant instances have monitoring enabled via SSM Automation.

4. **S3 Buckets Without Required Tags**
   
Resource: AWS::S3::Bucket

Logic:

Custom Lambda checks for a tag with Key=config, Value=lambda.

Non-compliant buckets are automatically tagged using SSM Automation.
