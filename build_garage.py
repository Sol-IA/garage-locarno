#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de pages statiques GARAGE LOCARNO (Marseille 5e).
Centralise l'en-tête, la nav, le pied de page partagés et émet du HTML statique pur.
Adapté du système LUMIA. Lancer : python3 build_garage.py
"""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Constantes
SITE = "https://garagelocarno.fr"
PHONE_DISPLAY = "09 84 28 23 20"
PHONE_TEL = "+33984282320"
MOBILE_DISPLAY = "06 14 99 19 97"
MOBILE_TEL = "+33614991997"
EMAIL = "garagelocarno@gmail.com"
GBP_URL = "https://maps.app.goo.gl/E4ziKJRRoAAL2yvo7"
GBP_REVIEW = "https://search.google.com/local/writereview?placeid=ChIJp zU" # remplacé ci-dessous
GBP_REVIEW = GBP_URL  # bouton "Laisser un avis" pointe vers la fiche (à affiner avec place_id réel)
RATING = "4.8"           # note Google (à confirmer en live)
REVIEW_COUNT = "50"      # plancher vérifiable (Bottin "50+") ; à actualiser sur la fiche live
# Endpoint Formspree à créer puis coller ici (V1 GitHub Pages). Voir note de livraison.
FORMSPREE = "https://formspree.io/f/REMPLACER_ID_FORMSPREE"

# ---------------------------------------------------------------- SVG
def svg_phone(cls=""):
    return ('<svg %sviewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
            '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.6.7 2.34a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.74-1.27a2 2 0 0 1 2.11-.45c.74.34 1.53.57 2.34.7A2 2 0 0 1 22 16.92z"/></svg>'
            % (('class="%s" ' % cls) if cls else ''))

def svg_star():
    return ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:14px;height:14px;vertical-align:-2px">'
            '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>')

LOGO_MARK = ('<svg class="nav__logo-mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">'
             '<rect x="1" y="1" width="38" height="38" rx="8" fill="#1C1A18"/>'
             '<path d="M20 9a11 11 0 1 0 0 22 11 11 0 0 0 0-22zm0 4.2a6.8 6.8 0 1 1 0 13.6 6.8 6.8 0 0 1 0-13.6z" fill="#C2742F"/>'
             '<circle cx="20" cy="20" r="2.4" fill="#C2742F"/>'
             '<path d="M20 4.2v4M20 31.8v4M4.2 20h4M31.8 20h4" stroke="#C2742F" stroke-width="2.2" stroke-linecap="round"/></svg>')

# ---------------------------------------------------------------- Schema JSON-LD
def schema_autorepair():
    return ('<script type="application/ld+json">'
'{"@context":"https://schema.org","@type":"AutoRepair","name":"Garage Locarno",'
'"description":"Garage automobile toutes marques à Marseille 5e : entretien, révision, freins, pneus, diagnostic. Entretien moto et scooter. Devis gratuit.",'
'"url":"%s/","telephone":"%s","email":"%s",'
'"image":"%s/assets/og-image.jpg","logo":"%s/assets/logo.png",'
'"address":{"@type":"PostalAddress","streetAddress":"5 rue de Locarno","addressLocality":"Marseille","postalCode":"13005","addressCountry":"FR"},'
'"geo":{"@type":"GeoCoordinates","latitude":43.2941075,"longitude":5.3945891},'
'"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"}],'
'"areaServed":[{"@type":"City","name":"Marseille"},{"@type":"PostalCode","name":"13005"},{"@type":"PostalCode","name":"13004"},{"@type":"PostalCode","name":"13006"}],'
'"priceRange":"€€","currenciesAccepted":"EUR","paymentAccepted":"Carte bancaire, sans contact, espèces",'
'"foundingDate":"2020-08-07","founder":{"@type":"Person","name":"Aymeric Assouline","jobTitle":"Gérant"},'
'"parentOrganization":{"@type":"Organization","name":"Groupe C\'Carré"},'
'"makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":"Révision et entretien auto"}},'
'{"@type":"Offer","itemOffered":{"@type":"Service","name":"Vidange"}},'
'{"@type":"Offer","itemOffered":{"@type":"Service","name":"Freinage"}},'
'{"@type":"Offer","itemOffered":{"@type":"Service","name":"Montage de pneus"}},'
'{"@type":"Offer","itemOffered":{"@type":"Service","name":"Diagnostic électronique"}},'
'{"@type":"Offer","itemOffered":{"@type":"Service","name":"Entretien moto et scooter"}}],'
'"aggregateRating":{"@type":"AggregateRating","ratingValue":"%s","reviewCount":"%s","bestRating":"5"},'
'"sameAs":["%s","https://www.pagesjaunes.fr/pros/61348491","https://www.allopneus.com/montage-pneu/bouches-du-rhone-13/marseille-13005/c-carre-le-garage-locarno-21351"]}'
'</script>\n' % (SITE, PHONE_TEL, EMAIL, SITE, SITE, RATING, REVIEW_COUNT, GBP_URL))

def schema_breadcrumb(items):
    # items : liste de (name, url-relatif-ou-absolu)
    el = []
    for i, (name, url) in enumerate(items, 1):
        full = url if url.startswith("http") else "%s/%s" % (SITE, url)
        el.append('{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}' % (i, name, full))
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}</script>\n'
            % ",".join(el))

def schema_service(name, desc, service_type):
    return ('<script type="application/ld+json">'
'{"@context":"https://schema.org","@type":"Service","name":"%s","description":"%s","serviceType":"%s",'
'"provider":{"@type":"AutoRepair","name":"Garage Locarno","telephone":"%s",'
'"address":{"@type":"PostalAddress","streetAddress":"5 rue de Locarno","addressLocality":"Marseille","postalCode":"13005","addressCountry":"FR"}},'
'"areaServed":{"@type":"City","name":"Marseille"}}</script>\n'
            % (name, desc, service_type, PHONE_TEL))

def schema_faq(qa):
    items = []
    for q, a in qa:
        a_txt = a.replace('"', '\\"')
        items.append('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a_txt))
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>\n'
            % ",".join(items))

# ---------------------------------------------------------------- Layout partagé
def topbar():
    return (
'<div class="topbar"><div class="container">'
'<div class="topbar__left"><a href="tel:%s">%s %s</a>'
'<a href="mailto:%s" class="topbar__email">%s</a></div>'
'<div class="topbar__right">'
'<span class="topbar__badge"><span class="stars">%s</span> <b>%s/5</b> sur Google &middot; plus de %s avis</span>'
'</div></div></div>' % (PHONE_TEL, svg_phone(), PHONE_DISPLAY, EMAIL, EMAIL,
                         '&#9733;&#9733;&#9733;&#9733;&#9733;', RATING.replace('.', ','), REVIEW_COUNT))

def nav():
    return (
'<nav id="nav" aria-label="Navigation principale"><div class="container">'
'<a href="index.html" class="nav__logo" aria-label="Garage Locarno, accueil"><img src="assets/logo.png?v=2" alt="Garage Locarno" width="122" height="42" loading="eager"></a>'
'<div class="nav__menu" id="nav-menu">'
'<a href="index.html">Accueil</a>'
'<div class="nav__dropdown"><a href="index.html#prestations">Services auto</a><div class="nav__dropdown-menu">'
'<a href="entretien-revision.html">Entretien &amp; révision</a>'
'<a href="vidange.html">Vidange</a>'
'<a href="freinage.html">Freins</a>'
'<a href="pneus.html">Pneus &amp; montage</a>'
'<a href="diagnostic.html">Diagnostic électronique</a>'
'<a href="climatisation.html">Climatisation</a>'
'<a href="batterie.html">Batterie &amp; éclairage</a></div></div>'
'<a href="moto-scooter.html">Moto / Scooter</a>'
'<a href="a-propos.html">À propos</a>'
'<a href="avis.html">Avis</a>'
'<a href="contact.html">Contact</a>'
'<a href="tel:%s" class="nav__phone">%s %s</a>'
'<a href="contact.html" class="btn-cta-nav">Devis gratuit</a></div>'
'<button class="nav__toggle" id="nav-toggle" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>'
'</div></nav>' % (PHONE_TEL, svg_phone(), PHONE_DISPLAY))

def footer():
    return (
'<footer><div class="container"><div class="footer-grid">'
'<div class="footer__brand"><img src="assets/logo.png?v=2" alt="Garage Locarno" width="160" height="55" class="footer__logo" loading="lazy">'
'<p>Garage automobile et moto toutes marques à Marseille 5e, en centre-ville. Entretien, réparation, révision, pneus et diagnostic. Devis gratuit, et on vous explique tout avant d\'intervenir.</p></div>'
'<nav class="footer__col" aria-label="Services"><p class="footer__title">Services</p><ul class="footer__links">'
'<li><a href="entretien-revision.html">Entretien &amp; révision</a></li>'
'<li><a href="vidange.html">Vidange</a></li>'
'<li><a href="freinage.html">Freins</a></li>'
'<li><a href="pneus.html">Pneus &amp; montage</a></li>'
'<li><a href="diagnostic.html">Diagnostic</a></li>'
'<li><a href="climatisation.html">Climatisation</a></li>'
'<li><a href="batterie.html">Batterie &amp; éclairage</a></li>'
'<li><a href="moto-scooter.html">Moto / Scooter</a></li></ul></nav>'
'<nav class="footer__col" aria-label="Le garage"><p class="footer__title">Le garage</p><ul class="footer__links">'
'<li><a href="a-propos.html">À propos</a></li>'
'<li><a href="avis.html">Avis clients</a></li>'
'<li><a href="blog.html">Conseils</a></li>'
'<li><a href="contact.html">Contact &amp; devis</a></li></ul></nav>'
'<div class="footer__contact"><p class="footer__title">Contact</p>'
'<p>5 rue de Locarno</p><p>13005 Marseille</p>'
'<p><a href="tel:%s">%s</a></p>'
'<p><a href="mailto:%s">%s</a></p><p>Lun-ven, 9h-18h</p></div>'
'</div><div class="footer__bottom">'
'<p>&copy; 2026 Garage Locarno &middot; Site réalisé par <a href="https://sol-ia.tech" target="_blank" rel="noopener">Sol&middot;IA</a></p>'
'<p><a href="mentions-legales.html">Mentions légales</a> &middot; <a href="politique-confidentialite.html">Confidentialité</a></p>'
'</div></div></footer>' % (PHONE_TEL, PHONE_DISPLAY, EMAIL, EMAIL))

def mobile_cta():
    return (
'<nav class="mobile-cta" aria-label="Actions rapides">'
'<a href="tel:%s" class="btn btn-outline">%s Appeler</a>'
'<a href="contact.html" class="btn btn-primary">Devis gratuit</a></nav>' % (PHONE_TEL, svg_phone()))

def page(filename, title, desc, canonical, body, schema="", robots="index, follow", og_type="website"):
    head = (
'<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
'<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
'<title>%s</title>\n<meta name="description" content="%s">\n'
'<meta name="robots" content="%s">\n<link rel="canonical" href="%s">\n'
'<meta property="og:type" content="%s">\n<meta property="og:title" content="%s">\n'
'<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
'<meta property="og:image" content="%s/assets/og-image.jpg">\n'
'<meta property="og:locale" content="fr_FR">\n<meta name="theme-color" content="#14110D">\n'
'<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">\n'
'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
'<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
'<link rel="stylesheet" href="css/style.min.css">\n%s</head>\n<body>\n'
% (title, desc, robots, canonical, og_type, title, desc, canonical, SITE, schema))
    html = (head
        + '<a href="#main" class="skip-link">Aller au contenu principal</a>\n'
        + topbar() + nav() + '<main id="main">\n' + body + '</main>\n' + footer() + mobile_cta()
        + '\n<script src="js/main.min.js" defer></script>\n</body>\n</html>\n')
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("écrit:", filename, len(html), "o")

# ---------------------------------------------------------------- Helpers contenu
def breadcrumb_html(items):
    parts = []
    for label, href in items:
        parts.append('<a href="%s">%s</a>' % (href, label) if href else label)
    return ('<nav class="breadcrumb" aria-label="Fil d\'Ariane">%s</nav>'
            % ' <span>&rsaquo;</span> '.join(parts))

def faq_html(qa):
    items = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in qa)
    return '<div class="faq">%s</div>' % items

def cta_band():
    return ('<div class="cta-band reveal"><div class="cta-band__text">'
            '<h3>Un souci sur votre véhicule ?</h3><p>Devis gratuit, on vous explique tout avant d\'intervenir.</p></div>'
            '<div class="cta-band__actions">'
            '<a href="tel:%s" class="btn btn-outline">%s %s</a>'
            '<a href="contact.html" class="btn btn-primary">Demander un devis</a></div></div>'
            % (PHONE_TEL, svg_phone(), PHONE_DISPLAY))

def cta_section():
    return ('<section class="cta-section"><div class="container">'
            '<h2>Besoin d\'un <span class="accent">devis gratuit</span> ?</h2>'
            '<p>Appelez le garage ou demandez votre devis en ligne. On vous répond rapidement, et rien n\'est lancé sans votre accord.</p>'
            '<div class="cta-actions">'
            '<a href="tel:%s" class="btn btn-primary btn-lg">%s %s</a>'
            '<a href="contact.html" class="btn btn-ghost-light btn-lg">Demande de devis</a>'
            '</div></div></section>\n' % (PHONE_TEL, svg_phone(), PHONE_DISPLAY))

def service_page(filename, title, desc, h1, crumb_label, intro_html, sections, qa, maillage, service_name, service_type):
    crumbs = [("Accueil", "index.html"), ("Services auto", "index.html#prestations"), (crumb_label, None)]
    sec_html = ''.join('<h2 class="reveal">%s</h2>%s' % (h2, html) for h2, html in sections)
    mail = ''.join('<li><a href="%s">%s</a></li>' % (href, label) for label, href in maillage)
    body = (
'<header class="page-header"><div class="container">%s<h1>%s</h1></div></header>\n'
'<article class="article-body"><div class="container">'
'%s'
'%s'
'%s'
'<h2 class="reveal">Questions fréquentes</h2>%s'
'<div class="callout reveal"><h3>Continuez votre entretien</h3><ul class="check-list">%s</ul></div>'
'</div></article>\n'
'%s'
        % (breadcrumb_html(crumbs), h1, intro_html, cta_band(), sec_html, faq_html(qa), mail, cta_section()))
    schema = (schema_breadcrumb([("Accueil", "index.html"), ("Services auto", "index.html#prestations"), (crumb_label, filename)])
              + schema_service(service_name, desc, service_type)
              + schema_faq(qa))
    page(filename, title, desc, "%s/%s" % (SITE, filename), body, schema=schema, og_type="article")

# ================================================================ PAGES
def build_home():
    icons = {
        'entretien': '<svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4l-6 6a2 2 0 0 0 2.8 2.8l6-6a4 4 0 0 0 5.4-5.4l-2.3 2.3-2.1-.6-.6-2.1z"/></svg>',
        'pneus': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4"/></svg>',
        'freins': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M21 12h-3M12 21v-3M3 12h3"/></svg>',
        'diag': '<svg viewBox="0 0 24 24"><path d="M3 12h4l2 5 4-12 2 7h6"/></svg>',
        'clim': '<svg viewBox="0 0 24 24"><path d="M12 3v18M3 8l18 8M21 8 3 16M8 4l4 3 4-3M8 20l4-3 4 3"/></svg>',
        'batterie': '<svg viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="11" rx="2"/><path d="M7 8V5h4v3M14 8V5h3v3M7 13h3M16 11v4M14 13h4"/></svg>',
        'moto': '<svg viewBox="0 0 24 24"><circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="M5 17h7l4-6h3M12 17l3-6M9 7h4"/></svg>',
        'vidange': '<svg viewBox="0 0 24 24"><path d="M5 4h9l3 4v3h-6V8H5zM8 11v5a2 2 0 0 0 2 2h0M14 14c1.5 2 3 3.2 3 5a3 3 0 0 1-6 0c0-1.8 1.5-3 3-5z"/></svg>',
    }
    cards = [
        ('entretien', 'Entretien &amp; révision', 'Vidange, filtres, 50 points de contrôle, diagnostic. Toutes marques, garantie constructeur préservée.', 'entretien-revision.html'),
        ('vidange', 'Vidange', 'Vidange et filtre à huile, huile adaptée à votre moteur, voyant remis à zéro.', 'entretien-revision.html'),
        ('freins', 'Freins', 'Plaquettes et disques contrôlés et remplacés, devis avant intervention.', 'freinage.html'),
        ('pneus', 'Pneus &amp; montage', 'Centre agréé Allopneus. Livrez vos pneus, on les monte. Équilibrage et parallélisme.', 'pneus.html'),
        ('diag', 'Diagnostic électronique', 'Voyant moteur allumé, lecture des codes à la valise OBD, on identifie avant de réparer.', 'diagnostic.html'),
        ('clim', 'Climatisation', 'Recharge de gaz, contrôle d\'étanchéité, clim qui ne refroidit plus.', 'climatisation.html'),
        ('batterie', 'Batterie &amp; éclairage', 'Test et remplacement de batterie, démarrage difficile, ampoules et feux.', 'batterie.html'),
        ('moto', 'Moto &amp; scooter', 'Même atelier, équipe 2-roues expérimentée : vidange, pneus, freins, révision.', 'moto-scooter.html'),
    ]
    cards_html = ''
    for i, (ic, t, p, href) in enumerate(cards):
        d = ' reveal-d%d' % ((i % 4) + 1)
        cards_html += (
'<article class="service-card reveal%s"><div class="service-card__body">'
'<div class="service-card__icon">%s</div>'
'<h3>%s</h3><p>%s</p>'
'<span class="service-card__cta">Voir le service &rarr;</span></div>'
'<a href="%s" class="service-card__link" aria-label="%s"></a></article>'
            % (d, icons[ic], t, p, href, t.replace('&amp;', 'et')))

    features = [
        ('1', 'On explique avant de réparer.', 'Chaque panne est diagnostiquée et le devis validé avec vous avant qu\'on touche à quoi que ce soit. C\'est la loi Hamon, et c\'est surtout notre façon de travailler.'),
        ('2', 'Toutes marques, auto et moto.', 'Une équipe qui travaille la mécanique depuis plus de 10 ans, sur voiture comme sur deux-roues, essence, diesel et hybride.'),
        ('3', 'Au bon prix.', 'Fidèles aux mêmes fournisseurs de pièces depuis des années, on négocie pour vous. Vous savez ce que vous payez, et pourquoi.'),
    ]
    feat_html = ''.join(
'<div class="feature reveal reveal-d%d"><span class="feature__num">%s</span><h3>%s</h3><p>%s</p></div>'
        % ((i % 3) + 1, n, t, p) for i, (n, t, p) in enumerate(features))

    reviews = [
        ('Daniel', 'Cela fait cinq ans que je confie mes véhicules au garage Locarno. Une équipe à l\'écoute, qui prend le temps d\'expliquer et un travail toujours soigné.'),
        ('Thibaut', 'Atelier propre et rénové, accueil sympathique. On m\'a prévenu d\'un ajustement sur le devis avant d\'intervenir, j\'apprécie cette transparence.'),
        ('Anissa', 'Prise en charge rapide de ma voiture, travail efficace et personnel agréable. Des gens sérieux et honnêtes, je recommande.'),
    ]
    STARS = '&#9733;&#9733;&#9733;&#9733;&#9733;'
    slides_html = ''.join(
'<figure class="testimonial"><div class="testimonial__quote">&ldquo;</div>'
'<div class="testimonial__stars">%s</div>'
'<blockquote class="testimonial__text">%s</blockquote>'
'<figcaption class="testimonial__author">%s <span>&middot; Client Garage Locarno</span></figcaption></figure>'
        % (STARS, t, n) for n, t in reviews)

    gallery = [
        ('atelier', 'tall', 'Notre atelier rénové'),
        ('pneus', '', 'Montage et équilibrage'),
        ('diag', '', 'Diagnostic à la valise'),
        ('moto', 'wide', 'Entretien moto et scooter'),
        ('freins', '', 'Freinage'),
        ('vidange', '', 'Vidange et révision'),
    ]
    gal_html = ''.join(
'<figure class="gallery-item %s reveal"><div class="img-placeholder" role="img" aria-label="%s (photo à fournir)">%s 〔photo〕</div>'
'<figcaption class="gallery-item__caption">%s</figcaption></figure>'
        % (cls, cap, cap, cap) for _key, cls, cap in gallery)

    faq = [
        ("Quels véhicules réparez-vous ?", "Toutes les marques, en essence, diesel et hybride, voitures comme motos et scooters."),
        ("Faut-il prendre rendez-vous ?", "Oui de préférence, par téléphone au 09 84 28 23 20. On vous donne un créneau rapidement, et on reçoit aussi sans rendez-vous selon l\'affluence."),
        ("Le devis est-il gratuit ?", "Oui, gratuit et sans engagement. On ne lance rien sans votre accord."),
        ("Où êtes-vous exactement ?", "5 rue de Locarno, 13005 Marseille, à 2 min des hôpitaux de la Conception et de la Timone."),
    ]

    rating_fr = RATING.replace('.', ',')
    ph = svg_phone()
    pin = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
           '<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>')
    clock = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
             '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>')
    body = f'''\
<header class="hero">
<div class="hero__media"><div class="img-placeholder img-placeholder--dark" role="img" aria-label="Photo de la façade du Garage Locarno (à fournir)">Photo façade atelier 〔hero〕</div></div>
<div class="hero__overlay"></div>
<div class="container"><div class="hero__inner">
<span class="eyebrow">Garage automobile et moto &middot; Marseille 5e</span>
<h1>Garage automobile à Marseille 5e, <span class="accent">toutes marques, auto et moto</span></h1>
<p class="hero__lead">5 rue de Locarno, à deux minutes des hôpitaux de la Conception et de la Timone. Entretien, réparation et révision toutes marques, voiture comme moto. Devis gratuit, et on vous explique tout avant d'intervenir.</p>
<div class="hero__actions"><a href="contact.html" class="btn btn-primary btn-lg">Devis gratuit</a>
<a href="tel:{PHONE_TEL}" class="hero__phone">{ph} {PHONE_DISPLAY}</a></div>
<div class="hero__stats"><div class="hero__stats-grid">
<div class="hero__stat"><div class="num">{rating_fr}<b>/5</b></div><div class="lab">{STARS} sur Google</div></div>
<div class="hero__stat"><div class="num">{REVIEW_COUNT}<b>+</b></div><div class="lab">avis clients</div></div>
<div class="hero__stat"><div class="num">10<b> ans</b></div><div class="lab">d'expérience</div></div>
<div class="hero__stat"><div class="num">2020</div><div class="lab">atelier rénové</div></div>
</div></div></div></div></header>
<section class="section" id="prestations"><div class="container">
<div class="section__header reveal"><span class="eyebrow"><span class="section-index">01</span> Nos prestations</span>
<h2>Tout l'entretien de votre véhicule</h2>
<p>Auto et moto, toutes marques. Choisissez une prestation pour le détail, ou demandez directement un devis.</p></div>
<div class="services-grid">{cards_html}</div>
<p class="text-center mt-2" style="color:var(--muted);font-size:.92rem">Huiles, lubrifiants et batteries également disponibles au comptoir.</p>
</div></section>
<section class="section section--dark"><div class="container">
<div class="section__header reveal"><span class="eyebrow"><span class="section-index">02</span> Pourquoi le Garage Locarno</span>
<h2>Un garagiste de confiance en centre-ville</h2></div>
<div class="feature-grid">{feat_html}</div></div></section>
<section class="section section--paper" id="avis"><div class="container">
<div class="section__header reveal"><span class="eyebrow"><span class="section-index">03</span> Avis clients</span>
<h2>Ils nous font confiance, {rating_fr}/5</h2>
<p>Plus de {REVIEW_COUNT} avis sur Google. Voici ce que disent nos clients.</p></div>
<div class="testimonials-carousel reveal" id="testimonials-carousel"><div class="testimonials-track" id="testimonials-track">{slides_html}</div>
<div class="carousel-arrows"><button class="carousel-arrow" id="carousel-prev" aria-label="Avis précédent">&#8249;</button><button class="carousel-arrow" id="carousel-next" aria-label="Avis suivant">&#8250;</button></div>
<div class="carousel-dots" id="carousel-dots"></div></div>
<div class="text-center mt-2"><a href="{GBP_URL}" target="_blank" rel="noopener" class="btn btn-outline">Voir tous les avis Google</a></div>
</div></section>
<section class="section"><div class="container">
<div class="section__header reveal"><span class="eyebrow"><span class="section-index">04</span> En images</span>
<h2>L'atelier et nos prestations</h2>
<p>Un atelier rénové en plein centre-ville. Les photos réelles seront ajoutées prochainement.</p></div>
<div class="gallery-grid">{gal_html}</div></div></section>
<section class="section section--paper-2"><div class="container"><div class="split">
<div class="split__media reveal"><div class="img-placeholder" role="img" aria-label="Intérieur de l'atelier (à fournir)">Photo atelier 〔atelier〕</div></div>
<div class="split__body reveal reveal-d1"><span class="eyebrow"><span class="section-index">05</span> Nous trouver</span>
<h2>En plein centre-ville, à 2 min des hôpitaux</h2>
<ul class="info-list mt-1">
<li><span class="info-ico">{pin}</span><span><strong>5 rue de Locarno, 13005 Marseille</strong>À deux minutes des hôpitaux de la Conception et de la Timone, près des boulevards Baille et Chave.</span></li>
<li><span class="info-ico">{clock}</span><span><strong>Lundi au vendredi, 9h-18h</strong>Samedi et dimanche fermé. Avec ou sans rendez-vous.</span></li>
<li><span class="info-ico">{ph}</span><span><strong><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></strong>On vous répond et on vous donne un créneau rapidement.</span></li>
</ul>
<a href="{GBP_URL}" target="_blank" rel="noopener" class="map-link">{pin} Ouvrir dans Google Maps</a>
</div></div></div></section>
<section class="section section--paper"><div class="container">
<div class="section__header reveal"><span class="eyebrow"><span class="section-index">06</span> Questions fréquentes</span>
<h2>Vous vous demandez peut-être</h2></div>{faq_html(faq)}</div></section>
''' + cta_section()
    schema = (schema_autorepair()
              + schema_breadcrumb([("Accueil", "index.html")])
              + schema_faq(faq))
    page("index.html",
         "Garage automobile à Marseille 5e | Garage Locarno",
         "Garage Locarno, votre garagiste toutes marques à Marseille centre (13005). Entretien, révision, freins, pneus, diagnostic. Devis gratuit. Appelez le 09 84 28 23 20.",
         SITE + "/", body, schema=schema)


def build_services():
    # 5.1 Entretien & révision
    service_page(
        "entretien-revision.html",
        "Révision & entretien auto à Marseille | Garage Locarno",
        "Révision et entretien toutes marques à Marseille 5e. Vidange, filtres, 50 points de contrôle, diagnostic. Devis gratuit, garantie constructeur préservée.",
        "Révision et entretien auto à Marseille",
        "Entretien &amp; révision",
        '<p class="intro-lead">Au Garage Locarno, on assure la révision et l\'entretien complet de votre voiture, toutes marques, à Marseille 5e. Vidange, filtres, points de contrôle et diagnostic : tout est passé en revue, puis on vous remet un devis clair avant la moindre intervention. Bonne nouvelle, un entretien chez nous préserve votre garantie constructeur (le règlement européen autorise l\'entretien hors réseau), et il est souvent moins cher qu\'en concession.</p>',
        [
            ("Que comprend une révision ?",
             '<p>Une révision complète, c\'est un véhicule passé au peigne fin. Concrètement, on contrôle et on remplace ce qui doit l\'être :</p>'
             '<ul class="check-list">'
             '<li>Vidange de l\'huile moteur et remplacement du filtre à huile</li>'
             '<li>Filtres air, habitacle et carburant selon l\'usure</li>'
             '<li>Niveaux : liquide de frein, refroidissement, lave-glace, direction</li>'
             '<li>Freins : plaquettes, disques, état du frein à main</li>'
             '<li>Pneus, éclairage et essuie-glaces</li>'
             '<li>Lecture des défauts à la valise OBD et remise à zéro du témoin d\'entretien</li></ul>'),
            ("Petite ou grande révision ?",
             '<p>La petite révision couvre l\'essentiel (vidange, filtre à huile, contrôles de sécurité). La grande révision ajoute les autres filtres et un contrôle plus poussé, en général sur les kilométrages élevés ou avant un long trajet. On vous oriente vers la bonne formule selon votre carnet d\'entretien.</p>'),
            ("Tous les combien faire sa révision ?",
             '<p>En règle générale, tous les 15 000 km environ ou tous les 1 à 2 ans, selon votre véhicule. Le mieux reste de suivre le carnet d\'entretien du constructeur. Dans le doute, appelez-nous, on vérifie ensemble.</p>'),
        ],
        [
            ("L\'entretien hors concession fait-il perdre la garantie ?", "Non. Le règlement européen autorise l\'entretien dans un garage indépendant sans perte de la garantie constructeur, à condition de respecter le plan d\'entretien. On le respecte et on conserve les justificatifs."),
            ("Quelle différence entre vidange et révision ?", "La vidange remplace l\'huile et le filtre à huile. La révision est plus large : vidange plus contrôle complet des organes de sécurité et des filtres."),
            ("Combien de temps ça prend ?", "Comptez en général de 1h30 à 3h selon la formule et le véhicule. On vous donne une estimation au moment du devis."),
            ("Dois-je prendre rendez-vous ?", "De préférence oui, par téléphone au 09 84 28 23 20, pour qu\'on vous réserve un créneau."),
        ],
        [("Vidange et entretien", "entretien-revision.html"), ("Diagnostic électronique", "diagnostic.html"), ("Freins, plaquettes et disques", "freinage.html")],
        "Révision et entretien auto", "Révision et entretien automobile",
    )

    # 5.4 Pneus
    service_page(
        "pneus.html",
        "Montage pneus Marseille, centre agréé Allopneus | Garage Locarno",
        "Montage et équilibrage de pneus à Marseille 5e, centre agréé Allopneus. Faites livrer vos pneus, on les monte. Parallélisme, géométrie, auto et moto. Devis gratuit.",
        "Montage et équilibrage de pneus à Marseille",
        "Pneus &amp; montage",
        '<p class="intro-lead">Le Garage Locarno est un centre de montage agréé Allopneus à Marseille 5e. Vous achetez vos pneus en ligne, vous les faites livrer chez nous, et on s\'occupe du montage, de l\'équilibrage et des valves. On fait aussi le parallélisme et la géométrie, sur toutes les dimensions, auto comme moto. Et si vous préférez, on vous conseille et on fournit les pneus directement.</p>',
        [
            ("Centre agréé Allopneus",
             '<p>En tant que centre de montage agréé Allopneus, on reçoit vos pneus commandés en ligne et on les monte au tarif convenu. Pratique : vous profitez des prix du web et d\'un montage par des professionnels, au même endroit.</p>'),
            ("Équilibrage, parallélisme, géométrie",
             '<p>Un pneu bien monté, c\'est un pneu équilibré. On ajoute les masses d\'équilibrage pour supprimer les vibrations, et on contrôle le parallélisme pour éviter l\'usure irrégulière et la surconsommation. En cas de tirage du volant ou d\'usure d\'un seul côté, on règle la géométrie.</p>'),
            ("Pneus auto et moto",
             '<p>On monte les pneus de tourisme, utilitaires et 4x4, mais aussi les pneus moto et scooter, toutes dimensions. Demandez-nous, on a sûrement la solution.</p>'),
            ("Quand changer ses pneus ?",
             '<ul class="check-list">'
             '<li>Témoin d\'usure atteint (1,6 mm de profondeur minimum légal)</li>'
             '<li>Usure irrégulière ou sur un seul flanc</li>'
             '<li>Craquelures, hernies ou coupures sur le flanc</li>'
             '<li>Perte d\'adhérence, distances de freinage allongées</li></ul>'),
        ],
        [
            ("Je peux faire livrer mes pneus chez vous ?", "Oui. On est centre de montage agréé Allopneus : commandez vos pneus en ligne, faites-les livrer au garage, et on les monte."),
            ("Vous montez les pneus moto ?", "Oui, on monte les pneus moto et scooter, toutes dimensions."),
            ("Le parallélisme est-il inclus ?", "Le montage et l\'équilibrage sont une chose, le parallélisme en est une autre. On vous l\'indique sur le devis et on le réalise si besoin."),
        ],
        [("Freins, plaquettes et disques", "freinage.html"), ("Entretien et révision", "entretien-revision.html"), ("Diagnostic électronique", "diagnostic.html")],
        "Montage de pneus", "Montage, équilibrage et géométrie de pneus",
    )

    # 5.3 Freinage
    service_page(
        "freinage.html",
        "Plaquettes & disques de frein à Marseille | Garage Locarno",
        "Freins à Marseille 5e : contrôle et remplacement des plaquettes et disques, toutes marques. Devis avant intervention. Garage Locarno, 09 84 28 23 20.",
        "Freins, plaquettes et disques à Marseille",
        "Freins",
        '<p class="intro-lead">Les freins, c\'est la sécurité avant tout. Au Garage Locarno, à Marseille 5e, on contrôle l\'ensemble du système de freinage (plaquettes, disques, frein à main) et on remplace ce qui est usé, toutes marques. Comme toujours, on vous montre l\'état des pièces et on valide le devis avec vous avant d\'intervenir.</p>',
        [
            ("Les signes d\'usure à surveiller",
             '<ul class="check-list">'
             '<li>Grincement ou couinement au freinage</li>'
             '<li>Vibrations dans la pédale ou le volant quand vous freinez</li>'
             '<li>Pédale molle ou qui s\'enfonce plus que d\'habitude</li>'
             '<li>Distance de freinage qui s\'allonge</li>'
             '<li>Voyant de frein allumé au tableau de bord</li></ul>'
             '<p>Au moindre de ces signes, ne tardez pas : un système de freinage négligé devient vite dangereux.</p>'),
            ("Plaquettes ou disques ?",
             '<p>Les plaquettes s\'usent en premier, c\'est la pièce de friction. Les disques s\'usent plus lentement mais finissent par se voiler ou trop s\'amincir. On contrôle l\'épaisseur des deux et on ne remplace que ce qui doit l\'être.</p>'),
            ("Quand changer ses freins ?",
             '<p>Cela dépend de votre conduite et du véhicule. En ville, les plaquettes s\'usent plus vite. Plutôt que de raisonner en kilomètres, on mesure l\'usure réelle lors d\'un contrôle. Profitez-en lors de votre révision.</p>'),
        ],
        [
            ("À quel kilométrage changer les plaquettes ?", "Il n\'y a pas de règle stricte : tout dépend de la conduite et du véhicule. On mesure l\'usure réelle des plaquettes lors d\'un contrôle plutôt que de se fier au seul kilométrage."),
            ("Un bruit au freinage, c\'est urgent ?", "Un grincement signale souvent des plaquettes en fin de vie. Passez nous voir rapidement pour un contrôle, avant que les disques ne soient touchés."),
            ("Faut-il aussi changer les disques ?", "Pas systématiquement. On contrôle leur épaisseur et leur état. On ne les remplace que si c\'est nécessaire, et toujours après votre accord."),
        ],
        [("Entretien et révision", "entretien-revision.html"), ("Pneus et montage", "pneus.html"), ("Diagnostic électronique", "diagnostic.html")],
        "Freinage", "Remplacement de plaquettes et disques de frein",
    )

    # 5.5 Diagnostic
    service_page(
        "diagnostic.html",
        "Diagnostic électronique auto à Marseille | Garage Locarno",
        "Diagnostic électronique auto à Marseille 5e : lecture des codes défauts à la valise OBD, voyant moteur allumé. On identifie avant de réparer. Devis gratuit.",
        "Diagnostic électronique à Marseille",
        "Diagnostic électronique",
        '<p class="intro-lead">Un voyant s\'allume au tableau de bord ? Au Garage Locarno, à Marseille 5e, on branche la valise OBD pour lire les codes défauts et identifier précisément l\'origine du problème, avant de réparer. Pas de réparation au hasard : on diagnostique, on vous explique, et on établit un devis ensuite.</p>',
        [
            ("Voyant allumé, que faire ?",
             '<p>Un voyant orange invite à la prudence : faites contrôler le véhicule rapidement. Un voyant rouge impose de vous arrêter dès que possible en sécurité. Dans tous les cas, le diagnostic électronique permet de savoir ce qui se passe vraiment, sans démonter à l\'aveugle.</p>'),
            ("Ce que révèle la valise",
             '<p>La valise dialogue avec les calculateurs du véhicule et remonte les codes défauts : moteur, injection, ABS, airbag, capteurs, antipollution. On interprète ces codes avec notre expérience, car un même code peut avoir plusieurs causes.</p>'),
            ("Diagnostic d\'abord, devis ensuite",
             '<p>Une fois l\'origine identifiée, on vous explique le problème et on chiffre la réparation. Vous décidez en connaissance de cause, rien n\'est lancé sans votre accord.</p>'),
        ],
        [
            ("Voyant moteur orange, je peux rouler ?", "Vous pouvez en général rejoindre le garage en roulant doucement, mais ne tardez pas. Un voyant moteur ignoré peut entraîner des dégâts plus coûteux. Appelez-nous au 09 84 28 23 20."),
            ("Combien coûte un diagnostic ?", "Cela dépend du véhicule et de la complexité. On vous l\'indique avant, sur devis gratuit."),
            ("Vous effacez le voyant ?", "On efface le code une fois le problème traité. Effacer sans réparer ne sert à rien : le voyant reviendra."),
        ],
        [("Entretien et révision", "entretien-revision.html"), ("Freins, plaquettes et disques", "freinage.html"), ("Pneus et montage", "pneus.html")],
        "Diagnostic électronique", "Diagnostic électronique automobile",
    )

    # 5.2 Vidange
    service_page(
        "vidange.html",
        "Vidange voiture à Marseille | Garage Locarno",
        "Vidange auto toutes marques à Marseille 5e : huile adaptée à votre moteur, filtre à huile remplacé, voyant remis à zéro. Devis gratuit, sans rendez-vous d'attente.",
        "Vidange auto à Marseille",
        "Vidange",
        '<p class="intro-lead">La vidange, c\'est l\'entretien de base de votre moteur. Au Garage Locarno, à Marseille 5e, on remplace l\'huile usagée et le filtre à huile par une huile adaptée à votre motorisation (essence, diesel ou hybride), on contrôle les niveaux et on remet le témoin d\'entretien à zéro. Simple, rapide, et toujours sur devis clair.</p>',
        [
            ("Pourquoi la vidange est essentielle",
             '<p>L\'huile lubrifie, refroidit et nettoie votre moteur. En vieillissant, elle s\'encrasse et perd ses propriétés : rouler avec une huile fatiguée use le moteur prématurément, parfois jusqu\'à la casse. Une vidange régulière, c\'est le geste le plus rentable pour faire durer votre voiture.</p>'),
            ("Quand faire sa vidange ?",
             '<p>Cela dépend de votre moteur et de votre usage. En repère : essence tous les 15 000 à 30 000 km, diesel tous les 15 000 à 25 000 km, hybride tous les 10 000 à 15 000 km, ou une fois par an si vous roulez peu. Le carnet d\'entretien reste la référence.</p>'),
            ("Quelle huile pour votre moteur ?",
             '<p>On utilise l\'huile à la viscosité et aux normes préconisées par le constructeur. Pas de mauvaise surprise : la bonne huile au bon endroit, c\'est ce qui protège vraiment le moteur. Huiles et lubrifiants sont aussi disponibles au comptoir.</p>'),
        ],
        [
            ("À quelle fréquence faire la vidange ?", "Selon le moteur : environ tous les 15 000 à 30 000 km en essence, 15 000 à 25 000 km en diesel, 10 000 à 15 000 km en hybride, ou une fois par an. On vérifie votre carnet d\'entretien."),
            ("Huile noire, faut-il vidanger ?", "L\'huile noircit normalement en captant les impuretés, ce n\'est pas toujours un signe d\'alerte. C\'est le kilométrage et la date de la dernière vidange qui comptent. Dans le doute, passez nous voir."),
            ("Vidange seule ou avec révision ?", "La vidange peut se faire seule entre deux révisions. Si l\'échéance constructeur approche, autant la coupler à une révision complète."),
        ],
        [("Entretien et révision", "entretien-revision.html"), ("Diagnostic électronique", "diagnostic.html"), ("Freins, plaquettes et disques", "freinage.html")],
        "Vidange", "Vidange automobile",
    )

    # 5.6 Climatisation
    service_page(
        "climatisation.html",
        "Recharge climatisation auto à Marseille | Garage Locarno",
        "Recharge et entretien de climatisation auto à Marseille 5e : gaz R134a ou R1234yf, contrôle d'étanchéité, assainissement. Clim qui ne refroidit plus ? Devis gratuit.",
        "Climatisation auto à Marseille",
        "Climatisation",
        '<p class="intro-lead">Votre climatisation ne refroidit plus comme avant ? Au Garage Locarno, à Marseille 5e, on recharge le gaz (R134a ou R1234yf selon votre véhicule), on contrôle l\'étanchéité du circuit et on assainit pour retrouver un air froid et sain. Une clim entretenue, c\'est du confort l\'été et de la sécurité (désembuage) l\'hiver.</p>',
        [
            ("Clim qui souffle chaud ?",
             '<p>Le plus souvent, c\'est une perte de gaz progressive : un circuit perd naturellement un peu de fluide chaque année. Une recharge remet le système d\'aplomb. Si le froid disparaît d\'un coup, on cherche une fuite ou une panne (compresseur) avant tout.</p>'),
            ("Recharge et contrôle d\'étanchéité",
             '<p>Recharger sans vérifier n\'a pas de sens si le gaz s\'échappe. On contrôle d\'abord l\'étanchéité, puis on recharge le bon fluide à la bonne quantité. Une mauvaise odeur à la ventilation ? On assainit le circuit et on remplace le filtre d\'habitacle.</p>'),
            ("Quand entretenir sa clim ?",
             '<p>Un contrôle tous les 2 ans, recharge incluse si besoin, suffit à garder une clim performante. Faites-la aussi tourner quelques minutes en hiver pour préserver le compresseur.</p>'),
        ],
        [
            ("À quelle fréquence recharger la clim ?", "En général tous les 2 ans environ, car le circuit perd un peu de gaz chaque année. Si une recharge ne tient que quelques mois, c\'est le signe d\'une fuite à traiter."),
            ("Mauvaise odeur à la clim, que faire ?", "C\'est souvent l\'évaporateur et le filtre d\'habitacle. On assainit le circuit et on remplace le filtre pour retrouver un air sain."),
            ("Quel gaz pour ma voiture ?", "Les modèles récents utilisent le R1234yf, les plus anciens le R134a. On vérifie l\'étiquette dans le compartiment moteur avant toute recharge."),
        ],
        [("Diagnostic électronique", "diagnostic.html"), ("Entretien et révision", "entretien-revision.html"), ("Batterie et éclairage", "batterie.html")],
        "Climatisation", "Recharge et entretien de climatisation automobile",
    )

    # 5.7 Batterie & éclairage
    service_page(
        "batterie.html",
        "Batterie & éclairage auto à Marseille | Garage Locarno",
        "Test et remplacement de batterie auto à Marseille 5e, démarrage difficile, ampoules et feux. Batteries disponibles au comptoir, vendues chargées. Devis gratuit.",
        "Batterie et éclairage à Marseille",
        "Batterie &amp; éclairage",
        '<p class="intro-lead">Démarrage difficile, voiture qui ne répond plus ? Au Garage Locarno, à Marseille 5e, on teste et on remplace votre batterie, et on s\'occupe de l\'éclairage (ampoules, feux), une cause fréquente de contre-visite au contrôle technique. On a des batteries au comptoir, vendues chargées, prêtes à poser.</p>',
        [
            ("Signes d\'une batterie en fin de vie",
             '<ul class="check-list">'
             '<li>Démarrage lent ou hésitant, surtout le matin</li>'
             '<li>Éclairage qui faiblit au ralenti</li>'
             '<li>Voyant batterie allumé au tableau de bord</li>'
             '<li>Accessoires électriques capricieux</li></ul>'
             '<p>Une batterie dure en moyenne 4 à 5 ans. Au-delà, mieux vaut anticiper avant la panne.</p>'),
            ("Test et remplacement",
             '<p>On teste la tension et la capacité de charge de votre batterie, et on vérifie l\'alternateur (qui la recharge). Si elle est en fin de vie, on la remplace par une batterie adaptée à votre véhicule, disponible sur place et vendue chargée.</p>'),
            ("Éclairage et feux",
             '<p>Une ampoule grillée, c\'est un risque de sécurité et un motif fréquent de contre-visite au contrôle technique. On remplace ampoules et feux rapidement, à l\'avant comme à l\'arrière.</p>'),
        ],
        [
            ("Quelle est la durée de vie d\'une batterie ?", "En moyenne 4 à 5 ans, parfois moins en cas de trajets courts répétés ou de fortes chaleurs. Au-delà, un test permet d\'anticiper la panne."),
            ("Avez-vous des batteries en stock ?", "Oui, on dispose d\'une gamme de batteries au comptoir, vendues chargées et prêtes à poser. 〔Stocks à confirmer selon les références〕."),
            ("Changez-vous les ampoules ?", "Oui, on remplace ampoules et feux avant et arrière, rapidement et au bon format pour votre véhicule."),
        ],
        [("Diagnostic électronique", "diagnostic.html"), ("Entretien et révision", "entretien-revision.html"), ("Climatisation", "climatisation.html")],
        "Batterie et éclairage", "Batterie et éclairage automobile",
    )

    # 6 Moto / scooter
    service_page(
        "moto-scooter.html",
        "Garage moto et scooter à Marseille | Garage Locarno",
        "Entretien et réparation moto et scooter toutes cylindrées à Marseille 5e : vidange, pneus, freins, révision. Devis gratuit. Garage Locarno, 5 rue de Locarno.",
        "Entretien moto et scooter à Marseille",
        "Moto &amp; scooter",
        '<p class="intro-lead">Le Garage Locarno, c\'est aussi le deux-roues. Dans le même atelier, à Marseille 5e, une équipe expérimentée entretient et répare votre moto ou votre scooter, toutes cylindrées : vidange, pneus, freins, révision. Devis gratuit, et on vous explique tout avant d\'intervenir.</p>',
        [
            ("Nos prestations 2-roues",
             '<ul class="check-list">'
             '<li>Vidange et révision (moteur 4 temps, transmission scooter)</li>'
             '<li>Montage et équilibrage de pneus moto et scooter</li>'
             '<li>Freins : plaquettes, mâchoires, liquide</li>'
             '<li>Batterie, éclairage et contrôles de sécurité</li></ul>'),
            ("Pneus moto, centre Allopneus",
             '<p>On monte les pneus moto et scooter, toutes dimensions, dans le respect du sens de rotation et de la pression. En tant que centre agréé Allopneus, vous pouvez aussi faire livrer vos pneus au garage et nous confier la pose.</p>'),
            ("Révision et vidange scooter",
             '<p>Un scooter bien suivi, c\'est moins de pannes et plus de sécurité. On contrôle la transmission (courroie, galets), les niveaux et les organes d\'usure. Avant l\'été, un passage rapide évite les mauvaises surprises.</p>'),
        ],
        [
            ("Travaillez-vous toutes les cylindrées ?", "Oui, du 50 cc au maxi-scooter et à la moto, toutes marques. Les contrôles de base sont les mêmes, certaines pièces et intervalles varient selon le modèle."),
            ("Montez-vous les pneus moto ?", "Oui, on monte et équilibre les pneus moto et scooter, toutes dimensions. Vous pouvez aussi les faire livrer via Allopneus."),
            ("Faut-il prendre rendez-vous ?", "De préférence oui, par téléphone au 09 84 28 23 20, pour réserver un créneau adapté à votre deux-roues."),
        ],
        [("Montage et équilibrage de pneus", "pneus.html"), ("Entretien et révision", "entretien-revision.html"), ("Freins, plaquettes et disques", "freinage.html")],
        "Entretien moto et scooter", "Entretien et réparation moto et scooter",
    )


def build_about():
    crumbs = [("Accueil", "index.html"), ("À propos", None)]
    body = (
'<header class="page-header"><div class="container">%s<h1>Le Garage Locarno, votre garagiste à Marseille centre</h1>'
'<p>Un atelier rénové, une équipe expérimentée, et une règle simple : on vous explique avant de réparer.</p></div></header>\n'
'<section class="section"><div class="container"><div class="split">'
'<div class="split__media reveal"><div class="img-placeholder" role="img" aria-label="Équipe du Garage Locarno (à fournir)">Photo équipe / atelier &middot; à fournir 〔équipe〕</div></div>'
'<div class="split__body reveal reveal-d1">'
'<span class="eyebrow">Notre histoire</span><h2 class="section__title-rule">Un garage de quartier, au niveau d\'exigence d\'un pro</h2>'
'<p>Le Garage Locarno, c\'est un atelier entièrement rénové en octobre 2020, au 5 rue de Locarno, en plein centre-ville de Marseille, à deux minutes des hôpitaux de la Conception et de la Timone.</p>'
'<p>Notre équipe travaille la mécanique depuis plus de 10 ans, sur voiture comme sur deux-roues. On répare toutes les marques, en essence, diesel et hybride.</p>'
'<p>Le garage est dirigé par <strong>Aymeric Assouline</strong> et appartient au groupe C\'Carré, fidèle à sa devise : pour que votre moteur tourne rond.</p>'
'</div></div></div></section>\n'
'<section class="section section--dark"><div class="container">'
'<div class="section__header reveal"><span class="eyebrow">Notre méthode</span><h2 class="section__title-rule">Diagnostic, explication, devis, accord, intervention</h2>'
'<p>La transparence, ce n\'est pas un slogan chez nous, c\'est la façon dont on travaille au quotidien, conformément à la loi Hamon.</p></div>'
'<div class="feature-grid">'
'<div class="feature reveal"><span class="feature__num">01</span><h3>On diagnostique</h3><p>On identifie précisément la panne, valise à l\'appui si besoin, avant de parler réparation.</p></div>'
'<div class="feature reveal reveal-d1"><span class="feature__num">02</span><h3>On explique et on chiffre</h3><p>On vous montre ce qui ne va pas et on établit un devis clair, sans surprise.</p></div>'
'<div class="feature reveal reveal-d2"><span class="feature__num">03</span><h3>On intervient après votre accord</h3><p>Rien n\'est lancé sans votre validation. Si un imprévu apparaît, on vous rappelle avant.</p></div>'
'</div></div></section>\n'
'<section class="section section--paper"><div class="container">'
'<div class="callout reveal"><h3>%s/5 sur Google, plus de %s avis</h3>'
'<p>Nos clients parlent d\'un garage honnête, à l\'écoute, qui prend le temps d\'expliquer et pratique des prix corrects. C\'est exactement ce qu\'on cherche à être. <a href="index.html#avis">Lire les avis</a>.</p></div>'
'<div class="callout callout--legal reveal"><p><strong>Bon à savoir.</strong> Atelier rénové 2020 &middot; équipe de 3 à 5 personnes &middot; centre de montage agréé Allopneus &middot; huiles, lubrifiants et batteries disponibles au comptoir. 〔Assurances et agréments complémentaires à confirmer〕.</p></div>'
'</div></section>\n'
+ cta_section()
        ) % (breadcrumb_html(crumbs), RATING.replace('.', ','), REVIEW_COUNT)
    schema = (schema_breadcrumb([("Accueil", "index.html"), ("À propos", "a-propos.html")])
              + schema_autorepair())
    page("a-propos.html",
         "À propos, votre garagiste à Marseille 5e | Garage Locarno",
         "Garage Locarno, atelier rénové en 2020 au 5 rue de Locarno, Marseille 5e. Équipe de plus de 10 ans d\'expérience, toutes marques auto et moto. Groupe C\'Carré.",
         SITE + "/a-propos.html", body, schema=schema)


def build_contact():
    crumbs = [("Accueil", "index.html"), ("Contact", None)]
    form = (
'<form id="contactForm" class="form" action="%s" method="post">'
'<input type="hidden" name="_subject" value="Demande de devis &middot; site Garage Locarno">'
'<input type="hidden" name="_next" value="%s/contact.html?statut=ok">'
'<div class="hp-field" aria-hidden="true"><label>Ne pas remplir<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
'<div class="form__group"><label class="form__label" for="nom">Nom et prénom</label>'
'<input class="form__input" type="text" id="nom" name="nom" required autocomplete="name"></div>'
'<div class="form__row">'
'<div class="form__group"><label class="form__label" for="email">Email</label>'
'<input class="form__input" type="email" id="email" name="email" required autocomplete="email"></div>'
'<div class="form__group"><label class="form__label" for="telephone">Téléphone</label>'
'<input class="form__input" type="tel" id="telephone" name="telephone" autocomplete="tel"></div></div>'
'<div class="form__row">'
'<div class="form__group"><label class="form__label" for="type">Type de demande</label>'
'<select class="form__select" id="type" name="type"><option>Auto</option><option>Moto / scooter</option><option>Autre</option></select></div>'
'<div class="form__group"><label class="form__label" for="immat">Immatriculation <span style="font-weight:400;color:var(--text-secondary)">(facultatif)</span></label>'
'<input class="form__input" type="text" id="immat" name="immatriculation" autocomplete="off" placeholder="AB-123-CD"></div></div>'
'<div class="form__group"><label class="form__label" for="message">Votre demande</label>'
'<textarea class="form__textarea" id="message" name="message" required placeholder="Décrivez le souci ou la prestation souhaitée."></textarea></div>'
'<div class="form__group"><label class="form__checkbox"><input type="checkbox" name="rgpd_consent" required>'
'J\'accepte que mes informations soient utilisées pour répondre à ma demande, conformément à la <a href="politique-confidentialite.html">politique de confidentialité</a>.</label></div>'
'<button type="submit" class="btn btn-primary btn-lg">Envoyer ma demande</button>'
'<div class="form__message" id="formStatus" role="status" aria-live="polite"></div>'
'</form>' % (FORMSPREE, SITE))

    pin = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
    clock = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
    mail = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'

    body = (
'<header class="page-header"><div class="container">%s<h1>Contact &amp; devis gratuit</h1>'
'<p>Appelez-nous, passez au garage, ou demandez un devis en ligne. On vous répond rapidement.</p></div></header>\n'
'<section class="section" id="formulaire"><div class="container"><div class="contact-grid">'
'<div class="reveal"><span class="eyebrow">Nous joindre</span><h2 class="section__title-rule">Le Garage Locarno</h2>'
'<ul class="info-list mt-2">'
'<li><span class="info-ico">%s</span><span><strong>5 rue de Locarno, 13005 Marseille</strong>À 2 min des hôpitaux de la Conception et de la Timone, près des boulevards Baille et Chave.</span></li>'
'<li><span class="info-ico">%s</span><span><strong><a href="tel:%s">%s</a></strong>Mobile : <a href="tel:%s">%s</a></span></li>'
'<li><span class="info-ico">%s</span><span><strong><a href="mailto:%s">%s</a></strong>On répond aussi par email.</span></li>'
'<li><span class="info-ico">%s</span><span><strong>Lundi au vendredi, 9h-18h</strong>Samedi et dimanche fermé. Avec ou sans rendez-vous. 〔Pause déjeuner à confirmer〕</span></li>'
'</ul>'
'<a href="%s" target="_blank" rel="noopener" class="map-link">%s Ouvrir dans Google Maps</a>'
'<div class="callout reveal mt-3"><h3>Devis gratuit, sans engagement</h3><p>On ne lance aucune intervention sans votre accord. Le diagnostic et le devis sont gratuits.</p></div>'
'</div>'
'<div class="reveal reveal-d1"><span class="eyebrow">Demande de devis</span><h2 class="section__title-rule">Décrivez votre besoin</h2>'
'<p class="mt-1" style="color:var(--text-secondary)">Réponse rapide pendant les horaires d\'ouverture. Pour une urgence, préférez le téléphone.</p>'
'%s</div>'
'</div></div></section>\n'
        ) % (breadcrumb_html(crumbs), pin, svg_phone(), PHONE_TEL, PHONE_DISPLAY, MOBILE_TEL, MOBILE_DISPLAY, mail, EMAIL, EMAIL, clock, GBP_URL, pin, form)
    schema = schema_breadcrumb([("Accueil", "index.html"), ("Contact", "contact.html")])
    page("contact.html",
         "Contact et devis gratuit à Marseille 5e | Garage Locarno",
         "Contactez le Garage Locarno à Marseille 5e : 09 84 28 23 20, 5 rue de Locarno, 13005. Devis gratuit en ligne, lundi au vendredi 9h-18h.",
         SITE + "/contact.html", body, schema=schema)


def build_legal():
    # Mentions légales
    body_ml = (
'<header class="page-header"><div class="container"><h1>Mentions légales</h1></div></header>\n'
'<article class="article-body"><div class="container">'
'<h2>Éditeur du site</h2>'
'<p>Le présent site est édité par <strong>LOC GARAGE</strong> (enseigne Garage Locarno, groupe C\'Carré).<br>'
'Siège : 5 rue de Locarno, 13005 Marseille &middot; société créée le 07/08/2020 &middot; capital social 2 000 €.<br>'
'SIRET : 88792791100016 &middot; SIREN : 887927911 &middot; RCS Marseille &middot; APE 4520A.<br>'
'Téléphone : <a href="tel:%s">%s</a> &middot; Email : <a href="mailto:%s">%s</a>.<br>'
'Directeur de la publication : Aymeric Assouline, gérant 〔à confirmer〕.</p>'
'<h2>Hébergement</h2>'
'<p>〔Hébergeur à préciser selon la mise en production : OVH SAS, 2 rue Kellermann, 59100 Roubaix, ou O2switch, 222-224 boulevard Gustave Flaubert, 63000 Clermont-Ferrand. En phase de recette, le site est hébergé sur GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis).〕</p>'
'<h2>Propriété intellectuelle</h2>'
'<p>L\'ensemble des contenus de ce site (textes, images, logo) est protégé. Toute reproduction sans autorisation est interdite.</p>'
'<h2>Médiation de la consommation</h2>'
'<p>Conformément à la réglementation, le consommateur peut recourir gratuitement à un médiateur de la consommation. 〔Médiateur rattaché à l\'entreprise à indiquer〕. Plateforme européenne de règlement des litiges : <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">ec.europa.eu/consumers/odr</a>.</p>'
'<h2>Données personnelles</h2>'
'<p>Le traitement de vos données est décrit dans notre <a href="politique-confidentialite.html">politique de confidentialité</a>.</p>'
'</div></article>\n'
        ) % (PHONE_TEL, PHONE_DISPLAY, EMAIL, EMAIL)
    page("mentions-legales.html", "Mentions légales | Garage Locarno",
         "Mentions légales du site Garage Locarno (LOC GARAGE SARL), Marseille 5e.",
         SITE + "/mentions-legales.html", body_ml, robots="noindex, follow")

    # Politique de confidentialité
    body_pc = (
'<header class="page-header"><div class="container"><h1>Politique de confidentialité</h1></div></header>\n'
'<article class="article-body"><div class="container">'
'<h2>Responsable du traitement</h2>'
'<p>LOC GARAGE SARL (Garage Locarno), 5 rue de Locarno, 13005 Marseille. Contact : <a href="mailto:%s">%s</a>.</p>'
'<h2>Données collectées</h2>'
'<p>Via le formulaire de contact : nom et prénom, email, téléphone, type de demande, immatriculation (facultative) et message.</p>'
'<h2>Finalité</h2>'
'<p>Ces données servent uniquement à répondre à votre demande de devis ou de contact. Elles ne sont ni vendues ni cédées à des tiers.</p>'
'<h2>Base légale</h2>'
'<p>Votre consentement, recueilli lors de l\'envoi du formulaire (article 6.1.a du RGPD).</p>'
'<h2>Durée de conservation</h2>'
'<p>Vos données sont conservées 12 mois maximum après le dernier échange, puis supprimées.</p>'
'<h2>Vos droits</h2>'
'<p>Vous disposez d\'un droit d\'accès, de rectification, de suppression, d\'opposition et de portabilité. Pour les exercer, écrivez à <a href="mailto:%s">%s</a>. Vous pouvez aussi saisir la CNIL (<a href="https://www.cnil.fr" target="_blank" rel="noopener">cnil.fr</a>).</p>'
'<h2>Cookies</h2>'
'<p>Ce site n\'utilise aucun cookie de suivi ni traceur publicitaire. Aucune donnée de navigation n\'est collectée à des fins marketing.</p>'
'</div></article>\n'
        ) % (EMAIL, EMAIL, EMAIL, EMAIL)
    page("politique-confidentialite.html", "Politique de confidentialité | Garage Locarno",
         "Politique de confidentialité et traitement des données personnelles du site Garage Locarno, Marseille 5e.",
         SITE + "/politique-confidentialite.html", body_pc, robots="noindex, follow")


def build_404():
    body = (
'<section class="section" style="padding-top:calc(var(--totalHeader) + 4rem);text-align:center">'
'<div class="container"><span class="eyebrow">Erreur 404</span>'
'<h1>Cette page a pris la route</h1>'
'<p class="lead" style="max-width:560px;margin:1rem auto 2rem">La page que vous cherchez n\'existe pas ou a été déplacée. Revenez à l\'accueil, ou appelez-nous directement.</p>'
'<div class="cta-actions" style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">'
'<a href="index.html" class="btn btn-primary">Retour à l\'accueil</a>'
'<a href="tel:%s" class="btn btn-outline">%s %s</a></div>'
'</div></section>\n'
        ) % (PHONE_TEL, svg_phone(), PHONE_DISPLAY)
    page("404.html", "Page introuvable | Garage Locarno", "La page demandée est introuvable.",
         SITE + "/404.html", body, robots="noindex, follow")


def build_avis():
    reviews = [
        ('Daniel', 'Cela fait cinq ans que je confie mes véhicules au garage Locarno. Une équipe à l\'écoute, qui prend le temps d\'expliquer et un travail toujours soigné.'),
        ('Thibaut', 'Atelier propre et rénové, accueil sympathique. On m\'a prévenu d\'un ajustement sur le devis avant d\'intervenir, j\'apprécie cette transparence.'),
        ('Anissa', 'Prise en charge rapide de ma voiture, travail efficace et personnel agréable. Des gens sérieux et honnêtes, je recommande.'),
    ]
    STARS = '&#9733;&#9733;&#9733;&#9733;&#9733;'
    rating_fr = RATING.replace('.', ',')
    cards = ''.join(
'<figure class="review reveal reveal-d%d"><div class="review__stars">%s</div>'
'<blockquote class="review__text">%s</blockquote>'
'<figcaption class="review__author">%s <span class="review__source">&middot; Client Garage Locarno</span></figcaption></figure>'
        % ((i % 3) + 1, STARS, t, n) for i, (n, t) in enumerate(reviews))
    crumbs = [("Accueil", "index.html"), ("Avis", None)]
    body = (
'<header class="page-header"><div class="container">%s<h1>Ce que disent nos clients</h1>'
'<p>Une note de %s/5 sur Google et plus de %s avis. Voici quelques retours, et le lien pour laisser le vôtre.</p></div></header>\n'
'<section class="section"><div class="container">'
'<div class="text-center reveal" style="margin-bottom:2.5rem">'
'<div style="font-family:var(--font-display);font-size:3.5rem;color:var(--copper-700);line-height:1">%s<span style="font-size:1.4rem;color:var(--muted)">/5</span></div>'
'<div style="color:var(--star);font-size:1.3rem;letter-spacing:.1em">%s</div>'
'<p style="color:var(--muted);margin-top:.5rem">Plus de %s avis vérifiés sur Google</p>'
'<a href="%s" target="_blank" rel="noopener" class="btn btn-primary mt-1">Laisser un avis sur Google</a></div>'
'<div class="reviews-grid">%s</div>'
'<div class="callout callout--legal reveal mt-3"><p>Les avis affichés sont issus des retours de nos clients. La note et le nombre d\'avis correspondent à notre fiche Google Business Profile. 〔Note et nombre exacts à actualiser depuis la fiche live〕.</p></div>'
'</div></section>\n'
+ cta_section()
        ) % (breadcrumb_html(crumbs), rating_fr, REVIEW_COUNT, rating_fr, STARS, REVIEW_COUNT, GBP_URL, cards)
    # Schema AggregateRating + Review
    rev_schema = ','.join(
        '{"@type":"Review","author":{"@type":"Person","name":"%s"},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":"%s"}'
        % (n, t.replace('"', '\\"')) for n, t in reviews)
    schema = (schema_breadcrumb([("Accueil", "index.html"), ("Avis", "avis.html")])
              + '<script type="application/ld+json">'
                '{"@context":"https://schema.org","@type":"AutoRepair","name":"Garage Locarno",'
                '"address":{"@type":"PostalAddress","streetAddress":"5 rue de Locarno","addressLocality":"Marseille","postalCode":"13005","addressCountry":"FR"},'
                '"aggregateRating":{"@type":"AggregateRating","ratingValue":"%s","reviewCount":"%s","bestRating":"5"},'
                '"review":[%s]}</script>\n' % (RATING, REVIEW_COUNT, rev_schema))
    page("avis.html", "Avis clients Garage Locarno Marseille (%s/5)" % rating_fr,
         "Avis clients du Garage Locarno à Marseille 5e : note de %s/5 sur Google. Garage honnête, à l'écoute, prix corrects. Laissez votre avis." % rating_fr,
         SITE + "/avis.html", body, schema=schema)


_MONTHS = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06",
           "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}

def _iso_date(s):
    parts = s.split()
    if len(parts) == 2 and parts[0] in _MONTHS:
        return "2026-%s-01" % _MONTHS[parts[0]]
    return "2026-01-01"

def _sanitize(s):
    return s.replace("—", ", ").replace("–", "-")

def build_blog():
    import json
    with open(os.path.join(ROOT, "blog/articles_content.json"), encoding="utf-8") as f:
        arts = json.load(f)

    # Index articles.json (racine) pour le JS articles connexes + listing
    idx = [{"slug": a["slug"], "title": _sanitize(a["h1"]), "desc": _sanitize(a["desc"]),
            "tag": a["tag"], "date": a["date"], "readTime": a["readTime"]} for a in arts]
    with open(os.path.join(ROOT, "articles.json"), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False)

    # Listing blog.html
    cards = ''
    for i, a in enumerate(arts):
        cards += (
'<article class="service-card reveal reveal-d%d"><div class="service-card__body">'
'<span class="service-card__cta">%s</span>'
'<h3>%s</h3><p>%s</p>'
'<p class="text-accent" style="font-size:.82rem;color:var(--muted);margin-top:1rem">%s &middot; %s</p></div>'
'<a href="%s" class="service-card__link" aria-label="%s"></a></article>'
            % ((i % 4) + 1, a["tag"], _sanitize(a["h1"]), _sanitize(a["desc"]), a["date"], a["readTime"],
               a["slug"], _sanitize(a["h1"])))
    crumbs = [("Accueil", "index.html"), ("Conseils", None)]
    blog_body = (
'<header class="page-header"><div class="container">%s<h1>Conseils auto et moto</h1>'
'<p>Entretien, freinage, pneus, diagnostic : nos conseils concrets de garagiste à Marseille pour entretenir votre véhicule sans vous tromper.</p></div></header>\n'
'<section class="section"><div class="container"><div class="services-grid">%s</div></div></section>\n'
+ cta_section()
        ) % (breadcrumb_html(crumbs), cards)
    blog_schema = (schema_breadcrumb([("Accueil", "index.html"), ("Conseils", "blog.html")])
                   + '<script type="application/ld+json">'
                     '{"@context":"https://schema.org","@type":"Blog","name":"Conseils Garage Locarno",'
                     '"url":"%s/blog.html","publisher":{"@type":"Organization","name":"Garage Locarno"},'
                     '"blogPost":[%s]}</script>\n'
                     % (SITE, ','.join(
                         '{"@type":"BlogPosting","headline":"%s","url":"%s/%s","datePublished":"%s"}'
                         % (_sanitize(a["h1"]).replace('"', '\\"'), SITE, a["slug"], _iso_date(a["date"])) for a in arts)))
    page("blog.html", "Conseils auto et moto | Garage Locarno",
         "Conseils d'entretien auto et moto par le Garage Locarno à Marseille 5e : vidange, révision, freins, pneus, diagnostic, climatisation.",
         SITE + "/blog.html", blog_body, schema=blog_schema)

    # Pages articles (à la racine)
    for a in arts:
        secs = ''.join('<h2 class="reveal">%s</h2>%s' % (_sanitize(s["h2"]), _sanitize(s["html"])) for s in a["sections"])
        qa = [(_sanitize(f["q"]), _sanitize(f["a"])) for f in a["faq"]]
        mail = ''.join(
'<a href="%s" class="service-card"><div class="service-card__body"><h3>%s</h3>'
'<span class="service-card__cta">Lire &rarr;</span></div></a>' % (m["href"], m["label"]) for m in a["maillage"])
        crumbs = [("Accueil", "index.html"), ("Conseils", "blog.html"), (_sanitize(a["h1"]), None)]
        body = (
'<header class="page-header"><div class="container">%s'
'<span class="eyebrow" style="justify-content:center">%s</span>'
'<h1>%s</h1><p>%s &middot; %s</p></div></header>\n'
'<article class="article-body"><div class="container">'
'%s%s'
'<h2 class="reveal">Questions fréquentes</h2>%s'
'</div></article>\n'
'<section class="section section--paper"><div class="container">'
'<div class="section__header reveal"><span class="eyebrow">À lire aussi</span><h2>Nos autres conseils</h2></div>'
'<div class="services-grid services-grid--2" data-related>%s</div></div></section>\n'
+ cta_section()
            ) % (breadcrumb_html(crumbs), a["tag"], _sanitize(a["h1"]), a["date"], a["readTime"],
                 _sanitize(a["intro"]), secs, faq_html(qa), mail)
        schema = (schema_breadcrumb([("Accueil", "index.html"), ("Conseils", "blog.html"), (_sanitize(a["h1"]), a["slug"])])
                  + '<script type="application/ld+json">'
                    '{"@context":"https://schema.org","@type":"Article","headline":"%s","description":"%s",'
                    '"datePublished":"%s","dateModified":"%s",'
                    '"author":{"@type":"Organization","name":"Garage Locarno"},'
                    '"publisher":{"@type":"Organization","name":"Garage Locarno","logo":{"@type":"ImageObject","url":"%s/assets/logo.png"}},'
                    '"mainEntityOfPage":"%s/%s"}</script>\n'
                    % (_sanitize(a["h1"]).replace('"', '\\"'), _sanitize(a["desc"]).replace('"', '\\"'),
                       _iso_date(a["date"]), _iso_date(a["date"]), SITE, SITE, a["slug"])
                  + schema_faq(qa))
        page(a["slug"], a["title"], _sanitize(a["desc"]), "%s/%s" % (SITE, a["slug"]),
             body, schema=schema, og_type="article")
    print("écrit: blog.html + articles.json + %d articles" % len(arts))


def build_meta_files():
    import json
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    static = ["", "entretien-revision.html", "vidange.html", "freinage.html", "pneus.html",
              "diagnostic.html", "climatisation.html", "batterie.html", "moto-scooter.html",
              "a-propos.html", "avis.html", "contact.html", "blog.html"]
    try:
        with open(os.path.join(ROOT, "blog/articles_content.json"), encoding="utf-8") as f:
            article_slugs = [a["slug"] for a in json.load(f)]
    except Exception:
        article_slugs = []
    urls = ""
    for p in static:
        prio = "1.0" if p == "" else ("0.8" if p.endswith(".html") and p not in ("avis.html", "blog.html") else "0.7")
        urls += '  <url><loc>%s/%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (SITE, p, prio)
    for s in article_slugs:
        urls += '  <url><loc>%s/%s</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n' % (SITE, s)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("écrit: robots.txt + sitemap.xml")


if __name__ == "__main__":
    build_home()
    build_services()
    build_about()
    build_contact()
    build_legal()
    build_avis()
    build_blog()
    build_404()
    build_meta_files()
    print("Build terminé.")
