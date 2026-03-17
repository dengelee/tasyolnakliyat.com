#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""39 İlçe SEO Sayfası Üretici — /bolgeler/ klasörüne yazar"""

import os
from seo_district_data import DISTRICTS

SITE_URL = "https://tasyolnakliyat.com"

def get_all_districts_links(current_slug):
    """Sidebar bölge linkleri — mevcut ilçe hariç"""
    links = []
    for d in DISTRICTS:
        if d['slug'] == current_slug:
            links.append(f'<strong style="color:var(--primary);">{d["name"]}</strong>')
        else:
            links.append(f'<a href="{d["slug"]}.html" style="color:var(--secondary);">{d["name"]}</a>')
    return " | ".join(links)

def get_neighbor_links(district):
    html = ""
    for i, n in enumerate(district['neighbors']):
        slug = district['neighbor_slugs'][i] if i < len(district['neighbor_slugs']) else ""
        html += f'<a href="{slug}.html" class="card-link">{n} Nakliyat</a>'
        if i < len(district['neighbors']) - 1:
            html += " | "
    return html

def generate_schema(district):
    return f'''<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "MovingCompany",
        "name": "Taşyol Nakliyat - {district['name']}",
        "url": "{SITE_URL}/bolgeler/{district['slug']}.html",
        "logo": "{SITE_URL}/images/logo-full.png",
        "image": "{SITE_URL}/images/og-image.png",
        "telephone": "+905365805059",
        "email": "info@tasyolnakliyat.com",
        "description": "{district['name']} evden eve nakliyat. Sigortalı, profesyonel ve sabit fiyat garantili taşıma hizmeti.",
        "areaServed": {{
          "@type": "AdministrativeArea",
          "name": "{district['name']}, İstanbul",
          "containedInPlace": {{
            "@type": "City",
            "name": "İstanbul"
          }}
        }},
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "{district['name']}",
          "addressRegion": "İstanbul",
          "addressCountry": "TR"
        }},
        "priceRange": "$$",
        "openingHoursSpecification": {{
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
          "opens": "07:00",
          "closes": "22:00"
        }},
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "4.9",
          "reviewCount": "127"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Ana Sayfa",
            "item": "{SITE_URL}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Hizmetler",
            "item": "{SITE_URL}/hizmetler/istanbul-evden-eve-nakliyat.html"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{district['name']} Nakliyat",
            "item": "{SITE_URL}/bolgeler/{district['slug']}.html"
          }}
        ]
      }}
    ]
  }}
  </script>'''

def generate_page(district):
    semtler_text = ", ".join(district['semtler'])
    neighbor_links = get_neighbor_links(district)
    all_links = get_all_districts_links(district['slug'])
    schema = generate_schema(district)
    wa_slug = district['slug'].replace('-evden-eve-nakliyat', '')

    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{district['name']} Evden Eve Nakliyat - Taşyol Nakliyat | Sabit Fiyat Garantisi</title>
  <meta name="description" content="{district['name']} evden eve nakliyat hizmeti. {district['geo_detail']} Sigortalı, profesyonel taşıma. Ücretsiz keşif: 0536 580 50 59">
  <meta name="keywords" content="{district['name']} nakliyat, {district['name']} evden eve nakliyat, {district['name']} nakliye, {district['name']} taşıma, {district['name']} nakliyat firmaları, {district['name']} nakliyat fiyatları">
  <link rel="canonical" href="{SITE_URL}/bolgeler/{district['slug']}.html">

  <!-- Open Graph -->
  <meta property="og:title" content="{district['name']} Evden Eve Nakliyat - Taşyol Nakliyat">
  <meta property="og:description" content="{district['name']} evden eve nakliyat. Sigortalı, profesyonel ve sabit fiyat garantili taşıma hizmeti.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE_URL}/bolgeler/{district['slug']}.html">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Taşyol Nakliyat">
  <meta property="og:image" content="{SITE_URL}/images/og-image.png">

  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../images/apple-touch-icon.png">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Main CSS -->
  <link rel="stylesheet" href="../css/style.min.css">

  <!-- Schema.org JSON-LD -->
  {schema}
