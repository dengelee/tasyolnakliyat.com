#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ana sayfa ve kök HTML dosyalarındaki iç linkleri yeni silo mimarisine güncelle"""

import os
import re

ROOT_DIR = "."

# Ana sayfalardaki link güncellemeleri (kök düzey sayfalar)
ROOT_PAGES = [
    "index.html", "hakkimizda.html", "fiyatlar.html",
    "referanslar.html", "blog.html", "iletisim.html", "sss.html"
]

def update_root_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1) Nav "hizmetler.html" → "hizmetler/istanbul-evden-eve-nakliyat.html"
    content = content.replace('href="hizmetler.html"', 'href="hizmetler/istanbul-evden-eve-nakliyat.html"')

    # 2) İlçe linkleri: ilceler/XXX-nakliyat.html → bolgeler/XXX-evden-eve-nakliyat.html
    # Pattern: ilceler/SLUG-nakliyat.html
    content = re.sub(
        r'href="ilceler/([a-z]+)-nakliyat\.html"',
        r'href="bolgeler/\1-evden-eve-nakliyat.html"',
        content
    )

    # 3) Footer hizmet linkleri (hizmetler.html → hizmetler/istanbul-evden-eve-nakliyat.html)
    # These were already caught by #1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def update_old_hizmetler():
    """Eski hizmetler.html dosyasını redirect/update et"""
    filepath = "hizmetler.html"
    if not os.path.exists(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add canonical redirect meta to old hizmetler.html
    if '<meta http-equiv="refresh"' not in content:
        redirect_html = '''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url=hizmetler/istanbul-evden-eve-nakliyat.html">
  <link rel="canonical" href="https://tasyolnakliyat.com/hizmetler/istanbul-evden-eve-nakliyat.html">
  <title>Yönlendiriliyor...</title>
</head>
<body>
  <p>Yönlendiriliyorsunuz... <a href="hizmetler/istanbul-evden-eve-nakliyat.html">Buraya tıklayın</a></p>
</body>
</html>'''
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(redirect_html)
        return True
    return False

def main():
    updated = 0

    # Update root pages
    for page in ROOT_PAGES:
        filepath = os.path.join(ROOT_DIR, page)
        if os.path.exists(filepath):
            if update_root_page(filepath):
                print(f"  UPDATED: {filepath}")
                updated += 1
            else:
                print(f"  NO CHANGE: {filepath}")

    # Convert old hizmetler.html to redirect
    if update_old_hizmetler():
        print(f"  REDIRECT: hizmetler.html → hizmetler/istanbul-evden-eve-nakliyat.html")
        updated += 1

    print(f"\n{updated} dosya güncellendi.")

if __name__ == "__main__":
    main()
