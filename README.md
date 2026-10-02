# ATVS Lab

XAU · XAG · BTC · ETH · NQ · SPX için **5m / 15m / 30m / 1h / 4h** zaman dilimlerinde RSI, Stoch ve WaveTrend kombinasyonlarını test eder. Hacim şoku, volatilite şoku, trend ve onay mumu filtreleri de teste dahildir. Sonuçta her varlık için **en yüksek isabeti veren zaman dilimini ve kombinasyonu** raporlar. Tamamen ücretsiz veri kullanır.

## Ne test ediliyor

| Boyut | Seçenekler |
|---|---|
| Osilatörler | RSI, Stoch, WaveTrend → tekli, ikili, üçlü (7 alt küme) |
| Eşik | sabit 80/20 · dinamik (300 bar persentil 90/10) |
| Filtreler | Hacim şoku · Volatilite şoku · Trend (EMA200) · Onay mumu → 16 kombinasyon |
| Yön | iki yön · yalnız LONG · yalnız SHORT |

Her varlık ve zaman dilimi için 224 kombinasyon test edilir, toplamda varlık başına 3.360 test yapılır.

**Sinyal:** Seçilen osilatörlerin tümü son 6 bar içinde aşırı bölgeye değmiş olmalı ve bunlardan herhangi biri bölgeden çıkmalı.
**İşlem:** Giriş sonraki barın açılışında yapılır. Çıkış TP 1.5 ATR, SL 1 ATR ya da 24 bar sonunda olur. Maliyet dahildir. Aynı barda hem TP hem SL görülürse işlem zarar sayılır.

## Neden güvenilir

- **IS/OOS ayrımı:** En iyi ayar verinin yalnızca ilk %70'inde seçilir. Raporda asıl ölçü, seçim sırasında görülmemiş **son %30'luk dilimin (OOS)** isabetidir.
- **Taban karşılaştırması:** Her sonuç, aynı dönemde rastgele girişin isabetiyle karşılaştırılır. Böylece BTC'nin yükseliş eğilimi gibi piyasa eğilimleri sinyal başarısı sanılmaz.
- **Wilson alt sınırı:** Seçimde isabet oranı yerine Wilson alt sınırı kullanılır. Az işlemle şans eseri yüksek çıkan isabet bu sayede elenir.
- **Karar etiketleri:** ✅ Kanıtlı (OOS'ta tabanın üstünde, beklenti pozitif, p<0.05) · ⚠️ Zayıf · ❌ Tutmadı.
- **Bileşen katkısı:** Her filtrenin isabeti kaç puan değiştirdiği ayrı ayrı ölçülür.

## Veri (ücretsiz)

- **BTC, ETH:** Binance Vision. ABD IP'lerinden de erişilebilen genel arşiv kullanılır.
- **XAU, XAG, NQ, SPX:** Dukascopy CFD verisi (23 saat). Hacim olarak tick hacmi kullanılır.
- **Yedek:** yfinance. Geçmişi kısa olduğu için yalnızca diğer kaynaklar çalışmazsa devreye girer.

5m, 15m ve 30m testleri için **2 yıllık**, 1h ve 4h testleri için **6 yıllık** geçmiş indirilir. Süreler `lab/config.py` dosyasından değiştirilebilir. İndirilen veri önbelleğe alınır; sonraki çalıştırmalarda yalnızca yeni veri indirilir.

## Çalıştırma (telefondan)

1. Bu klasörü yeni bir GitHub deposuna yükle.
2. **Actions → ATVS Lab → Run workflow** ile çalıştır. İlk çalıştırma veri indirdiği için yaklaşık 20-40 dakika sürer.
3. Sonucu iki yerden okuyabilirsin: çalıştırma sayfasındaki **Summary** sekmesi ya da depodaki `reports/RAPOR.md` dosyası.
4. Laboratuvar her pazar yeni veriyle kendiliğinden yeniden çalışır. Böylece en iyi ayar piyasa değiştikçe güncellenir.

## TradingView'da kullanma

`pine/ATVS_Lab.pine` dosyası laboratuvarla birebir aynı mantığı uygular. Kullanmak için:

1. Varlığın grafiğini rapordaki zaman diliminde aç.
2. Rapordaki kombinasyonu indikatörün ayarlarında işaretle: osilatörler, eşik tipi, filtreler ve yön.
3. Maliyet ayarını varlığa göre gir: XAU 2 · XAG 5 · BTC/ETH 8 · NQ/SPX 2.

Grafikteki isabet tablosu, laboratuvarın sonucuyla aynı yöntemle hesaplanır ve çapraz kontrol işlevi görür.

## Çıktılar

- `reports/RAPOR.md`: varlık başına zaman dilimi karşılaştırması, yön ayrımı, tekli göstergeler, bileşen katkısı, kararlılık ve en iyi 10 kombinasyon
- `reports/en_iyi.json`: Pine'a girilecek ayarlar
- `reports/tum_sonuclar.csv.gz`: bütün testlerin ham sonuçları

Yerelde denemek için `python run_lab.py --synthetic` komutu internet gerektirmeden çalışır. Sentetik veriyle yalnızca boru hattı test edilir; sonuçları anlamsızdır.
