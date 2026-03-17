/* ===== TAŞYOL NAKLIYAT - ANA JAVASCRIPT DOSYASI ===== */

document.addEventListener('DOMContentLoaded', function() {

  // ===== UTILITY: TOAST NOTIFICATION =====
  function showToast(message, duration) {
    duration = duration || 3000;
    var existing = document.querySelector('.toast');
    if (existing) existing.remove();
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = '<div class="toast-icon"><i class="fas fa-check-circle"></i></div><div class="toast-text">' + message + '</div>';
    document.body.appendChild(toast);
    setTimeout(function() { toast.classList.add('show'); }, 10);
    setTimeout(function() {
      toast.classList.remove('show');
      setTimeout(function() { toast.remove(); }, 400);
    }, duration);
  }

  // ===== UTILITY: FORM VALIDATION =====
  function showError(input, msg) {
    input.classList.add('error');
    input.classList.remove('success');
    var errEl = input.parentElement.querySelector('.form-error');
    if (!errEl) {
      errEl = document.createElement('div');
      errEl.className = 'form-error';
      errEl.innerHTML = '<i class="fas fa-exclamation-circle"></i> <span></span>';
      input.parentElement.appendChild(errEl);
    }
    errEl.querySelector('span').textContent = msg;
    errEl.classList.add('show');
  }

  function clearError(input) {
    input.classList.remove('error');
    var errEl = input.parentElement.querySelector('.form-error');
    if (errEl) errEl.classList.remove('show');
  }

  function markSuccess(input) {
    input.classList.remove('error');
    input.classList.add('success');
    var errEl = input.parentElement.querySelector('.form-error');
    if (errEl) errEl.classList.remove('show');
  }

  // ===== UTILITY: PHONE FORMATTING =====
  function formatPhone(value) {
    var digits = value.replace(/\D/g, '');
    if (digits.length === 0) return '';
    // Format: 05XX XXX XX XX
    var formatted = '';
    if (digits.length <= 4) {
      formatted = digits;
    } else if (digits.length <= 7) {
      formatted = digits.slice(0, 4) + ' ' + digits.slice(4);
    } else if (digits.length <= 9) {
      formatted = digits.slice(0, 4) + ' ' + digits.slice(4, 7) + ' ' + digits.slice(7);
    } else {
      formatted = digits.slice(0, 4) + ' ' + digits.slice(4, 7) + ' ' + digits.slice(7, 9) + ' ' + digits.slice(9, 11);
    }
    return formatted;
  }

  function isValidPhone(value) {
    var digits = value.replace(/\D/g, '');
    return digits.length === 11 && (digits.startsWith('05') || digits.startsWith('5'));
  }

  // ===== HEADER SCROLL =====
  var header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', function() {
      header.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // ===== HAMBURGER MENU =====
  var hamburger = document.querySelector('.hamburger');
  var navLinks = document.querySelector('.nav-links');
  if (hamburger && navLinks) {
    function toggleMenu(open) {
      var isOpen = typeof open === 'boolean' ? open : !navLinks.classList.contains('active');
      navLinks.classList.toggle('active', isOpen);
      hamburger.classList.toggle('active', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    }
    hamburger.addEventListener('click', function(e) {
      e.stopPropagation();
      toggleMenu();
    });
    navLinks.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() { toggleMenu(false); });
    });
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.nav-main') && navLinks.classList.contains('active')) {
        toggleMenu(false);
      }
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && navLinks.classList.contains('active')) {
        toggleMenu(false);
      }
    });
  }

  // ===== FAQ ACCORDION =====
  document.querySelectorAll('.faq-question').forEach(function(q) {
    q.addEventListener('click', function() {
      var item = q.parentElement;
      var wasActive = item.classList.contains('active');
      document.querySelectorAll('.faq-item').forEach(function(i) { i.classList.remove('active'); });
      if (!wasActive) item.classList.add('active');
    });
  });

  // ===== FADE UP ANIMATION =====
  var observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
  var fadeObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);
  document.querySelectorAll('.fade-up').forEach(function(el) { fadeObserver.observe(el); });

  // ===== COUNTER ANIMATION =====
  function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(function(counter) {
      if (counter.dataset.animated) return;
      var target = parseInt(counter.dataset.count);
      var suffix = counter.dataset.suffix || '';
      var duration = 2000;
      var step = target / (duration / 16);
      var current = 0;
      var update = function() {
        current += step;
        if (current >= target) {
          counter.textContent = target.toLocaleString('tr-TR') + suffix;
          counter.dataset.animated = 'true';
        } else {
          counter.textContent = Math.floor(current).toLocaleString('tr-TR') + suffix;
          requestAnimationFrame(update);
        }
      };
      update();
    });
  }
  var counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) animateCounters();
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.stats').forEach(function(el) { counterObserver.observe(el); });

  // ===== SET DATE MIN TO TODAY =====
  var dateInputs = document.querySelectorAll('input[type="date"]');
  if (dateInputs.length) {
    var today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(function(input) {
      input.setAttribute('min', today);
    });
  }

  // ===== PHONE INPUT FORMATTING =====
  document.querySelectorAll('input[name="phone"]').forEach(function(phoneInput) {
    phoneInput.addEventListener('input', function() {
      var cursorPos = this.selectionStart;
      var oldLen = this.value.length;
      this.value = formatPhone(this.value);
      var newLen = this.value.length;
      var newPos = cursorPos + (newLen - oldLen);
      this.setSelectionRange(newPos, newPos);
    });
    phoneInput.addEventListener('blur', function() {
      if (this.value.trim() && !isValidPhone(this.value)) {
        showError(this, 'Geçerli bir telefon numarası girin (05XX XXX XX XX)');
      } else if (this.value.trim()) {
        markSuccess(this);
      }
    });
    phoneInput.addEventListener('focus', function() { clearError(this); });
  });

  // ===== NAME INPUT VALIDATION =====
  document.querySelectorAll('input[name="name"]').forEach(function(nameInput) {
    nameInput.addEventListener('blur', function() {
      if (this.value.trim() && this.value.trim().length < 3) {
        showError(this, 'En az 3 karakter girin');
      } else if (this.value.trim()) {
        markSuccess(this);
      }
    });
    nameInput.addEventListener('focus', function() { clearError(this); });
  });

  // ===== MULTI-STEP QUOTE FORM =====
  var quoteForm = document.getElementById('quoteForm');
  var formStep1 = document.getElementById('formStep1');
  var formStep2 = document.getElementById('formStep2');
  var formNextBtn = document.getElementById('formNextBtn');
  var formBackBtn = document.getElementById('formBackBtn');
  var formProgressBar = document.getElementById('formProgressBar');
  var stepLabel = document.getElementById('stepLabel');

  if (formNextBtn && formStep1 && formStep2) {
    formNextBtn.addEventListener('click', function() {
      var nameInput = formStep1.querySelector('[name="name"]');
      var phoneInput = formStep1.querySelector('[name="phone"]');
      var valid = true;

      // Validate name
      if (!nameInput.value.trim()) {
        showError(nameInput, 'Ad ve soyadınızı girin');
        valid = false;
      } else if (nameInput.value.trim().length < 3) {
        showError(nameInput, 'En az 3 karakter girin');
        valid = false;
      } else {
        markSuccess(nameInput);
      }

      // Validate phone
      if (!phoneInput.value.trim()) {
        showError(phoneInput, 'Telefon numaranızı girin');
        valid = false;
      } else if (!isValidPhone(phoneInput.value)) {
        showError(phoneInput, 'Geçerli bir numara girin (05XX XXX XX XX)');
        valid = false;
      } else {
        markSuccess(phoneInput);
      }

      if (!valid) return;

      // Slide animation: step 1 → step 2
      formStep1.style.animation = 'slideOut 0.25s ease forwards';
      setTimeout(function() {
        formStep1.style.display = 'none';
        formStep1.style.animation = '';
        formStep2.style.display = 'block';
        formStep2.style.animation = 'slideIn 0.3s ease';
        if (formProgressBar) formProgressBar.style.width = '100%';
        if (stepLabel) stepLabel.parentElement.innerHTML = '<span id="stepLabel">Adım 2/2</span> — Taşınma Detayları';
      }, 250);
    });
  }

  if (formBackBtn && formStep1 && formStep2) {
    formBackBtn.addEventListener('click', function() {
      formStep2.style.animation = 'slideOut 0.25s ease forwards';
      setTimeout(function() {
        formStep2.style.display = 'none';
        formStep2.style.animation = '';
        formStep1.style.display = 'block';
        formStep1.style.animation = 'slideIn 0.3s ease';
        if (formProgressBar) formProgressBar.style.width = '50%';
        if (stepLabel) stepLabel.parentElement.innerHTML = '<span id="stepLabel">Adım 1/2</span> — Kişisel Bilgiler';
      }, 250);
    });
  }

  if (quoteForm) {
    quoteForm.addEventListener('submit', function(e) {
      e.preventDefault();

      // Validate step 2 fields
      var fromSelect = quoteForm.querySelector('[name="from"]');
      var toSelect = quoteForm.querySelector('[name="to"]');
      var dateInput = quoteForm.querySelector('[name="date"]');
      var typeSelect = quoteForm.querySelector('[name="type"]');
      var valid = true;

      if (!fromSelect.value) { showError(fromSelect, 'Nereden ilçe seçin'); valid = false; }
      else { markSuccess(fromSelect); }

      if (!toSelect.value) { showError(toSelect, 'Nereye ilçe seçin'); valid = false; }
      else { markSuccess(toSelect); }

      if (!dateInput.value) { showError(dateInput, 'Taşınma tarihi seçin'); valid = false; }
      else { markSuccess(dateInput); }

      if (!typeSelect.value) { showError(typeSelect, 'Ev tipi seçin'); valid = false; }
      else { markSuccess(typeSelect); }

      if (!valid) return;

      // Show loading state
      var btn = this.querySelector('button[type="submit"]');
      var originalHTML = btn.innerHTML;
      btn.classList.add('loading');
      btn.innerHTML = '<span class="btn-spinner"></span> Gönderiliyor...';

      var formData = new FormData(this);
      var name = formData.get('name') || '';
      var phone = formData.get('phone') || '';
      var from = formData.get('from') || '';
      var to = formData.get('to') || '';
      var date = formData.get('date') || '';
      var type = formData.get('type') || '';

      var message = 'Merhaba, tasyolnakliyat.com üzerinden teklif almak istiyorum.%0A%0A' +
        'Ad: ' + name + '%0ATelefon: ' + phone + '%0ANereden: ' + from + '%0ANereye: ' + to + '%0ATarih: ' + date + '%0ATip: ' + type;

      // Simulate brief loading then redirect
      setTimeout(function() {
        window.open('https://wa.me/905365805059?text=' + message, '_blank');

        btn.classList.remove('loading');
        btn.innerHTML = '<i class="fas fa-check"></i> Yönlendirildi!';
        btn.style.background = 'var(--success)';

        showToast('WhatsApp\'a yönlendirildiniz! Ekibimiz en kısa sürede dönüş yapacaktır.', 4000);

        setTimeout(function() {
          btn.innerHTML = originalHTML;
          btn.style.background = '';
        }, 3000);
      }, 800);
    });
  }

  // ===== SELECT FIELD VALIDATION ON CHANGE =====
  document.querySelectorAll('select.form-control').forEach(function(select) {
    select.addEventListener('change', function() {
      if (this.value) { markSuccess(this); }
    });
  });

  // ===== MOBILE STICKY CTA BAR — Always visible =====

  // ===== CONTACT FORM =====
  var contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var formData = new FormData(this);
      var name = formData.get('name') || '';
      var phone = formData.get('phone') || '';
      var message = formData.get('message') || '';

      // Validate
      var nameInput = this.querySelector('[name="name"]');
      var phoneInput = this.querySelector('[name="phone"]');
      var valid = true;

      if (!name.trim()) { showError(nameInput, 'Adınızı girin'); valid = false; }
      else { markSuccess(nameInput); }

      if (!phone.trim()) { showError(phoneInput, 'Telefon numaranızı girin'); valid = false; }
      else if (!isValidPhone(phone)) { showError(phoneInput, 'Geçerli bir numara girin'); valid = false; }
      else { markSuccess(phoneInput); }

      if (!valid) return;

      var msg = 'Merhaba, tasyolnakliyat.com iletişim formundan yazıyorum.%0A%0AAd: ' + name + '%0ATelefon: ' + phone + '%0AMesaj: ' + message;
      window.open('https://wa.me/905365805059?text=' + msg, '_blank');
      showToast('WhatsApp\'a yönlendirildiniz!', 3000);
    });
  }

  // ===== INTERACTIVE ISTANBUL MAP =====
  // SVG is now inline in HTML — no fetch needed
  var mapContainer = document.getElementById('mapContainer');
  if (mapContainer) {
    var svg = mapContainer.querySelector('svg');
    if (svg) {
      initMapInteraction(svg);
    }
  }

  function initMapInteraction(svg) {
    var districtPaths = svg.querySelectorAll('.district-path');
    var routeLine = svg.getElementById('routeLine');
    var routeStart = svg.getElementById('routeStart');
    var routeEnd = svg.getElementById('routeEnd');

    // District name to slug mapping
    function nameToSlug(name) {
      return name.toLowerCase()
        .replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ü/g, 'u')
        .replace(/ş/g, 's').replace(/ç/g, 'c').replace(/ğ/g, 'g')
        .replace(/â/g, 'a');
    }

    // Get center of a path
    function getPathCenter(path) {
      var bbox = path.getBBox();
      return { x: bbox.x + bbox.width / 2, y: bbox.y + bbox.height / 2 };
    }

    // Highlight a district
    function highlightDistrict(slug, color) {
      districtPaths.forEach(function(p) {
        if (p.getAttribute('data-district') === slug) {
          p.setAttribute('fill', color);
          p.setAttribute('stroke', color === '#2563EB' ? '#1E40AF' : '#1DA851');
          p.setAttribute('stroke-width', '2');
        }
      });
    }

    // Reset all districts
    function resetDistricts() {
      districtPaths.forEach(function(p) {
        p.setAttribute('fill', '#E2E8F0');
        p.setAttribute('stroke', '#94A3B8');
        p.setAttribute('stroke-width', '1');
      });
    }

    // Show route between two districts
    function showRoute(fromSlug, toSlug) {
      resetDistricts();

      var fromPath = svg.querySelector('[data-district="' + fromSlug + '"]');
      var toPath = svg.querySelector('[data-district="' + toSlug + '"]');

      if (fromPath) {
        highlightDistrict(fromSlug, '#2563EB');
        var fromCenter = getPathCenter(fromPath);
        routeStart.setAttribute('cx', fromCenter.x);
        routeStart.setAttribute('cy', fromCenter.y);
        routeStart.setAttribute('opacity', '1');

        if (toPath) {
          highlightDistrict(toSlug, '#25D366');
          var toCenter = getPathCenter(toPath);
          routeEnd.setAttribute('cx', toCenter.x);
          routeEnd.setAttribute('cy', toCenter.y);
          routeEnd.setAttribute('opacity', '1');

          routeLine.setAttribute('x1', fromCenter.x);
          routeLine.setAttribute('y1', fromCenter.y);
          routeLine.setAttribute('x2', toCenter.x);
          routeLine.setAttribute('y2', toCenter.y);
          routeLine.setAttribute('opacity', '1');
        } else {
          routeLine.setAttribute('opacity', '0');
          routeEnd.setAttribute('opacity', '0');
        }
      }
    }

    // Listen to form select changes
    var fromSelect = document.querySelector('select[name="from"]');
    var toSelect = document.querySelector('select[name="to"]');

    function updateMap() {
      var fromVal = fromSelect ? fromSelect.value : '';
      var toVal = toSelect ? toSelect.value : '';

      if (!fromVal && !toVal) {
        resetDistricts();
        routeLine.setAttribute('opacity', '0');
        routeStart.setAttribute('opacity', '0');
        routeEnd.setAttribute('opacity', '0');
        return;
      }

      var fromSlug = fromVal ? nameToSlug(fromVal) : '';
      var toSlug = toVal ? nameToSlug(toVal) : '';

      if (fromSlug && toSlug) {
        showRoute(fromSlug, toSlug);
      } else if (fromSlug) {
        resetDistricts();
        highlightDistrict(fromSlug, '#2563EB');
        var fp = svg.querySelector('[data-district="' + fromSlug + '"]');
        if (fp) {
          var fc = getPathCenter(fp);
          routeStart.setAttribute('cx', fc.x);
          routeStart.setAttribute('cy', fc.y);
          routeStart.setAttribute('opacity', '1');
        }
        routeLine.setAttribute('opacity', '0');
        routeEnd.setAttribute('opacity', '0');
      } else if (toSlug) {
        resetDistricts();
        highlightDistrict(toSlug, '#25D366');
        var tp = svg.querySelector('[data-district="' + toSlug + '"]');
        if (tp) {
          var tc = getPathCenter(tp);
          routeEnd.setAttribute('cx', tc.x);
          routeEnd.setAttribute('cy', tc.y);
          routeEnd.setAttribute('opacity', '1');
        }
        routeLine.setAttribute('opacity', '0');
        routeStart.setAttribute('opacity', '0');
      }
    }

    if (fromSelect) fromSelect.addEventListener('change', updateMap);
    if (toSelect) toSelect.addEventListener('change', updateMap);

    // Hover effect on paths
    districtPaths.forEach(function(path) {
      path.addEventListener('mouseenter', function() {
        if (this.getAttribute('fill') === '#E2E8F0') {
          this.setAttribute('fill', '#DBEAFE');
          this.setAttribute('stroke', '#60A5FA');
        }
      });
      path.addEventListener('mouseleave', function() {
        if (this.getAttribute('fill') === '#DBEAFE') {
          this.setAttribute('fill', '#E2E8F0');
          this.setAttribute('stroke', '#94A3B8');
        }
      });
    });
  }

  // ===== SMOOTH SCROLL =====
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ===== GTM DATALAYER — EVENT TRACKING =====
  window.dataLayer = window.dataLayer || [];

  // Track form submissions
  function trackEvent(eventName, eventData) {
    window.dataLayer.push(Object.assign({ event: eventName }, eventData || {}));
  }

  // Quote form step 1 completion tracking
  if (formNextBtn) {
    var origNextClick = formNextBtn.onclick;
    formNextBtn.addEventListener('click', function() {
      var nameInput = formStep1 ? formStep1.querySelector('[name="name"]') : null;
      var phoneInput = formStep1 ? formStep1.querySelector('[name="phone"]') : null;
      if (nameInput && phoneInput && nameInput.value.trim() && phoneInput.value.trim()) {
        trackEvent('form_step_complete', {
          form_name: 'quote_form',
          step: 1,
          step_name: 'kisisel_bilgiler'
        });
      }
    });
  }

  // Quote form submit tracking (wrap existing)
  if (quoteForm) {
    quoteForm.addEventListener('submit', function() {
      trackEvent('form_submit', {
        form_name: 'quote_form',
        form_type: 'whatsapp_redirect',
        page_location: window.location.pathname
      });
    });
  }

  // Contact form submit tracking
  if (contactForm) {
    contactForm.addEventListener('submit', function() {
      trackEvent('form_submit', {
        form_name: 'contact_form',
        form_type: 'whatsapp_redirect',
        page_location: window.location.pathname
      });
    });
  }

  // WhatsApp click tracking — all wa.me links
  document.querySelectorAll('a[href*="wa.me"]').forEach(function(link) {
    link.addEventListener('click', function() {
      var location = 'unknown';
      if (this.closest('.hero')) location = 'hero';
      else if (this.closest('.cta-banner')) location = 'cta_banner';
      else if (this.closest('.footer')) location = 'footer';
      else if (this.closest('.whatsapp-float')) location = 'floating_button';
      else if (this.closest('.mobile-cta-bar')) location = 'mobile_cta_bar';
      trackEvent('whatsapp_click', {
        click_location: location,
        page_location: window.location.pathname
      });
    });
  });

  // Phone call tracking — all tel: links
  document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {
    link.addEventListener('click', function() {
      var location = 'unknown';
      if (this.closest('.header')) location = 'header';
      else if (this.closest('.hero')) location = 'hero';
      else if (this.closest('.cta-banner')) location = 'cta_banner';
      else if (this.closest('.footer')) location = 'footer';
      else if (this.closest('.phone-float')) location = 'floating_button';
      else if (this.closest('.mobile-cta-bar')) location = 'mobile_cta_bar';
      trackEvent('phone_click', {
        click_location: location,
        phone_number: '05365805059',
        page_location: window.location.pathname
      });
    });
  });

  // ===== EXIT-INTENT POP-UP =====
  var exitPopupShown = false;
  var exitPopupEl = null;

  function createExitPopup() {
    var overlay = document.createElement('div');
    overlay.className = 'exit-popup-overlay';
    overlay.innerHTML =
      '<div class="exit-popup">' +
        '<button class="exit-popup-close" aria-label="Kapat">&times;</button>' +
        '<div class="exit-popup-icon"><i class="fab fa-whatsapp"></i></div>' +
        '<h3>Bekleyin! Gitmeden teklif alın</h3>' +
        '<p>Ücretsiz ekspertiz ve anında <strong>sabit fiyat teklifi</strong> için WhatsApp\'tan yazın. Bağlayıcı değildir.</p>' +
        '<a href="https://wa.me/905365805059?text=Merhaba%2C%20siteden%20ayr%C4%B1lmadan%20%C3%BCcretsiz%20teklif%20almak%20istiyorum." class="btn btn-whatsapp btn-lg exit-popup-cta" target="_blank">' +
          '<i class="fab fa-whatsapp"></i> WhatsApp ile Ücretsiz Teklif Al' +
        '</a>' +
        '<span class="exit-popup-dismiss">Teşekkürler, ilgilenmiyorum</span>' +
      '</div>';

    document.body.appendChild(overlay);
    exitPopupEl = overlay;

    // Animate in
    setTimeout(function() { overlay.classList.add('show'); }, 10);

    // Close handlers
    overlay.querySelector('.exit-popup-close').addEventListener('click', closeExitPopup);
    overlay.querySelector('.exit-popup-dismiss').addEventListener('click', closeExitPopup);
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closeExitPopup();
    });

    // Track
    trackEvent('exit_intent_shown', { page_location: window.location.pathname });

    // CTA click tracking
    overlay.querySelector('.exit-popup-cta').addEventListener('click', function() {
      trackEvent('exit_intent_click', {
        action: 'whatsapp_click',
        page_location: window.location.pathname
      });
      setTimeout(closeExitPopup, 500);
    });
  }

  function closeExitPopup() {
    if (exitPopupEl) {
      exitPopupEl.classList.remove('show');
      setTimeout(function() {
        if (exitPopupEl && exitPopupEl.parentNode) {
          exitPopupEl.parentNode.removeChild(exitPopupEl);
        }
      }, 400);
    }
  }

  // Trigger: mouse leaves viewport top (desktop only)
  if (window.innerWidth > 768) {
    document.addEventListener('mouseleave', function(e) {
      if (e.clientY < 5 && !exitPopupShown) {
        exitPopupShown = true;
        // Wait 5 seconds after page load before allowing popup
        if (performance.now() > 5000) {
          createExitPopup();
        }
        // Also store in session so it won't fire again
        try { sessionStorage.setItem('exitPopupShown', '1'); } catch(err) {}
      }
    });
    // Check if already shown this session
    try {
      if (sessionStorage.getItem('exitPopupShown')) exitPopupShown = true;
    } catch(err) {}
  }

  // ===== GOOGLE REVIEW WIDGET =====
  // Insert clickable Google review badge near the form
  var heroRight = document.querySelector('.hero-right');
  if (heroRight) {
    var reviewWidget = document.createElement('a');
    reviewWidget.href = 'https://g.page/tasyolnakliyat/review';
    reviewWidget.target = '_blank';
    reviewWidget.rel = 'noopener noreferrer';
    reviewWidget.className = 'google-review-widget';
    reviewWidget.innerHTML =
      '<div class="grw-left">' +
        '<svg class="grw-google-icon" width="20" height="20" viewBox="0 0 24 24">' +
          '<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>' +
          '<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>' +
          '<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>' +
          '<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>' +
        '</svg>' +
        '<div class="grw-stars"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>' +
      '</div>' +
      '<div class="grw-right">' +
        '<span class="grw-score">4.9</span>' +
        '<span class="grw-count">127+ Google Yorumu</span>' +
      '</div>' +
      '<i class="fas fa-external-link-alt grw-arrow"></i>';

    // Insert after the form
    heroRight.appendChild(reviewWidget);

    // Track click
    reviewWidget.addEventListener('click', function() {
      trackEvent('google_review_click', { page_location: window.location.pathname });
    });
  }

});
