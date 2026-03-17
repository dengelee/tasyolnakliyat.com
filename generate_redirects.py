#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""301 Redirect kurallarını .htaccess'e ekle ve eski /ilceler/ klasörünü sil"""

import os
import shutil
from seo_district_data import DISTRICTS

HTACCESS = ".htaccess"

def generate_redirects():
    rules = []
    rules.append("")
    rules.append("# --- 301 Redirects: /ilceler/ → /bolgeler/ (SEO Silo Migrasyonu) ---")
    rules.append("RewriteEngine On")
    rules.append("")
    rules.append("# Eski hizmetler.html → yeni pillar page")
    rules.append("RewriteRule ^hizmetler\\.html$ /hizmetler/istanbul-evden-eve-nakliyat.html [R=301,L]")
    rules.append("")
    rules.append("# Eski ilceler/ → yeni bolgeler/")

    for d in DISTRICTS:
        old_slug = d['old_file'].replace('ilceler/', '')  # e.g. kadikoy-nakliyat.html
        new_slug = d['slug'] + '.html'  # e.g. kadikoy-evden-eve-nakliyat.html
        old_pattern = old_slug.replace('.html', '\\.html')
        rules.append(f"RewriteRule ^ilceler/{old_pattern}$ /bolgeler/{new_slug} [R=301,L]")

    return "\n".join(rules) + "\n"

def update_htaccess():
    with open(HTACCESS, 'r', encoding='utf-8') as f:
        content = f.read()

    # Mevcut redirect kuralları varsa temizle
    if '301 Redirects: /ilceler/' in content:
        print("  Mevcut redirect kuralları tespit edildi, güncelleniyor...")
        # Eski bloğu kaldır
        import re
        content = re.sub(
            r'\n# --- 301 Redirects: /ilceler/.*?(?=\n# ---|\Z)',
            '',
            content,
            flags=re.DOTALL
        )

    redirect_block = generate_redirects()
    content = content.rstrip() + "\n" + redirect_block

    with open(HTACCESS, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  .htaccess güncellendi: {len(DISTRICTS)} redirect + 1 hizmetler redirect")

def remove_ilceler():
    if os.path.exists('ilceler'):
        count = len([f for f in os.listdir('ilceler') if f.endswith('.html')])
        shutil.rmtree('ilceler')
        print(f"  /ilceler/ klasörü silindi ({count} dosya)")
    else:
        print("  /ilceler/ klasörü zaten yok")

def main():
    print("=== 301 REDIRECT VE TEMİZLİK ===")
    update_htaccess()
    remove_ilceler()
    print("Tamamlandı.")

if __name__ == "__main__":
    main()
