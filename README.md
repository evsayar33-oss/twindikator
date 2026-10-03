# ATVS Lab v3

XAU · XAG · BTC · ETH · NQ · SPX için araştırma, finalist seçimi ve canlı kâğıt işlem sistemi. Tamamı ücretsiz veriyle GitHub Actions'ta çalışır, sinyaller Telegram'a gelir.

```
Araştırma (ayda bir)  →  Finalist kapıları  →  Portföy + risk seçimi  →  Canlı kâğıt işlem (saatlik)  →  Telegram
```

## Kurulum (bir kez)

1. **Dosyaları yükle.** Bu klasördeki her şeyi mevcut `atvs_lab` reposuna üzerine yaz. Eski `lab/engine.py` artık kullanılmıyor; silebilirsin.
2. **Telegram secret'larını ekle.** Repo → Settings → Secrets and variables → Actions:
   - `TELEGRAM_TOKEN`: bot token'ı (`TELEGRAM_BOT_TOKEN` adı da kabul edilir)
   - `TELEGRAM_CHAT_ID`
3. **Araştırmayı başlat.** Actions → **ATVS Lab (araştırma + finalist)** → Run workflow. Veri baştan indirildiği için ilk çalıştırma 1–3 saat sürebilir. Bitince Telegram'a finalist özeti gelir.
4. **Canlı motor otomatik başlar.** **ATVS Canlı** iş akışı her saat :07'de çalışır. Finalist yoksa ya da yeni mum kapanmamışsa saniyeler içinde çıkar.

> **Actions dakikaları:** Repo **public** ise sınırsızdır. Private ise ayda 2.000 dakika ücretsizdir. Saatlik canlı iş akışı her çalıştırmada 1–3 dakika kullanır; private repoda bu sınırı aşabilir. Böyle bir durumda `atvs_live.yml` içindeki cron satırını `7 */4 * * *` yap (4 saatte bir).

## 1) Araştırma

- **Kapsam:** 1h ve 4h zaman dilimleri. Aileler: MA, DONCH, SQZ, RSI2, REJIM, OSC, META. Her biri 11 çıkış yöntemi ve 3 yön ayarıyla test edilir.
- **Veri:** BTC/ETH için Binance arşivi, diğerleri için Dukascopy. Geçmiş, kaynakta ne kadar varsa o kadar; en fazla 15 yıl.
- **Doğrulama:** Her seri yfinance günlük kapanışıyla ay ay karşılaştırılır. Ölçek hatası olan aylar düzeltilir, düzeltilemeyenler ve tek barlık sıçramalar atılır. İndirilemeyen parçalar 4 tura kadar yeniden denenir. Giriş ile çıkış arasında veri boşluğu olan işlemler sayılmaz.
- **Örneklem:** İlk %70 IS (seçim), son %30 OOS (doğrulama).

## 2) Finalist kapıları

Tüm testler **çakışmasız** yapılır: her strateji aynı anda tek pozisyon taşır. Bir adayın finalist olması için altı kapının hepsini geçmesi gerekir:

| Kapı | Koşul |
|---|---|
| K1 | OOS'ta en az 30 işlem, beklenti > 0, alfa > 0 (rastgele girişe göre fark). **Benjamini–Hochberg** düzeltmesi: çok sayıda aday birlikte test edildiği için şans eseri geçenler elenir. |
| K2 | Tüm dönemde en az 80 işlem ve beklenti > 0 |
| K3 | Maliyet 2 katına çıktığında da beklenti > 0 |
| K4 | Komşu parametre setlerinin en az %70'i pozitif (ATR, zaman bariyeri, stop/hedef, aileye özel uzunluk ve eşikler) |
| K5 | En az 5 işlem açılan yılların en az %60'ı pozitif |
| K6 | Veri şüphesi yok |

- **Seçim:** Kapıları geçenler tüm dönem t-istatistiğine göre sıralanır. Varlık başına en fazla 2, toplamda en fazla 8 finalist alınır.
- **Sahte veri kontrolü:** Saf rastgele yürüyüşte finalist çıkmadığı öz-testle doğrulanır.

## 3) Portföy

Portföy simülasyonu olay tabanlıdır; işlemler gerçek giriş ve çıkış zamanlarıyla işlenir. Kurallar:

