---
publish_time: 1794504368
link: https://www.marktechpost.com/2026/11/12/aws-emulator-local-aws-api-emulator-ai-agents/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  AWS 发布 AWS Emulator，一个本地运行的 AWS API 模拟器：在笔记本、开发服务器或 CI 中运行，CLI 与 SDK 改指向它即可，无需账号、无服务费。其特殊之处在于全部代码由自主智能体编写与审查，基于 438 个 AWS API 模型覆盖 200+ 服务；v1.0.322 通过 24243/42857 项保真测试（56.6%），KMS 最佳（93.9%）、CloudFormation 最弱（15.8%），为开发者与编码智能体提供快速免费的 AWS 形态测试回路。
---

# AWS 发布 AWS Emulator：由 AI 智能体构建的本地 AWS API 模拟器

> 原文链接：https://www.marktechpost.com/2026/11/12/aws-emulator-local-aws-api-emulator-ai-agents/
> 来源：MarkTechPost

AWS has released AWS Emulator, a local emulator of the AWS APIs. You run it on a laptop, a dev server or in CI. The AWS CLI and SDKs talk to it instead of AWS. No AWS account is needed, and there is no service fee. The unusual part: autonomous agents wrote and reviewed all of its code. For developers and coding agents, AWS Emulator gives a fast, free test loop against AWS-shaped APIs.

TL;DR

Size: Built from 438 AWS API models, covering 200+ services. One Rust crate per service.

Runs on: Linux x86_64/aarch64 (RPM or Debian), or Docker on macOS/Windows with a 2 GiB memory limit. Source builds need 100 GB of free disk.

Performance: Passes 24,243 of 42,857 scored fidelity tests (56.6%) in release v1.0.322.

Best: AWS KMS at 93.9% (291 of 310 tests); Amazon SQS at 89.8%.

Worst: AWS CloudFormation at 15.8% (414 of 2,612 tests).

What is AWS Emulator?

AWS Emulator is a headless local program from AWS that serves an AWS API endpoint. You point the CLI or an SDK at it with environment variables. Your code does not change. Resources live in memory and vanish when it stops.

The docs show a DynamoDB example. A CreateTable call with a 2-character name fails with the same ValidationException text AWS returns.

How did AI agents build AWS Emulator?

The project began with a prompt to Kiro. It returned a passable Amazon SQS emulator in about 15 minutes. AWS then split the work across 3 teams of agents:

Test writers derive scenarios from the public Smithy API models and verify each against real AWS.

Issue finders replay those tests against the emulator and file failures.

Fixers take 1 issue each and submit a patch.

Every patch passes a merge gate covering build, code review, security and fidelity. Several security agents run adversarial reviews. Matthew Goldberg reports hundreds of concurrent agents fixing thousands of issues a day. The release pipeline runs on AWS Developer Tools, with CodeCommit as the agents&#8217; repository. Code reaches GitHub last.

&&&

How accurate is AWS Emulator?

AWS publishes a scores.json file with each release. We tallied the v1.0.322 file, scored on November 11, 2026.

Overall: 24,243 of 42,857 scored tests pass (56.6%); 80 were skipped.

Step level: 49,810 of 68,007 individual steps pass (73.2%).

Cross-service workflows: 2,752 of 6,569 pass (41.9%).

Core services: S3 79.1%, DynamoDB 77.3%, SNS 73.9%, Lambda 46.4%, EC2 41.5%.

Per the fidelity docs, control-plane APIs match AWS best. Data-plane, CloudFormation, Terraform and CDK support varies by service. Unimplemented operations return HTTP 501 NotImplemented. The tests live in aws-emulator-evaluation-suite, including failing ones.

How do you run AWS Emulator?

There are 4 paths, per the README:

Linux: install the RPM or Debian package and run aws-emulator.

macOS/Windows: build a container from AWS&#8217;s Dockerfile, capped at 2 GiB memory.

Rust embedded mode: add it as a dev-dependency for 1 isolated instance per test.

Coding agents: aws agent-toolkit add-skill --skill-name aws-emulator, with AWS CLI 2.35.0 or later.

A source build serves HTTPS on 127.0.0.1:9297 with a self-signed certificate. It needs a Rust toolchain, a C compiler and at least 100 GB of disk. Embedded mode carries the same build cost on the first cargo test.

How does it compare with LocalStack, Moto and Floci?

FeatureAWS EmulatorLocalStackMotoFlociLicenseCC0 1.0 (vendor/ Apache 2.0)Commercial plansApache-2.0MITPriceFreeHobby $0 (non-commercial); Base $39; Ultimate $89 per license/month (annual)FreeFreeService coverage200+ services, 438 API models30+ / 55+ / 110+ by planNot disclosed in READMENot totaled in READMEVendor token neededNoYes (auth token)NoNot disclosedDefault endpointHTTPS 127.0.0.1:9297Port 4566Port 5000Port 4566In-process test modeRust dev-dependencyNot disclosedPython @mock_aws decoratorNot disclosedFootprint2 GiB Docker limit in AWS guideNot disclosedNot disclosed~13 MiB idle, ~24 ms start (self-reported)Published fidelity scoresYes, per releaseNot disclosedNot disclosedNot disclosed

What are AWS Emulator&#8217;s limitations?

AWS lists them plainly:

No IAM evaluation. Identity and resource policies are not evaluated like AWS. Do not use it for security tests.

1 Region, 1 account. It accepts any IDs but does not isolate resources by them.

Verified in us-west-2 only, with global services checked in us-east-1.

In-memory and short-lived. It is not tested for long runs or load tests. Use --idle-timeout to stop it.

Telemetry is on by default. Turn it off with --telemetry off, EMULATOR_TELEMETRY=off, config.toml or the embedded API.

The release pace is fast. Versions v1.0.265 to v1.0.322 shipped between November 8 and 11.

Key Takeaways

AWS Emulator is a free, CC0 local copy of 200+ AWS services.

Agents wrote all the code; humans built the tests and merge gates.

It passes 56.6% of 42,857 published fidelity tests at launch.

SQS, KMS and S3 are strong; CloudFormation and IoT lag.

Use it for fast local and CI loops, not security or load testing.

Check out the GitHub repo, the user guide, the fidelity tests and the engineering post. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post AWS Releases AWS Emulator: A Local Copy of 200+ AWS Services Built by AI Agents appeared first on MarkTechPost.