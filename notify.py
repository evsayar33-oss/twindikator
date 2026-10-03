"""İş akışı hata/uyarı bildirimi: python notify.py "mesaj" """
import sys

import live

if __name__ == "__main__":
    live.tg(" ".join(sys.argv[1:]) or "ATVS bildirim")
