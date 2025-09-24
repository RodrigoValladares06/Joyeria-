from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"

PRODUCTS = [
    # ANILLOS
    {
        "id": 1,
        "slug": "anel-aurora",
        "name": "Anillo Aurora",
        "price": 129,
        "material": "Plata 925",
        "image": "https://cdn-media.glamira.com/media/product/newgeneration/view/1/sku/G100595/diamond/diamond-Brillant_AAA/alloycolour/yellow.jpg",
        "short": "Diseño minimalista con circonia.",
        "description": "Anillo de plata 925 acabado espejo, engaste pavé con circonia brillante.",
        "tags": ["anillo", "plata", "minimalista"],
    },
    {
        "id": 2,
        "slug": "anel-estelar",
        "name": "Anillo Estelar",
        "price": 159,
        "material": "Oro blanco 14k",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXjPflamDZFxwG6D2p4mIc61HLb5MI3Ems8_uJjxvhIP8SfgaPtwPHRNE6C5c5mXtKsOg&usqp=CAU",
        "short": "Elegante con zirconia central.",
        "description": "Anillo de oro blanco 14k con circonia en talla brillante y detalles laterales.",
        "tags": ["anillo", "oro", "elegante"],
    },
    {
        "id": 3,
        "slug": "anel-rosalia",
        "name": "Anillo Rosalia",
        "price": 189,
        "material": "Plata bañada en oro rosa",
        "image": "https://cdn-media.glamira.com/media/product/newgeneration/view/1/sku/Rosalia/alloycolour/red.jpg",
        "short": "Romántico en oro rosa.",
        "description": "Anillo de plata con baño en oro rosa, engaste delicado con piedras pequeñas.",
        "tags": ["anillo", "oro rosa", "romantico"],
    },

    # COLLARES
    {
        "id": 4,
        "slug": "collar-solsticio",
        "name": "Collar Solsticio",
        "price": 249,
        "material": "Oro 14k",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQf0ElXHEPBLFvFGCfMRtEEcLsK4bq7Rlah8A&s",
        "short": "Colgante sol en oro 14k.",
        "description": "Cadena veneciana 45cm con dije de sol texturizado en oro 14 quilates. Cierre seguro.",
        "tags": ["collar", "oro", "solar"],
    },
    {
        "id": 5,
        "slug": "collar-luz",
        "name": "Collar Luz",
        "price": 199,
        "material": "Plata 925",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYs7pzhnNMP6qsUXZGgWJJ343nnyGVFPpmBg&s",
        "short": "Colgante minimalista brillante.",
        "description": "Collar de plata con dije circular incrustado con zirconias.",
        "tags": ["collar", "plata", "minimalista"],
    },
    {
        "id": 6,
        "slug": "collar-perla",
        "name": "Collar Perla",
        "price": 279,
        "material": "Oro amarillo 18k",
        "image": "https://m.media-amazon.com/images/I/51khSoyxNlS._UY1000_.jpg",
        "short": "Clásico con perla natural.",
        "description": "Cadena fina de oro amarillo 18k con dije de perla natural cultivada.",
        "tags": ["collar", "oro", "perla"],
    },

    # ARETES
    {
        "id": 7,
        "slug": "aretes-luna",
        "name": "Aretes Luna",
        "price": 89,
        "material": "Baño de oro 18k",
        "image": "https://isabellajewelry.store/wp-content/uploads/2024/10/Zacilloluna-2.jpg",
        "short": "Aros luna creciente.",
        "description": "Aros ligeros con baño de oro 18k, libre de níquel. Perfectos para uso diario.",
        "tags": ["aretes", "baño de oro", "arcos"],
    },
    {
        "id": 8,
        "slug": "aretes-estrellas",
        "name": "Aretes Estrellas",
        "price": 109,
        "material": "Plata 925",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkDwl57itaMzycliQR7nV_-A0yA92ZIUogGg&s",
        "short": "Estrellas delicadas en plata.",
        "description": "Aretes pequeños de plata 925 en forma de estrellas, ideales para uso diario.",
        "tags": ["aretes", "plata", "estrellas"],
    },
    {
        "id": 9,
        "slug": "aretes-perla",
        "name": "Aretes Perla",
        "price": 139,
        "material": "Oro blanco 14k",
        "image": "https://www.joyaspangea.com/cdn/shop/files/hpX70PKQ.jpg?v=1716407524&width=640",
        "short": "Clásicos con perlas naturales.",
        "description": "Aretes de oro blanco 14k con perlas naturales cultivadas.",
        "tags": ["aretes", "oro", "perla"],
    },
]


def filter_products(q: str | None, material: str | None):
    results = PRODUCTS
    if q:
        ql = q.lower().strip()
        results = [
            p for p in results
            if ql in p["name"].lower() or any(ql in t.lower() for t in p["tags"]) or ql in p["material"].lower()
        ]
    if material:
        ml = material.lower()
        results = [p for p in results if ml in p["material"].lower()]
    return results

@app.context_processor
def inject_globals():
    return {"year": datetime.now().year}

@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS)

@app.route("/catalog")
def catalog():
    q = request.args.get("q")
    material = request.args.get("material")
    filtered = filter_products(q, material)
    return render_template("catalog.html", products=filtered, q=q, material=material)

@app.route("/product/<slug>")
def product_detail(slug: str):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        return redirect(url_for("catalog"))
    return render_template("detail.html", product=product)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    sent = False
    if request.method == "POST":
        sent = True
    return render_template("contact.html", sent=sent)

app.run(debug=True)
