#!/usr/bin/env python3
"""Generador del sitio estático de D&Habitat by Finance.
Uso: python3 build.py <carpeta_salida> [--preview]
--preview añade index.html a los enlaces para poder navegar sin servidor."""
import sys, os, re, html, json, shutil, unicodedata

PREVIEW = "--preview" in sys.argv
OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.dhabitat.es"
TODAY = "2026-10-24"
UP = "https://www.dhabitat.es/wp-content/uploads/"
PHONE, TEL = "931 70 41 89", "+34931704189"
MAPS = "https://www.google.com/maps/search/?api=1&query=D%26HABITAT+by+FINANCE+Terrassa"
FB = "https://www.facebook.com/dhabitatinmobiliaria/"
IG = "https://www.instagram.com/dhabitat.es/"
BRAND = "D&Habitat by Finance"
LOGO_URL = SITE + "/img/l/icon-512.png"
AICAT_URL = "https://www.dhabitat.es/wp-content/themes/dhabitat/dist/img/logo-aicat.png"


def esc(s): return html.escape(str(s), quote=True)
def eur(n): return f"{n:,.0f}".replace(",", ".") + " €"
def num(n): return f"{n:,.0f}".replace(",", ".")
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
def jl(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def href(path, depth):
    pre = "../" * depth if depth else "./"
    if PREVIEW and (path == "" or path.endswith("/")):
        return pre + path + "index.html"
    return pre + path


# ───────────────────────── Datos de inmuebles (cartera publicada en dhabitat.es, 24/10/2026)
def loc(u):
    """URL remota -> ruta local relativa (img/...). Si no hay copia local devuelve la URL tal cual."""
    if not u: return u
    if u.startswith(UP):
        r = "img/s/" + u[len(UP):]
    else:
        m = re.search(r"/(\d+)\.510396/", u)
        r = "img/p/" + m.group(1) + ".jpg" if m else None
    if r and os.path.exists(os.path.join(HERE, "assets", r)): return r
    return u

def absu(u):
    l = loc(u)
    return u if l == u or not u else SITE + "/" + l

def fs(code, name): return f"https://fotoshs.imghs.net/3xl/510396/{code}.510396/{name}"
TIPO = {"piso": "Piso", "casa": "Casa", "parking": "Plaza de parking", "solar": "Solar", "local": "Local comercial"}
PLURAL = {"piso": "Pisos", "casa": "Casas", "parking": "Parkings", "solar": "Solares", "local": "Locales"}

def P(ref, tipo, muni, zona, precio, m2, hab, ban, img, txt, ocup=False, nota=""):
    return dict(ref=ref, tipo=tipo, muni=muni, zona=zona, precio=precio, m2=m2, hab=hab, ban=ban, img=img, txt=txt, ocup=ocup, nota=nota)

PROPS = [
 # ── Terrassa
 P("0110705","casa","Terrassa","Vista Alegre",695900,197,2,1,fs("65875159215","510396_65875159215_80311080-2cb6-4087-af2f-0073883364e7.jpg"),
   "Casa de 197 m² construidos en Vista Alegre, una de las zonas más tranquilas y con más privacidad de Terrassa. Pensada para quien busca amplitud, confort y un entorno residencial sosegado."),
 P("0110699","piso","Terrassa","Cementiri Vell",315000,103,3,2,fs("65867548367","510396_65867548367_25_20260724120812640.jpg"),
   "Piso de 103 m² con 3 habitaciones y 2 baños frente al Parc de Vallparadís, en el barrio de Cementiri Vell. Luz, amplitud y un entorno ideal para disfrutar de la naturaleza sin salir de Terrassa."),
 P("0110696","piso","Terrassa","Pere Parres",305000,81,2,1,fs("65045702060","510396_65045702060_f5ae616e-76f8-40b9-9fef-bcc665efe76e.jpg"),
   "Planta baja luminosa y acogedora en el barrio consolidado de Pere Parres. 81 m² con 2 habitaciones y 1 baño, para quien busca comodidad, amplitud y espacios exteriores sin alejarse de los servicios."),
 P("0110692","piso","Terrassa","Poble Nou-Zona Olímpica",345000,112,4,2,fs("65050676111","510396_65050676111_06faff21-d795-4ee9-b97f-f4c6d2d59832.jpg"),
   "Piso amplio de 112 m² con 4 habitaciones y 2 baños en la Zona Esportiva de Terrassa. Incluye piscina, parking y trastero en una ubicación muy cotizada."),
 P("0110687","piso","Terrassa","Sant Pere",212100,56,1,1,fs("64222250296","510396_64222250296_2963b1cd-2398-4f1d-a0db-cb0dee616ffa.jpg"),
   "Piso moderno de 56 m², construido en 2025 y listo para entrar a vivir, en la zona de Sant Pere. Salón-comedor luminoso con cocina americana integrada y una habitación."),
 P("0110672","piso","Terrassa","Poble Nou-Zona Olímpica",259000,93,3,1,fs("62543987005","510396_62543987005_63b79f26-1603-4af9-ab82-88b03d053d17.jpg"),
   "Planta baja de 93 m² a reformar en la Zona Olímpica, con jardín. Tres habitaciones y un baño para diseñarla completamente a tu gusto. Inmueble en exclusiva de D&Habitat."),
 P("019061","piso","Terrassa","Torre-sana",69000,70,1,1,fs("57548792106","510396_57548792106_8a208b8c-6811-4aa6-8151-56aab55a67bb.jpg"),
   "Vivienda de 70 m² según Catastro, con salón-cocina, un dormitorio y un baño. Pensada para inversores.",ocup=True,
   nota="Inmueble ocupado por una persona sin justo título. Por su estado ocupacional no admite visitas."),
 P("019060v","piso","Terrassa","Sant Pere Nord",66000,90,3,1,fs("57535581102","510396_57535581102_03241571-9cdc-4309-90e7-90e74c1d3bc5.jpg"),
   "Luminosa vivienda de 90 m² según Catastro, elementos comunes incluidos, con salón-comedor, tres dormitorios y un baño. Pensada para inversores.",ocup=True,
   nota="Inmueble ocupado por una persona sin justo título. Por su estado ocupacional no admite visitas."),
 P("0310517","solar","Terrassa","Can Parellada",189700,506,0,0,fs("48402136053","510396_48402136053_19574445-5842-4b9c-b787-5339966dea2b.jpg"),
   "Solar residencial completamente llano de 506 m², con 20 m de fachada por 36 m de fondo, en una buena zona de Terrassa. Ideal para construir tu proyecto."),
 P("0310359","solar","Terrassa","Can Palet de Vista Alegre",108500,400,0,0,fs("36766153475","510396_36766153475_6_20230802130247587.jpg"),
   "Parcela de 400 m² en Can Palet de Vista Alegre, a pie de la carretera de Martorell. Totalmente urbanizada y con todos los servicios."),
 P("037028","solar","Terrassa","Les Fonts",410000,2700,0,0,None,
   "Terreno de 2.700 m² en una magnífica zona de Les Fonts de Terrassa."),
 P("0310300","local","Terrassa","Pere Parres",162100,116,0,2,fs("33354607938","510396_33354607938_1_20230419174232033.jpg"),
   "Local de 116 m² construidos en Pere Parres. Es un bar restaurante de decoración moderna y elegante, con licencia."),
 P("0310299","local","Terrassa","Ègara",149000,140,0,1,None,
   "Local de 140 m² en Ègara, actualmente un bar musical. Espacio diáfano."),
 P("10517","parking","Terrassa","Sant Pere",13500,12,0,0,fs("49242800072","510396_49242800072_98a3cadb-f487-41f0-86ce-94d330921146.jpg"),
   "Plaza de aparcamiento de 12 m² en una zona de Terrassa cercana al Mercat Municipal El Triumf de Sant Pere y al club de natación."),
 P("0110521","parking","Terrassa","Sant Pere",16900,11,0,0,fs("48368837431","510396_48368837431_c27547e5-82cb-46a2-b66e-8b40e77852ef.jpg"),
   "Plaza de aparcamiento de 11 m² en la calle Transversal, junto al Mercat Municipal El Triumf de Sant Pere, el segundo mercado más antiguo de Terrassa."),
 P("0410495","parking","Terrassa","Sant Pere",14500,12,0,0,None,
   "Gran plaza de parking de 12 m² en Sant Pere, con muy fácil acceso desde la calle. Está en la planta 2."),
 P("0310427","parking","Terrassa","Sant Pere",10500,12,0,0,fs("42529279413","510396_42529279413_3_20240313161045992.jpg"),
   "Plaza de parking de 12 m² en la calle Francesc Oller, en Sant Pere, con muy fácil acceso desde la calle. Está en la planta -2."),
 P("0310628","parking","Terrassa","Can Parellada",9900,8,0,0,fs("58417330740","510396_58417330740_767e22c4-2331-47aa-b90b-a38ecb006fc1.jpg"),
   "Siete plazas de aparcamiento en el polígono industrial de Can Parellada, a la venta o en alquiler. Cada plaza tiene 8 m² y está dispuesta en oblicuo, lo que facilita las maniobras de entrada y salida.",
   nota="Pregunta por las condiciones de venta o alquiler de cada plaza."),
 P("036413","parking","Terrassa","Pere Parres",12000,8,0,0,fs("681005918","510396_036413_foto_1_681005918_20180730101417.jpg"),
   "Plaza de parking para un coche en la zona de Pere Parres. 8 m²."),
 # ── Rubí
 P("0010703","casa","Rubí","Els Avets",380000,210,2,2,fs("65869703682","510396_65869703682_ebe22e1e-de3a-422f-a7d6-7717e82cd9fc.jpg"),
   "Casa adosada de 210 m² construidos, totalmente reformada, en la zona residencial de Els Avets, un entorno tranquilo de Rubí. Inmueble en exclusiva de D&Habitat."),
 P("0110702","piso","Rubí","Els Avets - Can Serrafossà - Ximelis",230000,100,3,1,fs("65921680795","510396_65921680795_15edaa58-963c-423c-92d1-a5149fd750db.jpg"),
   "Piso de 100 m² con 3 habitaciones en una zona residencial tranquila y consolidada de Rubí, ideal para vivir en familia."),
 P("0010446","casa","Rubí","Sant Muç",500000,400,6,4,fs("65066824944","510396_65066824944_b98ce58c-07a5-4eb5-abf8-888c55e67d14.jpg"),
   "Propiedad en Sant Muç formada por dos viviendas independientes pero pareadas, todo en planta, con 370 m² construidos. Una oportunidad en exclusiva para quien busca mucho espacio."),
 P("0110676","casa","Rubí","Castellnou",219000,90,2,1,fs("65036980267","510396_65036980267_6_20260602172411391.jpg"),
   "Casa a pie de calle de 90 m² en la tranquila zona de Castellnou, para quien busca comodidad y contacto con la naturaleza. Comedor luminoso con acceso directo a la cocina."),
 P("0110652","piso","Rubí","",220000,66,3,1,fs("60884901805","510396_60884901805_794edbd5-f2ed-4c59-9aeb-6a8aa24de6b7.jpg"),
   "Entresuelo de 66 m² totales (60 m² útiles) con una habitación individual, dos dobles y un baño. Tiene aire acondicionado frío y calor, ascensor, calefacción central y más de 50 años de antigüedad."),
 P("0010635","casa","Rubí","",598000,258,4,3,fs("60047343541","510396_60047343541_904cdf98-5dd5-4e1c-b272-de88596a0e35.jpg"),
   "Vivienda unifamiliar de 258 m², construida en 2011, con mucho encanto, ambiente cálido y techos altos revestidos de madera. Bien conservada."),
 P("0310664","solar","Rubí","Can Oriol",145000,235,0,0,fs("62502142949","510396_62502142949_bb70210b-35a7-4c8a-93c0-b996679b208c.jpg"),
   "Terreno urbano de 235 m² en una zona tranquila y residencial de Can Oriol, dentro del núcleo urbano, con servicios, comercios y transporte cerca."),
 P("0310247","solar","Rubí","Can Oriol",208000,600,0,0,fs("30027219098","510396_30027219098_3_20221214183527058.jpg"),
   "Terreno urbano esquinero de 600 m² en el centro del barrio de Ca n'Oriol, con todos los suministros y una pequeña edificación."),
 P("0310578","solar","Rubí","Can Mir",119990,473,0,0,fs("54253874811","510396_54253874811_b98eaa25-56b8-4107-8a93-e75ff4819c97.jpg"),
   "Terreno de 473 m² en la tranquila y consolidada urbanización de Can Mir, con una topografía que permite múltiples posibilidades de construcción."),
 P("037348","solar","Rubí","Can Mir",118000,560,0,0,fs("804243064","510396_037348_foto_3_804243064_20180730101621.jpg"),
   "Terreno de 560 m² en Can Mir, con proyecto de obra y garaje a pie de calle. Parcela muy limpia para empezar la obra, con 16 m de fachada por 35 m de fondo."),
 P("310117","solar","Rubí","Can Mir",89000,586,0,0,fs("23363239643","510396_23363239643_08f976ed-7080-48e0-a243-807abb420bb2.jpg"),
   "Terreno de 586 m² en la urbanización de Can Mir, totalmente urbanizado, con todos los suministros a pie de calle, excelentes vistas y buena comunicación."),
 P("0310527","solar","Rubí","Can Sola",73000,555,0,0,fs("49226659519","510396_49226659519_7484525e-1892-49c4-bf0c-482494b09a23.jpg"),
   "Terreno edificable en la urbanización de Can Sola. Pertenece al municipio de Rubí pero linda por el frente con Terrassa. Tiene una parada de bus delante de la parcela."),
 P("310149","solar","Rubí","Can Sola",88000,574,0,0,fs("25036406575","510396_25036406575_8_20220602112529469.jpg"),
   "Terreno edificable de 574 m² en la urbanización de Can Sola. Pertenece al municipio de Rubí pero linda por el frente con Terrassa."),
 P("310118","solar","Rubí","Can Sola",89000,815,0,0,None,
   "Terreno de 815 m² muy bien ubicado en la urbanización de Can Sola, totalmente urbanizado y con todos los suministros a pie de calle."),
 P("0310452","solar","Rubí","Castellnou",52000,479,0,0,fs("43365301151","510396_43365301151_2_20240429162656999.jpg"),
   "Terreno edificable de 479 m² en la urbanización de Castellnou, que pertenece a Rubí pero linda por el frente con Terrassa. Hay una parada de bus cerca."),
 P("310193","solar","Rubí","Castellnou",50000,533,0,0,fs("26762164726","510396_26762164726_73ab4a4e-e620-4b6f-b1ab-1d82c4f6bc5b.jpg"),
   "Terreno de 532,60 m² en Castellnou, a 15 minutos de la carretera de Martorell y a 10 minutos de la C-58."),
 P("038920","solar","Rubí","Castellnou - Vallès Park",99000,511,0,0,fs("14245692940","510396_14245692940_c3e26d4a-b973-4f74-a2ab-4f40c3479b27.jpg"),
   "Parcelas edificables de unos 500 m² en Castellnou, muy llanas y distribuidas en bancales. Zona urbana con alcantarillado y con luz, gas y agua a pie de calle.",
   nota="Hay tres parcelas disponibles al mismo precio: refs. 038920 (511 m²), 038921 (487 m²) y 038922 (519 m²)."),
 P("0310313","solar","Rubí","",175000,884,0,0,fs("34248651413","510396_34248651413_13_20230510135751949.jpg"),
   "Terreno de 884 m² con muy poco desnivel, cerca de todos los servicios y con buen acceso a las carreteras C-16 y C-58."),
 P("310135","solar","Rubí","Sant Muç",369000,9820,0,0,fs("24184415513","510396_24184415513_8_20220519104533704.jpg"),
   "Terreno de 9.820 m² en zona residencial unifamiliar de Rubí. Solo es edificable la parte clasificada como R.U.C. (área de conservación de estructura parcelaria). Parcela mínima de 1.200 m² y no se permite segregar."),
]
for p in PROPS:
    p["slug"] = re.sub(r"-+", "-", f"{p['tipo']}-venta-{slug(p['muni'])}-{slug(p['zona'])}-{p['ref'].lower()}").strip("-")
    p["label"] = TIPO[p["tipo"]]
    p["name"] = f"{p['label']} en venta en {p['muni']}" + (f" ({p['zona']})" if p["zona"] else "")
    p["path"] = f"inmueble/{p['slug']}/"
BY_REF = {p["ref"]: p for p in PROPS}
def of(muni): return [p for p in PROPS if p["muni"] == muni]
TERRASSA, RUBI = of("Terrassa"), of("Rubí")
FEATURED = [BY_REF[r] for r in ("0110696", "0110699", "0110692", "0010703", "0110702", "0010446")]

# ───────────────────────── Textos compartidos
TESTI = [
    ("Gary Acosta", "", "La mejor solución inmobiliaria en todo el Vallès."),
    ("Joan Casanova", "Rubí", "Desde el primer momento sabían cuáles eran mis necesidades y aplicaron sus conocimientos del mercado inmobiliario para valorar de manera justa la vivienda y obtener el máximo beneficio. Buenos comerciales y excelentes profesionales, ¡vendieron mi casa en tres semanas!"),
    ("Yolanda Cifuentes", "Terrassa", "Excelentes profesionales con un trato personal muy cercano. La venta de mi piso fue muy rápida y efectiva. Estuve informada y asesorada en todo momento. Me hicieron sentir muy tranquila. Una experiencia fantástica y un servicio impecable."),
]
TEAM = ["Dadimar", "Belkis", "Eva", "Magda", "Nayarid"]

FAQ = {
 "coste": ("¿Cuánto cuesta vender un piso con una inmobiliaria?",
   "Los honorarios se pactan por escrito antes de firmar el encargo de venta, así que sabes lo que vas a pagar antes de empezar. Además de los honorarios, quien vende suele afrontar la plusvalía municipal, la cancelación de la hipoteca si la hay y el certificado de eficiencia energética. En la tasación gratuita te explicamos el desglose para tu caso concreto."),
 "tasacion": ("¿Cómo funciona la tasación gratuita?",
   "Nos cuentas dónde está tu vivienda y cómo es, y la tasamos sin visitas y sin demoras, con datos de mercado de tu zona. Después te llamamos para explicarte el valor y el precio de salida que te recomendamos. No tiene coste ni compromiso."),
 "docs": ("¿Qué documentación necesito para comprar una vivienda en Terrassa?",
   "De forma orientativa, los bancos piden DNI o NIE, las últimas nóminas o justificantes de ingresos, la última declaración de la renta, la vida laboral y los extractos de tus cuentas. Para reservar la vivienda basta con tus datos de identificación. Si quieres financiarla, empezamos por un estudio financiero para saber cuánto puedes pedir."),
 "gastos": ("¿Qué gastos tiene comprar una vivienda en Cataluña?",
   "Además del precio, hay que contar con impuestos (ITP en vivienda de segunda mano; IVA y AJD en obra nueva), notaría, registro, gestoría y tasación si hay hipoteca. Como referencia general suelen sumar entre un 10 % y un 13 % del precio, según el tipo de vivienda y la situación de cada comprador. Pide tu caso a nuestro equipo para tener la cifra exacta."),
 "barrios": ("¿En qué barrios de Terrassa tenéis más oferta ahora mismo?",
   "En nuestra cartera de octubre de 2026 hay inmuebles en Sant Pere, Poble Nou-Zona Olímpica, Pere Parres, Vista Alegre, Cementiri Vell, Can Parellada, Les Fonts, Ègara y Torre-sana. La cartera cambia cada semana: consulta el listado actualizado o llámanos y te avisamos cuando entre algo que encaje."),
 "zonas": ("¿Trabajáis en Rubí y en el resto del Vallès Occidental?",
   "Sí. Nuestra oficina central está en Terrassa y el equipo comercial trabaja sobre todo en el Vallès Occidental. Tenemos inmuebles en Terrassa, Rubí, Vacarisses y Sabadell, y todas las oficinas comparten la misma cartera, así que te atendemos igual desde cualquier punto de la red."),
 "financia": ("¿Puedo financiar el 100 % de la vivienda?",
   "En algunos casos puede estudiarse una financiación de hasta el 100 % del importe, pero depende de tu perfil, de la vivienda y de la entidad. Con el estudio financiero sabrás qué opciones tienes antes de decidir."),
 "tiempo": ("¿Cuánto tarda en venderse un piso?",
   "Depende del precio, la zona y el estado de la vivienda. Un precio ajustado al mercado es lo que más acorta los plazos. Un cliente de Rubí cuenta en su opinión de Google que vendimos su casa en tres semanas, pero cada caso es distinto: en la tasación te damos una estimación realista."),
 "ocupado": ("¿Se pueden visitar los inmuebles ocupados?",
   "No. Algunos inmuebles de inversión están ocupados por personas sin justo título y, por ese estado ocupacional, no admiten visitas. La ficha de cada uno lo indica claramente antes de que pidas información."),
 "aicat": ("¿Qué es el Registre d'Agents Immobiliaris de Catalunya (AICAT)?",
   "Es el registro oficial de agentes inmobiliarios de Cataluña, al que deben estar inscritas las empresas que ejercen esta actividad. D&Habitat figura inscrita, como indica el sello del pie de página."),
 "cita": ("¿Cómo pido una visita o una cita en la oficina?",
   f"Llámanos al {PHONE}, escríbenos desde el formulario de contacto o pulsa «Pedir visita» en la ficha del inmueble. También atendemos con cita online. Nuestra oficina central está en Pla de l'Ametllera, 100, en Terrassa."),
}

AGENCY = {
    "@type": "RealEstateAgent", "@id": SITE + "/#agency", "name": BRAND, "legalName": "D&HABITAT FINANCE, S.L.",
    "alternateName": "D&Habitat", "url": SITE + "/", "logo": LOGO_URL, "image": absu(UP + "oficina-terrassa.jpg"),
    "telephone": TEL, "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": "Pla de l'Ametllera, 100, local L'Ametllera", "postalCode": "08225",
                "addressLocality": "Terrassa", "addressRegion": "Barcelona", "addressCountry": "ES"},
    "areaServed": [{"@type": "City", "name": n} for n in ("Terrassa", "Rubí", "Vacarisses", "Sabadell")] + [{"@type": "AdministrativeArea", "name": "Vallès Occidental"}],
    "sameAs": [FB, IG],
    "hasMap": MAPS,
}