</head>
<body>

  <!-- HEADER -->
  <header class="header">
    <div class="header-top">
      <div class="container">
        <div class="header-top-left">
          <span><i class="fas fa-phone-alt"></i> <a href="tel:05365805059">0536 580 50 59</a></span>
          <span><i class="fas fa-envelope"></i> info@tasyolnakliyat.com</span>
        </div>
        <div class="header-top-right">
          <span><i class="far fa-clock"></i> Pazartesi - Pazar: 07:00 - 22:00</span>
          <a href="https://wa.me/905365805059" class="phone-top" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp Hattı</a>
        </div>
      </div>
    </div>
    <nav class="nav-main">
      <div class="container">
        <a href="../index.html" class="logo">
          <img src="../images/logo-header.png" alt="Taşyol Nakliyat Logo" class="logo-img" loading="lazy">
          <div class="logo-text">
            <span class="logo-title">Taşyol <span>Nakliyat</span></span>
            <span class="logo-subtitle"><svg class="subtitle-icon" width="10" height="12" viewBox="0 0 10 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 0L10 2.5V5.5C10 8.5 7.5 11 5 12C2.5 11 0 8.5 0 5.5V2.5L5 0Z" fill="currentColor" opacity="0.6"/><path d="M4.2 7.5L2.5 5.8L3.2 5.1L4.2 6.1L6.8 3.5L7.5 4.2L4.2 7.5Z" fill="white"/></svg>Güvenli Taşıma</span>
          </div>
        </a>
        <div class="nav-links">
          <a href="../index.html">Ana Sayfa</a>
          <a href="../hizmetler/istanbul-evden-eve-nakliyat.html">Hizmetler</a>
          <a href="../hakkimizda.html">Hakkımızda</a>
          <a href="../fiyatlar.html">Fiyatlar</a>
          <a href="../referanslar.html">Referanslar</a>
          <a href="../blog.html">Blog</a>
          <a href="../iletisim.html">İletişim</a>
          <a href="../fiyatlar.html" class="nav-cta">Teklif Al</a>
        </div>
        <button class="hamburger" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
  </header>

  <!-- BREADCRUMB + DISTRICT HERO -->
  <section class="district-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="../index.html">Ana Sayfa</a>
        <span aria-hidden="true">/</span>
        <a href="../hizmetler/istanbul-evden-eve-nakliyat.html">Hizmetler</a>
        <span aria-hidden="true">/</span>
        <span>{district['name']} Nakliyat</span>
      </nav>
      <h1>{district['name']} Evden Eve Nakliyat</h1>
      <p>{district['geo_detail']} Eşyalarınız emin ellerde, sabit fiyat garantisiyle!</p>
    </div>
  </section>

  <!-- DISTRICT CONTENT -->
  <section class="section">
    <div class="container">
      <div class="district-content">
        <div class="district-main">

          <h2>{district['name']} Nakliyat Hizmeti</h2>
          <p>Taşyol Nakliyat olarak, İstanbul'un {district['side']} yakasında yaklaşık {district['population']} nüfusa sahip {district['name']} ilçesinde profesyonel evden eve nakliyat hizmeti sunuyoruz. {district['micro_content']}</p>

          <p>Bölgenin kendine özgü sokak yapısı, bina özellikleri ve ulaşım dinamiklerini çok iyi bilen ekibimiz, eşyalarınızı en güvenli şekilde yeni adresinize taşır. {semtler_text} gibi semtlere özel hizmet veriyoruz.</p>

          <h2>{district['name']} Nakliyat Fiyatları 2026</h2>
          <p>{district['name']} bölgesinde nakliyat fiyatları; eşya miktarı, mesafe, kat sayısı ve ek hizmet taleplerine göre değişiklik gösterir ({district['price_note']}). Genel fiyat aralıklarımız:</p>

          <div class="pricing-grid" style="margin: 24px 0;">
            <div class="price-card">
              <h3>1+1 Daire</h3>
              <div class="price-range">12.500 - 16.500 <small>TL</small></div>
            </div>
            <div class="price-card">
              <h3>2+1 Daire</h3>
              <div class="price-range">15.500 - 20.150 <small>TL</small></div>
            </div>
            <div class="price-card popular">
              <h3>3+1 Daire</h3>
              <div class="price-range">17.500 - 30.000 <small>TL</small></div>
            </div>
          </div>

          <p>Kesin fiyat için ücretsiz keşif hizmetimizden yararlanabilirsiniz. Ekspertiz ekibimiz evinize gelerek eşya miktarını, özel taşıma gerektiren parçaları ve diğer detayları yerinde değerlendirir.</p>

          <h2>{district['name']} Nakliyat Hizmetlerimiz</h2>
          <p>{district['name']} bölgesinde sunduğumuz kapsamlı hizmetler:</p>

          <div class="services-grid" style="margin: 24px 0;">
            <div class="service-card">
              <div class="service-icon"><i class="fas fa-house-chimney"></i></div>
              <h3>Evden Eve Nakliyat</h3>
              <p>{district['name']} içinden veya {district['name']}'a yapılacak tüm ev taşımalarınız için profesyonel hizmet.</p>
            </div>
            <div class="service-card">
              <div class="service-icon"><i class="fas fa-building"></i></div>
              <h3>Ofis Taşıma</h3>
              <p>{district['name']} bölgesindeki ofis ve iş yeri taşımaları için özel çözümler sunuyoruz.</p>
            </div>
            <div class="service-card">
              <div class="service-icon"><i class="fas fa-box-open"></i></div>
              <h3>Eşya Paketleme</h3>
              <p>Profesyonel paketleme malzemeleri ile eşyalarınız en üst düzey koruma altında.</p>
            </div>
            <div class="service-card">
              <div class="service-icon"><i class="fas fa-elevator"></i></div>
              <h3>Asansörlü Taşıma</h3>
              <p>Yüksek katlı binalarda dış cephe asansörü ile hızlı ve güvenli taşıma.</p>
            </div>
          </div>

          <h2>Neden {district['name']} Nakliyat İçin Taşyol?</h2>
          <p>Taşyol Nakliyat olarak {district['name']} bölgesinde tercih edilmemizin nedenleri:</p>

          <div class="about-features">
            <div class="about-feature">
              <div class="about-feature-icon"><i class="fas fa-shield-alt"></i></div>
              <div>
                <h4>Tam Kapsamlı Sigorta</h4>
                <p>Tüm eşyalarınız taşıma sırasında tam kapsamlı sigorta güvencesi altındadır.</p>
              </div>
            </div>
            <div class="about-feature">
              <div class="about-feature-icon"><i class="fas fa-clock"></i></div>
              <div>
                <h4>Zamanında Teslimat</h4>
                <p>Söz verdiğimiz saatte eşyalarınızı yeni adresinize teslim ediyoruz.</p>
              </div>
            </div>
            <div class="about-feature">
              <div class="about-feature-icon"><i class="fas fa-users"></i></div>
              <div>
                <h4>Deneyimli Ekip</h4>
                <p>{district['name']} bölgesini iyi tanıyan, eğitimli ve profesyonel taşıma ekibi.</p>
              </div>
            </div>
            <div class="about-feature">
              <div class="about-feature-icon"><i class="fas fa-hand-holding-dollar"></i></div>
              <div>
                <h4>Sabit Fiyat Garantisi</h4>
                <p>Teklif edilen fiyat, ödeyeceğiniz son fiyattır. Gizli maliyet yok.</p>
              </div>
            </div>
          </div>

          <h2>{district['name']} ve Çevresine Nakliyat</h2>
          <p>{district['name']} ilçesinden veya {district['name']} ilçesine yapılacak taşımalarda, yakın ilçelere de hizmet veriyoruz:</p>
          <p>Yakın ilçe nakliyat sayfaları: {neighbor_links}</p>

        </div>

        <!-- SIDEBAR -->
        <aside class="district-sidebar">
          <div class="sidebar-box" style="background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%); color: white; border: none;">
            <h4 style="color: white;"><i class="fas fa-phone-alt"></i> Hemen Arayın</h4>
            <p style="font-size: 1.5rem; font-weight: 800; margin-bottom: 12px;">0536 580 50 59</p>
            <a href="tel:05365805059" class="btn btn-secondary" style="width: 100%; justify-content: center;">Şimdi Ara</a>
            <div style="margin-top: 12px;">
              <a href="https://wa.me/905365805059?text=Merhaba%2C%20{wa_slug}%20nakliyat%20teklifi%20almak%20istiyorum." class="btn btn-whatsapp" style="width: 100%; justify-content: center;" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp</a>
            </div>
          </div>

          <div class="sidebar-box">
            <h4><i class="fas fa-file-invoice"></i> Hızlı Teklif Al</h4>
            <form id="sidebarQuoteForm" class="sidebar-quote-form">
              <div class="form-group">
                <input type="text" name="name" class="form-control" placeholder="Adınız Soyadınız" required>
              </div>
              <div class="form-group">
                <input type="tel" name="phone" class="form-control" placeholder="05XX XXX XX XX" required>
              </div>
              <div class="form-group">
                <select name="from" class="form-control" required>
                  <option value="">Nereden (İlçe Seçiniz)</option>
                  {"".join(f'<option value="{d["name"]}"{" selected" if d["name"]==district["name"] else ""}>{d["name"]}</option>' for d in DISTRICTS)}
                </select>
              </div>
              <div class="form-group">
                <select name="to" class="form-control" required>
                  <option value="">Nereye (İlçe Seçiniz)</option>
                  {"".join(f'<option value="{d["name"]}">{d["name"]}</option>' for d in DISTRICTS)}
                </select>
              </div>
              <div class="form-group">
                <input type="date" name="date" class="form-control" required>
              </div>
              <div class="form-group">
                <select name="type" class="form-control">
                  <option value="">Ev Tipi Seçiniz</option>
                  <option>1+1 Daire</option>
                  <option>2+1 Daire</option>
                  <option>3+1 Daire</option>
                  <option>4+1 Daire</option>
                  <option>5+1 Daire</option>
                  <option>Ofis / İş Yeri</option>
                  <option>Villa</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;"><i class="fas fa-paper-plane"></i> Ücretsiz Teklif Al</button>
            </form>
          </div>

          <div class="sidebar-box">
            <h4><i class="fas fa-map-marker-alt"></i> Hizmet Bölgelerimiz</h4>
            <p style="font-size: 0.85rem; line-height: 1.8;">
              {all_links}
            </p>
          </div>

          <!-- Internal Link: Hizmet Silosu -->
          <div class="sidebar-box">
            <h4><i class="fas fa-concierge-bell"></i> Tüm Hizmetlerimiz</h4>
            <ul class="footer-links" style="margin:0; padding:0; list-style:none;">
              <li><a href="../hizmetler/istanbul-evden-eve-nakliyat.html"><i class="fas fa-house-chimney"></i> Evden Eve Nakliyat</a></li>
              <li><a href="../hizmetler/ofis-ve-isyeri-tasimaciligi.html"><i class="fas fa-building"></i> Ofis Taşımacılığı</a></li>
              <li><a href="../hizmetler/asansorlu-nakliyat.html"><i class="fas fa-elevator"></i> Asansörlü Nakliyat</a></li>
              <li><a href="../hizmetler/sehir-ici-kamyonet-nakliye.html"><i class="fas fa-truck-pickup"></i> Kamyonet Nakliye</a></li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="cta-banner">
    <div class="container">
      <h2>{district['name']} Nakliyat Teklifi Alın</h2>
      <p>{district['name']} bölgesinde güvenilir ve uygun fiyatlı nakliyat için hemen bize ulaşın.</p>
      <div class="cta-buttons">
        <a href="tel:05365805059" class="btn btn-secondary btn-lg"><i class="fas fa-phone-alt"></i> 0536 580 50 59</a>
        <a href="https://wa.me/905365805059?text=Merhaba%2C%20{wa_slug}%20nakliyat%20teklifi%20almak%20istiyorum." class="btn btn-whatsapp btn-lg" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp ile Teklif Al</a>
      </div>
    </div>
  </section>

  <!-- PREMIUM TRUST BAND -->
  <section class="premium-trust-band">
    <div class="container">
      <div class="trust-band-items">
        <div class="trust-band-item"><i class="fas fa-hand-holding-usd"></i><span>Sabit Fiyat Garantisi</span></div>
        <div class="trust-band-item"><i class="fas fa-shield-alt"></i><span>Tam Kapsamlı Sigorta</span></div>
        <div class="trust-band-item"><i class="fas fa-headset"></i><span>7/24 Destek</span></div>
        <div class="trust-band-item"><i class="fas fa-star"></i><span>1500+ Mutlu Müşteri</span></div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4>Taşyol Nakliyat</h4>
          <p>İstanbul'un en güvenilir nakliyat firması. Sigortalı, profesyonel ve uygun fiyatlı evden eve nakliyat hizmeti.</p>
          <p><i class="fas fa-shield-alt"></i> Tam Kapsamlı Sigorta</p>
          <p><i class="fas fa-users"></i> Profesyonel Ekip</p>
          <p><i class="fas fa-clock"></i> Zamanında Teslimat</p>
        </div>
        <div>
          <h4>Hizmetlerimiz</h4>
          <ul class="footer-links">
            <li><a href="../hizmetler/istanbul-evden-eve-nakliyat.html">Evden Eve Nakliyat</a></li>
            <li><a href="../hizmetler/ofis-ve-isyeri-tasimaciligi.html">Ofis Taşıma</a></li>
            <li><a href="../hizmetler/asansorlu-nakliyat.html">Asansörlü Nakliyat</a></li>
            <li><a href="../hizmetler/sehir-ici-kamyonet-nakliye.html">Kamyonet Nakliye</a></li>
            <li><a href="../fiyatlar.html">Fiyat Listesi</a></li>
          </ul>
        </div>
        <div>
          <h4>Popüler Bölgeler</h4>
          <ul class="footer-links">
            <li><a href="kadikoy-evden-eve-nakliyat.html">Kadıköy Nakliyat</a></li>
            <li><a href="besiktas-evden-eve-nakliyat.html">Beşiktaş Nakliyat</a></li>
            <li><a href="uskudar-evden-eve-nakliyat.html">Üsküdar Nakliyat</a></li>
            <li><a href="sisli-evden-eve-nakliyat.html">Şişli Nakliyat</a></li>
            <li><a href="atasehir-evden-eve-nakliyat.html">Ataşehir Nakliyat</a></li>
            <li><a href="esenyurt-evden-eve-nakliyat.html">Esenyurt Nakliyat</a></li>
          </ul>
        </div>
        <div>
          <h4>İletişim</h4>
          <ul class="footer-contact">
            <li><i class="fas fa-phone-alt"></i> <a href="tel:05365805059">0536 580 50 59</a></li>
            <li><i class="fab fa-whatsapp"></i> <a href="https://wa.me/905365805059" target="_blank">WhatsApp Hattı</a></li>
            <li><i class="fas fa-envelope"></i> info@tasyolnakliyat.com</li>
            <li><i class="far fa-clock"></i> Pzt-Paz: 07:00-22:00</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Taşyol Nakliyat. Tüm hakları saklıdır. | <a href="../sss.html">SSS</a> | <a href="../iletisim.html">İletişim</a></p>
      </div>
    </div>
  </footer>

  <!-- FLOATING BUTTONS -->
  <a href="https://wa.me/905365805059?text=Merhaba%2C%20{wa_slug}%20nakliyat%20hakkinda%20bilgi%20almak%20istiyorum." class="whatsapp-float" target="_blank" aria-label="WhatsApp">
    <i class="fab fa-whatsapp" style="font-size:28px;"></i>
  </a>
  <a href="tel:05365805059" class="phone-float">
    <i class="fas fa-phone-alt"></i> 0536 580 50 59
  </a>

  <!-- Mobile Sticky CTA -->
  <div class="mobile-cta-bar">
    <a href="tel:05365805059" class="mobile-cta-btn cta-phone"><i class="fas fa-phone-alt"></i> Ara</a>
    <a href="https://wa.me/905365805059?text=Merhaba%2C%20{wa_slug}%20nakliyat%20teklifi%20almak%20istiyorum." class="mobile-cta-btn cta-whatsapp" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp</a>
    <a href="../fiyatlar.html" class="mobile-cta-btn cta-quote"><i class="fas fa-file-invoice"></i> Teklif</a>
  </div>

  <script src="../js/main.min.js"></script>
</body>
</html>'''

def main():
    out_dir = "bolgeler"
    os.makedirs(out_dir, exist_ok=True)

    for district in DISTRICTS:
        filename = f"{district['slug']}.html"
        filepath = os.path.join(out_dir, filename)
        html = generate_page(district)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  OK: {filepath}")

    print(f"\n{len(DISTRICTS)} bölge sayfası başarıyla üretildi.")

if __name__ == "__main__":
    main()
