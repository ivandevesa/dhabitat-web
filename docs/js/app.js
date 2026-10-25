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

  /* Calculadora hipotecaria completa (compra en Cataluña) */
  var mc = $(".mc");
  if (mc) {
    var $id = function (i) { return document.getElementById(i); };
    var val = function (i) { var v = parseFloat($id(i).value); return isFinite(v) ? v : 0; };
    var eur = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " €"; };
    var pct = function (n, d) { return n.toLocaleString("es-ES", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }) + " %"; };
    var cuotaDe = function (L, tin, y) {
      var n = y * 12, r = tin / 100 / 12;
      if (L <= 0 || n <= 0) return 0;
      return r === 0 ? L / n : L * r / (1 - Math.pow(1 + r, -n));
    };
    var itpCat = function (P) {
      var t = [[600000, 0.10], [900000, 0.11], [1500000, 0.12], [Infinity, 0.13]], prev = 0, s = 0, i;
      for (i = 0; i < t.length && P > prev; i++) { s += (Math.min(P, t[i][0]) - prev) * t[i][1]; prev = t[i][0]; }
      return s;
    };
    var run = function () {
      var P = val("m-precio"), S = val("m-ahorro"), inc = val("m-ingresos"), deb = val("m-deudas"), edad = val("m-edad"),
          anos = val("m-anos"), seg = val("m-seg"), nueva = $id("m-tipo").value === "nueva", hab = $id("m-uso").value === "hab",
          perfil = $id("m-perfil").value, modo = $id("m-modo").value;
      var tin = modo === "var" ? val("m-eur") + val("m-dif") : val("m-tin");
      var notes = [], reduc = hab && perfil !== "no";
      var plazoMax = Math.max(1, Math.min(40, 75 - edad));
      var y = anos; if (y > plazoMax) { y = plazoMax; notes.push("Por tu edad, el plazo máximo orientativo es de " + plazoMax + " años: la simulación usa " + plazoMax + "."); }
      var LTV = hab ? 0.8 : 0.7;
      var gastos = function (price) {
        var imp, impL;
        if (nueva) { imp = price * 0.10 + ((reduc && perfil === "joven") ? 0 : price * 0.015); impL = "IVA (10 %) y AJD" + ((reduc && perfil === "joven") ? " bonificado" : " (1,5 %)"); }
        else if (reduc) { imp = price * 0.05; impL = "ITP reducido (5 %)"; }
        else { imp = itpCat(price); impL = "ITP en Cataluña" + (price > 0 ? " (" + pct(imp / price * 100, 1) + ")" : ""); }
        var otros = price * 0.012, tas = 400;
        return { imp: imp, impL: impL, otros: otros, tas: tas, tot: imp + otros + tas };
      };
      var g = gastos(P), need = Math.max(0, P + g.tot - S);
      var q = cuotaDe(need, tin, y) + (need > 0 ? seg : 0);
      var ratio = inc > 0 ? (q + deb) / inc : 9;
      var shortage = Math.max(0, need - LTV * P);
      var cap = Math.min(need, LTV * P);
      var inter = cuotaDe(need, tin, y) * y * 12 - need;
      /* resultado */
      $id("r-cuota").textContent = eur(q);
      $id("r-precio").textContent = eur(P);
      $id("r-imp-l").textContent = g.impL; $id("r-imp").textContent = eur(g.imp);
      $id("r-otros").textContent = eur(g.otros); $id("r-tas").textContent = eur(g.tas);
      $id("r-gastos").textContent = eur(g.tot); $id("r-aho").textContent = eur(S);
      $id("r-hip").textContent = eur(need); $id("r-ltv").textContent = P > 0 ? pct(need / P * 100, 0) : "0 %";
      $id("r-int").textContent = eur(Math.max(0, inter)); $id("r-total").textContent = eur(need + Math.max(0, inter));
      var bar = $id("c-bar"); if (bar) bar.style.width = need > 0 ? Math.max(4, Math.min(100, need / (need + inter) * 100)) + "%" : "100%";
      $id("r-ratio").textContent = inc > 0 ? pct(ratio * 100, 1) : "—";
      var gf = $id("r-gfill"); gf.style.width = Math.min(100, ratio / 0.5 * 100) + "%";
      var state = (shortage > 0 || ratio > 0.35) ? "bad" : ratio > 0.30 ? "warn" : "ok";
      gf.className = state;
      var vd = $id("r-verdict"); vd.className = "verdict " + state;
      vd.textContent = state === "ok" ? "Operación viable" : state === "warn" ? "Viable, pero ajustada" : "No viable con estos datos";
      var mv = $id("mini-v"); if (mv) { mv.className = "verdict " + state; mv.textContent = state === "ok" ? "Viable" : state === "warn" ? "Ajustada" : "No viable"; $id("mini-q").textContent = eur(q) + "/mes"; }
      /* máximo asumible (búsqueda por bisección) */
      var qmax = 0.35 * inc - deb - seg, r = tin / 100 / 12, n = y * 12;
      var Lmax = qmax > 0 ? (r === 0 ? qmax * n : qmax * (1 - Math.pow(1 + r, -n)) / r) : 0;
      var lo = 0, hi = 5000000, mid, ok, i;
      for (i = 0; i < 50; i++) {
        mid = (lo + hi) / 2; var nd = mid + gastos(mid).tot - S;
        ok = nd <= LTV * mid && nd <= Lmax; if (ok) lo = mid; else hi = mid;
      }
      var Pmax = Math.floor(lo / 1000) * 1000, Lm = Math.max(0, Pmax + gastos(Pmax).tot - S);
      $id("r-max").textContent = Pmax >= 20000 ? "Vivienda de hasta " + eur(Pmax) : "Con estos datos aún no llegas";
      $id("r-maxd").textContent = Pmax >= 20000 ? "con una hipoteca de unos " + eur(Lm) + " y la cuota dentro del 35 %" : "Prueba a aportar más ahorro, ampliar el plazo o reducir deudas.";
      /* avisos */
      if (shortage > 0) notes.push("Te faltan unos " + eur(shortage) + " de ahorro: el banco financia como máximo el " + pct(LTV * 100) + " del valor y tú pones el resto más los gastos.");
      else if (P > 0) notes.push("Ahorro mínimo para esta compra: " + eur(P - LTV * P + g.tot) + " (entrada del " + pct((1 - LTV) * 100) + " más gastos).");
      if (ratio > 0.35 && inc > 0) notes.push("Tu cuota más deudas es el " + pct(ratio * 100, 1) + " de tus ingresos; el límite recomendado es el 35 %. Necesitarías unos " + eur((q + deb) / 0.35) + " netos al mes.");
      else if (ratio > 0.30) notes.push("Estás por encima del 30 % de endeudamiento: cualquier imprevisto te dejaría con poco margen.");
      if (modo === "var") notes.push("Si el Euríbor subiera un punto, tu cuota pasaría a unos " + eur(cuotaDe(need, tin + 1, y) + seg) + " al mes.");
      if (perfil !== "no" && !hab) notes.push("El tipo reducido solo se aplica a la vivienda habitual.");
      if (nueva && perfil !== "no" && perfil !== "joven" && hab) notes.push("En obra nueva el IVA no se reduce; solo se bonifica el AJD a los jóvenes de 35 años o menos.");
      $id("r-notes").innerHTML = notes.map(function (t) { return "<li>" + t.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</li>"; }).join("");
      mc._summary = "Simulación en la calculadora de D&Habitat:\n" +
        "- Precio: " + eur(P) + " (" + (nueva ? "obra nueva" : "segunda mano") + ", " + (hab ? "vivienda habitual" : "segunda residencia") + ")\n" +
        "- Ahorros: " + eur(S) + " · Ingresos netos: " + eur(inc) + "/mes · Otras deudas: " + eur(deb) + "/mes · Edad: " + edad + "\n" +
        "- Hipoteca: " + eur(need) + " a " + y + " años, " + (modo === "var" ? "variable (Euríbor " + val("m-eur") + " % + " + val("m-dif") + " %)" : "fijo " + val("m-tin") + " %") + "\n" +
        "- Cuota estimada: " + eur(q) + "/mes · Endeudamiento: " + pct(ratio * 100, 1) + " · Gastos de compra: " + eur(g.tot) + "\n";
    };
    /* sincronía número ↔ deslizador */
    $$("input[type=number]", mc).forEach(function (num) {
      var rng = document.getElementById(num.id + "-r");
      if (rng) {
        rng.addEventListener("input", function () { num.value = rng.value; run(); });
        num.addEventListener("input", function () { rng.value = num.value; });
      }
      num.addEventListener("input", run);
    });
    $$("select", mc).forEach(function (el) { el.addEventListener("change", function () {
      if (el.id === "m-modo") { $id("m-fijo-f").hidden = el.value === "var"; $id("m-var-f").hidden = el.value !== "var"; }
      if (el.id === "m-tipo") { $id("m-perfil-f").querySelector(".hint").textContent = el.value === "nueva" ? "En obra nueva se paga IVA (10 %) y AJD (1,5 %); a los jóvenes de 35 años o menos se les bonifica el AJD si es vivienda habitual y no superan 36.000 € de base." : "En Cataluña el ITP baja del 10 % al 5 % en vivienda habitual si la base imponible no supera 36.000 € (se comprueba en la liquidación)."; }
      run();
    }); });
    var send = $id("r-send");
    if (send) send.addEventListener("click", function () {
      var ta = $("#estudio textarea"), box = $id("estudio");
      if (ta) { ta.value = mc._summary || ""; ta.dispatchEvent(new Event("input", { bubbles: true })); }
      if (box) box.scrollIntoView({ behavior: "smooth", block: "start" });
      var nm = $("#estudio input[name=nombre]"); if (nm) setTimeout(function () { nm.focus({ preventScroll: true }); }, 500);
    });
    run();
  }

  /* Camino dinámico de pasos: la ruta se dibuja y el marcador avanza al hacer scroll */
  $$("[data-way]").forEach(function (way) {
    var list = $(".way-list", way), wrap = $(".way-wrap", way), base = $(".way-base", way), prog = $(".way-prog", way), pin = $(".way-pin", way);
    var lis = $$("li", list), still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!list || !base || !pin) return;
    way.classList.add("js");
    var L = 1, marks = [], cur = 0, target = 0;
    var build = function () {
      var o = wrap.getBoundingClientRect(), pts = lis.map(function (li) {
        var r = $(".way-dot", li).getBoundingClientRect();
        return { x: r.left - o.left + r.width / 2, y: r.top - o.top + r.height / 2 };
      });
      if (pts.length < 2) return;
      var horiz = Math.abs(pts[1].x - pts[0].x) > Math.abs(pts[1].y - pts[0].y);
      var d = "M" + pts[0].x + " " + pts[0].y;
      for (var i = 1; i < pts.length; i++) {
        var a = pts[i - 1], c = pts[i];
        d += horiz
          ? " C" + (a.x + (c.x - a.x) / 2) + " " + a.y + " " + (a.x + (c.x - a.x) / 2) + " " + c.y + " " + c.x + " " + c.y
          : " C" + a.x + " " + (a.y + (c.y - a.y) / 2) + " " + c.x + " " + (a.y + (c.y - a.y) / 2) + " " + c.x + " " + c.y;
      }
      base.setAttribute("d", d); prog.setAttribute("d", d);
      L = base.getTotalLength();
      prog.style.strokeDasharray = L; 
      marks = pts.map(function (pt) {
        var best = 0, bd = 1e9;
        for (var k = 0; k <= 240; k++) {
          var q = base.getPointAtLength(L * k / 240), dd = Math.pow(q.x - pt.x, 2) + Math.pow(q.y - pt.y, 2);
          if (dd < bd) { bd = dd; best = k / 240; }
        }
        return best;
      });
      draw();
    };
    var draw = function () {
      var q = base.getPointAtLength(L * cur);
      prog.style.strokeDashoffset = L * (1 - cur);
      pin.style.transform = "translate(" + q.x + "px," + q.y + "px)";
      var idx = -1;
      lis.forEach(function (li, i) {
        var on = cur >= marks[i] - 0.004; li.classList.toggle("on", on); if (on) idx = i;
        li.classList.toggle("cur", i === idx && cur < (marks[i + 1] === undefined ? 2 : marks[i + 1]) - 0.004);
      });
    };
    var calcTarget = function () {
      var r = way.getBoundingClientRect(), vh = window.innerHeight;
      var t = (vh * 0.82 - r.top - wrap.offsetTop) / (wrap.offsetHeight * 0.8 + vh * 0.1);
      target = Math.max(0, Math.min(1, t));
    };
    var raf = 0, tick = function () {
      raf = 0; calcTarget();
      var diff = target - cur;
      if (still) cur = target; else cur += diff * 0.09;
      if (Math.abs(target - cur) < 0.0015) cur = target;
      draw();
      if (cur !== target) raf = requestAnimationFrame(tick);
    };
    var kick = function () { if (!raf) raf = requestAnimationFrame(tick); };
    window.addEventListener("scroll", kick, { passive: true });
    window.addEventListener("resize", function () { build(); kick(); });
    if ("ResizeObserver" in window) new ResizeObserver(function () { build(); kick(); }).observe(wrap);
    build(); calcTarget(); cur = still ? 1 : 0; if (still) target = 1; draw(); kick();
  });

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
