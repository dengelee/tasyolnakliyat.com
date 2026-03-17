#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AŞAMA 3-4: SEO Silo Mimarisi Tamamlama
1) Bölge sayfalarında title formatını güncelle
2) GTM placeholder'ı bolgeler + hizmetler sayfalarına ekle
3) Ana sayfaya "İstanbul Hizmet Bölgelerimiz" bloğu ekle
4) Kök sayfaların footer'larına bölge linkleri ekle
"""

import os
import re
from seo_district_data import DISTRICTS

SITE_DIR = "."

GTM_SNIPPET = """  <!-- Google Tag Manager -->
  <script>
    window.dataLayer = window.dataLayer || [];
    // GTM snippet: GTM-XXXXXXX yerine gerçek GTM Container ID yazılacak
    // (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});
    // var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
    // j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
    // f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-XXXXXXX');
  </script>"""

# Popüler 10 ilçe (yüksek arama hacmi)
TOP_10 = [
    ("Kadıköy", "kadikoy-evden-eve-nakliyat"),
    ("Beşiktaş", "besiktas-evden-eve-nakliyat"),
    ("Şişli", "sisli-evden-eve-nakliyat"),
    ("Üsküdar", "uskudar-evden-eve-nakliyat"),
    ("Ataşehir", "atasehir-evden-eve-nakliyat"),
    ("Esenyurt", "esenyurt-evden-eve-nakliyat"),
    ("Bakırköy", "bakirkoy-evden-eve-nakliyat"),
    ("Beylikdüzü", "beylikduzu-evden-eve-nakliyat"),
    ("Maltepe", "maltepe-evden-eve-nakliyat"),
    ("Pendik", "pendik-evden-eve-nakliyat"),
]

def fix_1_title_format():
    """Bölge sayfalarında title formatını güncelle:
    Eski: "Kadıköy Evden Eve Nakliyat - Taşyol Nakliyat | Sabit Fiyat Garantisi"
    Yeni: "Kadıköy Evden Eve Nakliyat | Taşyol Sabit Fiyat Garantisi"
    """
    count = 0
    for d in DISTRICTS:
        filepath = os.path.join("bolgeler", f"{d['slug']}.html")
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        old_title = f"<title>{d['name']} Evden Eve Nakliyat - Taşyol Nakliyat | Sabit Fiyat Garantisi</title>"
        new_title = f"<title>{d['name']} Evden Eve Nakliyat | Taşyol Sabit Fiyat Garantisi</title>"

        if old_title in content:
            content = content.replace(old_title, new_title)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

    print(f"  [1] Title formatı güncellendi: {count} sayfa")
    return count

def fix_2_gtm_placeholder():
    """Bolgeler ve hizmetler sayfalarına GTM placeholder ekle"""
    count = 0
    dirs = ["bolgeler", "hizmetler"]

    for d in dirs:
        if not os.path.exists(d):
            continue
        for fname in os.listdir(d):
            if not fname.endswith('.html'):
                continue
            filepath = os.path.join(d, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # GTM zaten varsa atla
            if 'GTM-XXXXXXX' in content or 'Google Tag Manager' in content:
                continue

            # </head> öncesine GTM snippet ekle
            if '</head>' in content:
                content = content.replace('</head>', f'{GTM_SNIPPET}\n</head>')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1

    print(f"  [2] GTM placeholder eklendi: {count} sayfa")
    return count

def fix_3_bolge_block_index():
    """Ana sayfaya "İstanbul Hizmet Bölgelerimiz" bloğu ekle (CTA banner öncesine)"""
    filepath = "index.html"
    if not os.path.exists(filepath):
        print("  [3] index.html bulunamadı!")
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "istanbul-bolge-grid" in content:
        print("  [3] Bölge bloğu zaten mevcut, atlanıyor.")
        return 0

    # Bölge grid HTML'i oluştur
    bolge_cards = ""
    for name, slug in TOP_10:
        bolge_cards += f'''        <a href="bolgeler/{slug}.html" class="service-card" style="padding:20px; text-align:center; text-decoration:none; color:inherit;">
          <div class="service-icon"><i class="fas fa-map-marker-alt"></i></div>
          <h3 style="font-size:1rem; margin:8px 0 4px;">{name} Nakliyat</h3>
          <small style="color:var(--granit-light);">Evden Eve Taşıma</small>
        </a>
'''

    # Kalan 29 ilçenin küçük linkleri
    remaining = []
    top_slugs = {s for _, s in TOP_10}
    for d in DISTRICTS:
        if d['slug'] not in top_slugs:
            remaining.append(f'<a href="bolgeler/{d["slug"]}.html" style="color:var(--secondary);">{d["name"]}</a>')

    remaining_html = " · ".join(remaining)

    bolge_block = f'''
  <!-- İSTANBUL HİZMET BÖLGELERİMİZ -->
  <section class="section section-alt" id="istanbul-bolge-grid">
    <div class="container">
      <h2 class="section-title">İstanbul Hizmet Bölgelerimiz</h2>
      <p class="section-subtitle">39 ilçede sigortalı ve profesyonel evden eve nakliyat</p>
      <div class="services-grid" style="margin: 32px 0 24px;">
{bolge_cards}      </div>
      <div style="text-align:center; margin-top:16px; font-size:0.9rem; line-height:2;">
        <p><strong>Tüm İlçeler:</strong> {remaining_html}</p>
      </div>
    </div>
  </section>
'''

    # CTA banner öncesine ekle
    # Farklı olası konumları dene
    insertion_markers = [
        '<!-- CTA BANNER -->',
        '<section class="cta-banner">',
        '<!-- PREMIUM TRUST BAND -->'
    ]

    inserted = False
    for marker in insertion_markers:
        if marker in content:
            content = content.replace(marker, bolge_block + "\n  " + marker, 1)
            inserted = True
            break

    if not inserted:
        print("  [3] Uygun ekleme noktası bulunamadı!")
        return 0

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [3] Bölge bloğu index.html'e eklendi (Top 10 + 29 link)")
    return 1

def fix_4_footer_bolge_links():
    """Kök sayfaların footer'larında bölge linklerini yeni URL'lere güncelle"""
    root_pages = ["index.html", "hakkimizda.html", "fiyatlar.html",
                  "referanslar.html", "blog.html", "iletisim.html", "sss.html"]
    count = 0

    # Footer'da "Popüler Bölgeler" bloğu yoksa ekle
    footer_bolge_block = '''        <div>
          <h4>Popüler Bölgeler</h4>
          <ul class="footer-links">
            <li><a href="bolgeler/kadikoy-evden-eve-nakliyat.html">Kadıköy Nakliyat</a></li>
            <li><a href="bolgeler/besiktas-evden-eve-nakliyat.html">Beşiktaş Nakliyat</a></li>
            <li><a href="bolgeler/uskudar-evden-eve-nakliyat.html">Üsküdar Nakliyat</a></li>
            <li><a href="bolgeler/sisli-evden-eve-nakliyat.html">Şişli Nakliyat</a></li>
            <li><a href="bolgeler/atasehir-evden-eve-nakliyat.html">Ataşehir Nakliyat</a></li>
            <li><a href="bolgeler/esenyurt-evden-eve-nakliyat.html">Esenyurt Nakliyat</a></li>
          </ul>
        </div>'''

    for page in root_pages:
        filepath = os.path.join(SITE_DIR, page)
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Eski ilceler/ linklerini bolgeler/ linklerine güncelle
        if 'ilceler/' in content:
            content = re.sub(
                r'href="ilceler/([a-z]+)-nakliyat\.html"',
                r'href="bolgeler/\1-evden-eve-nakliyat.html"',
                content
            )
            changed = True

        # Footer'da "Popüler Bölgeler" yoksa ve footer-grid varsa ekle
        if 'Popüler Bölgeler' not in content and 'footer-grid' in content:
            # İletişim bloğunun hemen öncesine ekle
            if '<h4>İletişim</h4>' in content:
                content = content.replace(
                    '        <div>\n          <h4>İletişim</h4>',
                    footer_bolge_block + '\n        <div>\n          <h4>İletişim</h4>'
                )
                changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

    print(f"  [4] Footer bölge linkleri güncellendi: {count} sayfa")
    return count

def main():
    print("=" * 60)
    print("AŞAMA 3-4: SEO Silo Mimarisi Tamamlama")
    print("=" * 60)

    total = 0
    total += fix_1_title_format()
    total += fix_2_gtm_placeholder()
    total += fix_3_bolge_block_index()
    total += fix_4_footer_bolge_links()

    print(f"\nToplam {total} güncelleme yapıldı.")

if __name__ == "__main__":
    main()
