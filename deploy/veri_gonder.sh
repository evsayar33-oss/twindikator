#!/bin/bash
# Canlı bot verisini (kasa geçmişi, işlemler, açık pozisyonlar, son log) GitHub'daki
# "canli-veri" dalına gönderir. Streamlit paneli bu daldan okur. Ana kod dalına dokunmaz.
# Yalnızca ~/atvs.env içinde GH_TOKEN tanımlıysa çalışır.
set -e
[ -z "$GH_TOKEN" ] && exit 0
SRC=/home/ubuntu/atvs; DST=/home/ubuntu/atvs_veri; BR=canli-veri
URL=$(cd $SRC && git remote get-url origin | sed -E 's#https://([^@]*@)?#https://x-access-token:'"$GH_TOKEN"'@#')
if [ ! -d $DST/.git ]; then
  rm -rf $DST && mkdir -p $DST && cd $DST && git init -q && git remote add origin "$URL"
  if git ls-remote --exit-code --heads origin $BR >/dev/null 2>&1; then
    git fetch -q origin $BR && git checkout -q -b $BR origin/$BR
  else
    git checkout -q --orphan $BR
  fi
  git config user.name "atvs-bot"; git config user.email "atvs-bot@users.noreply.github.com"
fi
cd $DST && git remote set-url origin "$URL"
git fetch -q origin $BR 2>/dev/null && git reset -q --soft origin/$BR 2>/dev/null || true
mkdir -p veri
for f in kasa_log.csv trader_trades.csv trader_state.json; do
  [ -f $SRC/state/$f ] && cp $SRC/state/$f veri/$f
done
tail -n 300 /home/ubuntu/trader.log > veri/son_log.txt 2>/dev/null || true
date -u +"%Y-%m-%dT%H:%M:%SZ" > veri/guncelleme.txt
git add -A veri
git diff --cached --quiet && exit 0
# Şişmeyi önle: veri dosyaları zaten tüm geçmişi içerdiği için eski commit'lere gerek yok.
# 150 commit birikince dal tek commit'e sıfırlanır (zorla gönderim) → depo boyutu hep küçük kalır.
N=$(git rev-list --count HEAD 2>/dev/null || echo 0)
if [ "$N" -ge 150 ]; then
  git checkout -q --orphan tmp_$BR && git commit -q -m "canlı veri (sıkıştırıldı) $(date -u +%F)" \
    && git branch -D $BR -q && git branch -m $BR && git push -q -f origin $BR && git gc -q --prune=now
else
  git commit -q -m "canlı veri $(date -u +%F' '%H:%M)" && git push -q origin $BR
fi
