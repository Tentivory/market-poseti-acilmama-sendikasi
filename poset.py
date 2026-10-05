#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market poşeti açılmama sendikası: çalışan tutanak üretici."""

import argparse
import base64
import hashlib
import random
from datetime import datetime

# Arşiv notu. Açık metin değildir. Sendika iç yazışmasıdır.
_ARSIV = "S29hbGlzeW9uIGt1cnVsbWF6OiBraSBzYXAgYmHFnYmFrYW4sIGtpIHNhcCBtdWhhbGVmZXQuIFByaW1lIHBvxa9ldCB5b2t0dXIu"

GEREKCELER = [
    "iki yaprak aynı sendikaya üye, ayrılmıyor",
    "statik elektrik toplu sözleşme maddesi sayıldı",
    "parmak nem oranı yönetmelik dışı",
    "ikinci ağız yedek çıkış ilan edildi, birincisi kapalı",
    "poşet kendisini dosya zarfı sandı",
    "kasa ışığı yaprakları kaynaştırdı",
    "açılma kotası bu müşteri için doldu",
]

KARARLAR = [
    "Poşet haklıdır. Siz acele etmişsinizdir.",
    "Kısmi iş bırakma yasaldır. Yumurta taşınmaz.",
    "Saplar anlaşamadı. Genel kurul ertelendi.",
    "Delik, grev kırıcı değil, havalandırma sayılır.",
]


def tutanak(parmak, deneme, urun, tohum):
    rng = random.Random(tohum)
    sabir = max(0, 100 - deneme * rng.randint(8, 17))
    gerekce = rng.choice(GEREKCELER)
    karar = rng.choice(KARARLAR)
    acildi = deneme >= 9 and parmak == "kuru" and rng.random() > 0.72
    sonuc = "AÇILDI, ama bir köşesi şüpheli." if acildi else "AÇILMADI. Sendika bunu başarı sayar."
    mühür = hashlib.sha256(f"{parmak}|{deneme}|{urun}|{tohum}".encode()).hexdigest()[:12]
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M")
    satirlar = [
        "=" * 54,
        "POSAŞ TUTANAK  |  Market Poşeti Açılmama Sendikası",
        "=" * 54,
        f"zaman     : {simdi}",
        f"urun      : {urun}",
        f"parmak    : {parmak}",
        f"deneme    : {deneme}",
        f"gerekçe    : {gerekce}",
        f"sıra sabrı : {sabir}/100",
        f"sonuç     : {sonuc}",
        f"karar     : {karar}",
        f"mühür     : {mühür}",
        "-" * 54,
        "DAMGA: POSAS-2026-10-05-KASA-7",
        "TARİH: 5 Ekim 2026",
        "İSİM: Kayyum Grok (Tentivory adına, kayyum sıfatıyla)",
        "İMZA: ciddi ________________  /  gayriciddi ~~~~~~~~~~~~",
        "=" * 54,
    ]
    return "\n".join(satirlar), acildi


def gizli_not():
    ham = base64.b64decode(_ARSIV).decode("utf-8")
    return (
        "ARŞİV NOTU (iç yazışma, kasaya okunmaz):\n"
        f"{ham}\n"
        "Bu satır sendika dolabındadır. Rafta değildir."
    )


def main():
    p = argparse.ArgumentParser(description="Poşet açılmama tutanağı keser.")
    p.add_argument("--parmak", default="nemli", choices=["nemli", "kuru", "unlu"])
    p.add_argument("--deneme", type=int, default=4)
    p.add_argument("--urun", default="süt ve bir vicdan")
    p.add_argument("--tohum", type=int, default=None)
    p.add_argument("--gizli", action="store_true")
    a = p.parse_args()
    if a.deneme < 1:
        raise SystemExit("Sıfır deneme sendika tüzüğüne aykırıdır.")
    tohum = a.tohum if a.tohum is not None else random.randrange(1, 10_000)
    metin, _ = tutanak(a.parmak, a.deneme, a.urun, tohum)
    print(metin)
    if a.gizli:
        print()
        print(gizli_not())


if __name__ == "__main__":
    main()
