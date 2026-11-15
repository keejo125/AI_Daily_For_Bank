---
publish_time: 1792679424
link: https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/
source: Google DeepMind
status: pending
category: 其他
is_model_related: false
digest: |
  Google DeepMind 与 Google Research 联合 WRI、IIASA 发布 Forest Typology (ForTy) 2020 全球地图，以 10 米分辨率将每片土地分为原生林、天然再生林、人工林、种植园林、树木作物与农林业、其他土地六类，并附带 2017-2025 年时间序列，显示森林如何逐年变化及被何种用地替代。
  
  该地图基于约 170 万标注样本训练，关键输入为 AlphaEarth Foundations 的卫星观测嵌入，能识别种植模式、生长周期等细微差异；在 9000 多个随机站点验证中，森林类型识别准确率 90%、林与非林 95%，优于其他全球森林图。ForTy 以概率分数输出，可适配 EU 毁林法规等场景，现已在 Google Earth Engine 开放，用于构建无毁林供应链与森林金融。
---

# 超越树木覆盖：绘制全球森林类型地图

> 原文链接：https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/
> 来源：Google DeepMind

October 22, 2026
Research
Beyond tree cover: mapping the world’s forest types
Maxim Neumann and Charlotte Stanton
Read the paper
Share
A new 10-meter resolution map shows which of the world's forests are natural, planted, or farmed, and how they are changing over time
Protecting the planet's forests starts with a simple question: what type of forest are we looking at? From space, an old-growth rainforest, a eucalyptus plantation, and an oil palm estate can look like the same patch of green. But they hold very different amounts of carbon and biodiversity. Telling them apart, and knowing how each patch has changed over time, shows us where conservation is working and where natural forests are being converted into plantations and farms.
Today, Google DeepMind and Google Research, together with the World Resources Institute (WRI) and the International Institute for Applied Systems Analysis (IIASA), are releasing
Forest Typology (ForTy) 2020
, a global map that categorizes every 10-by-10-meter patch of land on Earth into six distinct forest and land-use types, a key baseline for the EU's deforestation regulation. Alongside it, we're sharing an early time series that tracks how these forests changed each year from 2017 to 2025, including where natural forests were replaced by plantations or farms. For the first time, users can see at 10-meter detail worldwide, year by year, not just where forest was lost, but what replaced it: a timber plantation, a tree-crop farm or other land.
Why "tree cover" isn't enough
All forests store carbon and, together, forests are home to most of the world's land-based plant and animal species. But a forest’s ecological value also depends on its history: a primary forest that has never been cleared holds far more carbon and biodiversity than a single-species timber plantation that is harvested every decade or two.
Most global maps only indicate whether trees are present. That's a challenge for those trying to protect natural forests. The European Union's regulation on deforestation-free products (EUDR), for example, requires that products like coffee, cocoa or palm oil do not originate from land that was forest in 2020 and has since been converted to agriculture. Similarly, wood products, such as furniture, must also be free of forest degradation: they can't come from primary forests that have since been converted into plantation or planted forests, or from naturally regenerating forests that have since been converted into plantation forests. As a result, companies and regulators need to know not just where trees are, but what kind of forest they form (primary or regrowing, planted or plantation, forest or farm) and what replaces that forest after a harvest.
Last year, we jointly released
Natural Forests of the World 2020
, a 10-meter resolution global map that separated natural forests from all other tree cover. It offered a starting point to help companies and regulators implement the EU Deforestation Regulation, and to support commodity producers in meeting their commitments not to convert natural forest. That map answered one question for every patch of land: was it natural forest in 2020 or not? ForTy goes further, showing what kind of forest is there, from primary forest to timber plantation to tree crops, and, with the new time series, how that changes each year.
How ForTy classifies the world's forests
Specifically, ForTy sorts land into six categories based on definitions from the UN Food and Agriculture Organization (FAO):
Primary forest: native forest with no visible signs of human disturbance.
Naturally regenerating forest: forest that grew back on its own, for example after logging or fire.
Planted forest: forest that people planted or seeded, and managed over long cycles.
Plantation forest: fast-growing, intensively managed tree farms, often of one species.
Tree crops and agroforestry: farms that grow things other than wood, like oil palm, rubber, cocoa, or fruit.
Other land: everything else, from grassland and cropland to cities and water.
The Forest Typology map for 2020. Each color shows the most common forest or land type in each square kilometer. Explore it at 10-meter detail in our
Earth Engine app
.
Training our ForTy model was challenging because these categories depend in part on how land is used, not just how it looks. To teach our model the difference, we built a large-scale collection of forest-type examples with about 1.7 million labeled locations drawn from expert surveys, national and regional datasets, and targeted reviews of places where the model struggled. The model uses a custom architecture designed for the challenges of remote sensing data, and takes as a key input
AlphaEarth Foundations embeddings
, data-compact summaries of years of satellite observations for each 10-meter pixel, so it can spot subtle clues like planting patterns, growth cycles and harvest rhythms.
From above, the five forest and tree-crop classes can look alike. ForTy is able to identify the subtle differences in structure and seasonal patterns that set them apart, accurately categorizing them in a global map database. Imagery © Google Earth, Maxar Technologies, Airbus.
Putting the map to the test
A map is only useful if people can trust it. So, with IIASA and WRI, we validated ForTy against more than 9,000 randomly chosen sites around the world. At each site, two trained experts studied high-resolution imagery and years of satellite records to determine which type of land was really there. ForTy picked the right forest type 90% of the time, and told forest apart from non-forest land 95% of the time, outperforming other global forest maps.
Beyond accuracy, we know that global conservation is not one-size-fits-all. Instead of giving a yes-or-no label for a specific patch of land, ForTy provides a probability score for each class, enabling users to adapt the classification to regional contexts and application-specific precision trade-offs. For example, a company assessing deforestation risk under EUDR might set a strict threshold, only accepting pixels the model is highly certain about to avoid regulatory risks. Meanwhile, a researcher estimating total forest extent might use the full spectrum of probabilities to get a fuller picture of the potential landscape.
From a single snapshot in time to a story of change
A map of a single year is a useful baseline, but forests change. Our
new early-release time series
applies a similar approach to every year from 2017 to 2025. It shows not only where forests disappear and where they grow back, but also what kind of change happened: a natural forest turned into a timber plantation, for example, or abandoned land slowly regenerating into forest.
This differentiation matters because some of the most important changes are hard to see from space. When a natural forest is logged and replanted as a plantation, the land soon looks green again, so standard tree-cover maps might not pick up the change. ForTy's time series makes these hidden changes visible, both losses and gains.
Your browser does not support the video tag.
Your browser does not support the video tag.
What's next
The Forest Typology 2020 map [described in Scientific Data] and the new time series are now freely available on Google Earth Engine under an open license. We hope governments, companies, conservation groups and scientists will use them to help build deforestation-free supply chains, direct forest finance where it’s needed, and protect the natural forests that matter most. Over the coming months, we'll keep improving the time series with our partners and users, and we'd love to hear how you use it. ForTy is part of our
portfolio
of research on
AI for Nature
, which includes mapping the drivers of forest loss, forecasting deforestation risk, modelling global species distributions, and monitoring biodiversity in the field. FortTy is also the latest addition to
Google Earth AI
, Google’s collection of geospatial models and datasets designed to help tackle the planet's most critical environmental challenges.
Explore the Forest Typology 2020 map
Explore the time series
Download the data
Use in Earth Engine
Acknowledgements
This work was co-developed by Google DeepMind and Google Research, with the World Resources Institute and the International Institute for Applied Systems Analysis. We'd like to thank our co-authors Anton Raichuk, Peter Potapov, Myroslava Lesiv, Matthew Overlan, Mélanie Rey, Ravindran Rajakumar, Michelangelo Conserva, Radost Stanimirova, Michelle Sims, Sarah Carter, Elizabeth Goldman, Yuchang Jiang, Linus Scheibenreif, Ivelina Georgieva, Maria Shchepashchenko, Steffen Fritz, Nicholas Clinton, Dan Morris and Drew Purves, as well as the trusted testers who helped improved the map.
Related posts
AlphaEarth Foundations helps map our planet in unprecedented detail
July 2025
Science
Learn more