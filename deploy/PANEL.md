# ATVS Paneli — Streamlit (ücretsiz, telefondan)

Panel şunları gösterir:
- **Kasa büyümesi:** kasa ile net yatırılan para, aynı grafikte
- **Öz sermaye getirisi:** zaman ağırlıklı hesaplanır, yani para yatırıp çekmen getiriyi bozmaz
- **Kıyaslama:** altın, S&P 500, dolar endeksi, Dolar/TL, Bitcoin ve Nasdaq 100 ile karşılaştırma
- **Risk ölçüleri:** zirveden düşüş, aylık getiri ısı tablosu, Sharpe, Sortino, Calmar, korelasyon, beta ve alfa
- **İşlem kaydı:** her işlemin USDT ve R cinsinden sonucu, CSV olarak indirilebilir
- **Canlı karne:** canlı sonuçların backtest beklentisiyle uyumlu olup olmadığı
- **Backtest kıyası:** 2011'den bugüne strateji ile seçtiğin varlıklar, yıl yıl
- **Bot günlüğü** ve açık pozisyonlar

Veri yolu şöyle işler: sunucudaki bot her saat verisini GitHub'daki **`canli-veri`** dalına gönderir, panel de oradan okur. Panelde Bitget anahtarı **yoktur**; borsaya hiç bağlanmaz.

---

## 1) GitHub token'ı oluştur (botun veri gönderebilmesi için)
1. GitHub'da şu yola git: **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Ayarları şöyle yap:
   - **Repository access:** Only select repositories → `twindikator`
   - **Permissions → Contents:** **Read and write**. Diğer her şey "No access" kalsın.
   - **Expiration:** en uzun seçeneği seç ve süresi dolunca yenile.
3. Oluşan token'ı Oracle kurulum betiğindeki `GH_TOKEN=""` satırına, tırnakların arasına yapıştır.

> Sunucu zaten kuruluysa betiği yeniden çalıştırmak gerekmez. `~/atvs.env` dosyasına `GH_TOKEN=...` satırını eklemen yeterli. Bunu birlikte yapabiliriz.

## 2) Paneli Streamlit Community Cloud'a kur
1. Telefon tarayıcısından **share.streamlit.io** adresine git ve **GitHub ile giriş yap**.
2. **Create app → Deploy a public app from GitHub** seç ve şunları gir:
   - Repository: `evsayar33-oss/twindikator`
   - Branch: `main`
   - Main file path: **`panel/app.py`**
3. **Advanced settings → Secrets** bölümüne şunu yapıştır:
   ```toml
   REPO = "evsayar33-oss/twindikator"
   # Repo PRIVATE ise ayrıca bunu ekle (yalnızca "Contents: Read-only" yetkili ayrı bir token):
   # GH_TOKEN = "github_pat_..."
   ```
4. **Deploy**. Birkaç dakikada `https://....streamlit.app` adresinde açılır. Telefonda ana ekrana ekleyebilirsin.

### Gizlilik
- **Repo public ise** işlem kaydın ve kasa geçmişin GitHub'da herkese açık olur. Uygulama adresi de herkese açıktır.
- Gizli tutmak istersen:
  - Repoyu **private** yap.
  - Panele yalnızca okuma yetkili bir token ver.
  - Streamlit'te uygulamanın **Sharing** ayarını "Only specific people" yap.
- Her iki durumda da hiçbir yerde Bitget anahtarı bulunmaz.

## 3) Para yatırma ve çekme
- Bot, Bitget'teki transferleri otomatik kaydetmeye çalışır.
- Panelde "Net yatırılan" çizgisi yanlış görünürse repoya **`yatirimlar.csv`** dosyasını ekle. Dosya varsa otomatik kaydın yerine geçer:
  ```
  tarih,tutar
  2026-10-05,50
  2026-12-01,105
  2027-03-10,-20
  ```
  Eksi tutar para çekimi demektir. Her yatırım ya da çekimde dosyaya bir satır eklemen yeterli.

## Notlar
- Panel veriyi 10 dakikada bir yeniler. Hemen görmek için kenar menüdeki **Veriyi yenile** düğmesine bas.
- **Backtest kıyası** sekmesi canlı veri olmadan da çalışır. Bot kurulmadan önce de açılabilir.
- 90 günden kısa canlı dönemde yıllık oranlar (CAGR, Sharpe) anlamlı değildir.
