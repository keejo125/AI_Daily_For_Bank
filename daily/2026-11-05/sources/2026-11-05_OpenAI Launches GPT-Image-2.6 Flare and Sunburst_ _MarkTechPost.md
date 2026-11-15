---
publish_time: 1793862197
link: https://www.marktechpost.com/2026/11/04/openai-gpt-image-2-6-flare-sunburst/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: ""
---

# OpenAI Launches GPT-Image-2.6 Flare and Sunburst: Adds GIFs, SVG Export and 6-Second API Generation

> 原文链接：https://www.marktechpost.com/2026/11/04/openai-gpt-image-2-6-flare-sunburst/
> 来源：MarkTechPost

OpenAI just shipped Images 2.6 across ChatGPT, Codex and the API. For developers, the core release is GPT-Image-2.6, shipped as two API models: Flare and Sunburst. OpenAI team states that Images 2.6 generates images 50% faster than before. The update also adds GIF output, SVG export, markup-guided edits and a new complexity parameter.

TL;DR

Size: Closed weights, token-billed image API.

Runs on: OpenAI-hosted only (ChatGPT, Codex, API).

Performance: 50% faster image generation than the previous release, per OpenAI.

Best: Flare can return an image in as little as 6 seconds at low quality.

Worst: No benchmark scores and no per-image cost table published for 2.6.

image source: openai

What is GPT-Image-2.6?

GPT-Image-2.6 is OpenAI&#8217;s image generation and editing model family for the API. It accepts text and image inputs and returns images. GPT-Image-2.6 Flare is built for fast iteration and interactive workflows. GPT-Image-2.6 Sunburst is built for detailed compositions and editing.

OpenAI states that Flare can generate images in as little as 6 seconds when quality is set to low. Sunburst targets higher quality and stronger consistency across edits at medium or high quality. 

What changed in ChatGPT Images 2.6?

ChatGPT users can now turn a prompt or a photo into an animated GIF. They can adjust animation speed, edit individual frames and share the result. Users can also save and tag reference images of people, pets and characters. Those references can be reused later without uploading them again.

Usage keeps climbing. OpenAI says people now generate more than 4B images per week across ChatGPT and the API. That is up from more than 3B per week 8 weeks earlier, at the Images 2.5 launch. On average, that is over 500M images per day.

How does the new complexity parameter work?

The complexity field sets how much the model plans before it renders. The image generation guide lists 3 levels: low, medium and high. If you omit it, both models use high.

Low suits focused edits, such as changing a background or a sign. High helps with dense text, complex layouts and relationships between objects. OpenAI warns that higher complexity can add latency and introduce unwanted changes. Adjusting complexity has no separate fee. It is separate from quality, which controls rendering detail and fidelity.

&&

Markup edits, SVG and GIF output in the API

Image markup lets you mark up the exact region you want changed. The launch post says markup is coming to the API. The guide already lists markup-guided edits as supported for both models. It also lists SVG output and animated GIF output through the Image API.

SVG matters for icons, diagrams and UI assets that must scale without blur. GIF output removes a separate animation step for social and product teams.

How much does GPT-Image-2.6 cost?

Pricing is token-based and identical for Flare and Sunburst, per the model pages:

Text input: $5.00 per 1M tokens ($1.25 cached)

Image input: $8.00 per 1M tokens ($2.00 cached)

Image output: $30.00 per 1M tokens

How does GPT-Image-2.6 compare with Nano Banana 2.1 and FLUX 3 Image?

FeatureGPT-Image-2.6 Flare / SunburstGPT-Image-2.5 Flare / SunburstGoogle Nano Banana 2.1BFL FLUX 3 ImageReleasedNov 4, 2026Sep 8, 2026Oct 2026Oct 1, 2026ParametersNot disclosedNot disclosedNot disclosedNot disclosed (Klein: 5.6B)WeightsClosedClosedClosedClosed (Klein open, FLUX Kommunity License)Planning controlcomplexity: low / medium / highNot disclosedThinking: minimal / medium / highBounding boxes in promptMax reference imagesNot disclosedNot disclosed1410Max outputNot disclosedNot disclosed4K4K (about 16 MP)GIF outputYesNot disclosedNot disclosedNot disclosedSVG outputYesNot disclosedNot disclosedNot disclosedPricing$8 / $30 per 1M image in / out$8 / $30 per 1M image in / out$0.0336 per 1K image$0.048 per 1K imageSpeed claimFlare: 6 s minimum at low qualityFlare: up to 50% lower latency vs GPT-Image-2Not disclosedNot disclosed

Google and BFL publish per-image prices. Nano Banana 2.1 starts at $0.0336 per 1K image and reaches $0.113 at 4K. FLUX 3 Image starts at $0.048 per 1K image and reaches $0.607 at 4K. Its open-weight sibling, FLUX 3 Image Klein, runs on consumer GPUs down to an RTX 3090. OpenAI&#8217;s edge is native GIF and SVG output. Its gap is transparency on per-image cost and quality.

Key Takeaways

Flare returns images in as little as 6 seconds at low quality.

Sunburst targets detail and edit consistency at medium or high quality.

New complexity parameter (low, medium, high; default high) costs nothing extra.

Token prices match GPT-Image-2.5: $30 per 1M image output tokens.

Check out the launch post, the Flare model card, the Sunburst model card and the image generation guide. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post OpenAI Launches GPT-Image-2.6 Flare and Sunburst: Adds GIFs, SVG Export and 6-Second API Generation appeared first on MarkTechPost.