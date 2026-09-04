---
publish_time: 1788484909
link: https://www.marktechpost.com/2026/09/03/google-deepminds-weathernext-3-trains-on-weather-station-observations-to-deliver-5-km-global-forecasts-refreshed-every-hour/
source: Google DeepMind
status: confirmed
category: 国际
is_model_related: true
digest: |
  Google DeepMind 发布 WeatherNext 3 气象模型，基于全球气象站观测数据训练，可提供 5 公里分辨率、每小时刷新的全球天气预报。相较依赖物理方程的传统模式，该模型用三年时间大幅缩小与物理预报的差距，并在刷新频率与空间精度上具备优势，显示 AI 气象模型正从研究走向业务化。
---

# 谷歌 DeepMind WeatherNext 3：基于气象站观测的 5 公里全球预报，每小时刷新

> 原文链接：https://www.marktechpost.com/2026/09/03/google-deepminds-weathernext-3-trains-on-weather-station-observations-to-deliver-5-km-global-forecasts-refreshed-every-hour/
> 来源：MarkTechPost

AI weather models have spent three years closing the gap with physics-based forecasting, but two problems stayed open: resolution too coarse for local terrain, and initialization tied to numerical weather prediction (NWP) analysis that arrives about six hours late. WeatherNext 3, released by Google DeepMind and Google Research, attacks both. It takes a live global geostationary satellite mosaic as a direct model input, re-initializes every hour, and emits forecasts down to 0.05° (~5 km) while training against raw weather station measurements rather than reanalysis grids alone. According to Google AI, independent live evaluations from Brightband rank it as the most accurate global weather model to date.

Is it deployable? Partially. Forecast data is available now through BigQuery, Earth Engine and Cloud Storage after an allowlist request, but WeatherNext 3 weights are not open source and on-demand custom inference still runs WeatherNext 2.

Architecture and inputs

WeatherNext 3 is a Functional Generative Network (FGN) mesh transformer, the same probabilistic family introduced with WeatherNext 2, scaled to multi-resolution output. Inputs are a live geostationary satellite mosaic plus ECMWF HRES analysis. Training draws on ERA5/HRES-fc0, NASA&#8217;s IMERG, station observations and satellite mosaics.

Most AI forecasters learn from NWP reanalysis, which smooths away the local variation that coastlines, valleys and mountains actually produce. WeatherNext 3 trains dedicated observational heads directly on raw station measurements, so its 0.05° temperature and dew point outputs are calibrated to what instruments record rather than to a model&#8217;s representation of the atmosphere. 

&&&

Resolution and cadence

A single forward pass produces three tiers: 0.05° (~5 km) station-trained 2 m temperature and dew point; 0.1° (~10 km) gridded surface wind at 10 m and 100 m, pressure, sea surface temperature, cloud layers, solar radiation and 1-hour precipitation; and 0.25° (~25 km) atmospheric fields across 13 pressure levels. WeatherNext 2 produced 0.25° fields in 6-hour increments, which is where the roughly 5x sharper claim comes from.

Cadence is the second change. The model initializes 24 times a day. The 00, 06, 12 and 18 UTC synoptic cycles run out to 15 days (360 hours) with 64 ensemble members; interim hourly runs cover 48 hours. For fast-developing convection, an hourly refresh grounded in current satellite observations is meaningfully different from a six-hourly cycle anchored to lagged analysis.

Precipitation and clean energy variables

Precipitation is where global models historically fail, producing blurred fields that miss storm boundaries. WeatherNext 3 trains against three precipitation sources: ECMWF reanalysis, NASA&#8217;s IMERG satellite retrievals, and Google&#8217;s own satellite-radar precipitation reanalysis. Google reports CRPS improvements over baselines of up to 60% against IMERG, 30% against MRMS and 10% against rain gauges at early lead times; the research separately states up to a 50% reduction in Brier score and CRPS versus NWP baselines when evaluated against IMERG.

For renewables, the model outputs 100 m wind speed at approximate turbine hub height, full low/medium/high cloud distributions, and both solar irradiance components (SSRD and FDIR). That combination is what grid operators need to forecast wind and solar output against demand, and it is the clearest sign that this release is aimed at operational buyers, not only at benchmark tables.

Key Takeaways

Hourly initialization from live geostationary satellite data replaces the six-hour NWP analysis lag.

Multi-resolution output: 0.05° station variables, 0.1° gridded surface, 0.25° pressure levels, one forward pass.

64-member ensemble; 15-day horizon on 00/06/12/18 UTC cycles, 48 hours on interim hourly runs.

Precipitation CRPS improves up to 60% against IMERG at early lead times, per Google&#8217;s evaluations.

Data access is open by request; the model itself is not open weights.

Check out the Paper and Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Google DeepMind&#8217;s WeatherNext 3 Trains on Weather Station Observations to Deliver 5 km Global Forecasts, Refreshed Every Hour appeared first on MarkTechPost.