# ───────────────────────── Maquetación común
def imgsrc(u):
    l = loc(u)
    return u if l == u else "@IMG/" + l

def ph(src, alt, ar="4/3", eager=False, cls=""):
    if not src:
        return f'<div class="ph {cls}" style="--ar:{ar}" role="img" aria-label="{esc(alt)}"></div>'
    a = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="ph {cls}" style="--ar:{ar}"><img src="{esc(imgsrc(src))}" alt="{esc(alt)}" {a} onerror="this.remove()"></div>')

NAV = [("vender/", "Vender", "vender"), ("financiacion/", "Financiación", "financiacion"), ("nosotros/", "Nosotros", "nosotros")]
BUY_MENU = [("inmobiliaria-terrassa/", "Terrassa", "terrassa"), ("inmobiliaria-rubi/", "Rubí", "rubi")]

def header(depth, cur):
    items = "".join(f'<a href="{href(p, depth)}"' + (' aria-current="page"' if k == cur else "") + f">{t}</a>" for p, t, k in BUY_MENU)
    on = " on" if cur in ("comprar", "terrassa", "rubi") else ""
    dd = (f'<div class="dd"><button class="dd-btn{on}" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="dd-comprar">Comprar'
          f'<svg width="12" height="8" viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m1 1.5 5 5 5-5"/></svg></button>'
          f'<div class="dd-menu" id="dd-comprar">{items}</div></div>')
    links = dd + "".join(f'<a href="{href(p, depth)}"' + (' aria-current="page"' if k == cur else "") + f">{t}</a>" for p, t, k in NAV)
    return f'''<a class="skip" href="#main">Saltar al contenido</a>
<header class="hdr"><div class="wrap">
<a class="brand" href="{href("", depth)}" aria-label="{BRAND}, inicio"><img src="{href("img/l/logo.png", depth)}" alt="D&amp;Habitat, gestión inmobiliaria" width="213" height="44"></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menú</button>
<nav class="nav" id="nav" aria-label="Principal">{links}
<a class="tel" href="tel:{TEL}">{PHONE}</a>
<a class="btn" href="{href("contacto/", depth)}">Contactar</a></nav>
</div></header>'''

