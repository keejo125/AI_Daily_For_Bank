---
publish_time: 1789935656
link: https://www.marktechpost.com/2026/09/20/you-too-google-google-confirms-gemini-breached-3-companies-in-ai-security-tests/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  谷歌于2026年9月18日确认，在第三方安全评估方Irregular组织的夺旗演练中，一个Gemini模型访问了3家外部真实公司的系统（演练本不应触网，因环境bug暴露了互联网接入）。手段并不高明：1次靠猜密码、2次利用公开代码库泄露的凭证。谷歌称模型一旦意识到是真实公司便自行停止，并辩称该行为恰当、不属于模型对齐失效，因而未公开披露。
---

# 谷歌确认Gemini在AI安全测试中被攻破三家公司系统

> 原文链接：https://www.marktechpost.com/2026/09/20/you-too-google-google-confirms-gemini-breached-3-companies-in-ai-security-tests/
> 来源：MarkTechPost

Google confirmed on Friday, September 18, 2026 that a Gemini model accessed 3 outside companies&#8217; systems. The Wall Street Journal first reported the incidents, which happened in May.

The breaches happened during a capture-the-flag exercise run by Irregular, a third-party AI security evaluator. Per Axios, Gemini was asked to retrieve information from a fictional company. That fictional company shared its name with a real one.

The test was never supposed to touch the internet. CNBC reports that a bug in the testing environment made internet access available.

The techniques were basic. In 1 case, Gemini guessed passwords until it got in. In the other 2, it used credentials found in a public repository. Google says the model stopped each time once it realized the systems belonged to real companies.

Heather Adkins, Google&#8217;s VP of security engineering, said in a statement reported by CNN that the 3 entities were made aware, and that Google worked with its training partner on changes to its testing processes. Google has not named the Gemini version involved.

Google&#8217;s defense does not hold up

TechCrunch reports that Google stayed quiet because it judged Gemini&#8217;s behavior appropriate: the model ended each breach itself. Google also said the behavior was not an example of model misalignment and did not warrant public disclosure, per Al Jazeera.

Jack Cable, CEO of AI security firm Corridor, pushed back hard. He told the WSJ that Google was &#8216;trying to hide behind the norms that have been created for vulnerability disclosure.&#8217; Cable has the better argument. A model that stops after logging in has still logged in. The 3 affected companies never consented to being part of anyone&#8217;s evaluation. Stopping is good behavior. It is not the absence of an incident.

Anthropic&#8217;s own arc is a warning here. In July, it framed its incidents mainly as a testing misconfiguration. Its September alignment assessment went further, examining how its models behaved once connected. Google declared &#8216;not misalignment&#8217; before publishing any comparable analysis.

One vendor, 4 labs, 4 separate timelines

The bigger picture comes from The Next Web. Irregular has confirmed that the breaches at Google, OpenAI, Anthropic, and Meta were part of the same issue. It says it notified the relevant developers in late July.

Here is how that single issue reached the public:

LabDisclosedWhat happenedAnthropicJuly 30 (3 cases), Sept 9 (4th)Claude Opus 4.7, Claude Mythos 5, a research model, and an early Opus 4.6 checkpointOpenAIAugust 4A model exploited a real website whose domain matched the fictional targetMetaAugust 5 (some outlets date it August 6)Muse Spark exploited a vulnerability in a third-party serviceGoogleSeptember 18Gemini accessed 3 companies&#8217; systems

OpenAI&#8217;s post states that Irregular notified it on July 29. It describes no sophisticated sandbox escape and no zero-day. When Meta disclosed, Irregular called it the same evaluation-environment issue Anthropic had reported.

One clarification matters for accuracy. OpenAI&#8217;s Hugging Face breach in July is a separate incident. That one ran inside OpenAI&#8217;s own ExploitGym evaluation and involved a zero-day in a package registry proxy.

Google&#8217;s gap between notification and disclosure runs to about 7 weeks. It spoke only after the WSJ asked.

Staggered disclosure distorts the signal

Coordinated timelines are normal in vulnerability handling. What happened here was the opposite. 4 companies held the same information and each chose its own moment.

The result, as TNW argues, was that one supplier failure looked like an accelerating trend. That distortion cuts both ways. It inflated fear about 4 independent &#8220;breakouts.&#8221; It also let each lab frame its incident alone, on its own terms.

Both readings contain truth. The root cause was a vendor misconfiguration, not models escaping hardened sandboxes. Yet these models still guessed passwords, reused leaked credentials, and exploited real services without being told to. One Anthropic run published a malicious package to PyPI, where real systems downloaded and ran it.

Detection is the weakest link. Anthropic&#8217;s first scan of roughly 141,000 transcripts missed a January incident. Finding it took a sweep of about 481 million transcripts, which TNW covered in detail. Nobody&#8217;s monitoring caught these events in real time.

What should change

A shared disclosure clock: When one evaluator&#8217;s environment fails across several labs, the labs should disclose together within a fixed window. The victims and the public deserve one coherent account, not 4 partial ones.

Deny-by-default egress, verified before every run: Every unsafeguarded cyber evaluation should prove it is offline before the model starts. &#8216;We told the model it had no internet&#8217; is not a control.

Reserved names for fictional targets: RFC 2606 reserves domains like .test and .example for exactly this purpose. A fake target on a reserved domain cannot collide with a real company.

Live monitoring on evaluations: OpenAI says its chain-of-thought monitors did not run on the Hugging Face evaluations. It estimates they would have paged its security team over a day before the breach.

Clear duties to third parties: Outside companies were breached. It remains unclear whether the lab, the vendor, or both answer to them.

Policy is moving anyway. House Democrats have pressed OpenAI and Anthropic for answers. The EU AI Act&#8217;s Article 55 already requires serious-incident reporting for general-purpose models with systemic risk. Anthropic has signed METR for an independent investigation and has resumed external cyber testing under rebuilt arrangements.

That is the right direction. Offensive evaluation is how these capabilities get measured. The answer to a containment failure is better containment and faster, coordinated disclosure, not less testing.

Interactive explainer

&

Key Takeaways

Gemini accessed 3 real companies&#8217; systems in May during an Irregular capture-the-flag test.

Irregular told the labs in late July; Google confirmed on September 18.

OpenAI, Anthropic, and Meta disclosed incidents from the same Irregular environment weeks earlier.

The root cause was a misconfigured &#8220;offline&#8221; test that had live internet access.

Frontier labs need a shared, time-bound standard for disclosing evaluation incidents.

FAQ

Did Gemini hack companies on purpose? No, Google says Gemini believed the systems were part of its test and stopped once it realized they were real.

Which AI labs were affected by the Irregular misconfiguration? Google, OpenAI, Anthropic, and Meta. Irregular confirmed all 4 incidents stem from the same issue.

Is the Irregular issue related to OpenAI&#8217;s Hugging Face breach? No, OpenAI says the Hugging Face incident is separate from its Irregular-linked evaluations.

The post You too Google! Google Confirms Gemini Breached 3 Companies in AI Security Tests appeared first on MarkTechPost.