# ATVS Lab v2.3

**v2.3 değişiklikleri**

- **Veri doğrulama.** Her seri yfinance günlük kapanışıyla ay ay karşılaştırılır. Ölçek hatası olan aylar düzeltilir. Düzeltilemeyen aylar ve tek barlık sahte sıçramalar atılır. Raporun başında bir doğrulama tablosu yer alır.
- **Temiz önbellek.** Önbellek sürümü `v3` oldu. Tüm veri baştan ve temiz indirilir. 1h tabanı için kaynakta ne kadar geçmiş varsa o kullanılır (en fazla 15 yıl).
- **Odak modu.** Yalnızca 1h ve 4h test edilir. Aileler: MA, DONCH, SQZ, RSI2, REJIM, OSC, META. Test sayısı azaldığı için istatistikler daha güçlüdür. Kapsamı değiştirmek için ortam değişkenlerini kullan: `ATVS_TFS=30m,1h,4h`, `ATVS_FAMILIES=` (boş bırakılırsa tüm aileler).
- **Alfa.** Her sonuç, aynı çıkışla rastgele girişin beklentisiyle karşılaştırılır. Böylece boğa piyasasında yalnızca LONG tarafta durarak "kazanan" stratejiler ayıklanır.
- **🚩 Veri şüphesi.** OOS beklentisi 1.5R'nin veya isabeti %85'in üstündeki sonuçlar işaretlenir. Bu sonuçlar seçime ve portföye alınmaz.

XAU · XAG · BTC · ETH · NQ · SPX varlıklarını **5m / 15m / 30m / 1h / 4h** zaman dilimlerinde test eder. Kapsam: **13 strateji ailesi** (yaklaşık 280 giriş) × **11 çıkış yöntemi** × 3 yön (iki yön / LONG / SHORT). Sonuçta her varlık için **OOS'ta en yüksek beklentiyi (R) veren** ayarı raporlar. Tamamen ücretsiz veri kullanır.

## Strateji aileleri

| Aile | İçerik |
|---|---|
| OSC | RSI / Stoch / WaveTrend dönüşü: 7 alt küme × sabit veya dinamik eşik × 16 filtre (hacim şoku, volatilite şoku, EMA200, onay mumu) |
| REJIM | Rejim anahtarı: yatay piyasada dönüş, trendde geri çekilme ya da ikisinin birleşimi (verimlilik oranı persentili) |
| RSI2 | Connors tipi RSI(2) aşırılığı, trend filtreli ya da filtresiz |
| DONCH | Donchian 20/55 kırılımı: filtresiz, hacim şoku, trend ya da sıkışma sonrası |
| MA | EMA 9/21, 20/50, 50/200 kesişimleri ve zaman serisi momentumu |
| SQZ | Bollinger–Keltner sıkışmasının çözülmesi |
| VWAP | Seans VWAP'ından sapma sonrası dönüş ve VWAP kırılımı (≤1h) |
| ORB | New York 09:30 ve Londra 08:00 açılış aralığı kırılımı (≤30m) |
| IMOM | Gün içi momentum: sabah getirisinin yönünde 15:30 NY işlemi (≤30m) |
| SEZON | Saat etkisi. Yalnızca IS döneminde öğrenilir |
| PAIR | Eş varlığa göre göreli değer dönüşü (XAU/XAG, BTC/ETH, NQ/SPX) |
| LEADLAG | Eş varlıktaki ani hareketi takip |
| FUNDING | BTC/ETH fonlama oranı uç değerleri (kalabalığa karşı işlem) |
| META | Gradient boosting: bütün ailelerin adaylarından hangisinin çalışacağını öğrenir. IS sonuçları katlama dışı tahminden gelir |

## Çıkış yöntemleri

1R = ilk stop mesafesi.

| Ad | Kural |
|---|---|
| SABIT_1R / 1.5R / 2R / 3R | Stop 1 ATR, sabit hedef |
| TP1>BE_2R / 3R | 1R'de stop girişe çekilir, hedef 2R veya 3R |
| %50@1R>BE_2R / 3R | 1R'de pozisyonun yarısı kapanır, stop girişe çekilir, kalan 2R veya 3R'ye gider |
| %50@1R>BE_IZ | 1R'de yarısı kapanır, stop girişe çekilir, kalan 2 ATR iz süren stop ile yönetilir |
| GENIS_%50@1R>BE_3R | Aynı mantık, ilk stop 1.5 ATR |
| IZ_SUREN_2.5ATR | Hedef yok, 2.5 ATR iz süren stop |

