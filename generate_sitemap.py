#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO Sitemap.xml üretici + Kalite Kontrol"""

import os
import re
from datetime import datetime
from seo_district_data import DISTRICTS, SERVICES

SITE_URL = "https://tasyolnakliyat.com"
TODAY = datetime.now().strftime("%Y-%m-%d")

def generate_sitemap():
    urls = []

    # Ana Sayfa (en yüksek öncelik)
    urls.append(("", "1.0", "weekly"))

    # Kurumsal Sayfalar
    for page in ["hakkimizda.html", "iletisim.html", "fiyatlar.html", "referanslar.html", "blog.html", "sss.html"]:
        urls.append((page, "0.7", "monthly"))

    # Hizmet Silosu (yüksek öncelik)
    for s in SERVICES:
        priority = "0.9" if s.get("is_pillar") else "0.8"
        urls.append((f"hizmetler/{s['slug']}.html", priority, "weekly"))

    # Bölge Silosu
    for d in DISTRICTS:
        urls.append((f"bolgeler/{d['slug']}.html", "0.8", "monthly"))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for path, priority, freq in urls:
        url = f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"
        xml += f'  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{TODAY}</lastmod>\n'
        xml += f'    <changefreq>{freq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += f'  </url>\n'

    xml += '</urlset>\n'

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"sitemap.xml olusturuldu: {len(urls)} URL")
    return urls

def quality_control():
    errors = []
    warnings = []
    total_pages = 0

    # 1. Bölge sayfaları kontrol
    print("\n=== BÖLGE SAYFALARI KONTROL ===")
    for d in DISTRICTS:
        filepath = f"bolgeler/{d['slug']}.html"
        if not os.path.exists(filepath):
            errors.append(f"MISSING: {filepath}")
            continue

        total_pages += 1
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # URL temizliği
        slug = d['slug']
        if any(c in slug for c in ['ş','ç','ğ','ü','ö','ı','İ','Ş','Ç','Ğ','Ü','Ö']):
            errors.append(f"TURKISH CHAR in slug: {slug}")
        if ' ' in slug:
            errors.append(f"SPACE in slug: {slug}")

        # Meta tag kontrolü
        if f'<title>{d["name"]}' not in content:
            errors.append(f"TITLE missing district name: {filepath}")
        if '<meta name="description"' not in content:
            errors.append(f"META DESC missing: {filepath}")
        if f'<link rel="canonical"' not in content:
            errors.append(f"CANONICAL missing: {filepath}")

        # Schema.org kontrolü
        if '"@type": "MovingCompany"' not in content:
            errors.append(f"SCHEMA MovingCompany missing: {filepath}")
        if '"@type": "BreadcrumbList"' not in content:
            errors.append(f"SCHEMA BreadcrumbList missing: {filepath}")

        # Mikro-yerel içerik kontrolü (duplicate check)
        if d['micro_content'][:50] not in content:
            warnings.append(f"MICRO CONTENT missing: {filepath}")

        # İç link kontrolü
        if 'hizmetler/istanbul-evden-eve-nakliyat.html' not in content:
            warnings.append(f"PILLAR LINK missing: {filepath}")

        # H1 kontrolü
        if f'<h1>{d["name"]}' not in content:
            errors.append(f"H1 missing district name: {filepath}")

    print(f"  {total_pages} bolge sayfasi kontrol edildi")

    # 2. Hizmet sayfaları kontrol
    print("\n=== HİZMET SAYFALARI KONTROL ===")
    for s in SERVICES:
        filepath = f"hizmetler/{s['slug']}.html"
        if not os.path.exists(filepath):
            errors.append(f"MISSING: {filepath}")
            continue

        total_pages += 1
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<title>' not in content:
            errors.append(f"TITLE missing: {filepath}")
        if '"@type": "BreadcrumbList"' not in content:
            errors.append(f"SCHEMA BreadcrumbList missing: {filepath}")

    print(f"  {len(SERVICES)} hizmet sayfasi kontrol edildi")

    # 3. Ana sayfa link kontrolü
    print("\n=== ANA SAYFA LİNK KONTROL ===")
    if os.path.exists("index.html"):
        with open("index.html", 'r', encoding='utf-8') as f:
            idx = f.read()
        total_pages += 1

        if 'hizmetler/istanbul-evden-eve-nakliyat.html' not in idx:
            errors.append("index.html: hizmetler link not updated")
        if 'ilceler/' in idx:
            warnings.append("index.html: still has old ilceler/ links")

    # 4. Redirect kontrolü
    print("\n=== REDIRECT KONTROL ===")
    if os.path.exists("hizmetler.html"):
        with open("hizmetler.html", 'r', encoding='utf-8') as f:
            content = f.read()
        if 'http-equiv="refresh"' in content:
            print("  OK: hizmetler.html redirect active")
        else:
            warnings.append("hizmetler.html: redirect not set")

    # 5. Duplicate content check (basit)
    print("\n=== DUPLICATE CONTENT CHECK ===")
    micro_contents = set()
    for d in DISTRICTS:
        mc = d['micro_content'][:80]
        if mc in micro_contents:
            errors.append(f"DUPLICATE micro content: {d['name']}")
        micro_contents.add(mc)
    print(f"  {len(micro_contents)} benzersiz mikro-yerel icerik")

    # Rapor
    print("\n" + "="*50)
    print(f"TOPLAM: {total_pages} sayfa kontrol edildi")
    print(f"HATALAR: {len(errors)}")
    for e in errors:
        print(f"  [ERROR] {e}")
    print(f"UYARILAR: {len(warnings)}")
    for w in warnings:
        print(f"  [WARN] {w}")

    if not errors:
        print("\n✅ TÜM KALİTE KONTROLLERİ GEÇTİ!")
    else:
        print(f"\n❌ {len(errors)} HATA BULUNDU")

    return errors, warnings

if __name__ == "__main__":
    generate_sitemap()
    quality_control()
