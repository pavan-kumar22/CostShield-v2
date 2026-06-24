# Deployment Guide

## Step 1

Create IAM Role

Attach:

- AWSLambdaBasicExecutionRole

Custom Policy:

- DescribeVolumes
- DeleteVolume
- DescribeSnapshots
- DeleteSnapshot
- DescribeImages

---

## Step 2

Create Lambda Function

Runtime

Python 3.12

Architecture

x86_64

Memory

128 MB

Timeout

30 seconds

---

## Step 3

Upload Project

Upload ZIP

---

## Step 4

Configure Environment Variables

DRY_RUN=true

RETENTION_DAYS=30

COST_PER_GB=0.08

LOG_LEVEL=INFO

AWS_REGION=ap-southeast-2

---

## Step 5

Create EventBridge Schedule

cron(0 2 * * ? *)

Timezone

Asia/Kolkata

---

## Step 6

Verify CloudWatch Logs