- Aynı anda en fazla 4 pozisyon açık olabilir.
- Birlikte hareket eden varlıklar aynı kümede sayılır ve her kümede aynı anda en fazla 1 pozisyon açılır: **ABD endeksleri** (NQ+SPX), **metaller** (XAU+XAG), **kripto** (BTC+ETH).
- Günlük zarar limiti %3'tür.
- Risk, giriş anındaki kasanın yüzdesi olarak hesaplanır ve sonuç çıkış anında kasaya yazılır.

**Risk seçimi:** %0.25 ile %2 arasındaki risk seviyeleri Monte Carlo ile test edilir (3.000 farklı 1 yıllık yol). Maksimum düşüşün %95 olasılıkla **%15'i aşmadığı en yüksek risk** önerilir. Önerilen risk Telegram mesajlarına yazılır.

## 4) Canlı kâğıt işlem motoru (`live.py`)

- **Aynı kod:** Veri, doğrulama ve sinyal kodu araştırmayla birebir aynıdır. Öz-test, saatlik çalıştırmaların tekrar oynatılmasıyla canlı motorun ürettiği işlemlerin backtest işlemleriyle **aynı** olduğunu doğrular. Bu kontrol gecikmeli veri ve atlanan çalıştırmalar için de yapılır.
- **Giriş:** Sinyal mumundan sonraki mumun açılışı.
- **Eksik mum koruması:** Üst zaman diliminin mumu, içindeki tüm saatlik veriler gelmeden işlenmez.
- **Geriye dönük tarama:** Kaçırılan çalıştırmalar için son 12 mum taranır.

**Telegram mesajları:**

| Mesaj | Ne zaman gelir |
|---|---|
| 🟢/🔴 YENİ SİNYAL | Sinyal oluştuğunda; stop, TP1, hedef ve önerilen pozisyon büyüklüğüyle |
| 📍 GİRİŞ GERÇEKLEŞTİ | Giriş fiyatı belli olunca; kesin seviyelerle |
| 🔒 TP1 | TP1'e ulaşıldığında (gerekiyorsa kısmi kapama) — stopu girişe çek |
| ↗️ İz süren stop | Stop en az 0.5 ATR ilerlediğinde |
| ✅/❌ KAPANDI | İşlem kapandığında; sonuç R cinsinden, maliyet dahil |
| 📊 Haftalık karne | Pazartesi; canlı sonuçlar backtest beklentisiyle karşılaştırılır |
| ⚠️ Hata | Bir hata oluştuğunda (aynı hata tekrar tekrar gönderilmez) |

**Durum dosyaları:** `state/positions.json`, `state/ledger.csv` (tüm kâğıt işlemler), `state/last_run.txt`.

## 5) TradingView

`pine/ATVS_Finalist.pine` bir Pine **strategy** betiğidir: TradingView'ın strateji test aracında çapraz kontrol ve görsel takip için kullanılır.

- Ailesini, parametrelerini ve çıkış ayarlarını RAPOR.md'deki **Kurallar** bölümüne göre gir.
- **META** ailesi Pine'da yoktur; onu yalnızca Telegram motoru izler.
- TradingView'ın mum içi fiyat sırası varsayımı laboratuvarınkinden farklı olabilir; küçük sonuç farkları normaldir.

`pine/ATVS_Lab.pine` dosyası eski OSC göstergesidir.

## Çıktılar

**reports/**
- `RAPOR.md`: doğrulama, finalistler, portföy ve araştırma ayrıntıları
- `finalists.json`
- `finalist_islemler.csv.gz`
- `portfoy_kasa.csv`
- `secili_sonuclar.csv.gz`
- `calisma_logu.txt`

**state/** (canlı motor kullanır)
- `finalists.json`
- `positions.json`
- `ledger.csv`

## Öz-test

`python selftest.py` internetsiz çalışır ve şunları test eder:

- çıkış simülatörlerinin birebir aynı sonuç vermesi
- veri ayrıştırıcıları ve doğrulama
- boşluk koruması
- trend içeren sentetik veride uçtan uca çalışma
- **rastgele veride finalist çıkmaması**
- canlı motorla backtest'in eşitliği (normal, gecikmeli ve atlanan çalıştırmalar)
- META'nın canlı modda çalışması

Araştırma iş akışı önce bu testleri çalıştırır. Bir test başarısız olursa araştırma durur ve Telegram'a uyarı gönderilir.

> Kâğıt işlem / ileri test sistemidir; yatırım tavsiyesi değildir. Gerçek paraya geçmeden önce en az 1–3 ay canlı kâğıt işlem sonuçlarını backtest beklentisiyle karşılaştır (haftalık karne).
