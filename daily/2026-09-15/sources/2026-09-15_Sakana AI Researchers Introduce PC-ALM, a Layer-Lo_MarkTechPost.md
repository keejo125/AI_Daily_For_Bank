---
publish_time: 1789418776
link: https://www.marktechpost.com/2026/09/14/sakana-ai-researchers-introduce-pc-alm-a-layer-local-alternative-to-backpropagation-that-trains-1000-layer-networks/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  Sakana AI 提出增强拉格朗日预测编码（PC-ALM），作为反向传播的层局部替代方案。它保留每一步更新的层局部性，同时恢复与反向传播对齐的信用信号，在 MNIST 上以约 2 个百分点差距训练出至多 1000 层的残差 MLP。研究以 MIT 许可的 JAX 参考实现开源、可在 CPU 运行，但目前仅是训练方法而非模型，且仅在小型图像基准上验证，能否扩展到大规模任务尚待观察。
---

# Sakana 提出 PC-ALM：层局部替代反向传播，训练千层网络

> 原文链接：https://www.marktechpost.com/2026/09/14/sakana-ai-researchers-introduce-pc-alm-a-layer-local-alternative-to-backpropagation-that-trains-1000-layer-networks/
> 来源：MarkTechPost

Backpropagation is a global algorithm: a forward pass, then a backward pass, then a weight update, each locked behind the previous one. Brains have no known mechanism for that kind of network-wide phase locking, which is why local-learning alternatives such as predictive coding (PC) keep drawing research interest. Sakana AI researchers propose Augmented Lagrangian Predictive Coding (PC-ALM), a variant of PC that keeps every update layer-local yet recovers backprop-aligned credit signals. The research team reports training residual MLPs up to 1000 layers within about 2 percentage points of backprop on MNIST.

Is it deployable? Yes, as research code: an MIT-licensed JAX reference implementation runs on CPU and reproduces the paper&#8217;s width-depth grid. It is a training method, not a model, and has only been tested on small image benchmarks.

Why standard PC stalls in deep, narrow networks

PC treats every hidden activation as an optimization variable and penalizes the squared mismatch between each layer&#8217;s activation and the prediction arriving from the layer below. Inference is gradient descent on that energy; learning is a Hebbian-like weight step. The catch is that supervision enters at the output and must diffuse through a chain of local compromises. In deep, narrow networks the credit signal fades long before it reaches the input. Innocenti et al. characterized this PC-BP gap as a function of width and depth, and it is worst when width is smaller than depth.

What PC-ALM changes

PC-ALM starts from the constrained view of training: minimize the supervised loss subject to hi=σ(Wihi−1)h_i = \sigma(W_i h_{i-1})  at every layer. PC is the quadratic-penalty relaxation of that problem. PC-ALM uses the augmented Lagrangian instead, attaching a Lagrange multiplier λi∈ℝdisuch thatdim(λi)=dim(hi)\lambda_i \in \mathbb{R}^{d_i} \quad \text{such that} \quad \text{dim}(\lambda_i) = \text{dim}(h_i) to each layer constraint while keeping PC&#8217;s penalty. Setting λ = 0 recovers PC exactly.

Inference alternates 2 local steps: a primal gradient step on the activations, and a dual step λi←λi+αri\lambda_i \leftarrow \lambda_i + \alpha r_i that accumulates the layer&#8217;s prediction error. Completing the square shows each primal step is a standard PC step with the prediction target shifted by −λi/ρ-\lambda_i/\rho. After T steps the weight update acts on the composite signal λi+ρri\lambda_i + \rho r_i. The research team read this as a PI controller per layer: the prediction error is the proportional term and the multiplier is the integral term. α = 0 gives PC; α = ρ with the inner problem solved exactly gives the classical method of multipliers.

Exact backprop gradients in the linear case

LeCun observed in 1988 that the Lagrange multipliers of a constrained network equal the backprop adjoints at a KKT point. The team proves that in linear PC networks, under a spectral-radius stability condition, PC-ALM converges to that KKT point: activations return to their forward-pass values while each λi\lambda_i integrates to the exact BP adjoint. The per-mode stability bound is ηhσi2(2ρ+α)<4\eta_h \sigma_i^2 (2\rho + \alpha) < 4, which reduces to PC&#8217;s condition at α = 0. Unlike PC&#8217;s monotone gradient flow, PC-ALM&#8217;s iteration matrix has complex eigenvalues that produce damped oscillations; α sets their frequency but not their decay rate.

Results

The research team sweeps residual MLPs with width and depth from 8 to 128 on Fashion-MNIST and MNIST under the mean-field parameterization of Innocenti et al., training for 1 epoch. With an inference budget of T = 2L, PC-ALM matches backprop across every width, depth, and activation (identity, tanh, ReLU), while PC drops sharply in deep, narrow cells. The repo&#8217;s reference cell (width 32, depth 32, ReLU, Fashion-MNIST) reports 78.66% test accuracy for BP, 68.13% for PC, and 77.75% for PC-ALM, with gradient cosine to BP rising from 0.604 to 0.909.

The research extends the picture: 1000-layer residual MLPs on MNIST (width 32, ReLU, 5 epochs) stay within roughly 2 points of BP, and PC-ALM improves over PC on every benchmark tried, including ResNet-18 on CIFAR-10 and Tiny ImageNet.

&&

Key Takeaways

PC-ALM adds a per-layer Lagrange multiplier to predictive coding; every update stays layer-local.

In linear networks the multipliers converge to exact backprop gradients.

Matches BP across the 8 to 128 width-depth grid at T = 2L; PC fails in deep, narrow cells.

Trains 1000-layer residual MLPs within about 2 points of BP on MNIST.

MIT-licensed JAX code reproduces the results on CPU.

Check out the Paper, Blog, and GitHub Repo. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Sakana AI Researchers Introduce PC-ALM, a Layer-Local Alternative to Backpropagation That Trains 1000-Layer Networks appeared first on MarkTechPost.