Tüm yöntemler için ortak kurallar:
- Zaman bariyeri 48 bar.
- Aynı barda hem hedef hem stop görülürse stop sayılır (muhafazakâr).
- Stopu girişe çekme kuralı bir sonraki bardan itibaren geçerli olur.
- Maliyet dahildir.

## Neden güvenilir

- **IS/OOS ayrımı:** Seçim verinin ilk %70'inde, beklentinin %95 alt sınırına göre yapılır. Karar, seçimde hiç görülmemiş son %30'luk dilimde verilir.
- **✅ Kanıtlı koşulları:** OOS'ta pozitif beklenti, en az 30 işlem ve **Bonferroni düzeltmeli** p < 0.05/k. Burada k, o tablodaki test sayısıdır.
- **Sahte veri testi:** Rastgele sentetik veride 6 varlığın hiçbirinde ✅ çıkmadı. Yani sistem şans eseri kazananları eliyor.
- **Sağlamlık satırı:** IS'te en iyi 20 ayarın kaçının OOS'ta pozitif kaldığını gösterir.
- **Ek kontroller:** Kararlılık blokları ve maksimum düşüş (R) raporlanır.

## Çalıştırma

1. Repoya bu dosyaları yükle. Eski `lab/engine.py` artık kullanılmıyor; silebilirsin.
2. **Actions → ATVS Lab → Run workflow** ile başlat.
3. Sonucu iki yerden okuyabilirsin: çalıştırma sayfasındaki **Summary** sekmesi ya da depodaki `reports/RAPOR.md`.

Veri önbellekte duruyor; sonraki çalıştırmalar yalnızca yeni veriyi indirir. Geçmiş süresi `lab/config.py` içindeki `YEARS_INTRADAY` (varsayılan 2) ve `YEARS_HOURLY` (varsayılan 6) ile ayarlanır.

## Portföy ve iflas riski (v2.2)

Laboratuvar, IS döneminde en sağlam görünen stratejileri tek bir portföyde birleştirir. Seçim kuralları:

- IS t-istatistiği en az 1.5 olmalı.
- Varlık başına en fazla 3 strateji alınır; aynı varlıkta her aileden yalnızca bir tane.
- Toplamda en fazla 15 strateji.

Portföy, her işlemde kasanın %0.25, %0.5 ve %1'i riske atılarak ayrı ayrı simüle edilir. Günlük zarar limiti %3'tür: bu limite ulaşılınca o gün yeni işlem açılmaz. Her strateji yalnızca kendi OOS döneminde işlem yapar.

Rapor şunları gösterir:

- günde ortalama işlem sayısı
- isabet oranı
- toplam ve yıllık getiri
- maksimum düşüş ve en uzun düşüş süresi
- pozitif gün ve pozitif ay oranı

Monte Carlo analizi, 2.000 farklı 1 yıllık senaryo üretir ve her risk seviyesi için şu olasılıkları hesaplar:

- yılı zararla kapama
- kasanın %20, %30 veya %50 düşmesi

Bu analiz için 1h tabanının geçmişi 10 yıla uzatıldı. Önbellekteki eski veri otomatik olarak tamamlanır.

## TradingView

`pine/ATVS_Lab.pine` şimdilik yalnızca OSC ailesini kapsar. Diğer ailelerden kazanan çıkarsa, o stratejinin Pine sürümü laboratuvarla birebir aynı mantıkla ayrıca yazılacak.

## Çıktılar

- `reports/RAPOR.md`: özet, varlık × zaman dilimi ısı tablosu, aile sıralaması, çıkış yöntemi karşılaştırması, sağlamlık, kararlılık ve ilk 15 ayar
- `reports/en_iyi.json`: varlık başına seçilen ayar
- `reports/portfoy_islemler.csv.gz`, `reports/portfoy_kasa_oos.csv`: portföy işlemleri ve OOS kasa eğrisi
- `reports/secili_sonuclar.csv.gz`: her varlık × zaman dilimi için IS'te ilk 150 sonuç ve her ailenin en iyisi