def footer(depth):
    h = lambda p: href(p, depth)
    return f'''<footer class="ftr"><div class="wrap">
<div class="cols">
<div><a class="brand" href="{h("")}" aria-label="{BRAND}, inicio"><img src="{h("img/l/logo.png")}" alt="D&amp;Habitat, gestión inmobiliaria" width="238" height="49" loading="lazy"></a>
<p class="small" style="margin-top:18px">Pla de l'Ametllera, 100, local L'Ametllera<br>08225 Terrassa (Barcelona)<br><a href="tel:{TEL}">{PHONE}</a></p>
<p class="small"><a href="{FB}" rel="noopener">Facebook</a> · <a href="{IG}" rel="noopener">Instagram</a> · <a href="{MAPS}" rel="noopener">Opiniones en Google</a></p>
<div class="aicat"><img src="{href("img/l/logo-aicat.png", depth)}" alt="Registre d'Agents Immobiliaris de Catalunya (AICAT)" loading="lazy" height="40" onerror="this.remove()"><span>Inscrita en el Registre d'Agents Immobiliaris de Catalunya</span></div></div>
<div><h4>Comprar por zona</h4><ul>
<li><a href="{h("inmobiliaria-terrassa/")}">Inmobiliaria en Terrassa</a></li>
<li><a href="{h("inmobiliaria-rubi/")}">Inmobiliaria en Rubí</a></li>
<li><a href="{h("comprar/")}?poblacion=terrassa&amp;tipo=piso">Pisos en venta en Terrassa</a></li>
<li><a href="{h("comprar/")}?poblacion=rubi&amp;tipo=solar">Terrenos en venta en Rubí</a></li>
<li><a href="{h("comprar/")}">Todos los inmuebles</a></li></ul></div>
<div><h4>Servicios</h4><ul>
<li><a href="{h("vender/")}">Tasación gratuita</a></li>
<li><a href="{h("financiacion/")}">Financiación y calculadora</a></li>
<li><a href="{h("preguntas-frecuentes/")}">Preguntas frecuentes</a></li></ul></div>
<div><h4>D&amp;Habitat</h4><ul>
<li><a href="{h("nosotros/")}">Nosotros y equipo</a></li>
<li><a href="{h("inmobiliaria-terrassa/")}">Oficina en Terrassa</a></li>
<li><a href="{h("contacto/")}">Contacto</a></li>
<li><a href="{h("condiciones-legales/")}">Condiciones legales</a></li>
<li><a href="{h("politica-privacidad/")}">Política de privacidad</a></li>
<li><a href="{h("politica-cookies/")}">Política de cookies</a></li></ul></div>
</div>
<div class="legal"><span>© 2026 D&amp;HABITAT FINANCE, S.L. · CIF B67372052</span><span>Atendemos en Terrassa, Rubí, Vacarisses, Sabadell y todo el Vallès Occidental</span></div>
</div></footer>
<div class="cookies" id="cookies" hidden role="dialog" aria-label="Cookies"><p>Usamos cookies de analítica, solo si las aceptas, para mejorar la web. Más información en la <a class="tlink" href="{h("politica-cookies/")}">política de cookies</a>.</p>
<div class="row"><button class="btn" type="button" data-cookie="yes">Aceptar</button><button class="btn btn-ghost" type="button" data-cookie="no">Rechazar</button></div></div>'''

