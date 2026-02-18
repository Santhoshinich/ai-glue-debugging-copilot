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

Glue Job (FAILED)
→ EventBridge Rule
→ Lambda Function
→ CloudWatch Log Retrieval
→ OpenAI Analysis
→ Structured JSON Root Cause Report

The system automatically:
- Extracts jobRunId from Glue failure event
- Pulls relevant log streams
- Truncates and analyzes logs
- Classifies error type
- Suggests corrective action
- Returns structured JSON output

---

## Architecture
![Architecture Diagram]![architecture](AI_glue_copilot.png)

Architecture flow diagram as below

            +-------------------+
            |   AWS Glue Job    |
            |    (Failure)      |
            +---------+---------+
                      |
                      v
            +-------------------+
            |  EventBridge Rule |
            +---------+---------+
                      |
                      v
            +-------------------+
            |      Lambda       |
            |  GlueAICopilot    |
            +---------+---------+
                      |
    +-----------------+-----------------+
    |  CloudWatch Logs OpenAI API (LLM) |  
    +---------------+-------------------+

```markdown
# Architecture Overview 

Event-driven AI debugging pipeline:

1. AWS Glue job fails
2. EventBridge captures failure event
3. Lambda extracts jobRunId
4. Lambda retrieves logs from CloudWatch
5. Logs are sent to OpenAI for structured analysis
6. AI returns root cause classification
---

## Technologies Used

- AWS Glue
- AWS Lambda (Python 3.11)
- Amazon EventBridge
- Amazon CloudWatch Logs
- IAM (least privilege roles)
- OpenAI API
- Event-driven architecture

## Repository Structure
![Repositiry]![repo](repository.png)

---

## IAM Design

Lambda Execution Role:
- AWSLambdaBasicExecutionRole
- CloudWatchLogsReadOnlyAccess

Trust Policy:
- Allows `lambda.amazonaws.com` to assume role

EventBridge Permission:
- Explicit invocation permission added to Lambda

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

a. Packaging Lambda without incompatible dependencies

b. Handling PowerShell JSON escaping issues

c. Configuring IAM pass-role permissions

d. Dynamically retrieving CloudWatch log streams using jobRunId

e. Managing Lambda timeouts for external API calls

f. Structured JSON validation of LLM output

Deployment

See deployment_steps.md for full reproducible setup instructions.

Future Improvements

a. Persist AI results in DynamoDB

b. Slack/Teams alert integration

c. Retry automation suggestions

Dashboard UI

Multi-tenant SaaS version

## Author

Santhoshini ch  
Cloud & Data Engineering | AI-Native Platform Development

Focused on building event-driven, serverless systems that integrate LLMs into real-world infrastructure workflows.


