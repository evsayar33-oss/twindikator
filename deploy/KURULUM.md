# ATVS Bitget Botu — Kurulum (telefondan, ücretsiz)

Bot Oracle Cloud'un süresiz ücretsiz sunucusunda (Avrupa) çalışır. Her saat başını 10 geçe kapanmış 4 saatlik mumları kontrol eder; sinyal varsa Bitget'te pozisyon açar ve yönetir. Senin bir şey yapmana gerek kalmaz. Açılan pozisyonları ve emirleri Bitget uygulamasından görebilirsin.

---

## Adım 0 — Dosyaları GitHub'a yükle
Zip'teki her şeyi `twindikator` reposuna üzerine yükle. Yeni dosyalar şunlar: `trader.py`, `deploy/` klasörü ve güncellenmiş `requirements.txt`.

> Repo **private** ise sunucunun repoyu indirebilmesi için bir token gerekir:
> 1. GitHub → Settings → Developer settings → Fine-grained tokens → Generate.
> 2. Yalnızca bu repoyu seç; Contents: **Read-only**.
> 3. Oluşan token'ı Adım 3'teki REPO satırında `https://KULLANICI:TOKEN@github.com/...` biçiminde kullan.

## Adım 1 — Bitget DEMO API anahtarı
1. Bitget uygulamasında **Demo Trading** moduna geç.
2. API Management → **HMAC** ile yeni anahtar oluştur:
   - Name: `atvs-bot`
   - Passphrase: kendin belirle ve **not al**
   - Bind IP: şimdilik boş
   - Yetkiler: **Read-write**, yalnızca **Futures order** ve **Futures Holdings**. Diğer her şey kapalı; **Withdraw ve Transfer kesinlikle kapalı**.
3. API Key, Secret Key ve Passphrase'i güvenli bir yere kaydet. Secret yalnızca bir kez gösterilir.
4. Demo hesabında USDT-M vadeli cüzdanında sahte USDT olduğundan emin ol.

## Adım 2 — Oracle Cloud hesabı
1. Tarayıcıdan **oracle.com/cloud/free** adresine git → "Start for free".
2. **Home Region** olarak **Germany Central (Frankfurt)** ya da **Netherlands Northwest (Amsterdam)** seç. Bölge sonradan değiştirilemez; ABD bölgesi seçme.
3. Kart doğrulaması istenir. "Always Free" kaynaklar için ücret alınmaz.

## Adım 3 — Sunucuyu oluştur (bot kendini kurar)
1. Oracle menüsü → **Compute → Instances → Create instance**.
2. **Image:** Canonical **Ubuntu** (22.04 veya 24.04).
3. **Shape:** "Always Free-eligible" etiketli bir seçenek:
   - **VM.Standard.E2.1.Micro**, ya da
   - **VM.Standard.A1.Flex** (1 OCPU / 6 GB). Bunda kapasite olmayabilir; olmazsa Micro'yu seç.
4. **Add SSH keys:** "Generate a key pair for me" → **Save private key** (telefona indir; zorunlu değil ama sakla).
5. Sayfanın altında **Show advanced options → Management** → **Paste cloud-init script**.
6. `deploy/oracle_kurulum.sh` dosyasının **tamamını** buraya yapıştır ve **en üstteki 4 satırı doldur**:
   - `REPO` — repo adresin
   - `BITGET_KEY`, `BITGET_SECRET`, `BITGET_PASS` — Adım 1'deki bilgiler
7. **Create**. Sunucu yaklaşık 2 dakikada açılır; kurulum arka planda 5–10 dakika daha sürer.

## Adım 4 — Kurulumun başarılı olduğunu kontrol et
1. Instance sayfası → **Console connection** (ya da "Console history") → **Capture console history**.
2. En altta şu blok görünmeli:
   ```
   ════════ ATVS KURULUM SONUCU ════════
   Bağlantı: DEMO hesap · ...
   Kasa: 10000.00 USDT
     F1_XAU_4h_DONCH: XAU/USDT:USDT bulundu ...
     F2_ETH_4h_DONCH: ETH/USDT:USDT bulundu ...
   Kontrol tamam.
   ```
3. Hata görürsen ekran görüntüsünü gönder.
   - "sembol bulunamadı" hatası: Bitget'teki altın kontratının adı farklı demektir. Birlikte düzeltiriz.
4. Instance sayfasındaki **Public IP address** değerini not al.

## Adım 5 — API anahtarını sunucu IP'sine bağla (güvenlik)
Bitget → API Management → anahtarı düzenle → **Bind IP address** alanına sunucunun Public IP'sini yaz. Böylece anahtar çalınsa bile başka bir yerden kullanılamaz.

## Adım 6 — Demo dönemi (2–4 hafta)
- Bot sinyal geldikçe Bitget **demo** hesabında işlem açar. Ayda yaklaşık 4–5 işlem beklenir.
- Bitget uygulamasında şunları gör:
  - açılan pozisyonlar
  - borsada bekleyen **stop (tetikli) emri** ve **hedef emri**
  - stopun +0.5R'de (XAU) girişe çekilmesi, ETH'de iz süren stopun ilerlemesi
- Her şey doğru çalışıyorsa gerçek hesaba geçiş için bana yaz.

## Gerçek hesaba geçiş (demo başarılı olunca)
1. Bitget **gerçek** hesapta yeni API anahtarı oluştur: aynı yetkiler, **Bind IP = sunucu IP'si**.
2. Oracle'da instance'ı **Terminate** et ve Adım 3'ü tekrarla. Bu sefer:
   - Gerçek anahtarları yaz.
   - Betikteki `BITGET_DEMO=1` satırını `BITGET_DEMO=0` yap.
   
   Yeni sunucunun IP'si değişirse Adım 5'i yeni IP ile tekrarla.
3. Risk %1 (`ATVS_RISK=0.01`). Kasa %10 düşerse `~/atvs.env` içinde 0.005 yap.

---

### Bot ne yapar, ne yapmaz
- ✅ Sinyalleri laboratuvarla **aynı kodla** hesaplar. Veri kaynağı da aynı: altın için Dukascopy, ETH için Binance.
- ✅ Giriş anında **stop emrini borsaya koyar**. Sunucu kapansa bile pozisyon korumasız kalmaz.
- ✅ TP1'de stopu girişe çeker, iz süren stopu günceller, 48 mumda pozisyonu kapatır.
- ✅ Pozisyon büyüklüğü = kasa × %1 ÷ stop mesafesi.
- ✅ Sinyal mumu kapandıktan sonra 2 saatten fazla geçmişse işleme girmez (fiyatın peşinden koşmaz).
- ❌ Para çekemez ve transfer yapamaz (API yetkisi yok).
- ⚠️ Araştırma iş akışı her ayın 1'inde finalistleri yeniden belirler. Bot bir sonraki çalıştırmada güncel listeyi kullanır. Listeden çıkan bir stratejinin açık pozisyonu kapanana kadar yönetilmeye devam eder.

> Yatırım tavsiyesi değildir. Gerçek parayla işlemden önce demo sonuçlarını mutlaka gözlemle.
