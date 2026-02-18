# Deployment Steps

## 1. Create IAM Role for Lambda

- Attach:
  - AWSLambdaBasicExecutionRole
  - CloudWatchLogsReadOnlyAccess

## 2. Deploy Lambda

- Runtime: Python 3.11
- Timeout: 20 seconds
- Environment variable:
  OPENAI_API_KEY=<your_key>

## 3. Create EventBridge Rule

Event pattern:

{
  "source": ["aws.glue"],
  "detail-type": ["Glue Job State Change"],
  "detail": {
    "state": ["FAILED"]
  }
}

## 4. Add Lambda as EventBridge Target

## 5. Grant EventBridge Invoke Permission

aws lambda add-permission ...

## 6. Trigger Glue Failure

Run Glue job with invalid S3 path to test automation.

```markdown
# Architecture Overview

Event-driven AI debugging pipeline:

1. AWS Glue job fails
2. EventBridge captures failure event
3. Lambda extracts jobRunId
4. Lambda retrieves logs from CloudWatch
5. Logs are sent to OpenAI for structured analysis
6. AI returns root cause classification