def _page(path, title, desc, main, cur="", schema=None, og=None, robots=None, preload=None, imgdns=False):
    depth = len([s for s in path.split("/") if s])
    canon = SITE + "/" + path
    og = absu(og or UP + "inmuebles-fons-1200x731.jpg")
    extra = ""
    if preload: extra += f'<link rel="preload" as="image" href="{esc(imgsrc(preload))}" fetchpriority="high">\n'
    sch = "".join(jl(s) for s in (schema or []))
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    assets = "../" * depth if depth else "./"
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{rb}<meta name="theme-color" content="#fdfdf7">
<link rel="icon" href="{assets}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{assets}img/l/icon-192.png"><link rel="apple-touch-icon" href="{assets}img/l/apple-touch-icon.png"><link rel="manifest" href="{assets}site.webmanifest">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{esc(og)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500&amp;display=swap">
{extra}<link rel="stylesheet" href="{assets}css/style.css">
{sch}
</head>
<body>
{header(depth, cur)}
<main id="main">
{main}
</main>
{footer(depth)}
<script src="{assets}js/config.js"></script>
<script src="{assets}js/app.js" defer></script>
</body>
</html>
'''

def page(path, *a, **k):
    depth = len([x for x in path.split("/") if x])
    return _page(path, *a, **k).replace("@IMG/", "../" * depth if depth else "./")

def crumbs(items, depth):
    out, ld = [], []
    for i, (t, p) in enumerate(items):
        last = i == len(items) - 1
        out.append(f"<span>{esc(t)}</span>" if last else f'<a href="{href(p, depth)}">{esc(t)}</a>')
        ld.append({"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + "/" + p})
    html_ = '<nav class="crumbs wrap" aria-label="Migas de pan">' + '<span aria-hidden="true">/</span>'.join(out) + "</nav>"
    return html_, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}

def card(p, depth):
    meta = [f"{num(p['m2'])} m²"]
    if p["hab"]: meta.append(f"{p['hab']} hab.")
    if p["ban"]: meta.append(f"{p['ban']} {'baño' if p['ban']==1 else 'baños'}")
    tag = f'<span class="tag warn">Ocupado · sin visitas</span>' if p["ocup"] else f'<span class="tag">{p["label"]}</span>'
    zona = f" · {p['zona']}" if p["zona"] else ""
    return f'''<article class="card pc" data-poblacion="{slug(p['muni'])}" data-tipo="{p['tipo']}" data-precio="{p['precio']}">
{tag}{ph(p["img"], p["name"], "4/3")}
<div class="body"><div class="price">{eur(p["precio"])}</div>
<h3><a href="{href(p["path"], depth)}">{esc(p["label"])} en venta en {esc(p["muni"])}{esc(zona)}</a></h3>
<div class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</div><div class="ref">Ref. {esc(p["ref"])}</div></div></article>'''

def grid(props, depth, id_=""):
    return f'<div class="grid g3"' + (f' id="{id_}"' if id_ else "") + ">" + "".join(card(p, depth) for p in props) + "</div>"

def faq_html(keys):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(FAQ[k][0])}</summary><div class="ans"><p>{esc(FAQ[k][1])}</p></div></details>' for k in keys) + "</div>"

def faq_ld(keys):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": FAQ[k][0], "acceptedAnswer": {"@type": "Answer", "text": FAQ[k][1]}} for k in keys]}

def testimonials():
    out = ""
    for n, c, t in TESTI:
        out += f'<figure class="sand quote" style="margin:0"><span class="stars" aria-label="5 estrellas">★★★★★</span><blockquote>«{esc(t)}»</blockquote><cite>{esc(n)}{" · " + esc(c) if c else ""}</cite></figure>'
    return f'<div class="grid g3">{out}</div>'

def rating_line():
    return f'<p class="lead" style="margin-top:20px"><b style="font-weight:500;color:#000">4,9 ★</b> en 321 opiniones de Google. <a class="tlink" href="{MAPS}" rel="noopener">Léelas en Google Maps</a></p>'

def band(depth, h="¿Quieres vender tu casa?", p="Tasamos tu vivienda sin visitas y sin demoras. Cuéntanos dónde está y te llamamos."):
    return f'''<section class="sec tight"><div class="wrap"><div class="band"><div><h2>{esc(h)}</h2><p>{esc(p)}</p>
<a class="btn btn-orange" href="{href("vender/", depth)}">Pedir tasación gratuita</a></div>
{ph(UP + "call-to.jpg", "Vivienda tasada por D&Habitat", "4/3", cls="r2")}</div></div></section>'''

def contact_form(origen, extra_fields="", btn="Enviar", show_tipo=False):
    return f'''<form data-form="{esc(origen)}" novalidate>
<div class="field"><label for="{origen}-n">Nombre</label><input id="{origen}-n" name="nombre" autocomplete="name" required></div>
<div class="field"><label for="{origen}-t">Teléfono</label><input id="{origen}-t" name="telefono" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="{origen}-e">Email</label><input id="{origen}-e" name="email" type="email" autocomplete="email"></div>
{extra_fields}
<div class="field"><label for="{origen}-m">Mensaje</label><textarea id="{origen}-m" name="mensaje"></textarea></div>
<div class="hp" aria-hidden="true"><input name="web" tabindex="-1" autocomplete="off"></div>
<label class="check"><input type="checkbox" name="privacidad" required><span>Acepto la <a class="tlink" href="__PRIV__">política de privacidad</a></span></label>
<button class="btn btn-block" type="submit">{btn}</button><div class="form-msg" role="status" hidden></div></form>'''

def with_priv(s, depth): return s.replace("__PRIV__", href("politica-privacidad/", depth))

def stats(props):
    pisos = [p["precio"] for p in props if p["tipo"] == "piso" and not p["ocup"]]
    casas = [p["precio"] for p in props if p["tipo"] == "casa"]
    solares = [p["precio"] for p in props if p["tipo"] == "solar"]
    return pisos, casas, solares

def zona_counts(props):
    d = {}
    for p in props:
        if p["zona"]: d[p["zona"]] = d.get(p["zona"], 0) + 1
    return sorted(d.items(), key=lambda x: (-x[1], x[0]))

SITEMAP = []
def write(path, content, index=True, prio="0.7", freq="weekly"):
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f: f.write(content)
    if index: SITEMAP.append((path, prio, freq))


def _wic(p): return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
WAY_IC = {
 "val": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
 "est": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.2"/>',
 "vis": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.2A6.5 6.5 0 0 1 21.5 20"/>',
 "fir": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M16 7l3 3M14 9l2 2"/>',
 "cue": '<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/>',
 "tas": '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/>',
 "mer": '<path d="M3 11l9-8 9 8M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
}
def way(eyebrow, h2, steps):
    lis = "".join(f'<li><span class="way-dot" aria-hidden="true">{i}</span><div class="way-card"><span class="way-ic">{_wic(WAY_IC[ic])}</span><h3>{t}</h3><p>{p}</p></div></li>'
                  for i, (ic, t, p) in enumerate(steps, 1))
    return (f'<div class="way" data-way><p class="eyebrow">{eyebrow}</p><h2 class="t-h">{h2}</h2>'
            f'<div class="way-wrap"><svg class="way-svg" aria-hidden="true"><path class="way-base"/><path class="way-prog"/></svg>'
            f'<span class="way-pin" aria-hidden="true">{_wic(WAY_IC["mer"])}</span><ol class="way-list">{lis}</ol></div></div>')

# ───────────────────────── Páginas
def build_home():
    d = 0
    finder = f'''<form class="finder" action="{href("comprar/", d)}" method="get" aria-label="Buscar inmuebles">
<div class="field"><label for="h-pob">Población</label><select id="h-pob" name="poblacion"><option value="">Todas</option><option value="terrassa">Terrassa</option><option value="rubi">Rubí</option></select></div>
<div class="field"><label for="h-tipo">Tipo</label><select id="h-tipo" name="tipo"><option value="">Todos</option><option value="piso">Piso</option><option value="casa">Casa</option><option value="solar">Solar</option><option value="local">Local</option><option value="parking">Parking</option></select></div>
<div class="field"><label for="h-max">Precio máximo</label><select id="h-max" name="max"><option value="">Sin límite</option><option value="100000">100.000 €</option><option value="200000">200.000 €</option><option value="300000">300.000 €</option><option value="500000">500.000 €</option><option value="750000">750.000 €</option></select></div>
<div class="field"><label>Cartera</label><div style="padding:15px 0;color:#666">{len(PROPS)} inmuebles</div></div>
<button class="btn" type="submit">Buscar</button></form>'''
    pt, ct, st = stats(TERRASSA); pr, cr, sr = stats(RUBI)
    zonas = f'''<div class="grid g2">
<a class="card" href="{href("inmobiliaria-terrassa/", d)}" style="text-decoration:none;display:block">{ph(UP + "oficina-terrassa.jpg", "Oficina de D&Habitat en Terrassa", "16/9")}
<div style="padding:28px"><h3 class="t-sub">Terrassa</h3><p class="muted" style="margin:10px 0 0">{len(TERRASSA)} inmuebles. Pisos libres desde {eur(min(pt))}. Oficina central en Sant Pere.</p></div></a>
<a class="card" href="{href("inmobiliaria-rubi/", d)}" style="text-decoration:none;display:block">{ph(UP + "inmuebles-rubi-1200x498.jpg", "Inmuebles en venta en Rubí", "16/9")}
<div style="padding:28px"><h3 class="t-sub">Rubí</h3><p class="muted" style="margin:10px 0 0">{len(RUBI)} inmuebles. Casas desde {eur(min(cr))} y terrenos desde {eur(min(sr))}.</p></div></a></div>'''
    svc = f'''<div class="grid g3">
<div class="sand svc"><h3>Vender</h3><p>Tasamos tu vivienda sin visitas y sin demoras, con datos reales de tu zona, y la comercializamos con nuestro método.</p><a class="tlink" href="{href("vender/", d)}">Pedir tasación gratuita</a></div>
<div class="sand svc"><h3>Comprar</h3><p>Elige dónde quieres vivir, selecciona la vivienda que mejor encaje con lo que necesitas y solicita una visita con nosotros.</p><a class="tlink" href="{href("comprar/", d)}">Ver inmuebles</a></div>
<div class="sand svc"><h3>Financiar</h3><p>Asesoramiento hipotecario personalizado. Estudiamos tu caso a fondo y te acompañamos en todos los trámites.</p><a class="tlink" href="{href("financiacion/", d)}">Estudio financiero</a></div></div>'''
    steps = way("Cómo vendemos", "Del precio justo a la firma, en cuatro pasos", [
        ("val", "Valoración", "Tasación gratuita, sin visitas y sin demoras."),
        ("est", "Estrategia", "Fijamos el precio de salida y publicamos el inmueble."),
        ("vis", "Visitas y oferta", "Filtramos interesados, organizamos visitas y negociamos."),
        ("fir", "Firma", "Te acompañamos hasta la firma y la entrega de llaves.")])
    team = '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">' + "".join(
        f'<div class="person"><div class="avatar" aria-hidden="true">{n[0]}</div><h3>{n}</h3><span class="small muted">Equipo D&amp;Habitat</span></div>' for n in TEAM) + "</div>"
    main = f'''
<section class="photo-hero wrap">
<div class="ph-hero">{ph(UP + "inmuebles-fons-1200x731.jpg", "Casa moderna con piscina, ejemplo de inmueble de la cartera de D&Habitat", "16/9", eager=True)}
<div class="ph-hero-in">
<div class="hero-card">
<p class="eyebrow">Inmobiliaria en Terrassa, Rubí y el Vallès Occidental</p>
<h1 class="t-hl">Tu inmobiliaria de confianza en Terrassa y el Vallès</h1>
<p class="lead">Comprar, vender o financiar tu vivienda con todas las garantías, con un equipo que atiende a cada cliente por su nombre.</p>
<div class="row"><a class="btn" href="{href("comprar/", d)}">Ver inmuebles</a><a class="btn btn-ghost" href="{href("vender/", d)}">Tasación gratuita</a></div>
</div>
{finder}
</div></div></section>
<section class="sec tight wrap"><div class="row" style="justify-content:space-between;align-items:end;margin-bottom:32px"><div><p class="eyebrow">Inmuebles destacados</p><h2 class="t-h">Viviendas para entrar a vivir</h2></div>
<a class="btn btn-ghost" href="{href("comprar/", d)}">Ver todos</a></div>{grid(FEATURED, d)}</section>
<section class="sec tight wrap"><div class="facts">
<div><b>4,9 ★</b><span>321 opiniones en Google</span></div>
<div><b>Desde 2014</b><span>Oficina central en Terrassa</span></div>
<div><b>{len(PROPS)} inmuebles</b><span>en Terrassa y Rubí, a 24 de octubre de 2026</span></div></div></section>
<section class="sec wrap"><p class="eyebrow">Dónde trabajamos</p><h2 class="t-h" style="margin-bottom:40px">Terrassa y Rubí, desde dentro</h2>{zonas}</section>
<section class="sec wrap"><p class="eyebrow">Qué hacemos por ti</p><h2 class="t-h" style="margin-bottom:40px">Comprar, vender y financiar en un solo sitio</h2>{svc}</section>
<section class="sec wrap">{steps}</section>
<section class="sec wrap"><div class="row" style="justify-content:space-between;align-items:end;margin-bottom:40px"><div><p class="eyebrow">Equipo</p><h2 class="t-h">Las personas que más nombran nuestros clientes</h2></div>
<a class="btn btn-ghost" href="{href("nosotros/", d)}">Conocer al equipo</a></div>{team}</section>
<section class="sec wrap"><p class="eyebrow">Opiniones de clientes</p><h2 class="t-h">¿Qué opinan de nosotros?</h2>{rating_line()}<div style="margin-top:40px">{testimonials()}</div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:start"><div><p class="eyebrow">Preguntas frecuentes</p><h2 class="t-h">Lo que nos preguntan antes de empezar</h2>
<p style="margin-top:24px"><a class="tlink" href="{href("preguntas-frecuentes/", d)}">Ver todas las preguntas</a></p></div>{faq_html(["coste", "tasacion", "docs", "financia"])}</div></section>
{band(d)}'''
    schema = [{"@context": "https://schema.org", "@graph": [AGENCY,
              {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "inLanguage": "es", "publisher": {"@id": SITE + "/#agency"}}]}]
    write("", page("", f"Inmobiliaria en Terrassa y Rubí · {BRAND}",
        "Inmobiliaria en Terrassa, Rubí y el Vallès Occidental. Compra, vende o financia tu vivienda con D&Habitat: 4,9 ★ en Google y tasación gratuita sin visitas.",
        main, schema=schema, preload=UP + "inmuebles-fons-1200x731.jpg"), prio="1.0")

def build_listing():
    d = 1
    crb, crl = crumbs([("Inicio", ""), ("Comprar", "comprar/")], d)
    main = f'''{crb}
<section class="wrap" style="padding-top:32px"><h1 class="t-hl" style="max-width:16ch">Inmuebles en venta en Terrassa y Rubí</h1>
<p class="lead" style="margin-top:24px">Pisos, casas, terrenos, locales y plazas de parking de nuestra cartera. Elige dónde quieres vivir, selecciona la vivienda que mejor encaje con lo que necesitas y solicita una visita.</p></section>
<section class="sec tight wrap"><div class="sand" style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;align-items:end">
<div class="field" style="margin:0"><label for="f-poblacion">Población</label><select id="f-poblacion"><option value="">Todas</option><option value="terrassa">Terrassa</option><option value="rubi">Rubí</option></select></div>
<div class="field" style="margin:0"><label for="f-tipo">Tipo</label><select id="f-tipo"><option value="">Todos</option><option value="piso">Pisos</option><option value="casa">Casas</option><option value="solar">Solares</option><option value="local">Locales</option><option value="parking">Parkings</option></select></div>
<div class="field" style="margin:0"><label for="f-max">Precio máximo</label><select id="f-max"><option value="">Sin límite</option><option value="100000">100.000 €</option><option value="200000">200.000 €</option><option value="300000">300.000 €</option><option value="500000">500.000 €</option><option value="750000">750.000 €</option></select></div>
<div class="field" style="margin:0"><label for="f-orden">Ordenar</label><select id="f-orden"><option value="">Recientes</option><option value="asc">Precio, de menor a mayor</option><option value="desc">Precio, de mayor a menor</option></select></div></div>
<p class="count" id="f-count" style="margin:28px 0 20px" aria-live="polite">{len(PROPS)} inmuebles</p>
{grid(PROPS, d, "listado")}
<p class="empty" id="f-empty" hidden>No hay inmuebles con esos filtros. <a class="tlink" href="{href("contacto/", d)}">Cuéntanos qué buscas</a> y te avisamos cuando entre algo.</p></section>
{band(d, "¿No encuentras lo que buscas?", "Cuéntanos qué necesitas y te avisamos cuando entre un inmueble que encaje.")}'''
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Inmuebles en venta de D&Habitat",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + p["path"], "name": p["name"]} for i, p in enumerate(PROPS)]}
    write("comprar/", page("comprar/", "Inmuebles en venta en Terrassa y Rubí · D&Habitat",
        f"{len(PROPS)} inmuebles en venta en Terrassa y Rubí: pisos, casas, terrenos, locales y parkings. Filtra por zona, tipo y precio y pide visita con D&Habitat.",
        main, cur="comprar", schema=[crl, ld], imgdns=True), prio="0.9", freq="daily")

GAL = {}
_gdir = os.path.join(HERE, "assets", "img", "g")
if os.path.isdir(_gdir):
    for _f in sorted(os.listdir(_gdir)):
        GAL.setdefault(_f.split("_")[0], []).append(_f)
GAL_CAP = 10  # la vista previa del chat solo lleva las primeras fotos (límite de ficheros); el zip lleva todas

def gallery(p, d):
    code = (re.search(r"/(\d+)\.510396/", p["img"]) or [None, None])[1] if p["img"] else None
    extra = [f for f in GAL.get(code, []) if not f.endswith("_01.jpg")]
    slides = [imgsrc(p["img"])] + ["@IMG/img/g/" + f for f in extra] if p["img"] else []
    if PREVIEW: slides = slides[:GAL_CAP]
    if len(slides) < 2:
        return ph(p["img"], p["name"], "3/2", eager=True, cls="r2")
    n = len(slides)
    th = "".join(f'<li><button type="button" data-full="{s}" data-alt="{esc(p["name"])} · foto {i+1} de {n}" aria-label="Ver foto {i+1} de {n}"><img src="{s}" alt="" loading="lazy" decoding="async" width="96" height="68"></button></li>' for i, s in enumerate(slides))
    nav = lambda: ('<button class="gal-nav prev" type="button" aria-label="Foto anterior">&#8249;</button><button class="gal-nav next" type="button" aria-label="Foto siguiente">&#8250;</button>')
    return (f'<div class="gal" data-gal role="group" aria-label="Fotografías de {esc(p["name"])}">'
            f'<div class="gal-main"><img src="{slides[0]}" alt="{esc(p["name"])}" fetchpriority="high" width="1000" height="667">{nav()}'
            f'<button class="gal-zoom" type="button" aria-label="Ampliar foto">&#10530;</button><span class="gal-count" aria-live="polite">1 / {n}</span></div>'
            f'<ul class="gal-thumbs">{th}</ul>'
            f'<dialog class="gal-lb" aria-label="Fotografías ampliadas"><div class="lb-in"><button class="lb-x" type="button" aria-label="Cerrar">&#10005;</button>{nav()}<img alt=""><span class="gal-count"></span></div></dialog></div>')

def property_page(p):
    d = 2
    cb, cl = crumbs([("Inicio", ""), ("Comprar", "comprar/"), (p["muni"], "inmobiliaria-" + slug(p["muni"]) + "/"), (p["name"], p["path"])], d)
    facts = [("Tipo", p["label"]), ("Municipio", p["muni"])]
    if p["zona"]: facts.append(("Zona", p["zona"]))
    facts.append(("Superficie", f"{num(p['m2'])} m²"))
    if p["hab"]: facts.append(("Habitaciones", p["hab"]))
    if p["ban"]: facts.append(("Baños", p["ban"]))
    facts.append(("Referencia", p["ref"]))
    dl = '<dl class="dl">' + "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in facts) + "</dl>"
    notice = f'<div class="notice">{esc(p["nota"])}</div>' if p["ocup"] else ""
    nota = f'<p class="muted">{esc(p["nota"])}</p>' if p["nota"] and not p["ocup"] else ""
    like = [q for q in PROPS if q is not p and q["muni"] == p["muni"] and q["tipo"] == p["tipo"]][:3]
    if len(like) < 3: like += [q for q in PROPS if q is not p and q["muni"] == p["muni"] and q not in like][: 3 - len(like)]
    zonatxt = f" en {p['zona']}, {p['muni']}" if p["zona"] else f" en {p['muni']}"
    detalles = []
    if p["hab"]: detalles.append(f"{p['hab']} {'habitación' if p['hab']==1 else 'habitaciones'}")
    if p["ban"]: detalles.append(f"{p['ban']} {'baño' if p['ban']==1 else 'baños'}")
    det = (" con " + " y ".join(detalles)) if detalles else ""
    desc = f"{p['label']} de {num(p['m2'])} m²{det}{zonatxt}. {eur(p['precio'])}. Ref. {p['ref']}. Pide visita con D&Habitat."
    title = f"{p['name']} · {eur(p['precio'])} · D&Habitat"
    form = with_priv(f'''<div class="sand aside"><div class="price">{eur(p["precio"])}</div>
<p class="muted" style="margin:6px 0 22px">Ref. {esc(p["ref"])}</p>
<a class="btn btn-block" href="tel:{TEL}" style="margin-bottom:12px">Llamar al {PHONE}</a>
<p class="small muted" style="margin:18px 0 12px">{"Pide información sobre este inmueble" if p["ocup"] else "O pide una visita y te llamamos"}</p>
<form data-form="ficha-{esc(p["ref"])}" novalidate>
<input type="hidden" name="referencia" value="{esc(p["ref"])}">
<div class="field"><label for="v-n">Nombre</label><input id="v-n" name="nombre" autocomplete="name" required></div>
<div class="field"><label for="v-t">Teléfono</label><input id="v-t" name="telefono" type="tel" autocomplete="tel" required></div>
<div class="hp" aria-hidden="true"><input name="web" tabindex="-1" autocomplete="off"></div>
<label class="check"><input type="checkbox" name="privacidad" required><span>Acepto la <a class="tlink" href="__PRIV__">política de privacidad</a></span></label>
<button class="btn btn-block" type="submit">{"Pedir información" if p["ocup"] else "Pedir visita"}</button><div class="form-msg" role="status" hidden></div></form></div>''', d)
    main = f'''{cb}
<article class="wrap prop"><div>
<p class="eyebrow">{esc(p["label"])} · {esc(p["muni"])}</p>
<h1 class="t-h">{esc(p["name"])}</h1>
{gallery(p, d)}
{notice}{dl}
<div class="prose"><h2>Sobre este inmueble</h2><p>{esc(p["txt"])}</p>{nota}
<p>Si quieres ver más inmuebles de la zona, consulta la <a href="{href("inmobiliaria-" + slug(p["muni"]) + "/", d)}">inmobiliaria D&amp;Habitat en {esc(p["muni"])}</a>. Si necesitas financiación, haz tu <a href="{href("financiacion/", d)}">estudio financiero</a>.</p></div>
</div>{form}</article>
<section class="sec wrap"><h2 class="t-hs" style="margin-bottom:32px">Otros inmuebles en {esc(p["muni"])}</h2>{grid(like, d)}</section>'''
    kind = {"piso": "Apartment", "casa": "House"}.get(p["tipo"])
    about = {"@type": kind or "Place", "name": p["name"],
             "address": {"@type": "PostalAddress", "addressLocality": p["muni"], "addressRegion": "Barcelona", "addressCountry": "ES"}}
    if kind:
        about["floorSize"] = {"@type": "QuantitativeValue", "value": p["m2"], "unitCode": "MTK"}
        if p["hab"]: about["numberOfBedrooms"] = p["hab"]
        if p["ban"]: about["numberOfBathroomsTotal"] = p["ban"]
    else:
        about["additionalProperty"] = {"@type": "PropertyValue", "name": "Superficie", "value": p["m2"], "unitCode": "MTK"}
    ld = {"@context": "https://schema.org", "@type": "RealEstateListing", "name": p["name"], "url": SITE + "/" + p["path"], "description": p["txt"],
          "offers": {"@type": "Offer", "price": p["precio"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "seller": {"@id": SITE + "/#agency"}},
          "about": about}
    if p["img"]:
        _c = re.search(r"/(\d+)\.510396/", p["img"]).group(1)
        ld["image"] = [absu(p["img"])] + [SITE + "/img/g/" + f for f in GAL.get(_c, []) if not f.endswith("_01.jpg")][:7]
    write(p["path"], page(p["path"], title, desc, main, cur="comprar", schema=[cl, ld], og=p["img"] or None, imgdns=True), prio="0.6")

def city_page(muni, props, path, h1, lead, title, desc, zonas_txt, cur, office=False, hero_img=None, faqs=()):
    d = 1
    cb, cl = crumbs([("Inicio", ""), (muni, path)], d)
    pt, ct, st = stats(props)
    f = []
    f.append(f'<div><b>{len(props)} inmuebles</b><span>en nuestra cartera de {muni}</span></div>')
    if pt: f.append(f'<div><b>Desde {eur(min(pt))}</b><span>pisos libres, hasta {eur(max(pt))}</span></div>')
    if ct: f.append(f'<div><b>Casas desde {eur(min(ct))}</b><span>hasta {eur(max(ct))}</span></div>')
    elif st: f.append(f'<div><b>Terrenos desde {eur(min(st))}</b><span>hasta {eur(max(st))}</span></div>')
    chips = "".join(f'<span class="chip">{esc(z)} · {n}</span>' for z, n in zona_counts(props))
    office_html = ""
    if office:
        office_html = f'''<section class="sec wrap" id="oficina"><div class="grid g2" style="align-items:center">
{ph(UP + "oficina-terrassa.jpg", "Oficina central de D&Habitat en Terrassa", "4/3", cls="r2")}
<div><p class="eyebrow">Nuestra oficina</p><h2 class="t-h">Oficina central en el barrio de Sant Pere</h2>
<p class="lead" style="margin-top:20px">Es la oficina central de D&amp;Habitat desde 2014: aquí está la dirección de la empresa, parte de los departamentos de apoyo y equipos comerciales que operan sobre todo en el Vallès Occidental. Espacios abiertos y modernos para que te sientas como en casa.</p>
<p style="margin-top:24px"><b style="font-weight:500">Pla de l'Ametllera, 100, local L'Ametllera</b><br>08225 Terrassa (Barcelona)<br><a class="tlink" href="tel:{TEL}">{PHONE}</a></p>
<div class="row" style="margin-top:24px"><a class="btn" href="{MAPS}" rel="noopener">Cómo llegar</a><a class="btn btn-ghost" href="{href("contacto/", d)}">Pedir cita</a></div></div></div></section>'''
    main = f'''{cb}
<section class="hero wrap" style="padding-top:32px"><h1 class="t-hl" style="max-width:18ch">{esc(h1)}</h1><p class="lead">{esc(lead)}</p>
<div class="row"><a class="btn" href="tel:{TEL}">Llamar al {PHONE}</a><a class="btn btn-ghost" href="{href("vender/", d)}">Tasación gratuita</a></div></section>
<section class="sec tight wrap" id="inmuebles"><div class="facts" style="margin-bottom:48px">{"".join(f)}</div>
<p class="eyebrow">Cartera en {esc(muni)}</p><h2 class="t-h" style="margin-bottom:24px">Inmuebles en venta en {esc(muni)}</h2>
<div class="chips" style="margin-bottom:32px">{chips}</div>{grid(props, d)}
<p style="margin-top:32px"><a class="tlink" href="{href("comprar/", d)}?poblacion={slug(muni)}">Filtrar por tipo y precio</a></p></section>
<section class="sec wrap"><div class="prose"><h2>Comprar y vender en {esc(muni)}</h2>{zonas_txt}</div></section>
{office_html}
<section class="sec wrap"><p class="eyebrow">Opiniones de clientes</p><h2 class="t-h">Lo que dicen quienes ya han vendido con nosotros</h2>{rating_line()}<div style="margin-top:40px">{testimonials()}</div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:start"><div><p class="eyebrow">Preguntas frecuentes</p><h2 class="t-h">Preguntas sobre {esc(muni)}</h2></div>{faq_html(faqs)}</div></section>
{band(d, f"¿Quieres vender tu vivienda en {muni}?", "Tasamos tu vivienda sin visitas y sin demoras. Cuéntanos dónde está y te llamamos.")}'''
    ld_list = {"@context": "https://schema.org", "@type": "ItemList", "name": f"Inmuebles en venta en {muni}",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/" + p["path"], "name": p["name"]} for i, p in enumerate(props)]}
    sch = [cl, ld_list, faq_ld(faqs)]
    if office: sch.insert(0, {"@context": "https://schema.org", **AGENCY})
    write(path, page(path, title, desc, main, cur=cur, schema=sch, imgdns=True), prio="0.9")

def build_cities():
    zt = "".join(f"<p>{t}</p>" for t in [
        f"En nuestra cartera de octubre de 2026 hay inmuebles en Sant Pere, Poble Nou-Zona Olímpica, Pere Parres, Vista Alegre, Cementiri Vell, Can Parellada, Les Fonts, Ègara y Torre-sana. Entre los pisos libres, los precios van de {eur(min(stats(TERRASSA)[0]))} a {eur(max(stats(TERRASSA)[0]))}, con opciones para entrar a vivir y viviendas a reformar.",
        "La Zona Esportiva ofrece pisos amplios con piscina, parking y trastero. Cementiri Vell destaca por estar frente al Parc de Vallparadís, y Sant Pere, por su mercado municipal y su oferta de plazas de parking. Para una vivienda unifamiliar, Vista Alegre es una de las zonas más tranquilas de la ciudad.",
        "Si quieres vender, empezamos por una tasación gratuita sin visitas y sin demoras. Si compras, te ayudamos a elegir y a conseguir la financiación."])
    city_page("Terrassa", TERRASSA, "inmobiliaria-terrassa/", "Inmobiliaria en Terrassa: pisos, casas y locales en venta",
        "Somos la inmobiliaria de confianza de Terrassa. Oficina central en Sant Pere, 4,9 ★ en Google y una cartera de pisos, casas, locales y parkings.",
        "Inmobiliaria en Terrassa: pisos y casas en venta · D&Habitat",
        f"Inmobiliaria en Terrassa con oficina central en Sant Pere. {len(TERRASSA)} inmuebles en venta, 4,9 ★ en Google y tasación gratuita sin visitas.",
        zt, "terrassa", office=True, hero_img=UP + "oficina-terrassa.jpg", faqs=["barrios", "docs", "gastos", "cita"])
    pr, cr, sr = stats(RUBI)
    zr = "".join(f"<p>{t}</p>" for t in [
        f"En Rubí tenemos casas desde {eur(min(cr))}, pisos de 66 a 100 m² y una amplia oferta de terrenos edificables desde {eur(min(sr))} en urbanizaciones como Can Sola, Can Mir y Castellnou. Varias de estas parcelas pertenecen a Rubí pero lindan por el frente con Terrassa, con parada de autobús cerca.",
        "Els Avets reúne casas adosadas reformadas y pisos amplios en una zona residencial tranquila. Sant Muç ofrece propiedades con mucho espacio, y Can Oriol, terrenos urbanos dentro del núcleo urbano, con servicios, comercios y transporte cerca.",
        "El equipo de la oficina central de Terrassa trabaja habitualmente en Rubí y todas nuestras oficinas comparten la misma cartera de inmuebles."])
    city_page("Rubí", RUBI, "inmobiliaria-rubi/", "Inmobiliaria en Rubí: casas, pisos y terrenos en venta",
        "Casas, pisos y terrenos en Rubí, con el equipo de D&Habitat. Tasación gratuita sin visitas y asesoramiento hipotecario.",
        "Inmobiliaria en Rubí: casas y terrenos en venta · D&Habitat",
        f"Inmobiliaria en Rubí. {len(RUBI)} inmuebles en venta: casas desde {eur(min(cr))} y terrenos desde {eur(min(sr))}. Tasación gratuita con D&Habitat.",
        zr, "rubi", hero_img=UP + "inmuebles-rubi-1200x498.jpg", faqs=["zonas", "tiempo", "gastos", "cita"])

def build_vender():
    d = 1
    cb, cl = crumbs([("Inicio", ""), ("Tasación gratuita", "vender/")], d)
    extra = '''<div class="field"><label for="vd-p">Población del inmueble</label><select id="vd-p" name="poblacion"><option>Terrassa</option><option>Rubí</option><option>Sabadell</option><option>Vacarisses</option><option>Otra</option></select></div>
<div class="field"><label for="vd-tp">Tipo de inmueble</label><select id="vd-tp" name="tipo"><option>Piso</option><option>Casa</option><option>Solar</option><option>Local</option><option>Parking</option></select></div>'''
    form = with_priv(contact_form("tasacion", extra, "Pedir tasación gratuita"), d)
    main = f'''{cb}
<section class="hero wrap" style="padding-top:32px"><h1 class="t-hl" style="max-width:18ch">Tasación gratuita de tu vivienda en Terrassa, Rubí y el Vallès</h1>
<p class="lead">Conocer el valor de tu vivienda es básico para venderla por un precio acorde a sus características y su ubicación. Te la tasamos sin visitas y sin demoras.</p>
</section>
<section class="sec tight wrap"><div class="grid g2" style="align-items:start"><div>{way("Cómo funciona", "Cuatro pasos hasta la firma", [("cue", "Cuéntanos", "Dónde está y cómo es tu vivienda."), ("tas", "Te la tasamos", "Sin visitas y sin demoras, con datos de tu zona."), ("mer", "Salimos al mercado", "Precio de salida, publicación y visitas."), ("fir", "Firmamos", "Te acompañamos hasta la entrega de llaves.")])}</div>
<div class="sand first-m"><h2 class="t-hs" style="margin-bottom:24px">Solicita tu tasación</h2>{form}</div></div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:center">{ph(UP + "oficina-sabadell2.jpg", "Equipo de D&Habitat atendiendo a un cliente", "4/3", cls="r2")}
<div class="prose"><p class="eyebrow">Por qué tasar con nosotros</p><h2 style="margin-top:0">Un precio justo se apoya en la zona, no en una media</h2>
<p>El precio de un piso en Pere Parres no se parece al de uno en la Zona Olímpica, y una casa en Els Avets se mueve en otro mercado que un terreno en Can Sola. Conocemos Terrassa, Rubí y el Vallès Occidental porque vendemos aquí cada semana.</p>
<p>Con la tasación sabrás cuánto vale tu vivienda, qué precio de salida te recomendamos y qué gastos tendrás al vender. Sin compromiso.</p></div></div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:start"><div><p class="eyebrow">Preguntas frecuentes</p><h2 class="t-h">Antes de vender</h2></div>{faq_html(["coste", "tasacion", "tiempo", "docs"])}</div></section>
<section class="sec wrap"><h2 class="t-h" style="margin-bottom:32px">Lo que cuentan quienes han vendido</h2>{testimonials()}</section>'''
    ld = {"@context": "https://schema.org", "@type": "Service", "name": "Tasación gratuita de vivienda", "serviceType": "Tasación inmobiliaria",
          "provider": {"@id": SITE + "/#agency"}, "areaServed": ["Terrassa", "Rubí", "Vallès Occidental"], "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}}
    write("vender/", page("vender/", "Tasación gratuita de vivienda en Terrassa y Rubí · D&Habitat",
        "Tasación gratuita de tu vivienda en Terrassa, Rubí y el Vallès Occidental, sin visitas y sin demoras. Conoce el valor de tu casa con D&Habitat.",
        main, cur="vender", schema=[cl, ld, faq_ld(["coste", "tasacion", "tiempo", "docs"])]), prio="0.9")

def build_fin():
    d = 1
    cb, cl = crumbs([("Inicio", ""), ("Financiación", "financiacion/")], d)
    form = with_priv(contact_form("financiacion", "", "Solicitar estudio financiero"), d)
    main = f'''{cb}
<section class="wrap fin-wrap"><div class="fin-hero">
<div class="fin-txt"><p class="eyebrow">Asesoramiento hipotecario</p><h1 class="t-hl">Financiación para tu hogar</h1>
<p class="lead">Ofrecemos un servicio personalizado de asesoramiento hipotecario. Estudiamos a fondo tus necesidades y te acompañamos en todos los trámites.</p>
<div class="row"><a class="btn" href="#calc">Calcular mi cuota</a><a class="btn btn-ghost-w" href="#estudio">Solicitar estudio</a></div></div>
<ul class="fin-pts">
<li><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/></svg></span><div><b>Estudio personalizado</b><span>Analizamos tu caso y tus necesidades reales.</span></div></li>
<li><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg></span><div><b>Amplio abanico de opciones</b><span>Te presentamos distintas posibilidades para elegir.</span></div></li>
<li><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/></svg></span><div><b>Acompañamiento en los trámites</b><span>Te informamos y facilitamos cada paso.</span></div></li>
</ul></div></section>
<section class="sec tight wrap"><div class="grid g2 fin-two" style="align-items:start">
<div class="calc" id="calc"><div class="calc-top"><p class="eyebrow">Calculadora hipotecaria</p>
<output id="c-cuota" aria-live="polite">0 €</output><p class="small">Cuota mensual orientativa</p></div>
<div class="calc-body">
<div class="field"><label for="c-importe">Importe a solicitar</label><div class="num"><input id="c-importe" type="number" inputmode="numeric" min="1000" step="1000" value="200000"><i>€</i></div><input class="rng" id="c-importe-r" type="range" min="20000" max="1000000" step="5000" value="200000" aria-label="Importe a solicitar"></div>
<div class="field"><label for="c-anos">Años de amortización</label><div class="num"><input id="c-anos" type="number" inputmode="numeric" min="1" max="40" value="30"><i>años</i></div><input class="rng" id="c-anos-r" type="range" min="5" max="40" step="1" value="30" aria-label="Años de amortización"></div>
<div class="field"><label for="c-tipo">Tipo de interés anual</label><div class="num"><input id="c-tipo" type="number" inputmode="decimal" min="0" step="0.05" value="3"><i>%</i></div><input class="rng" id="c-tipo-r" type="range" min="0" max="8" step="0.05" value="3" aria-label="Tipo de interés anual"></div>
<div class="split" aria-hidden="true"><i id="c-bar" style="width:62%"></i></div>
<div class="split-leg"><span><u class="a"></u>Capital <b id="c-cap">0 €</b></span><span><u class="b"></u>Intereses <b id="c-int">0 €</b></span></div>
<div class="res"><div><span>Total final a pagar</span><b id="c-total">0 €</b></div></div>
<p class="muted small" style="margin:18px 0 0">Simulación orientativa, sin comisiones ni seguros. Las condiciones reales dependen de la entidad y de tu perfil.</p></div></div>
<div id="estudio" class="fin-form"><p class="eyebrow">Estudio financiero</p><h2 class="t-h" style="margin-bottom:16px">Cuéntanos tu caso</h2>
<p class="lead" style="margin-bottom:24px">Te asesoramos para la compra de tu vivienda y para solicitar una hipoteca según tus necesidades reales. Te acompañamos e informamos de todos los trámites a realizar.</p>
<div class="sand">{form}</div></div></div></section>
<section class="sec wrap"><p class="eyebrow">Cómo trabajamos</p><h2 class="t-h" style="margin-bottom:36px">Tres pasos hasta tu hipoteca</h2>
<div class="grid g3 fin-steps">
<div class="fcard"><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><em>01</em><h3>Estudiamos tu caso</h3><p>Hablamos contigo para entender qué necesitas y qué puedes asumir, antes de elegir vivienda.</p></div>
<div class="fcard"><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h18M3 6h18M3 18h18"/></svg></span><em>02</em><h3>Comparamos opciones</h3><p>Te ofrecemos un amplio abanico de posibilidades para que decidas con información.</p></div>
<div class="fcard"><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></span><em>03</em><h3>Te acompañamos en los trámites</h3><p>Facilitamos y te explicamos cada gestión hasta la firma.</p></div></div></section>
<section class="sec wrap"><div class="fin-photo"><div class="prose"><p class="eyebrow">Antes de elegir vivienda</p><h2 style="margin-top:0">Lo que te acompañará los próximos años es la hipoteca</h2>
<p>Encontrar un piso o una casa que te encaje es importante, y comprar a buen precio también. Pero lo que vas a pagar cada mes durante años es la hipoteca. Por eso conviene hacer un buen estudio antes de decidir.</p>
<p>Somos una empresa especializada en el sector financiero, con un trato familiar y cercano. Facilitamos los trámites y estudiamos a fondo tus necesidades para ofrecerte un amplio abanico de posibilidades.</p></div>
{ph(UP + "estudio-hipotecario.jpg", "Estudio hipotecario con un asesor de D&Habitat", "4/3", cls="r2")}</div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:start"><div><p class="eyebrow">Preguntas frecuentes</p><h2 class="t-h">Antes de pedir una hipoteca</h2></div>{faq_html(["financia", "docs", "gastos"])}</div></section>'''
    ld = {"@context": "https://schema.org", "@type": "Service", "name": "Asesoramiento hipotecario", "serviceType": "Asesoramiento financiero para la compra de vivienda",
          "provider": {"@id": SITE + "/#agency"}, "areaServed": ["Terrassa", "Rubí", "Vallès Occidental"]}
    write("financiacion/", page("financiacion/", "Financiación y asesoramiento hipotecario en Terrassa · D&Habitat",
        "Asesoramiento hipotecario personalizado y calculadora de hipoteca. Pide tu estudio financiero con D&Habitat en Terrassa.",
        main, cur="financiacion", schema=[cl, ld, faq_ld(["financia", "docs", "gastos"])]), prio="0.8")

def build_nosotros():
    d = 1
    cb, cl = crumbs([("Inicio", ""), ("Nosotros", "nosotros/")], d)
    team = '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">' + "".join(
        f'<div class="person"><div class="avatar" aria-hidden="true">{n[0]}</div><h3>{n}</h3><span class="small muted">Equipo D&amp;Habitat</span></div>' for n in TEAM) + "</div>"
    vals = [("Entendemos a las personas", "Nos centramos en entender a nuestros clientes como personas: qué dicen, pero también qué sienten, a qué aspiran, qué les frustra y qué necesitan."),
            ("Cuidamos tu patrimonio", "Sabemos lo que un inmueble representa: años de esfuerzo y ahorro. Por eso recomendamos las mejores decisiones para proteger y hacer productivo el patrimonio de nuestros clientes."),
            ("Agilidad en cada paso", "Promovemos mejoras e innovación de forma continua para dar la máxima agilidad a los procesos con los que promovemos los inmuebles de nuestra cartera.")]
    v = '<div class="grid g3">' + "".join(f'<div class="svc"><h3>{t}</h3><p>{x}</p></div>' for t, x in vals) + "</div>"
    form = with_priv(contact_form("nosotros", "", "Enviar mensaje"), d)
    main = f'''{cb}
<section class="hero wrap" style="padding-top:32px"><h1 class="t-hl" style="max-width:18ch">Agencia inmobiliaria en Terrassa y el Vallès Occidental</h1>
<p class="lead">En D&amp;Habitat anteponemos los intereses de nuestros clientes ofreciendo el mejor asesoramiento y nuestro método de venta. Acompañamos todo el proceso: enseñarte tu futura vivienda, ayudarte a elegir y llevarte hasta la firma.</p>
<div class="row"><a class="btn" href="{href("contacto/", d)}">Contactar</a><a class="btn btn-ghost" href="tel:{TEL}">Llamar al {PHONE}</a></div></section>
<section class="sec tight wrap"><p class="eyebrow">Cómo trabajamos</p><h2 class="t-h" style="margin-bottom:40px">Tres ideas que guían cada operación</h2>{v}</section>
<section class="sec wrap"><div class="grid g2" style="align-items:center"><div class="prose"><p class="eyebrow">Equipo</p><h2 style="margin-top:0">Las personas detrás de las opiniones</h2>
<p>En Google, nuestros clientes agradecen por su nombre a quienes les han acompañado. Respondemos cada opinión una a una, y esos nombres son los que verás en la oficina.</p>
{rating_line()}</div>{ph(UP + "oficina-terrassa.jpg", "Oficina central de D&Habitat en Terrassa", "4/3", cls="r2")}</div>
<div style="margin-top:56px">{team}</div></section>
<section class="sec wrap"><div class="grid g2" style="align-items:start"><div class="prose"><p class="eyebrow">Confianza y regulación</p><h2 style="margin-top:0">Datos de la empresa</h2>
<p>D&amp;HABITAT FINANCE, S.L. · CIF B67372052.<br>Pla de l'Ametllera, 100, local L'Ametllera, 08225 Terrassa (Barcelona).</p>
<p>Inscrita en el Registre d'Agents Immobiliaris de Catalunya (AICAT), el registro oficial de los agentes inmobiliarios de Cataluña.</p>
<p>Oficina central desde 2014. Todas las oficinas comparten la misma cartera de inmuebles y dan servicio en cualquier punto de la red.</p></div>
<div class="sand"><h2 class="t-hs" style="margin-bottom:24px">Solicita información</h2>{form}</div></div></section>
<section class="sec wrap"><h2 class="t-h" style="margin-bottom:32px">Lo que dicen nuestros clientes</h2>{testimonials()}</section>'''
    write("nosotros/", page("nosotros/", "Nosotros · Agencia inmobiliaria D&Habitat en Terrassa",
        "Conoce a D&Habitat by Finance: agencia inmobiliaria con oficina central en Terrassa desde 2014, equipo cercano y 4,9 ★ en Google.",
        main, cur="nosotros", schema=[{"@context": "https://schema.org", **AGENCY}, cl]), prio="0.7")

def build_contact():
    d = 1
    cb, cl = crumbs([("Inicio", ""), ("Contacto", "contacto/")], d)
    form = with_priv(contact_form("contacto", '<div class="field"><label for="ct-a">Motivo</label><select id="ct-a" name="motivo"><option>Quiero comprar</option><option>Quiero vender</option><option>Quiero financiar</option><option>Otro</option></select></div>', "Enviar mensaje"), d)
    main = f'''{cb}
<section class="wrap" style="padding-top:32px"><h1 class="t-hl">Contacta con D&amp;Habitat</h1><p class="lead" style="margin-top:24px">Llámanos, escríbenos o pasa por la oficina. Te respondemos por tu nombre.</p></section>
<section class="sec tight wrap"><div class="grid g2" style="align-items:start">
<div class="sand"><h2 class="t-hs" style="margin-bottom:24px">Escríbenos</h2>{form}</div>
<div class="prose"><h2 style="margin-top:0">Oficina en Terrassa</h2>
<p><b style="font-weight:500">D&amp;HABITAT by FINANCE</b><br>Pla de l'Ametllera, 100, local L'Ametllera<br>08225 Terrassa (Barcelona)</p>
<p>Teléfono: <a href="tel:{TEL}">{PHONE}</a></p>
<p>También atendemos con cita online.</p>
<div class="row"><a class="btn" href="{MAPS}" rel="noopener">Cómo llegar</a><a class="btn btn-ghost" href="{FB}" rel="noopener">Facebook</a><a class="btn btn-ghost" href="{IG}" rel="noopener">Instagram</a></div></div></div></section>'''
    write("contacto/", page("contacto/", "Contacto · Inmobiliaria D&Habitat en Terrassa",
        f"Contacta con D&Habitat by Finance en Terrassa: teléfono {PHONE}, formulario y cómo llegar a la oficina de Pla de l'Ametllera, 100.",
        main, cur="", schema=[{"@context": "https://schema.org", **AGENCY}, cl]), prio="0.7")

def build_faq():
    d = 1
    cb, cl = crumbs([("Inicio", ""), ("Preguntas frecuentes", "preguntas-frecuentes/")], d)
    keys = ["coste", "tasacion", "tiempo", "docs", "gastos", "financia", "barrios", "zonas", "ocupado", "aicat", "cita"]
    main = f'''{cb}
<section class="wrap" style="padding-top:32px"><h1 class="t-hl" style="max-width:18ch">Preguntas frecuentes sobre comprar y vender en el Vallès</h1>
<p class="lead" style="margin-top:24px">Respuestas directas a lo que más nos preguntan en Terrassa y Rubí. Si tu duda no está aquí, llámanos al <a class="tlink" href="tel:{TEL}">{PHONE}</a>.</p></section>
<section class="sec tight wrap narrow" style="margin-inline:0;max-width:var(--max)"><div style="max-width:820px">{faq_html(keys)}</div></section>
{band(d, "¿Tienes otra pregunta?", "Cuéntanosla y te respondemos.")}'''
    write("preguntas-frecuentes/", page("preguntas-frecuentes/", "Preguntas frecuentes · Comprar y vender en Terrassa y Rubí",
        "Cuánto cuesta vender un piso, qué documentación necesitas para comprar, gastos, financiación y más. Respuestas de D&Habitat en Terrassa y Rubí.",
        main, schema=[cl, faq_ld(keys)]), prio="0.7")

def build_legal():
    d = 1
    items = [("condiciones-legales/", "Condiciones legales"), ("politica-privacidad/", "Política de privacidad"), ("politica-cookies/", "Política de cookies")]
    for path, t in items:
        main = f'''<section class="wrap" style="padding-top:64px"><h1 class="t-hl">{t}</h1>
<div class="prose" style="margin-top:32px"><h2>Titular</h2><p>D&amp;HABITAT FINANCE, S.L. · CIF B67372052<br>Pla de l'Ametllera, 100, local L'Ametllera, 08225 Terrassa (Barcelona)<br>Teléfono <a href="tel:{TEL}">{PHONE}</a></p>
<div class="notice">Pendiente de migrar: pega aquí el texto legal completo y vigente de la web actual antes de publicar. Esta página está marcada como noindex hasta entonces.</div></div></section>'''
        write(path, page(path, f"{t} · {BRAND}", f"{t} de D&HABITAT FINANCE, S.L.", main, robots="noindex,follow"), index=False)
    main = f'''<section class="wrap" style="padding-top:96px;padding-bottom:40px"><h1 class="t-hl">Esta página no existe</h1>
<p class="lead" style="margin-top:24px">Puede que el enlace haya cambiado. Prueba con el listado de inmuebles o llámanos al {PHONE}.</p>
<div class="row" style="margin-top:32px"><a class="btn" href="{href("comprar/", 0)}">Ver inmuebles</a><a class="btn btn-ghost" href="{href("", 0)}">Ir al inicio</a></div></section>'''
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(page("", "Página no encontrada · " + BRAND, "Página no encontrada", main, robots="noindex").replace('="./', '="/'))

def build_extras():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio, freq in SITEMAP:
        xml.append(f"<url><loc>{SITE}/{path}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(f"""# {BRAND}

> Agencia inmobiliaria con oficina central en Terrassa (Barcelona) desde 2014. Compra, venta, tasación gratuita y asesoramiento hipotecario en Terrassa, Rubí y el Vallès Occidental. Valoración de 4,9 sobre 5 en 321 opiniones de Google.

Nombre comercial: {BRAND} (también «D&Habitat»). Razón social: D&HABITAT FINANCE, S.L.
Dirección: Pla de l'Ametllera, 100, local L'Ametllera, 08225 Terrassa. Teléfono: {PHONE}.

## Páginas principales
- [Inmobiliaria en Terrassa]({SITE}/inmobiliaria-terrassa/): oficina central, barrios y cartera en Terrassa.
- [Inmobiliaria en Rubí]({SITE}/inmobiliaria-rubi/): casas, pisos y terrenos en Rubí.
- [Inmuebles en venta]({SITE}/comprar/): listado completo con filtros.
- [Tasación gratuita]({SITE}/vender/): cómo funciona y formulario.
- [Financiación]({SITE}/financiacion/): asesoramiento hipotecario y calculadora.
- [Preguntas frecuentes]({SITE}/preguntas-frecuentes/): costes, documentación, gastos y plazos.
""")
    redirects = """# Redirecciones 301 desde la web WordPress actual (formato Netlify/Cloudflare Pages)
/compra-inmueble/        /comprar/                      301
/alquila-inmueble/       /comprar/                      301
/valoraciones/           /vender/                       301
/financiamiento/         /financiacion/                 301
/dhabitat/               /nosotros/                     301
/oficina-en-terrassa/    /inmobiliaria-terrassa/        301
/oficina-en-rubi/        /inmobiliaria-rubi/            301
/oficina-en-cerdanyola/  /inmobiliaria-terrassa/        301
/contactar/              /contacto/                     301
/inmuebles/venta/TERRASSA/  /inmobiliaria-terrassa/     301
/inmuebles/venta/RUBI/      /inmobiliaria-rubi/         301
/inmuebles/venta/*       /comprar/                      301
/inmuebles/alquiler/*    /comprar/                      301
/inmuebles-poblacion/    /comprar/                      301
/politica-de-cookies/    /politica-cookies/             301
"""
    open(os.path.join(OUT, "_redirects"), "w").write(redirects)

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "css")); os.makedirs(os.path.join(OUT, "js"))
    shutil.copy(os.path.join(HERE, "assets/style.css"), os.path.join(OUT, "css/style.css"))
    shutil.copy(os.path.join(HERE, "assets/app.js"), os.path.join(OUT, "js/app.js"))
    shutil.copy(os.path.join(HERE, "assets/config.js"), os.path.join(OUT, "js/config.js"))
    shutil.copytree(os.path.join(HERE, "assets/img"), os.path.join(OUT, "img"))
    shutil.copy(os.path.join(HERE, "assets/favicon.ico"), os.path.join(OUT, "favicon.ico"))
    json.dump({"name": BRAND, "short_name": "D&Habitat", "lang": "es", "start_url": "/", "display": "browser",
               "background_color": "#fdfdf7", "theme_color": "#0a2633",
               "icons": [{"src": "img/l/icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "img/l/icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "img/l/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
              open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    build_home(); build_listing(); build_cities(); build_vender(); build_fin(); build_nosotros(); build_contact(); build_faq()
    for p in PROPS: property_page(p)
    build_legal()
    if not PREVIEW: build_extras()
    if PREVIEW:  # la vista previa solo lleva las fotos de galería que realmente muestra
        used = set()
        for r, _, fs_ in os.walk(OUT):
            for f in fs_:
                if f.endswith(".html"): used |= set(re.findall(r"img/g/([\w.\-]+)", open(os.path.join(r, f), encoding="utf-8").read()))
        gd = os.path.join(OUT, "img", "g")
        for f in os.listdir(gd):
            if f not in used: os.remove(os.path.join(gd, f))
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("OK", len(PROPS), "fichas;", n, "ficheros en", OUT)
