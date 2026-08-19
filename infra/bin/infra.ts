#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { LeetcodeCloneStack } from "../lib/infra-stack";

const app = new cdk.App();

new LeetcodeCloneStack(app, "LeetcodeCloneStack", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  // Read from CDK context (see README for how to pass these):
  //   cdk deploy -c keyPairName=your-key-name -c githubRepoUrl=https://github.com/you/repo.git
  keyPairName: app.node.tryGetContext("keyPairName"),
  githubRepoUrl: app.node.tryGetContext("githubRepoUrl"),
});