#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# ATVS — Oracle Cloud sunucu otomatik kurulum betiği (cloud-init)
# Oracle'da sunucu oluştururken "Show advanced options" → "Management" →
# "Paste cloud-init script" kutusuna bu dosyanın TAMAMINI yapıştır.
# Aşağıdaki 4 satırı (BURAYA yazan yerleri) doldur. 5. satır (GH_TOKEN) isteğe bağlı:
# doldurursan bot verisi Streamlit paneline gider (deploy/PANEL.md).
# ═══════════════════════════════════════════════════════════════════════════
REPO="https://github.com/evsayar33-oss/twindikator.git"   # repo private ise: https://KULLANICI:TOKEN@github.com/evsayar33-oss/twindikator.git
BITGET_KEY="BURAYA_API_KEY"
BITGET_SECRET="BURAYA_SECRET_KEY"
BITGET_PASS="BURAYA_PASSPHRASE"
GH_TOKEN=""          # isteğe bağlı: yalnızca bu repoya "Contents: Read and write" yetkili GitHub token'ı (panel için)

# ───────── aşağısına dokunma ─────────
U=ubuntu; H=/home/$U
cat > $H/atvs.env <<ENV
BITGET_KEY=$BITGET_KEY
BITGET_SECRET=$BITGET_SECRET
BITGET_PASS=$BITGET_PASS
BITGET_DEMO=1
ATVS_RISK=0.02
ATVS_LEVERAGE=50
SYM_XAU=XAU/USDT:USDT
SYM_ETH=ETH/USDT:USDT
SYM_NQ=QQQ/USDT:USDT
SYM_SPX=SPY/USDT:USDT
ATVS_ONLY=XAU
ATVS_DRY=0
GH_TOKEN=$GH_TOKEN
ENV
chmod 600 $H/atvs.env; chown $U:$U $H/atvs.env

# 1 GB RAM'li ücretsiz sunucu için 2 GB takas alanı
if [ ! -f /swapfile ]; then fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile && echo '/swapfile none swap sw 0 0' >> /etc/fstab; fi

apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv python3-pip git
timedatectl set-timezone UTC || true

sudo -u $U bash -c "cd $H && rm -rf atvs && git clone -q --single-branch --branch main $REPO atvs && cd atvs && python3 -m venv .venv && .venv/bin/pip install -q --upgrade pip && .venv/bin/pip install -q -r requirements.txt"

cat > $H/run.sh <<'RUN'
#!/bin/bash
cd /home/ubuntu/atvs || exit 1
git pull -q || true
set -a; . /home/ubuntu/atvs.env; set +a
.venv/bin/pip install -q -r requirements.txt >/dev/null 2>&1 || true
flock -n /tmp/atvs.lock .venv/bin/python trader.py "$@" >> /home/ubuntu/trader.log 2>&1
bash /home/ubuntu/atvs/deploy/veri_gonder.sh >> /home/ubuntu/trader.log 2>&1 || echo "(panel verisi gönderilemedi)" >> /home/ubuntu/trader.log
tail -c 200000 /home/ubuntu/trader.log > /home/ubuntu/trader.log.tmp && mv /home/ubuntu/trader.log.tmp /home/ubuntu/trader.log
RUN
chmod +x $H/run.sh; chown $U:$U $H/run.sh
( crontab -u $U -l 2>/dev/null | grep -v run.sh ; echo "10 * * * * /home/ubuntu/run.sh" ) | crontab -u $U -

# ilk kontrol: sonucu Oracle konsolundaki "Console history" ekranında görebilirsin
sudo -u $U bash -c "$H/run.sh --kontrol"
echo "════════ ATVS KURULUM SONUCU ════════" > /dev/console
tail -n 25 $H/trader.log > /dev/console
echo "═════════════════════════════════════" > /dev/console
