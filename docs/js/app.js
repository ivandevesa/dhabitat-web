/* D&Habitat — JS mínimo (sin dependencias). Configuración en config.js */
(function () {
  "use strict";
  var CFG = window.DH || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Siempre al principio de la página: al entrar, al volver atrás y al pulsar el enlace de la página actual */
  try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) {}
  var toTop = function () { if (!location.hash) window.scrollTo(0, 0); };
  toTop();
  window.addEventListener("pageshow", function (e) { if (e.persisted) toTop(); });
  var norm = function (p) { return p.replace(/index\.html$/, "").replace(/\/+$/, "/"); };
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank") return;
    if (a.origin !== location.origin || a.hash) return;
    if (norm(a.pathname) === norm(location.pathname) && a.search === location.search) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
      if (nav) nav.classList.remove("open");
    }
  });

  /* Menú móvil */
  var tg = $(".nav-toggle"), nav = $("#nav");
  if (tg && nav) {
    tg.addEventListener("click", function () {
      var o = nav.classList.toggle("open");
      tg.setAttribute("aria-expanded", o ? "true" : "false");
    });
  }
  /* Desplegable «Comprar» */
  $$(".dd").forEach(function (dd) {
    var b = $(".dd-btn", dd);
    var set = function (o) { dd.classList.toggle("open", o); b.setAttribute("aria-expanded", o ? "true" : "false"); };
    b.addEventListener("click", function () { set(!dd.classList.contains("open")); });
    document.addEventListener("click", function (e) { if (!dd.contains(e.target)) set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { set(false); b.focus(); } });
  });
  var hdr = $(".hdr");
  if (hdr) {
    var f = function () { hdr.classList.toggle("scrolled", window.scrollY > 8); };
    f(); window.addEventListener("scroll", f, { passive: true });
  }

  /* Imágenes que no cargan: se quitan y queda el fondo de reserva */
  $$(".ph img").forEach(function (im) {
    if (im.complete && im.naturalWidth === 0) im.remove();
    im.addEventListener("error", function () { im.remove(); });
  });


  /* Galería de ficha: visor + miniaturas + ampliación */
  $$("[data-gal]").forEach(function (g) {
    var main = $(".gal-main > img", g), cnt = $(".gal-count", g), thumbs = $$(".gal-thumbs button", g);
    var lb = $(".gal-lb", g), lbi = lb && $("img", lb), lbc = lb && $(".gal-count", lb);
    var n = thumbs.length, cur = 0;
    var src = function (i) { return thumbs[i].getAttribute("data-full"); };
    var show = function (i) {
      cur = (i + n) % n;
      main.src = src(cur); main.alt = thumbs[cur].getAttribute("data-alt") || "";
      cnt.textContent = (cur + 1) + " / " + n;
      thumbs.forEach(function (b, k) { b.setAttribute("aria-current", k === cur ? "true" : "false"); });
      var t = thumbs[cur], box = t.parentNode.parentNode;
      box.scrollTo({ left: t.parentNode.offsetLeft - (box.clientWidth - t.offsetWidth) / 2, behavior: "smooth" });
      if (lb && lb.open) { lbi.src = src(cur); lbc.textContent = (cur + 1) + " / " + n; }
      var nx = new Image(); nx.src = src((cur + 1) % n);
    };
    thumbs.forEach(function (b, k) { b.addEventListener("click", function () { show(k); }); });
    $$(".gal-nav.prev", g).forEach(function (b) { b.addEventListener("click", function () { show(cur - 1); }); });
    $$(".gal-nav.next", g).forEach(function (b) { b.addEventListener("click", function () { show(cur + 1); }); });
    var open = function () { if (lb && lb.showModal) { lb.showModal(); lbi.src = src(cur); lbi.alt = main.alt; lbc.textContent = (cur + 1) + " / " + n; } };
    main.addEventListener("click", open);
    var z = $(".gal-zoom", g); if (z) z.addEventListener("click", open);
    if (lb) {
      $(".lb-x", lb).addEventListener("click", function () { lb.close(); });
      lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-in")) lb.close(); });
    }
    g.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { show(cur - 1); } else if (e.key === "ArrowRight") { show(cur + 1); }
    });
    var x0 = null;
    var wrap = $(".gal-main", g);
    wrap.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    wrap.addEventListener("touchend", function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
    });
    show(0);
  });

  /* Filtros del listado */
  var list = $("#listado");
  if (list) {
    var cards = $$(".pc", list);
    var fp = $("#f-poblacion"), ft = $("#f-tipo"), fm = $("#f-max"), fo = $("#f-orden");
    var cnt = $("#f-count"), empty = $("#f-empty");
    var qs = new URLSearchParams(location.search);
    if (qs.get("poblacion") && fp) fp.value = qs.get("poblacion");
    if (qs.get("tipo") && ft) ft.value = qs.get("tipo");
    if (qs.get("max") && fm) fm.value = qs.get("max");
    var apply = function () {
      var p = fp ? fp.value : "", t = ft ? ft.value : "", m = fm && fm.value ? +fm.value : 0;
      var shown = cards.filter(function (c) {
        var ok = (!p || c.dataset.poblacion === p) && (!t || c.dataset.tipo === t) && (!m || +c.dataset.precio <= m);
        c.hidden = !ok; return ok;
      });
      var o = fo ? fo.value : "";
      if (o) {
        var sorted = cards.slice().sort(function (a, b) {
          return o === "asc" ? a.dataset.precio - b.dataset.precio : b.dataset.precio - a.dataset.precio;
        });
        sorted.forEach(function (c) { list.appendChild(c); });
      }
      if (cnt) cnt.textContent = shown.length + (shown.length === 1 ? " inmueble" : " inmuebles");
      if (empty) empty.hidden = shown.length > 0;
    };
    [fp, ft, fm, fo].forEach(function (el) { if (el) el.addEventListener("change", apply); });
    apply();
  }

  /* Calculadora hipotecaria (cuota constante, sistema francés) */
  var calc = $("#calc");
  if (calc) {
    var fmt = function (n) { return n.toLocaleString("es-ES", { maximumFractionDigits: 0 }) + " €"; };
    var run = function () {
      var P = +$("#c-importe").value, y = +$("#c-anos").value, i = +$("#c-tipo").value / 100;
      var n = y * 12, r = i / 12, q;
      if (!(P > 0) || !(n > 0)) return;
      q = r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n));
      $("#c-cuota").textContent = fmt(q);
      $("#c-int").textContent = fmt(q * n - P);
      $("#c-total").textContent = fmt(q * n);
    };
    $$("input", calc).forEach(function (el) { el.addEventListener("input", run); });
    run();
  }

  /* Analítica (solo con consentimiento y si hay ID de GA4) */
  function track(name, params) {
    if (window.gtag) window.gtag("event", name, params || {});
  }
  function loadGA() {
    if (!CFG.GA4_ID || window.gtag) return;
    var s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CFG.GA4_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date()); window.gtag("config", CFG.GA4_ID, { anonymize_ip: true });
  }
  var banner = $("#cookies"), choice = null;
  try { choice = localStorage.getItem("dh-cookies"); } catch (e) {}
  if (choice === "yes") loadGA();
  else if (!choice && banner && CFG.GA4_ID) banner.hidden = false;
  $$("[data-cookie]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.dataset.cookie;
      try { localStorage.setItem("dh-cookies", v); } catch (e) {}
      banner.hidden = true; if (v === "yes") loadGA();
    });
  });
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener("click", function () { track("click_llamada"); }); });

  /* Formularios */
  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if ($(".hp input", form) && $(".hp input", form).value) return;
      var show = function (t) { msg.textContent = t; msg.hidden = false; };
      if (!CFG.FORM_ENDPOINT) {
        show("Esta versión de demostración todavía no envía formularios. Para que te atendamos ahora, llama al 931 70 41 89.");
        return;
      }
      var data = new FormData(form); data.append("origen", form.dataset.form);
      fetch(CFG.FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset(); show("Gracias. Hemos recibido tu mensaje y te llamaremos lo antes posible.");
          track("generate_lead", { form: form.dataset.form });
        })
        .catch(function () { show("No hemos podido enviar el mensaje. Inténtalo de nuevo o llama al 931 70 41 89."); });
    });
  });
})();
