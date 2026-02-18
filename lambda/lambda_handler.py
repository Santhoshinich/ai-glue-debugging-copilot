import os
import json
import requests
import boto3

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LOG_GROUPS = [
    "/aws-glue/jobs/logs-v2",
    "/aws-glue/jobs/error",
    "/aws-glue/jobs/output"
]

logs_client = boto3.client("logs")

ERROR_CATEGORIES = {
    "SCHEMA_MISMATCH",
    "S3_PATH_NOT_FOUND",
    "ACCESS_DENIED",
    "SPARK_MEMORY_ERROR",
    "UNKNOWN"
}


def get_glue_logs(job_run_id):

    for log_group in LOG_GROUPS:
        try:
            response = logs_client.describe_log_streams(
                logGroupName=log_group,
                orderBy="LastEventTime",
                descending=True
            )

            for stream in response["logStreams"]:
                if job_run_id in stream["logStreamName"]:

                    events = logs_client.get_log_events(
                        logGroupName=log_group,
                        logStreamName=stream["logStreamName"],
                        limit=200
                    )

                    logs_text = "\n".join(
                        [event["message"] for event in events["events"]]
                    )

                    return logs_text

        except logs_client.exceptions.ResourceNotFoundException:
            continue

    return "No logs found."


def analyze_logs(log_text):

    truncated_logs = log_text[-3000:]

    prompt = f"""
You are an AWS Glue debugging assistant.

Return ONLY valid JSON in this format:

{{
  "error_category": "",
  "root_cause": "",
  "suggested_fix": "",
  "confidence_score": 0.0
}}

Choose error_category from:
SCHEMA_MISMATCH
S3_PATH_NOT_FOUND
ACCESS_DENIED
SPARK_MEMORY_ERROR
UNKNOWN

Logs:
{truncated_logs}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0
        }
    )

    data = response.json()

    if "choices" not in data:
        raise Exception(f"OpenAI API error: {data}")

    raw_output = data["choices"][0]["message"]["content"]

    return json.loads(raw_output)


def lambda_handler(event, context):

    print("Received event:", json.dumps(event))

    detail = event.get("detail", {})
    job_run_id = detail.get("jobRunId")

    if not job_run_id:
        return {
            "statusCode": 400,
            "body": "No jobRunId found."
        }

    logs_text = get_glue_logs(job_run_id)

    print("Retrieved Logs (first 500 chars):", logs_text[:500])

    result = analyze_logs(logs_text)

    print("AI Result:", result)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
