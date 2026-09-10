---
publish_time: 1788897114
link: https://www.marktechpost.com/2026/09/08/nvidia-announces-cuda-rust-with-cuda-oxide-simt-and-cutile-rs-tile-for-compile-time-safe-gpu-kernels/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA 宣布 CUDA Rust，推动 Rust 成为编写 GPU kernel 的一等语言。配套两个 NVlabs 开源项目：cuda-oxide（SIMT 模型）与 cutile-rs（Tile 模型），均原生编译 Rust kernel，并借助 Rust 所有权规则在编译期拦截别名 bug。cutile-rs 已发布于 crates.io，支持稳定版 Rust 1.89+，用于 Hugging Face Grout 推理引擎与 mistral.rs；cuda-oxide 仍处早期 alpha。AI 系统层（推理引擎、驱动、Agent 运行时）正加速向 Rust 迁移。
---

# NVIDIA 发布 CUDA Rust：用 Rust 编写 GPU 内核的一等语言

> 原文链接：https://www.marktechpost.com/2026/09/08/nvidia-announces-cuda-rust-with-cuda-oxide-simt-and-cutile-rs-tile-for-compile-time-safe-gpu-kernels/
> 来源：MarkTechPost

NVIDIA has announced CUDA Rust, a push to make Rust a first-class language for writing GPU kernels. Rust code could already launch CUDA kernels, but the kernel body usually had to be written elsewhere. CUDA Rust closes that gap with two NVlabs open-source projects: cuda-oxide for the SIMT model and cutile-rs for the newer Tile model. Both compile Rust kernels natively and use Rust&#8217;s ownership rules to reject aliasing bugs at compile time. 

Is it deployable? Partially. cutile-rs is published on crates.io, runs on stable Rust 1.89+, and is already used in Hugging Face&#8217;s Grout inference engine and in mistral.rs. cuda-oxide is early alpha. The both projects are in alpha phase and not confirmed for production.

Why Rust for the GPU Kernel

The systems layer of AI, from inference engines to drivers and agent runtimes, is increasingly written in Rust. NVIDIA&#8217;s Nova Linux driver is in Rust, NVIDIA Dynamo has a Rust core, and NVTX has Rust bindings. The GPU kernel was the exception.

The two tracks mirror the two programming models CUDA already offers. SIMT is the model used in CUDA C++ and numba-cuda: you describe what one thread does and launch thousands of them. Tile is the newer model, also available in C++ and Python: you describe what one tile of data does, and the Tile IR compiler handles thread mapping and memory layout. NVIDIA recommends Tile first, with SIMT for explicit thread and memory control. Planned inter-language interop means choosing Rust will not lock developers out of C++ or Python.

The SIMT Track: cuda-oxide

cuda-oxide is a custom rustc codegen backend. It routes #[kernel] functions through Rust MIR, the community Pliron IR framework, and LLVM IR down to PTX, then hands everything else to the standard backend. NVIDIA wrote the GPU dialects on top of Pliron.

Requirements: Linux, a GPU with compute capability 8.0 or later, CUDA 12.x or newer, clang with libclang, and a pinned nightly toolchain (nightly-2026-04-03). cargo oxide doctor checks the setup and cargo oxide new scaffolds a vector addition program, with host and device code in one file.

The safety argument sits in the kernel signature. Inputs a and b are ordinary shared slices. The output c is a DisjointSlice<f32>, a type that gives each thread exclusive access to its own element. A plain &mut [f32] would need every thread to hold the same mutable borrow, which Rust refuses. c.get_mut(idx) returns an Option, so out-of-bounds access becomes a handled branch. A #[launch_contract] attribute declares the block shape, and the generated prepare_vecadd method validates the launch configuration against it before the safe launch runs.

The Tile Track: cutile-rs

cutile-rs works one level higher. Each tile block runs the kernel body once as a single logical thread over one sub-tensor, and the compiler decides how many real GPU threads back it. The #[cutile::module] macro embeds the kernel&#8217;s AST in the host binary and JIT-compiles it through CUDA Tile IR when the kernel is first launched.

Requirements are lighter: compute capability 8.0 or later, CUDA 13.3, stable Rust 1.89 or newer, and Linux, with no nightly and no custom LLVM. Setup is cargo new, then cargo add cutile.

The host-side .partition([128]) call does 3 jobs. It gives each tile exclusive ownership of its 128-element chunk, fixes the grid at 1,024 / 128 = 8 tiles, and supplies the const tile width B. Input tensors use -1 as a dynamic dimension resolved at launch. The generated launcher takes ownership of all tensors and returns them when the GPU finishes. Nothing executes until .sync_on(&stream); everything before it is a lazy description recorded in one chain.

&

What the Compiler Catches

Passing the SIMT kernel&#8217;s output buffer as one of its own inputs fails with error[E0502]: cannot borrow c_dev as mutable because it is also borrowed as immutable. The same aliasing on the Tile side fails with error[E0382]: use of moved value: z. cuda-oxide checks each launch call; cutile-rs&#8217;s ownership follows tensors across the launch boundary, which NVIDIA calls the stronger guarantee.

Tile exposes no shared memory or thread indexing to misuse. SIMT keeps that control, but shared memory in cuda-oxide currently requires unsafe.

Key Takeaways

CUDA Rust adds 2 native GPU kernel tracks in Rust: cuda-oxide (SIMT) and cutile-rs (Tile).

cuda-oxide compiles Rust MIR through Pliron and LLVM to PTX; it needs a pinned nightly.

cutile-rs runs on stable Rust 1.89+ with CUDA 13.3 and JIT-compiles via CUDA Tile IR.

Both reject buffer aliasing at compile time using Rust&#8217;s borrow checker and ownership.

cutile-rs already powers Grout and mistral.rs; neither project is production-ready yet.

Check out the Technical details here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post NVIDIA Announces CUDA Rust with cuda-oxide (SIMT) and cutile-rs (Tile) for Compile-Time-Safe GPU Kernels appeared first on MarkTechPost.