---
publish_time: 1791098999
link: https://www.marktechpost.com/2026/10/04/google-research-moves-federated-learning-into-tees-gboard-now-trains-with-externally-verifiable-differential-privacy/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Research 宣布基于可信执行环境（TEE）构建的新一代联邦学习（FL）系统，宣称首次为 FL 提供可外部验证的中心化差分隐私（DP）保障。自 2017 年 FL 问世以来，Gboard 联想词预测、Smart Compose 等依赖它，但旧系统存在信任缺口：外部无法验证数据是否未被记录或检查，且安全聚合与矩阵分解 DP-FTRL 等先进中心化 DP 算法不兼容，还需信任谷歌正确注入 DP 噪声。
  
  新设计将客户端梯度计算迁移至服务端并使其可证明（attestable），运营方不再需要被信任。系统协调数据上传、KMS 与策略校验、TEE 内计算、公开透明日志四大组件，在保密前提下实现可验证的隐私保护。
---

# 谷歌研究将联邦学习引入可信执行环境：Gboard 实现可外部验证的差分隐私训练

> 原文链接：https://www.marktechpost.com/2026/10/04/google-research-moves-federated-learning-into-tees-gboard-now-trains-with-externally-verifiable-differential-privacy/
> 来源：MarkTechPost

Google Research has announced a next-generation Federated Learning (FL) system built on Trusted Execution Environments (TEEs). The research team claims externally verifiable central differential privacy (DP) guarantees for FL for the first time. 

What Problem Does TEE-Based Federated Learning Solve?

Google introduced Federated Learning FL in 2017. It powers next-word prediction and Smart Compose on Gboard, reply suggestions in Google Messages, and Smart Text Selection in Android.

Earlier systems had a trust gap. Devices uploaded data for immediate aggregation, but outsiders could not verify that data was never logged or inspected. Secure Aggregation added cryptographic protection. However, it was not compatible with state-of-the-art central DP algorithms like matrix factorization DP-FTRL. Google also had to be trusted to add DP noise correctly.

The new design moves client gradient computation to the server. It then makes that server logic attestable, so the operator no longer needs to be trusted.

How Does the System Work?

The system builds on Google&#8217;s earlier confidential federated analytics work. It coordinates 4 core components:

Data upload: Devices encrypt training examples locally and pre-authorize an access policy. The policy lists which TEE computations may process the data. Policies must appear in a public transparency log.

KMS and policy verification: A Key Management System, built from TEEs running the RAFT consensus protocol, releases keys only to workloads matching the policy.

Workload execution: A root TEE runs a Python training loop and delegates subtasks to worker TEEs. Orchestration uses Federated Language, derived from TensorFlow Federated. Only DP model weights are released.

Fault-tolerant recovery: Each round saves a KMS-encrypted recovery state for handling root or worker failures.

Why Is the Privacy Guarantee Verifiable?

Access policies are published to Rekor, Sigstore&#8217;s public transparency log. External auditors can track every server workload a device could feed. The KMS and data processing binaries are reproducibly buildable from open source code.

The policies directly describe the Python training program. To protect proprietary model architectures, TEEs support sideloading serialized logic at runtime. All privacy-relevant logic must stay hardcoded in the attested program. Workload operators see only metrics and DP model weights. Encrypted data can be decrypted only for a limited time after upload.

What Did Gboard Gain?

Gboard used the system to launch English and Japanese next-word prediction models with stronger privacy guarantees and improved accuracy. Two design choices drive this:

First, all uploads are collected before server-side training runs. Diurnal swings in device availability no longer slow training. The program can compute an optimal participation schedule and tune DP parameters. Google&#8217;s privacy-utility curves come from training an English model for 5000 rounds with cohorts of 6500 devices on both systems.

Second, the bottleneck moved to the server. Previous FL models took 1 to 2 months each to train. Training now parallelizes across machines, limited only by TEE resource availability. Google reports substantially faster compute times but does not publish a single speedup figure.

Interactive Explainer: Inside the TEE-Based FL Pipeline

How Google&#8217;s TEE-based Federated Learning works
Interactive explainer based on Google Research&#8217;s Oct 2, 2026 post and paper (arXiv:2609.31494).

  1. Data pipeline
  2. Who can see what
  3. Tamper test

      Phonesencrypt locally+ access policy
      KMS (TEEs)RAFT clusterchecks policy
      Root TEEPython training+ worker TEEs
      AnalystDP modelweights only
      KMS-encrypted recovery state

    Step 1Data upload
    Step 2KMS + policy
    Step 3Workload execution
    Step 4Fault recovery

  &#9654; Auto-playNext step

  Earlier FLTEE-based FL

  Pick the server workload that asks the KMS for decryption keys. Only code listed in the published access policy gets them.

    Approved training programhash = matches policy in Rekor log

    Modified program (logs raw data)hash = not in access policy

  Request decryption key
  &#128274;
Waiting for a request. The KMS verifies the TEE&#8217;s remote attestation against the access policy.

Sources: research.google blog, arXiv:2609.31494Built by Marktechpost

&#9654;&#10074;&#10074;

&#128274;&#128275;&#128274;

How Does It Compare With Other FL Frameworks?

FeatureGoogle TEE-based FLNVIDIA FLAREFlowerApple pfl-researchPrimary useProduction cross-device training (live in Gboard)Production FL SDK with Docker, Kubernetes and cloud toolingFramework for building federated AI systemsSimulation only; not intended for third-party deploymentsWhere client updates are computedServer-side TEEsAt each participating siteOn clientsSimulatedHardware TEE supportYes, built on Project OakYes: AMD SEV-SNP, Intel TDX, NVIDIA GPU confidential computingNot part of the core frameworkNoDifferential privacyCentral DP, externally verifiableDP filters, DP-SGD via OpacusCentral and local DPLocal and central DP mechanismsOther privacy techKMS-gated decryption; Willow secure aggregation containerHomomorphic encryption, private set intersectionSecAgg and SecAgg+Not applicable (simulation)Public transparency log for server codeYes, Sigstore RekorNot documentedNot documentedNot applicableReproducible TEE buildsYes (KMS and data processing binaries)Not documentedNot applicableNot applicableLicenseApache 2.0Apache 2.0Apache 2.0Apache 2.0

Sources: Google Research blog, Confidential Federated Compute repo, NVIDIA FLARE docs, FLARE attestation guide, Flower 1.8 release notes, pfl-research repo. Verified October 4, 2026.

Key Takeaways

Google moved FL gradient computation from phones into attested server-side TEEs.

Central DP guarantees are now externally verifiable via Rekor and reproducible builds.

Gboard ships English and Japanese next-word models on the new system.

Training once took 1 to 2 months per model; TEE capacity is now the limit.

Core TEE binaries and Federated Language are open source under Apache 2.0.

Check out the Paper, Technical details and GitHub Repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google Research Moves Federated Learning Into TEEs: Gboard Now Trains With Externally Verifiable Differential Privacy appeared first on MarkTechPost.