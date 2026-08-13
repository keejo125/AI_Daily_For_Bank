---
publish_time: 1786543319
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google DeepMind 发布大规模多语言手语转文本模型 SL2T，将手语 AI 从实验室带入消费产品，服务于全球约 7000 万听障与重听用户及 200 多种手语。

  口语 AI 在过去数十年飞速发展，实现了自动翻译、听写与对话界面，但这一技术革命长期未能惠及手语社区。SL2T 在质量与通用性上取得突破，为听障与重听用户带来新的手语功能，标志着 AI 在无障碍领域迈出重要一步。
link: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
source: Google DeepMind
---

# 将手语 AI 交到用户手中

> 原文链接：https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
> 来源：Google DeepMind

August 12, 2026
Models
Putting sign language AI into usersâ hands
Google DeepMind Sign Language Team
Share
Introducing sign-language-to-text (SL2T), our breakthrough model powering new sign language features for Deaf and hard of hearing users.
AI's ability to process spoken languages has advanced rapidly over recent decades, enabling automatic translation, dictation, and conversational interfaces that feel effortless to hearing users. Yet this technological revolution has not reached the worldâs more than 200 sign languages â and the estimated 70 million Deaf and hard of hearing people who use them.
Today, weâre introducing a massively multilingual sign-language-to-text (SL2T) translation model that marks a breakthrough in quality and generality. With it, we are bringing sign language AI out of the lab and into consumer products for the first time: SL2T powers sign-to-text dictation in Gboard and Live Transcribe on
Pixel 11
, starting with American Sign Language (ASL) to English. More devices are coming soon, and additional languages will follow.
Similarly to how hearing users can use dictation to speak instead of typing, this feature enables Deaf users to sign to their phone anywhere theyâd normally type. You can sign to search the web, draft messages or documents, and ask Gemini to solve queries or execute tasks. In Live Transcribe, you can sign responses in conversations instead of having to type back and forth. According to our testers, signing in ASL is faster, more natural, and more delightful than typing in English.
Your browser does not support the video tag.
Your browser does not support the video tag.
Sign-to-text, powered by SL2T, enables users to sign to their phone anywhere they'd normally type.
Why sign languages matter
Sign languages are the primary languages of Deaf communities around the world and the cornerstone of Deaf cultural identity. There is great diversity among deaf people in terms of their level of proficiency in signing, speaking, reading, and writing, so it is important to support access in all modalities. Deaf people can benefit from sign language processing in the same way that hearing people benefit from spoken language processing, plus the technology opens new possibilities for bridging the communication gap between Deaf and hearing communities. Despite this opportunity for positive social impact, progress in sign language AI has been slow â both because building AI for sign languages presents complex challenges and because widespread misconceptions exist about how the languages themselves work.
Compared to spoken language transcription, sign language translation presents two core challenges. First, transcribing speech is a matter of performing a sequential mapping from sound to text in the same language, whereas sign languages are independent, natural languages with their own distinct grammars and lexicons. As a result, they require true machine translation rather than a sequential process of sign-to-word transformations. Second, the model must learn to âseeâ and understand physical movement. Sign languages convey meaning through simultaneous movements of the hands, arms, torso, head, and face. Accurately tracking these at high frame rates is a difficult and computationally demanding computer vision task.
Given this background, it is easy to understand why some early attempts at sign language technology, like sign language gloves, were fundamentally limited: sign languages aren't simply âEnglish on the hands.â They require complex visual perception of fine-grained whole-body movements and full-fledged language translation. SL2T is designed to deliver both.
Your browser does not support the video tag.
Your browser does not support the video tag.
SL2T sees sign language inputs as points on the signer's body and translates them into streaming text outputs. Example from the FLEURS-ASL benchmark.
How SL2T works
We built SL2T by combining a user-centric, culturally informed approach with massive data scaling. The model is trained on over 100,000 hours of data across more than 50 sign languages â with roughly a quarter of the data in ASL. Training jointly on diverse languages, dialects, and proficiency levels causes the model to learn shared underlying structures, outperforming single-language models in our experiments.
To protect user privacy, SL2T sees sign language as a sequence of pose landmark locations rather than a raw camera feed. An on-device model (
MediaPipe Holistic
) tracks the location of points on the signer, and only these geometric coordinates are sent to the server for translation, allowing the original video to be discarded immediately.
SL2T translates this coordinate sequence directly into text, bypassing intermediate annotations known as âglossesâ that are widely used in prior work on sign language translation. Glosses fail to capture rich, non-linear aspects of sign languages such as non-manual markers and spatial constructions. Translating directly from landmarks removes artificial vocabulary limits and allows translation quality to scale directly with data.
SL2T is the most capable sign language translation model to date according to key benchmarks like
FLEURS-ASL
(sd-test), which assesses ASL to English translation quality. SL2T achieves a remarkable zero-shot score of 70 BLEURT, which is significantly higher than any previously reported score. But optimizing academic benchmarks alone doesnât guarantee usability in real-world applications, so we worked hard on practical issues like minimizing streaming latency, preventing hallucination on non-signing inputs, ensuring fairness for the 10% of signers who are left-handed, and improving performance for one-handed signing, which is used while holding a smartphone in the other hand.
Original English
SL2T's ASL â English output
The Cook Islands do not have any cities but are composed of 15 different islands. The main ones are Rarotonga and Aitutaki.
The Cook Islands have no cities and consist of 15 islands. The two main islands are Rarotonga and Aitutaki.
The games kicked off at 10:00am with great weather and apart from mid morning drizzle which quickly cleared up, it was a perfect day for 7's rugby.
Games start at 10 a.m. in great weather. There is a light rain in the morning that clears up. It's a perfect day for 7v7 rugby.
In some federal countries, such as the United States and Canada, income tax is levied both at the federal level and at the local level, so the rates and brackets can vary from region to region.
In some federal countries, like the US and Canada, income tax is collected at both the federal and local levels. This means that the rates and brackets vary depending on your region.
This fully feathered, warm blooded bird of prey was believed to have walked upright on two legs with claws like the Velociraptor.
This creature is warm-blooded, eats grey, and is covered in feathers. It is believed that it walks on two legs like a velociraptor.
Maybe one day, your great grandchildren will be standing atop an alien world wondering about their ancient ancestors?
Maybe one day your great-grandchildren will stand on an alien world and reflect on their ancestors.
Examples from the FLEURS-ASL benchmark. SL2T accurately translates complex ASL into fluent English. Occasional errors remain in rare signs, rapid fingerspelling ("prey" â "grey"), passive constructions, classifier depictions (dropping "claws"), and tense without context ("kicked off" â "start").
Building with the community
We believe in building
with
the Deaf community, not just
for
it. Deaf perspectives have shaped every stage of this project â from conceptualization by Sam Sepah, a Deaf Googler, to data collection with Deaf partners, evaluation in Deaf user studies, and impact assessment of the technology with Deaf experts.
To guide responsible real-world deployment, we established the AI Sign Language Advisory Committee (AISLAC), bringing together many global Deaf organizations and subject-matter experts. Through this participatory governance model, the communities most impacted by our technology directly influence our development priorities. We co-authored a
joint impact report
for the release of SL2T 1.0 in Gboard and Live Transcribe, transparently detailing the technology's capabilities and current limitations â a collaborative approach we plan to continue for all major sign language releases.
Looking ahead
SL2T builds upon decades of foundational research across academia and industry, but bringing ASL input to usersâ phones is only the beginning. Googleâs mission is to organize the world's information and make it universally accessible and useful. Achieving universal accessibility means reaching full parity with spoken and written languages. Our team is working to expand this technology into additional sign languages, sign language generation, and frontier AI capabilities. We look forward to sharing our progress responsibly in order to make access through sign languages standard across the digital landscape.
You can experience SL2T in Gboard and Live Transcribe first on
Pixel 11
, with more devices coming soon â all at no additional cost.
Acknowledgements
This work was done jointly by teams from Google DeepMind and Android. The core team who developed the SL2T model is: Garrett Tanzer, Benoit Brard, Elizabeth Clark, Tim Dozat, Sebastian Ebert, Dan Garrette, Manfred Georg, Vicky Holgate, Shankar Kumar, Mohammad Saboorian, MiloÅ¡ StanojeviÄ, Megh Umekar, John Wieting, Andy Zhang, and Chris Dyer.
The Android team who integrated the model into Gboard and Live Transcribe is: Ausmus Chang, Sai Aditya Chitturu, Dayle Chiu, Anna Chou, Ajay Dudani, Angana Ghosh, Alex Huang, Joanne Kim, Ed Lee, Thomas Lin, James Su, Yanchao Su, and Sharlene Yuan.
We are grateful for additional support from Anelia Angelova, Abhishek Bapna, Sara Basson, Glenn Cameron, Scott Crowell, Trevor Cohn, Noah Fiedel, Zoubin Ghahramani, Raia Hadsell, Tom Hudson, Alexander Hauerslev Jensen, Kazuya Kawakami, Peike Li, Liam McCafferty, Caroline Pantofaru, Abhinav Parashar, Christopher Patnoe, Laura Rimell, Sagar Savla, Sam Sepah, Thad Starner, Dave Uthus, and Biao Zhang.
Many thanks also go to those who participated in early stage testing of our models.