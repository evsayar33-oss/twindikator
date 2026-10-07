# v4 — 3. varlık (SPY / QQQ) araştırması

## Ne yapar?
1. **Mevcut finalistleri (XAU, ETH) Bitget'in gerçek maliyetiyle yeniden ölçer.**
   - Eski hesap CFD spread'ine göre yapılmıştı (altında 2 baz puan).
   - Bitget'te piyasa emriyle gidiş-dönüş yaklaşık 14 baz puan ödenir. Buna fonlama (funding) ücreti de eklenir.
2. **NQ (QQQ) ve SPX (SPY) için ABD seansına göre günlük stratejileri tarar.** Toplam 1.236 ayar test edilir. Aileler:
   - RSI(2), 2 günlük RSI toplamı, IBS, N-gün dibi, art arda düşüş, Bollinger
   - **3 MACD kombinasyonu**
   - Yavaş trend
3. **Laboratuvarın kapılarını uygular:** IS → OOS (çoklu test düzeltmesi) → maliyet ×2 → komşu ayarlar → yıllar.
4. **Geçen her adayı mevcut portföye ekleyip Monte Carlo ile test eder.**
   - Amaç: yıllık getiri (CAGR) en yüksek olsun.
   - Kısıt: %95 olasılıkla düşüş ≤ %15. Bu oran iş akışındaki "hedef" kutusundan değiştirilebilir.
   - Ek şart: iyileşme OOS döneminde de görülmeli.

## Nasıl çalıştırılır? (telefondan)
1. Zip'i repoya yükle.
2. GitHub → **Actions → "ATVS Endeks (3. varlık araştırması)" → Run workflow**.
3. Yaklaşık 20–60 dakika sürer; veri önbellekteyse daha kısa.
4. Sonuç `reports/ENDEKS_RAPOR.md` dosyasına yazılır. Panelin **Backtest kıyası** sekmesinde de görünür.

## Öneri çıkarsa
- Öneri `state/endeks_finalist.json` dosyasına yazılır.
- Bot bu stratejiyi **kendiliğinden işlemez**.
- Devreye almak için `aktif_botlar.txt` dosyasında `# SPX OTO` (ya da `# NQ OTO`) satırının başındaki `# ` işaretini sil.
- Kurulum sonundaki kontrol çıktısı SPY/QQQ için asgari kasayı da gösterir.

## Bitget hisse vadelileri hakkında
- Fiyat 7/24 oluşur, ama **ABD piyasası kapalıyken yeni pozisyon açılamaz**. Bu yüzden bot giriş ve çıkışları New York saatiyle 15:00–15:50 arasında yapar.
- Gece ve hafta sonu stop, fiyat boşluğuyla (gap) geçilebilir. Backtest bunu hesaba katar.
- ABD tatil günlerinde emir reddedilirse bot o günü atlar.
