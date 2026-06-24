# CostShield v2.0

## Automated AWS FinOps Cost Optimization Engine

CostShield is a serverless FinOps automation solution that identifies unused AWS storage resources, estimates potential cost savings, and safely removes unnecessary resources using AWS Lambda.

---

## Features

- Detect unattached EBS Volumes
- Detect old EBS Snapshots
- Protect snapshots used by AMIs
- DRY_RUN mode for safe testing
- Monthly & Annual Cost Estimation
- CloudWatch Logging
- EventBridge Automation
- Modular Python Architecture

---

## AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon EventBridge Scheduler
- Amazon CloudWatch
- AWS IAM

---

## Technologies

- Python 3.9+
- Boto3
- AWS SDK
- JSON
- IAM Policies

---

## Project Structure

```

CostShield/

├── lambda_function.py
├── config.py
├── logger.py
├── utils.py
├── volume_scanner.py
├── snapshot_scanner.py
├── finops.py
├── requirements.txt
├── deployment_guide.md
├── iam_policy.json
├── .gitignore
└── README.md

```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| DRY_RUN | Enable safe execution |
| RETENTION_DAYS | Snapshot retention period |
| COST_PER_GB | Monthly storage cost |
| LOG_LEVEL | Logging level |
| AWS_REGION | AWS Region |

---

## How It Works

EventBridge

↓

Lambda

↓

Volume Scanner

↓

Snapshot Scanner

↓

FinOps Engine

↓

CloudWatch Logs

↓

Savings Report

---

## Future Improvements

- S3 Cleanup
- Idle EC2 Detection
- Unused Elastic IP Detection
- RDS Storage Optimization
- SNS Email Notifications

---

## Author

Built as a FinOps Automation Project using AWS Serverless Technologies.
