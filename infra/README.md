# Infrastructure (AWS CDK)

Automates provisioning the EC2 instance, security group, and Elastic IP for
this project. Does NOT automate creating `.env` or bringing up the app
itself -- that's a deliberate choice, so real secrets never pass through
CloudFormation/instance metadata.

## Prerequisites

- Node.js
- AWS CLI, configured with your credentials (`aws configure`)
- An existing EC2 key pair (create one via the EC2 console or:
  `aws ec2 create-key-pair --key-name your-key-name --query 'KeyMaterial' --output text > your-key-name.pem`)

## First-time setup

```
cd infra
npm install
npx cdk bootstrap
```

`cdk bootstrap` only needs to run once per AWS account/region -- it sets up
a small S3 bucket CDK uses internally for deployments.

## Deploy

```
npx cdk deploy -c keyPairName=your-key-name -c githubRepoUrl=https://github.com/you/your-repo.git
```

This provisions the instance and prints outputs including:
- The Elastic IP (fixed, won't change on restart)
- A suggested `.nip.io` domain to use in your `.env`
- The exact SSH command to connect

## After deploying

SSH in using the printed command, then:

```
cd app
cp .env.example .env
nano .env    # fill in real values, including DOMAIN from the CDK output
docker compose up -d piston
# install Piston languages (see project README)
docker compose up -d --build
```

## Tearing down

```
npx cdk destroy
```

This deletes the instance, security group, and Elastic IP. Nothing else in
your AWS account is touched.