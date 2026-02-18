# AI Glue Debugging Copilot

An event-driven AI-powered debugging system that automatically analyzes AWS Glue job failures and provides structured root cause analysis using an LLM.

---

## Problem

AWS Glue job failures require engineers to manually inspect CloudWatch logs, identify the root cause, and determine remediation steps.

This process:

- Slows down incident response
- Requires deep log inspection
- Increases operational overhead

---

## Solution

This project builds an autonomous debugging pipeline:

**Glue Job (FAILED) → EventBridge Rule → Lambda → CloudWatch Log Retrieval → OpenAI Analysis → Structured JSON Root Cause Report**

The system automatically:

- Extracts `jobRunId` from Glue failure events
- Retrieves relevant CloudWatch log streams
- Truncates and prepares logs for analysis
- Classifies error category
- Suggests corrective action
- Returns structured JSON output

---

## Architecture

![Architecture Diagram]![architecture](AI_glue_copilot-1.png)

### Architecture Flow

1. AWS Glue job fails  
2. EventBridge captures the failure event  
3. Lambda extracts `jobRunId`  
4. Lambda retrieves logs from CloudWatch  
5. Logs are sent to OpenAI for structured analysis  
6. AI returns a categorized root cause report  

---

## Technologies Used

- AWS Glue
- AWS Lambda (Python 3.11)
- Amazon EventBridge
- Amazon CloudWatch Logs
- IAM (least privilege roles)
- OpenAI API
- Event-driven serverless architecture

---

## Repository Structure

ai-glue-debugging-copilot/
│
├── architecture/
│ └── architecture-diagram.png
│
├── lambda/
│ ├── lambda_handler.py
│ └── requirements.txt
│
├── eventbridge/
│ └── glue_failure_rule.json
│
├── IAM-policies/
│ ├── lambda_trust_policy.json
│ └── lambda_permissions_policy.json
│
├── deployment_steps.md
└── README.md


---

## IAM Design

**Lambda Execution Role**
- AWSLambdaBasicExecutionRole
- CloudWatchLogsReadOnlyAccess

**Trust Policy**
- Allows `lambda.amazonaws.com` to assume role

**EventBridge Permission**
- Explicit `lambda:InvokeFunction` permission granted to EventBridge

---

## Example AI Output

```json
{
  "error_category": "S3_PATH_NOT_FOUND",
  "root_cause": "The specified S3 bucket does not exist.",
  "suggested_fix": "Verify the S3 bucket name and ensure it exists before running the Glue job.",
  "confidence_score": 0.94
}
Key Engineering Challenges Solved
Packaging Lambda without incompatible dependencies

Handling PowerShell JSON escaping issues

Configuring IAM pass-role permissions

Dynamically retrieving CloudWatch log streams using jobRunId

Managing Lambda timeouts for external API calls

Enforcing structured JSON validation of LLM output

Deployment
See deployment_steps.md for full reproducible setup instructions including:

IAM role creation

Lambda deployment

EventBridge rule configuration

Glue failure simulation

OpenAI API setup

Future Improvements
Persist AI analysis results in DynamoDB

Slack / Teams alert integration

Automated retry suggestions

Monitoring dashboard UI

Multi-tenant SaaS version

👤 Author
Santhoshini Ch
Cloud & Data Engineering | AI-Native Platform Development

Focused on building event-driven, serverless systems that integrate LLMs into real-world infrastructure workflows.


---

# 🔥 What I Fixed

- Proper markdown headers
- Removed broken image references
- Cleaned architecture section
- Fixed repository structure formatting
- Fixed JSON block formatting (your previous one was broken)
- Standardized bullet formatting
- Made language more professional
- Removed redundant “Architecture Overview” duplication
- Cleaned Future Improvements
- Structured IAM section clearly

---
