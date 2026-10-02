# ATVS Lab v2 Raporu — 2026-10-02 18:48 UTC

**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).
**Seçim** ilk %70 veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %30 (OOS) verisine göre** verilir. ✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · ⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.
Giriş: sinyalden sonraki bar açılışı · zaman bariyeri 48 bar · aynı barda hedef+stop = stop. TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1h | SHORT | OSC · RSI+WaveTrend · sabit · hacim şoku | IZ_SUREN_2.5ATR | +15.572R (199) | **+19.637R** (122) | %99.2 | 2388.32 | 3.9 | 1.00R | <0.001 | ✅ Kanıtlı |
| **XAG** | 5m | LONG | OSC · RSI+WaveTrend · sabit · hacim şoku+volatilite şoku | TP1>BE_3R | +0.487R (62) | **-0.010R** (21) | %19.0 | 0.98 | 1.8 | 5.89R | 0.513 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | **+0.030R** (132) | %25.0 | 1.04 | 4.0 | 36.38R | 0.439 | ⚠️ Pozitif, anlamsız |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | **+0.329R** (61) | %34.4 | 1.48 | 1.9 | 11.52R | 0.090 | ⚠️ Pozitif, anlamsız |
| **NQ** | 4h | LONG | OSC · WaveTrend · dinamik · volatilite şoku | IZ_SUREN_2.5ATR | +1.373R (42) | **-0.186R** (17) | %35.3 | 0.72 | 0.5 | 9.52R | 0.712 | ❌ OOS'ta tutmadı |
| **SPX** | 30m | iki yön | OSC · Stoch+WaveTrend · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +1.100R (56) | **+0.214R** (25) | %24.0 | 1.26 | 4.9 | 7.10R | 0.364 | ⚠️ Pozitif, anlamsız |

## Portföy (IS'te seçilen stratejilerin birlikte çalışması)

