# 🛡️ SRE Automated Remediation: Port 22 Lock-Down

[![AWS](https://img.shields.io/badge/AWS-CloudFormation-orange.svg)](https://aws.amazon.com/cloudformation/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

## 🎯 Overview
As Site Reliability Engineers (SREs), minimizing Mean Time To Resolution (MTTR) and reducing manual toil is critical. This project provides an **event-driven, serverless automation playbook** designed to instantly detect and remediate one of the most common cloud security risks: accidentally (or maliciously) leaving SSH Port 22 open to the public (`0.0.0.0/0`).

Instead of relying on slow periodic polling, this solution uses **AWS CloudTrail** and **Amazon EventBridge** to detect the exact `AuthorizeSecurityGroupIngress` API call and immediately trigger a **Python AWS Lambda** function to revoke the unauthorized rule.

---

## 🎥 Video Walkthrough

Watch the full demonstration and technical deep-dive on Loom:

> **[▶️ Watch the SRE Automation Loom Video Here](#)** *(Replace `#` with your actual Loom link)*

---

## 🏗️ Architecture & Tech Stack

* **Infrastructure as Code (IaC):** AWS CloudFormation (`automated-sre-remediation.yaml`)
* **Compute:** AWS Lambda (Python 3.11, Boto3)
* **Event Routing:** Amazon EventBridge
* **Auditing:** AWS CloudTrail
* **IAM:** Principle of Least Privilege Execution Roles

---

## 🚀 Deployment

To ensure this environment is easily reproducible, the entire architecture is deployed via AWS CloudFormation. 

### Prerequisites
1. AWS CLI installed and configured.
2. **AWS CloudTrail** enabled in your account to capture API events.
   
   ![AWS CloudTrail Enabled](Screenshots/Enable%20CloudTrail%20Logging.png)

### Run CloudFormation
Deploy the stack using the AWS CLI. Note the `--capabilities CAPABILITY_IAM` flag is required as the template provisions custom IAM roles.

```bash
aws cloudformation deploy \
  --template-file automated-sre-remediation.yaml \
  --stack-name sre-remediation-stack \
  --capabilities CAPABILITY_IAM
```

Wait for the terminal to output `Successfully created/updated stack - sre-remediation-stack`. 
     ![Cloud Formation Stack Completed](Screenshots/Cloud%20Formation%20Stack%20Complete.png)

### Step 3: Test the Automation
1. Go to the **EC2 Dashboard** in the AWS Console.
2. Navigate to **Security Groups** and find the one named `TargetSecurityGroup`.
3. Select it, click **Edit inbound rules**, and add a new rule:
   * **Type:** SSH
   * **Port Range:** 22
   * **Source:** Custom -> `0.0.0.0/0`
4. Click **Save rules**.
5. Wait about 5 to 10 seconds, and refresh the page. The rule will automatically disappear.
![Manually Add Inbound SSH Rule](Screenshots/Manually%20add%20ssh%20inbound%20rule.png)
![Inbound Rule Removed](Screenshots/Inbound%20Rule%20Violation%20Removed.png)

### Step 4: Check Observability (Logs)
1. Go to the **CloudWatch Dashboard**.
2. Click on **Log groups** and search for `/aws/lambda/SREAutomatedRemediationFunction`.
3. Open the latest log stream. You will see: `VIOLATION DETECTED: Port 22 open to 0.0.0.0/0` followed by a success message.
![CloudWatch Logs](Screenshots/CloudWatch%20Logs.png)

### Step 5: Clean Up
To remove the resources from your AWS account:

```bash
aws cloudformation delete-stack \
  --stack-name sre-remediation-stack
  ```