Seçim kuralı (yalnızca IS): IS beklentisi > 0, t ≥ 1.5, varlık başına en fazla 3, aynı varlıkta aynı aile bir kez, toplam en fazla 15. OOS penceresi: **2024-01-07 → bugün** (her strateji yalnızca kendi OOS döneminde işlem yapar; 1h/4h stratejileri kısa geçmiş nedeniyle sonradan katılır). Stratejiler arası ortalama günlük korelasyon: **0.03** (0'a yakın = iyi çeşitlendirme).

| # | Varlık | ZD | Yön | Giriş | Çıkış | IS t | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|---|---|---|---|
| 1 | XAU | 1h | SHORT | META · gradient boosting · tüm adaylar · üst %35 | TP1>BE_3R | 242.61 | +2.750R (6644) | +2.948R (5133) | %98.7 |
| 2 | XAU | 1h | iki yön | SEZON · saat etkisi UTC 13↓ 14↓ 15↓ 16↓ 17↑ 18↑ 19↑ 20↑ 21↑ 22↑ | IZ_SUREN_2.5ATR | 83.28 | +4.967R (21516) | +8.835R (9484) | %50.3 |
| 3 | XAU | 1h | SHORT | LEADLAG · XAG ani hareketini takip | TP1>BE_3R | 57.81 | +2.551R (757) | +2.935R (536) | %98.3 |
| 4 | BTC | 4h | iki yön | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 4.71 | +0.300R (1724) | -0.012R (1014) | %25.7 |
| 5 | ETH | 4h | LONG | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_2R | 4.65 | +0.410R (141) | +0.100R (61) | %55.7 |
| 6 | BTC | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | 3.83 | +0.639R (306) | +0.030R (132) | %25.0 |
| 7 | NQ | 1h | LONG | MA · zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | 3.77 | +0.286R (1094) | +0.355R (495) | %31.7 |
| 8 | ETH | 1h | iki yön | VWAP · VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | 3.67 | +0.268R (1123) | +0.124R (546) | %29.3 |
| 9 | ETH | 1h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 3.61 | +0.115R (5337) | -0.052R (2248) | %26.5 |
| 10 | NQ | 1h | LONG | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | 3.49 | +0.306R (795) | +0.023R (344) | %26.2 |
| 11 | NQ | 4h | LONG | OSC · Stoch · sabit · EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | 3.30 | +0.361R (137) | -0.037R (44) | %47.7 |
| 12 | SPX | 4h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 3.28 | +0.270R (851) | +0.301R (302) | %29.5 |
| 13 | SPX | 4h | LONG | MA · EMA 20/50 kesişimi | TP1>BE_3R | 3.20 | +0.523R (118) | +0.185R (54) | %25.9 |
| 14 | SPX | 4h | LONG | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 3.03 | +0.422R (351) | +0.111R (147) | %27.2 |
| 15 | BTC | 1h | LONG | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 2.49 | +0.183R (1068) | -0.072R (476) | %27.7 |

### Portföy performansı — işlem başına sabit risk, günlük zarar limiti %3

| Risk/işlem | Dönem | İşlem/gün | İsabet | Beklenti | Toplam getiri | Yıllık | Maks. düşüş | En uzun düşüş (gün) | Pozitif gün | Pozitif ay |
|---|---|---|---|---|---|---|---|---|---|---|
| %0.25 | IS | 15.48 | %46.6 | +3.109R | %106011575270831944373124145543039954075344171241022093159748092939084935752577031959909837905679170879029047346439500240810166569134754627584.0 | %456019006917164662784.0 | %44.5 | 740 | %67.1 | %76.1 |
| %0.25 | **OOS** | 21.10 | %57.0 | +4.792R | %11161640697484908918564321966459927595599467909666004128675862914892257628875421320432866157973015204317888512.0 | %169565730913849148696975333742115133849600.0 | %9.9 | 26 | %97.3 | %100.0 |
| %0.5 | IS | 14.13 | %47.2 | +3.047R | %9791894934859869585009668012356512482340047221893774191033198728879031308530904029334541287339736483841994127045156357817167107286442797512969109696920278155855329989452401255790100284787111762713513652455247705829951713123869136939725023608832.0 | %51710666332942046725466924032983040.0 | %63.1 | 299 | %59.9 | %77.3 |
| %0.5 | **OOS** | 20.19 | %56.8 | +4.580R | %97267073445233749308034518323248251073567665553497412952140105935513256605585150833777727445100084746222515584615936600052788883158000439769763721702765252063156142358533918073048398667060346880.0 | %2275284339477176849684032963474708657342147333819870888907070696824242176.0 | %17.6 | 26 | %88.8 | %100.0 |
| %1 | IS | 11.28 | %48.4 | +3.001R | — | — | %96.2 | 1089 | %48.2 | %67.1 |
| %1 | **OOS** | 17.13 | %57.0 | +4.218R | %3911138876780264409613016917971026648860333510006047339188895050284738403789819459322155783528001282803770534342596842246620770646960045882021213679230127121132078348488721032525014720499226248591816091561330119784276676423228166718549691988322715453016795979062186131356645862865587897630720.0 | %1335652420083025135239435680457003149837267094400556996283882843499195833963066775141435264112493970549899264.0 | %20.6 | 28 | %68.8 | %100.0 |

### Monte Carlo — OOS günlük getirilerinden 2.000 adet 1 yıllık yol (5 günlük blok bootstrap)

| Risk/işlem | Medyan yıllık getiri | En kötü %5 senaryo | Yılı zararla kapama | Kasa %20 düşer | %30 düşer | %50 düşer | Medyan maks. düşüş | Medyan en uzun düşüş (gün) |
|---|---|---|---|---|---|---|---|---|
| %0.25 | %219952029978609363583201685511904165888000.0 | %2866403906076521184928567625021724295168.0 | %0.0 | %0.0 | %0.0 | %0.0 | %3.6 | 5 |
| %0.5 | %3606660133670083271690224108238334745358424856110235080947432605674897408.0 | %667929397324410297843769750766669679880958532586777980249218889023488.0 | %0.0 | %0.1 | %0.0 | %0.0 | %7.5 | 5 |
| %1 | %1131593396959039702947975857121886619904615693099801782880202233344025793807472228829243000600784082785271808.0 | %142249962663835138662911790656765186252493011688186104687092708487622094447951433361047727745565458432.0 | %0.0 | %4.2 | %0.1 | %0.0 | %13.5 | 5 |

> Okuma: OOS beklentisi eksiyse risk seviyesi ne olursa olsun kasa uzun vadede erir — sabit oranlı risk yalnızca erimeyi yavaşlatır. OOS pozitifse, kasanın %30 düşme olasılığı kabul edilebilir düzeyde olan en yüksek risk seviyesi seçilir.


## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 5m | 15m | 30m | 1h | 4h |
|---|---|---|---|---|---|
| **XAU** | ⚠ +0.056R (41) | ❌ -0.250R (22) | ⏳ +0.100R (5) | ✅ +19.637R (122) | ✅ +4.956R (285) |
| **XAG** | ❌ -0.010R (21) | ⚠ +0.030R (23) | ⏳ +0.044R (11) | ⚠ +0.002R (194) | ⏳ -0.122R (8) |
| **BTC** | ❌ -0.360R (85) | ❌ -0.205R (47) | ⚠ +0.075R (27) | ⚠ +0.001R (130) | ⚠ +0.030R (132) |
| **ETH** | ❌ -0.045R (88) | ❌ -0.175R (175) | ❌ -0.347R (18) | ⚠ +0.124R (546) | ⚠ +0.329R (61) |
| **NQ** | ❌ -0.225R (38) | ❌ -0.169R (135) | ❌ -0.804R (22) | ⚠ +0.112R (75) | ❌ -0.186R (17) |
| **SPX** | ❌ -0.139R (71) | ❌ -0.129R (27) | ⚠ +0.214R (25) | ⚠ +0.372R (312) | ⚠ +0.185R (54) |

## XAU

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 160,558 | 2024-10-02 → 2026-03-18 | 2026-03-18 → 2026-10-01 | 0.237R | çalıştı |
| 15m | 53,522 | 2024-10-02 → 2026-03-18 | 2026-03-18 → 2026-10-01 | 0.131R | çalıştı |
| 30m | 26,762 | 2024-10-02 → 2026-03-18 | 2026-03-18 → 2026-10-01 | 0.092R | çalıştı |
| 1h | 76,016 | 2016-10-02 → 2024-02-24 | 2024-02-24 → 2026-10-01 | 0.004R | çalıştı |
| 4h | 19,493 | 2016-10-02 → 2024-01-31 | 2024-01-31 → 2026-10-01 | 0.002R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **OSC** | 1h | SHORT | RSI+WaveTrend · sabit · hacim şoku | IZ_SUREN_2.5ATR | +15.572R (199) | +19.637R (122) | %99.2 | 2388.32 | <0.001 | ✅ Kanıtlı |
| **META** | 1h | SHORT | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +14.501R (6644) | +15.272R (5133) | %98.8 | 1865.84 | <0.001 | ✅ Kanıtlı |
| **PAIR** | 1h | LONG | XAG'e göre göreli değer dönüşü ±1.5σ | IZ_SUREN_2.5ATR | +8.824R (362) | +15.064R (170) | %76.5 | 66.58 | <0.001 | ✅ Kanıtlı |
| **RSI2** | 1h | SHORT | RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +5.761R (1260) | +14.634R (404) | %97.5 | 844.69 | <0.001 | ✅ Kanıtlı |
| **REJIM** | 1h | SHORT | yatayda dönüş · Stoch · filtresiz | IZ_SUREN_2.5ATR | +10.392R (757) | +13.991R (421) | %100.0 | — | <0.001 | ✅ Kanıtlı |
| **LEADLAG** | 1h | SHORT | XAG ani hareketini takip | IZ_SUREN_2.5ATR | +12.242R (757) | +13.277R (536) | %98.5 | 1185.92 | <0.001 | ✅ Kanıtlı |
| **VWAP** | 1h | SHORT | VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | +8.597R (610) | +12.538R (294) | %99.0 | 1843.42 | <0.001 | ✅ Kanıtlı |
| **SEZON** | 1h | SHORT | saat etkisi UTC 13↓ 14↓ 15↓ 16↓ 17↑ 18↑ 19↑ 20↑ 21↑ 22↑ | IZ_SUREN_2.5ATR | +6.560R (9056) | +12.317R (3792) | %70.6 | 43.43 | <0.001 | ✅ Kanıtlı |
| **MA** | 1h | SHORT | zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | +5.085R (1121) | +9.412R (414) | %82.4 | 58.29 | <0.001 | ✅ Kanıtlı |
| **DONCH** | 1h | SHORT | Donchian 20 · filtresiz | IZ_SUREN_2.5ATR | +4.663R (1283) | +7.113R (668) | %78.3 | 176.77 | <0.001 | ✅ Kanıtlı |
| **IMOM** | 30m | LONG | sabah getirisi → 15:30 NY yönü | %50@1R>BE_IZ | +0.208R (214) | -0.104R (70) | %41.4 | 0.81 | 0.746 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | LONG | New York açılış 30dk · hacim şoku | GENIS_%50@1R>BE_3R | +0.205R (99) | -0.113R (33) | %42.4 | 0.78 | 0.727 | ❌ OOS'ta tutmadı |
| **SQZ** | 15m | LONG | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | +0.081R (198) | -0.153R (79) | %41.8 | 0.75 | 0.873 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +18.340R | %100.0 | %94.0 | +6.321R | %41.1 | 167 |
| %50@1R>BE_IZ | +13.440R | %100.0 | %93.3 | +4.195R | %41.1 | 167 |
| SABIT_3R | +2.788R | %100.0 | %94.8 | +0.658R | %41.1 | 167 |
| TP1>BE_3R | +2.781R | %100.0 | %94.5 | +0.657R | %41.1 | 167 |
| GENIS_%50@1R>BE_3R | +1.903R | %100.0 | %96.8 | +0.254R | %41.3 | 167 |
| %50@1R>BE_3R | +1.878R | %100.0 | %96.1 | +0.247R | %41.1 | 167 |
| SABIT_2R | +1.840R | %100.0 | %94.8 | +0.247R | %41.1 | 167 |
| TP1>BE_2R | +1.835R | %100.0 | %94.5 | +0.247R | %41.1 | 167 |
| SABIT_1.5R | +1.401R | %100.0 | %96.1 | +0.042R | %41.1 | 167 |
| %50@1R>BE_2R | +1.398R | %100.0 | %96.1 | +0.041R | %41.1 | 167 |
| SABIT_1R | +0.920R | %100.0 | %96.1 | -0.164R | %41.1 | 167 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %100.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +18.177R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · RSI+WaveTrend · sabit · hacim şoku · IZ_SUREN_2.5ATR · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2016-11-02 → 2021-08-09 | 80 | %55.0 | +9.112R |
| 2021-08-16 → 2023-04-24 | 80 | %100.0 | +19.915R |
| 2023-05-01 → 2024-12-30 | 80 | %100.0 | +19.921R |
| 2025-01-06 → 2026-09-28 | 81 | %98.8 | +19.490R |

Maksimum düşüş: IS 9.49R · OOS 1.00R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +14.414R (10186) | +16.422R (7456) | %98.3 |
| 2 | OSC · RSI+WaveTrend · sabit · hacim şoku | IZ_SUREN_2.5ATR | +13.793R (224) | +19.637R (122) | %99.2 |
| 3 | OSC · RSI+Stoch+WaveTrend · sabit · hacim şoku | IZ_SUREN_2.5ATR | +13.728R (225) | +19.637R (122) | %99.2 |
| 4 | OSC · RSI+Stoch+WaveTrend · sabit · filtresiz | IZ_SUREN_2.5ATR | +12.843R (310) | +19.529R (159) | %99.4 |
| 5 | OSC · RSI+WaveTrend · sabit · filtresiz | IZ_SUREN_2.5ATR | +12.793R (311) | +19.529R (159) | %99.4 |
| 6 | META · gradient boosting · tüm adaylar · üst %35 | %50@1R>BE_IZ | +10.322R (10186) | +11.712R (7456) | %98.4 |
| 7 | OSC · RSI+Stoch+WaveTrend · sabit · hacim şoku+onay mumu | IZ_SUREN_2.5ATR | +10.988R (152) | +19.453R (57) | %98.2 |
| 8 | OSC · RSI+WaveTrend · sabit · hacim şoku+onay mumu | IZ_SUREN_2.5ATR | +10.988R (152) | +19.453R (57) | %98.2 |
| 9 | OSC · WaveTrend · sabit · hacim şoku | IZ_SUREN_2.5ATR | +10.469R (295) | +19.637R (122) | %99.2 |
| 10 | OSC · WaveTrend · dinamik · hacim şoku | IZ_SUREN_2.5ATR | +9.515R (328) | +19.653R (124) | %98.4 |
| 11 | OSC · RSI+Stoch · sabit · hacim şoku | IZ_SUREN_2.5ATR | +9.473R (339) | +12.316R (192) | %70.8 |
| 12 | OSC · RSI+Stoch · sabit · filtresiz | IZ_SUREN_2.5ATR | +8.933R (745) | +11.811R (453) | %64.7 |
| 13 | OSC · RSI+Stoch+WaveTrend · sabit · onay mumu | IZ_SUREN_2.5ATR | +9.311R (197) | +19.505R (63) | %98.4 |
| 14 | OSC · RSI+WaveTrend · sabit · onay mumu | IZ_SUREN_2.5ATR | +9.093R (199) | +19.505R (63) | %98.4 |
| 15 | OSC · WaveTrend · dinamik · hacim şoku | %50@1R>BE_IZ | +8.644R (328) | +17.743R (124) | %98.4 |

## XAG

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 127,071 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | 0.395R | çalıştı |
| 15m | 42,357 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | 0.223R | çalıştı |
| 30m | 21,179 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | 0.156R | çalıştı |
| 1h | 76,210 | 2016-10-02 → 2024-02-22 | 2024-02-22 → 2026-10-01 | 0.132R | çalıştı |
| 4h | 19,544 | 2016-10-02 → 2024-01-28 | 2024-01-28 → 2026-10-01 | 0.069R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **ORB** | 30m | LONG | New York açılış 30dk · hacim şoku | GENIS_%50@1R>BE_3R | +0.317R (47) | +0.044R (11) | %54.5 | 1.14 | 0.435 | ⏳ OOS yetersiz |
| **IMOM** | 30m | SHORT | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.074R (121) | +0.010R (50) | %56.0 | 1.03 | 0.468 | ⚠️ Pozitif, anlamsız |
| **OSC** | 5m | LONG | RSI+WaveTrend · sabit · hacim şoku+volatilite şoku | TP1>BE_3R | +0.487R (62) | -0.010R (21) | %19.0 | 0.98 | 0.513 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 4h | SHORT | XAU ani hareketini takip | GENIS_%50@1R>BE_3R | +0.010R (205) | -0.061R (142) | %50.0 | 0.88 | 0.748 | ❌ OOS'ta tutmadı |
| **SEZON** | 1h | LONG | saat etkisi UTC 14↓ 15↓ 17↑ 18↑ 20↑ 21↑ | GENIS_%50@1R>BE_3R | -0.040R (8324) | -0.068R (3804) | %44.1 | 0.87 | 1.000 | ❌ OOS'ta tutmadı |
| **RSI2** | 30m | SHORT | RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | +0.020R (601) | -0.083R (233) | %48.5 | 0.84 | 0.877 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | -0.105R (702) | -0.104R (245) | %46.5 | 0.82 | 0.919 | ❌ OOS'ta tutmadı |
| **REJIM** | 1h | iki yön | anahtar (ikisi) · Stoch · filtresiz | GENIS_%50@1R>BE_3R | -0.062R (1064) | -0.119R (393) | %45.8 | 0.78 | 0.984 | ❌ OOS'ta tutmadı |
| **PAIR** | 4h | iki yön | XAU'e göre göreli değer dönüşü ±1.5σ | GENIS_%50@1R>BE_3R | +0.044R (251) | -0.135R (122) | %46.7 | 0.76 | 0.912 | ❌ OOS'ta tutmadı |
| **VWAP** | 1h | iki yön | VWAP kırılımı · hacim şoku | GENIS_%50@1R>BE_3R | -0.105R (1034) | -0.149R (431) | %45.9 | 0.74 | 0.997 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | iki yön | Donchian 20 · hacim şoku | SABIT_1R | +0.102R (85) | -0.181R (16) | %43.8 | 0.69 | 0.761 | ❌ OOS'ta tutmadı |
| **META** | 4h | SHORT | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.099R (887) | -0.209R (380) | %22.4 | 0.73 | 0.988 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | EMA 50/200 kesişimi | TP1>BE_3R | +0.354R (94) | -0.246R (49) | %12.2 | 0.59 | 0.910 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (5m) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | -0.097R | %30.0 | %28.3 | -0.200R | %27.1 | 249 |
| TP1>BE_2R | -0.101R | %10.0 | %29.0 | -0.246R | %26.1 | 249 |
| TP1>BE_3R | -0.105R | %10.0 | %19.7 | -0.221R | %18.8 | 249 |
| %50@1R>BE_2R | -0.143R | %0.0 | %50.8 | -0.266R | %47.3 | 249 |
| %50@1R>BE_3R | -0.144R | %0.0 | %50.6 | -0.254R | %47.2 | 249 |
| SABIT_2R | -0.148R | %10.0 | %34.8 | -0.235R | %33.7 | 249 |
| %50@1R>BE_IZ | -0.164R | %0.0 | %50.9 | -0.233R | %47.2 | 249 |
| SABIT_1R | -0.179R | %0.0 | %50.0 | -0.287R | %47.5 | 249 |
| SABIT_1.5R | -0.191R | %5.0 | %40.0 | -0.254R | %39.5 | 249 |
| IZ_SUREN_2.5ATR | -0.209R | %20.0 | %27.6 | -0.211R | %26.1 | 249 |
| GENIS_%50@1R>BE_3R | -0.218R | %0.0 | %45.3 | -0.186R | %48.3 | 249 |

**Sağlamlık (5m):** IS'te en iyi 20 ayarın %0.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.218R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · RSI+WaveTrend · sabit · hacim şoku+volatilite şoku · TP1>BE_3R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-10-07 → 2025-01-27 | 20 | %35.0 | +0.423R |
| 2025-02-06 → 2025-05-28 | 21 | %42.9 | +0.685R |
| 2025-06-10 → 2025-09-30 | 21 | %33.3 | +0.350R |
| 2025-10-07 → 2026-10-01 | 21 | %19.0 | -0.010R |

Maksimum düşüş: IS 5.93R · OOS 5.89R

### İlk 15 ayar (5m, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · RSI+Stoch · sabit · hacim şoku+volatilite şoku | GENIS_%50@1R>BE_3R | +0.080R (109) | -0.129R (43) | %48.8 |
| 2 | OSC · RSI+Stoch+WaveTrend · sabit · hacim şoku+volatilite şoku | GENIS_%50@1R>BE_3R | +0.084R (102) | -0.048R (41) | %53.7 |
| 3 | OSC · RSI+Stoch+WaveTrend · sabit · volatilite şoku | GENIS_%50@1R>BE_3R | +0.018R (147) | -0.298R (82) | %42.7 |
| 4 | OSC · RSI+Stoch+WaveTrend · sabit · hacim şoku+volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.055R (100) | -0.048R (41) | %53.7 |
| 5 | OSC · RSI+WaveTrend · sabit · hacim şoku+volatilite şoku | GENIS_%50@1R>BE_3R | +0.051R (102) | -0.058R (41) | %53.7 |
| 6 | OSC · RSI+WaveTrend · sabit · hacim şoku+volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.051R (102) | -0.058R (41) | %53.7 |
| 7 | OSC · RSI+Stoch+WaveTrend · sabit · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.008R (146) | -0.317R (82) | %41.5 |
| 8 | OSC · RSI · sabit · hacim şoku+volatilite şoku | GENIS_%50@1R>BE_3R | +0.038R (110) | -0.204R (46) | %45.7 |
| 9 | OSC · RSI · sabit · hacim şoku+volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.038R (110) | -0.204R (46) | %45.7 |
| 10 | OSC · RSI · sabit · volatilite şoku | GENIS_%50@1R>BE_3R | -0.005R (167) | -0.345R (93) | %38.7 |
| 11 | OSC · RSI+Stoch · sabit · hacim şoku+volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.042R (105) | -0.129R (43) | %48.8 |
| 12 | OSC · RSI+Stoch · sabit · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | -0.001R (156) | -0.306R (88) | %40.9 |
| 13 | OSC · RSI+Stoch+WaveTrend · sabit · filtresiz | GENIS_%50@1R>BE_3R | -0.043R (238) | -0.299R (125) | %42.4 |
| 14 | OSC · RSI+Stoch · sabit · volatilite şoku | GENIS_%50@1R>BE_3R | -0.003R (158) | -0.289R (88) | %42.0 |
| 15 | OSC · RSI+WaveTrend · sabit · volatilite şoku | GENIS_%50@1R>BE_3R | -0.002R (150) | -0.309R (82) | %41.5 |

## BTC

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 210,240 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.580R | çalıştı |
| 15m | 70,080 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.297R | çalıştı |
| 30m | 35,041 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.200R | çalıştı |
| 1h | 79,879 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-02 | 0.102R | çalıştı |
| 4h | 19,986 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-02 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.293R (498) | +0.263R (219) | %28.3 | 1.38 | 0.068 | ⚠️ Pozitif, anlamsız |
| **OSC** | 30m | SHORT | Stoch · dinamik · volatilite şoku+EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.394R (51) | +0.075R (27) | %55.6 | 1.15 | 0.375 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.386R (853) | +0.036R (503) | %25.8 | 1.05 | 0.364 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | %25.0 | 1.04 | 0.439 | ⚠️ Pozitif, anlamsız |
| **VWAP** | 1h | iki yön | VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | +0.138R (1250) | +0.016R (503) | %28.2 | 1.02 | 0.435 | ⚠️ Pozitif, anlamsız |
| **FUNDING** | 4h | LONG | fonlama uç değeri ±1.5σ (kalabalığa karşı) | GENIS_%50@1R>BE_3R | +0.279R (91) | -0.004R (94) | %50.0 | 0.99 | 0.513 | ❌ OOS'ta tutmadı |
| **SEZON** | 1h | iki yön | saat etkisi UTC 14↑ 16↑ 17↑ 18↑ 19↑ | IZ_SUREN_2.5ATR | -0.008R (11660) | -0.077R (4983) | %26.5 | 0.90 | 0.996 | ❌ OOS'ta tutmadı |
| **PAIR** | 1h | iki yön | ETH'e göre göreli değer dönüşü ±1.5σ | GENIS_%50@1R>BE_3R | -0.097R (855) | -0.092R (383) | %50.9 | 0.83 | 0.951 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.383R (571) | -0.105R (256) | %25.4 | 0.86 | 0.807 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | LONG | yatayda dönüş · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.551R (130) | -0.201R (62) | %22.6 | 0.74 | 0.801 | ❌ OOS'ta tutmadı |
| **ORB** | 15m | SHORT | New York açılış 30dk · hacim şoku | GENIS_%50@1R>BE_3R | +0.129R (128) | -0.205R (47) | %46.8 | 0.66 | 0.897 | ❌ OOS'ta tutmadı |
| **IMOM** | 30m | SHORT | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.119R (177) | -0.216R (86) | %46.5 | 0.62 | 0.974 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 4h | LONG | ETH ani hareketini takip | GENIS_%50@1R>BE_3R | +0.294R (69) | -0.270R (33) | %36.4 | 0.59 | 0.915 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.497R (183) | -0.328R (64) | %18.8 | 0.59 | 0.952 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.077R | %25.0 | %47.0 | -0.077R | %45.7 | 210 |
| SABIT_1R | -0.090R | %25.0 | %48.7 | -0.169R | %44.5 | 210 |
| %50@1R>BE_IZ | -0.104R | %15.0 | %47.9 | -0.133R | %44.5 | 210 |
| %50@1R>BE_3R | -0.123R | %5.0 | %47.9 | -0.128R | %44.5 | 210 |
| %50@1R>BE_2R | -0.125R | %10.0 | %47.7 | -0.140R | %44.5 | 210 |
| SABIT_1.5R | -0.126R | %15.0 | %37.6 | -0.182R | %35.1 | 210 |
| TP1>BE_3R | -0.127R | %10.0 | %15.4 | -0.087R | %17.9 | 210 |
| IZ_SUREN_2.5ATR | -0.129R | %20.0 | %22.9 | -0.135R | %25.3 | 210 |
| TP1>BE_2R | -0.137R | %15.0 | %22.7 | -0.112R | %25.1 | 210 |
| SABIT_2R | -0.193R | %15.0 | %29.1 | -0.157R | %30.1 | 210 |
| SABIT_3R | -0.195R | %5.0 | %22.1 | -0.105R | %24.3 | 210 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %10.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.130R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · sıkışma sonrası · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-09-13 → 2019-11-04 | 109 | %43.1 | +0.917R |
| 2019-11-08 → 2022-02-15 | 110 | %27.3 | +0.195R |
| 2022-02-28 → 2024-06-30 | 109 | %33.9 | +0.799R |
| 2024-07-23 → 2026-09-08 | 110 | %24.5 | -0.083R |

Maksimum düşüş: IS 21.66R · OOS 36.38R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | %25.0 |
| 2 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.552R (369) | -0.028R (158) | %24.1 |
| 3 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.555R (266) | -0.152R (125) | %21.6 |
| 4 | DONCH · Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.610R (188) | -0.323R (96) | %16.7 |
| 5 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.300R (1724) | -0.012R (1014) | %25.7 |
| 6 | DONCH · Donchian 20 · filtresiz | IZ_SUREN_2.5ATR | +0.421R (494) | -0.038R (210) | %25.7 |
| 7 | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.598R (162) | -0.335R (74) | %14.9 |
| 8 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.344R (306) | -0.049R (132) | %15.9 |
| 9 | MA · EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.383R (571) | -0.105R (256) | %25.4 |
| 10 | DONCH · Donchian 55 · hacim şoku | %50@1R>BE_IZ | +0.368R (188) | -0.166R (96) | %45.8 |
| 11 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.346R (266) | -0.145R (125) | %14.4 |
| 12 | DONCH · Donchian 55 · sıkışma sonrası | %50@1R>BE_IZ | +0.388R (162) | -0.113R (74) | %48.6 |
| 13 | DONCH · Donchian 55 · hacim şoku | TP1>BE_3R | +0.382R (188) | -0.198R (96) | %13.5 |
| 14 | DONCH · Donchian 20 · sıkışma sonrası | %50@1R>BE_IZ | +0.286R (306) | +0.000R (132) | %54.5 |
| 15 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +0.382R (369) | -0.065R (160) | %26.9 |

## ETH

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 210,240 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.364R | çalıştı |
| 15m | 70,080 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.191R | çalıştı |
| 30m | 35,041 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | 0.130R | çalıştı |
| 1h | 79,879 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-02 | 0.077R | çalıştı |
| 4h | 19,986 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-02 | 0.037R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 4h | LONG | Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | +0.329R (61) | %34.4 | 1.48 | 0.090 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.296R (778) | +0.291R (483) | %29.4 | 1.43 | 0.007 | ⚠️ Pozitif, anlamsız |
| **VWAP** | 1h | iki yön | VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | +0.268R (1123) | +0.124R (546) | %29.3 | 1.18 | 0.104 | ⚠️ Pozitif, anlamsız |
| **PAIR** | 4h | LONG | BTC'e göre göreli değer dönüşü ±1.5σ | GENIS_%50@1R>BE_3R | +0.182R (107) | -0.020R (63) | %49.2 | 0.96 | 0.557 | ❌ OOS'ta tutmadı |
| **RSI2** | 1h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.194R (2033) | -0.043R (888) | %26.5 | 0.94 | 0.724 | ❌ OOS'ta tutmadı |
| **IMOM** | 30m | iki yön | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.062R (364) | -0.044R (156) | %52.6 | 0.91 | 0.690 | ❌ OOS'ta tutmadı |
| **SEZON** | 1h | iki yön | saat etkisi UTC 17↑ 18↑ 19↑ | IZ_SUREN_2.5ATR | +0.008R (6998) | -0.054R (2989) | %26.3 | 0.93 | 0.919 | ❌ OOS'ta tutmadı |
| **FUNDING** | 1h | iki yön | fonlama uç değeri ±2.0σ (kalabalığa karşı) | IZ_SUREN_2.5ATR | +0.357R (196) | -0.089R (112) | %27.7 | 0.88 | 0.685 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.234R (582) | -0.097R (294) | %23.1 | 0.87 | 0.789 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 1h | iki yön | BTC ani hareketini takip | GENIS_%50@1R>BE_3R | +0.098R (276) | -0.115R (128) | %47.7 | 0.79 | 0.882 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_IZ | +0.485R (64) | -0.207R (25) | %40.0 | 0.67 | 0.808 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | iki yön | New York açılış 30dk · hacim şoku | SABIT_2R | +0.144R (188) | -0.221R (85) | %30.6 | 0.72 | 0.930 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | %23.5 | 0.58 | 0.854 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | iki yön | yatayda dönüş · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.769R (94) | -0.417R (38) | %18.4 | 0.43 | 0.986 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.223R | %75.0 | %29.5 | -0.023R | %25.3 | 203 |
| SABIT_3R | +0.143R | %70.0 | %30.5 | -0.097R | %24.5 | 203 |
| GENIS_%50@1R>BE_3R | +0.042R | %70.0 | %51.2 | -0.032R | %47.8 | 203 |
| TP1>BE_3R | +0.039R | %45.0 | %19.1 | -0.076R | %16.7 | 203 |
| %50@1R>BE_IZ | +0.030R | %55.0 | %50.0 | -0.062R | %47.1 | 203 |
| SABIT_1.5R | +0.023R | %45.0 | %42.7 | -0.119R | %36.9 | 203 |
| SABIT_2R | +0.021R | %45.0 | %35.5 | -0.087R | %31.7 | 203 |
| %50@1R>BE_3R | -0.013R | %35.0 | %49.9 | -0.088R | %47.1 | 203 |
| TP1>BE_2R | -0.038R | %35.0 | %25.4 | -0.081R | %24.5 | 203 |
| %50@1R>BE_2R | -0.039R | %35.0 | %49.8 | -0.090R | %47.1 | 203 |
| SABIT_1R | -0.043R | %35.0 | %50.1 | -0.099R | %47.1 | 203 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %60.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.065R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · hacim şoku · SABIT_3R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-10-13 → 2020-04-06 | 50 | %48.0 | +0.883R |
| 2020-04-16 → 2022-07-14 | 51 | %45.1 | +0.766R |
| 2022-07-28 → 2024-07-19 | 50 | %34.0 | +0.302R |
| 2024-08-23 → 2026-09-21 | 51 | %31.4 | +0.208R |

Maksimum düşüş: IS 6.20R · OOS 11.52R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 55 · sıkışma sonrası | TP1>BE_3R | +0.514R (139) | +0.338R (70) | %27.1 |
| 2 | REJIM · yatayda dönüş · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.769R (94) | -0.417R (38) | %18.4 |
| 3 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.687R (123) | -0.381R (49) | %18.4 |
| 4 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.490R (284) | +0.677R (118) | %36.4 |
| 5 | DONCH · Donchian 55 · sıkışma sonrası | SABIT_3R | +0.514R (139) | +0.495R (70) | %38.6 |
| 6 | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.411R (284) | +0.345R (118) | %34.7 |
| 7 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.375R (291) | +0.118R (131) | %22.9 |
| 8 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.358R (284) | +0.218R (118) | %22.9 |
| 9 | OSC · Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | %23.5 |
| 10 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_IZ | +0.485R (64) | -0.207R (25) | %40.0 |
| 11 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_3R | +0.652R (64) | -0.250R (25) | %20.0 |
| 12 | DONCH · Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.360R (139) | +0.189R (70) | %58.6 |
| 13 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_3R | +0.431R (64) | -0.210R (25) | %40.0 |
| 14 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_3R | +0.286R (284) | +0.163R (118) | %57.6 |
| 15 | DONCH · Donchian 20 · hacim şoku | TP1>BE_2R | +0.298R (284) | +0.227R (118) | %34.7 |

## NQ

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 78,398 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | 0.320R | çalıştı |
| 15m | 26,133 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | 0.170R | çalıştı |
| 30m | 13,067 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | 0.114R | çalıştı |
| 1h | 70,259 | 2016-10-03 → 2024-02-08 | 2024-02-08 → 2026-10-02 | 0.082R | çalıştı |
| 4h | 18,446 | 2016-10-03 → 2024-01-09 | 2024-01-10 → 2026-10-02 | 0.041R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | %50@1R>BE_2R | +0.269R (68) | +0.136R (47) | %53.2 | 1.28 | 0.213 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | LONG | RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.134R (1921) | +0.134R (761) | %29.2 | 1.19 | 0.054 | ⚠️ Pozitif, anlamsız |
| **MA** | 1h | LONG | EMA 50/200 kesişimi | IZ_SUREN_2.5ATR | +0.731R (139) | +0.112R (75) | %30.7 | 1.18 | 0.317 | ⚠️ Pozitif, anlamsız |
| **LEADLAG** | 1h | iki yön | SPX ani hareketini takip | GENIS_%50@1R>BE_3R | -0.094R (160) | +0.095R (78) | %57.7 | 1.28 | 0.191 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 1h | LONG | Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.306R (795) | +0.023R (344) | %26.2 | 1.03 | 0.433 | ⚠️ Pozitif, anlamsız |
| **VWAP** | 1h | LONG | VWAP kırılımı · hacim şoku | GENIS_%50@1R>BE_3R | +0.094R (574) | +0.013R (355) | %51.8 | 1.03 | 0.414 | ⚠️ Pozitif, anlamsız |
| **IMOM** | 30m | iki yön | sabah getirisi → 15:30 NY yönü | IZ_SUREN_2.5ATR | +0.441R (159) | -0.084R (68) | %33.8 | 0.86 | 0.660 | ❌ OOS'ta tutmadı |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | SABIT_3R | +0.166R (934) | -0.129R (344) | %24.4 | 0.83 | 0.928 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | WaveTrend · dinamik · volatilite şoku | IZ_SUREN_2.5ATR | +1.373R (42) | -0.186R (17) | %35.3 | 0.72 | 0.712 | ❌ OOS'ta tutmadı |
| **PAIR** | 4h | LONG | SPX'e göre göreli değer dönüşü ±1.5σ | TP1>BE_3R | +0.435R (75) | -0.190R (40) | %25.0 | 0.68 | 0.820 | ❌ OOS'ta tutmadı |
| **ORB** | 15m | LONG | New York açılış 30dk · hacim şoku | SABIT_1.5R | +0.245R (81) | -0.491R (29) | %24.1 | 0.41 | 0.993 | ❌ OOS'ta tutmadı |
| **REJIM** | 30m | LONG | anahtar (ikisi) · WaveTrend · filtresiz | SABIT_1.5R | +0.391R (66) | -0.804R (22) | %13.6 | 0.16 | 1.000 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.683R | %100.0 | %31.3 | +0.447R | %30.5 | 139 |
| SABIT_3R | +0.222R | %85.0 | %32.6 | +0.150R | %31.4 | 139 |
| %50@1R>BE_IZ | +0.199R | %90.0 | %49.1 | +0.250R | %53.0 | 139 |
| GENIS_%50@1R>BE_3R | +0.120R | %80.0 | %54.0 | +0.088R | %54.7 | 139 |
| TP1>BE_3R | +0.093R | %75.0 | %22.6 | +0.090R | %22.1 | 139 |
| SABIT_1.5R | +0.034R | %50.0 | %43.4 | +0.027R | %43.5 | 139 |
| SABIT_2R | +0.022R | %60.0 | %36.4 | +0.039R | %37.2 | 139 |
| TP1>BE_2R | +0.018R | %50.0 | %30.0 | +0.046R | %29.6 | 139 |
| %50@1R>BE_3R | +0.017R | %50.0 | %49.4 | +0.050R | %53.0 | 139 |
| %50@1R>BE_2R | -0.020R | %30.0 | %49.5 | +0.028R | %53.0 | 139 |
| SABIT_1R | -0.040R | %35.0 | %50.3 | +0.011R | %53.0 | 139 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %80.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.460R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · WaveTrend · dinamik · volatilite şoku · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-03-22 → 2018-10-12 | 14 | %35.7 | +0.999R |
| 2018-10-25 → 2020-06-29 | 15 | %53.3 | +1.925R |
| 2020-08-12 → 2024-02-22 | 15 | %53.3 | +1.156R |
| 2024-02-29 → 2026-07-30 | 15 | %26.7 | -0.379R |

Maksimum düşüş: IS 5.04R · OOS 9.52R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +1.041R (61) | +0.996R (28) | %39.3 |
| 2 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.724R (82) | +1.310R (25) | %40.0 |
| 3 | OSC · WaveTrend · dinamik · volatilite şoku | IZ_SUREN_2.5ATR | +0.742R (75) | +0.819R (32) | %37.5 |
| 4 | OSC · Stoch · dinamik · EMA200 trend | IZ_SUREN_2.5ATR | +0.429R (225) | +0.253R (81) | %27.2 |
| 5 | OSC · Stoch · dinamik · EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.462R (184) | +0.633R (64) | %34.4 |
| 6 | OSC · Stoch · sabit · volatilite şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.643R (85) | +1.704R (34) | %32.4 |
| 7 | OSC · Stoch · sabit · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.608R (91) | +1.421R (38) | %28.9 |
| 8 | OSC · Stoch · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +0.384R (249) | +0.227R (109) | %21.1 |
| 9 | OSC · Stoch · dinamik · EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.263R (184) | +0.067R (64) | %46.9 |
| 10 | DONCH · Donchian 20 · EMA200 trend | SABIT_3R | +0.264R (365) | +0.067R (184) | %28.8 |
| 11 | OSC · Stoch · sabit · EMA200 trend | GENIS_%50@1R>BE_3R | +0.221R (249) | -0.033R (109) | %46.8 |
| 12 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | %50@1R>BE_IZ | +0.435R (61) | +0.451R (28) | %57.1 |
| 13 | OSC · Stoch · sabit · EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.213R (213) | +0.056R (89) | %49.4 |
| 14 | OSC · Stoch · dinamik · EMA200 trend | GENIS_%50@1R>BE_3R | +0.205R (225) | -0.016R (81) | %44.4 |
| 15 | OSC · Stoch · dinamik · EMA200 trend | SABIT_3R | +0.285R (225) | -0.002R (81) | %27.2 |

## SPX

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 5m | 127,584 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | 0.493R | çalıştı |
| 15m | 42,528 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | 0.261R | çalıştı |
| 30m | 21,264 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | 0.176R | çalıştı |
| 1h | 72,895 | 2016-10-03 → 2024-04-03 | 2024-04-03 → 2026-10-01 | 0.118R | çalıştı |
| 4h | 18,991 | 2016-10-03 → 2024-02-25 | 2024-02-25 → 2026-10-01 | 0.059R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **LEADLAG** | 1h | SHORT | NQ ani hareketini takip | TP1>BE_3R | +0.333R (107) | +1.376R (38) | %57.9 | 5.34 | <0.001 | ✅ Kanıtlı |
| **SQZ** | 4h | LONG | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | +0.212R (49) | +0.379R (23) | %60.9 | 1.91 | 0.083 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.270R (851) | +0.301R (302) | %29.5 | 1.43 | 0.022 | ⚠️ Pozitif, anlamsız |
| **OSC** | 30m | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +1.100R (56) | +0.214R (25) | %24.0 | 1.26 | 0.364 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | LONG | EMA 20/50 kesişimi | TP1>BE_3R | +0.523R (118) | +0.185R (54) | %25.9 | 1.32 | 0.211 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.422R (351) | +0.111R (147) | %27.2 | 1.16 | 0.300 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 20 · EMA200 trend | TP1>BE_3R | +0.182R (400) | -0.006R (193) | %19.7 | 0.99 | 0.523 | ❌ OOS'ta tutmadı |
| **PAIR** | 4h | iki yön | NQ'e göre göreli değer dönüşü ±2.0σ | IZ_SUREN_2.5ATR | +0.424R (151) | -0.097R (40) | %30.0 | 0.86 | 0.639 | ❌ OOS'ta tutmadı |
| **VWAP** | 1h | SHORT | sapma dönüşü ±2.5σ · yatay rejim | GENIS_%50@1R>BE_3R | +0.071R (131) | -0.153R (82) | %45.1 | 0.74 | 0.892 | ❌ OOS'ta tutmadı |
| **IMOM** | 30m | iki yön | sabah getirisi → 15:30 NY yönü | %50@1R>BE_IZ | -0.083R (255) | -0.159R (110) | %45.5 | 0.71 | 0.936 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | LONG | New York açılış 30dk · hacim şoku | SABIT_3R | +0.305R (97) | -0.264R (42) | %21.4 | 0.70 | 0.850 | ❌ OOS'ta tutmadı |
| **REJIM** | 30m | LONG | yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | SABIT_3R | +0.666R (43) | -0.390R (14) | %21.4 | 0.57 | 0.829 | ⏳ OOS yetersiz |

### Çıkış yöntemleri (30m) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.206R | %15.0 | %46.4 | -0.203R | %45.4 | 159 |
| TP1>BE_2R | -0.262R | %5.0 | %23.7 | -0.229R | %24.3 | 159 |
| TP1>BE_3R | -0.273R | %15.0 | %16.2 | -0.195R | %18.0 | 159 |
| SABIT_1.5R | -0.291R | %5.0 | %35.4 | -0.272R | %35.7 | 159 |
| %50@1R>BE_IZ | -0.301R | %5.0 | %44.2 | -0.247R | %45.3 | 159 |
| SABIT_1R | -0.306R | %10.5 | %42.8 | -0.257R | %45.3 | 159 |
| %50@1R>BE_2R | -0.312R | %5.3 | %42.4 | -0.243R | %45.3 | 159 |
| %50@1R>BE_3R | -0.317R | %5.0 | %42.2 | -0.226R | %45.3 | 159 |
| IZ_SUREN_2.5ATR | -0.349R | %5.0 | %21.2 | -0.217R | %24.0 | 159 |
| SABIT_2R | -0.361R | %5.0 | %27.7 | -0.272R | %30.1 | 159 |
| SABIT_3R | -0.417R | %0.0 | %20.2 | -0.252R | %23.8 | 159 |

**Sağlamlık (30m):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.413R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · Stoch+WaveTrend · sabit · EMA200 trend · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-10-11 → 2025-01-29 | 20 | %60.0 | +1.604R |
| 2025-02-03 → 2025-12-17 | 20 | %50.0 | +1.487R |
| 2025-12-18 → 2026-05-15 | 20 | %20.0 | -0.133R |
| 2026-05-26 → 2026-09-28 | 21 | %23.8 | +0.371R |

Maksimum düşüş: IS 11.23R · OOS 7.10R

### İlk 15 ayar (30m, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · Stoch+WaveTrend · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +1.100R (56) | +0.214R (25) | %24.0 |
| 2 | OSC · Stoch+WaveTrend · sabit · EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +1.076R (52) | -0.169R (22) | %22.7 |
| 3 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | SABIT_3R | +0.538R (66) | -0.629R (24) | %16.7 |
| 4 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | %50@1R>BE_IZ | +0.381R (66) | -0.495R (24) | %37.5 |
| 5 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | GENIS_%50@1R>BE_3R | +0.312R (66) | -0.239R (24) | %45.8 |
| 6 | OSC · RSI+Stoch+WaveTrend · dinamik · EMA200 trend+onay mumu | SABIT_3R | +0.550R (55) | -0.784R (30) | %10.0 |
| 7 | REJIM · anahtar (ikisi) · RSI+Stoch+WaveTrend · filtresiz | SABIT_3R | +0.421R (90) | -0.489R (40) | %20.0 |
| 8 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | %50@1R>BE_3R | +0.284R (66) | -0.507R (24) | %37.5 |
| 9 | REJIM · anahtar (ikisi) · RSI+Stoch+WaveTrend · filtresiz | GENIS_%50@1R>BE_3R | +0.256R (90) | -0.322R (40) | %42.5 |
| 10 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | TP1>BE_3R | +0.386R (66) | -0.609R (24) | %8.3 |
| 11 | REJIM · anahtar (ikisi) · RSI+Stoch+WaveTrend · filtresiz | IZ_SUREN_2.5ATR | +0.491R (90) | -0.566R (40) | %20.0 |
| 12 | OSC · RSI+WaveTrend · dinamik · EMA200 trend+onay mumu | SABIT_3R | +0.441R (73) | -0.596R (44) | %15.9 |
| 13 | OSC · RSI+Stoch+WaveTrend · dinamik · EMA200 trend | SABIT_3R | +0.494R (59) | -0.443R (31) | %19.4 |
| 14 | OSC · Stoch+WaveTrend · sabit · EMA200 trend+onay mumu | SABIT_3R | +0.526R (52) | -0.078R (22) | %27.3 |
| 15 | REJIM · yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | %50@1R>BE_2R | +0.223R (66) | -0.486R (24) | %37.5 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
