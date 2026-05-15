import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename


import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")

cred = credentials.Certificate("borrowbuddy-7ebe6-firebase-adminsdk-fbsvc-9945534579.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sell", methods=["GET", "POST"])
def sell_page():
    if request.method == "POST":
        title         = request.form.get("title")
        category      = request.form.get("other_category") or request.form.get("category")
        description   = request.form.get("description")
        price_per_day = float(request.form.get("price"))
        location      = request.form.get("location")
        owner_email   = request.form.get("owner_email")
        phone         = request.form.get("phone")  

        if not owner_email:
            flash("You must be logged in to post a listing.", "error")
            return redirect(url_for("login"))

        image_file = request.files.get("image")
        if not image_file or image_file.filename == "":
            flash("Please select an image to upload.", "error")
            return redirect(url_for("sell_page"))

        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(image_path)
        image_url = url_for("static", filename=f"uploads/{filename}")

        db.collection("items").add({
            "title":         title,
            "category":      category,
            "description":   description,
            "price_per_day": price_per_day,
            "location":      location,
            "owner_email":   owner_email,
            "phone":         phone,  # ✅ saved to Firestore
            "image_url":     image_url,
            "created_at":    firestore.SERVER_TIMESTAMP
        })
        return redirect(url_for("buy_page"))

    return render_template("sell.html")


@app.route("/buy")
def buy_page():
    items = []
    docs = db.collection("items").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        items.append(data)
    return render_template("buy.html", products=items)


@app.route("/item/<item_id>")
def item_detail(item_id):
    doc = db.collection("items").document(item_id).get()
    if not doc.exists:
        flash("Item not found.", "error")
        return redirect(url_for("buy_page"))

    item = doc.to_dict()
    item["id"] = doc.id
    return render_template("item.html", item=item)


@app.route("/request-rent/<item_id>", methods=["POST"])
def request_rent(item_id):
    requester_email = request.form.get("requester_email")
    rental_days     = int(request.form.get("days"))

    if not requester_email or rental_days < 1:
        flash("Rental request invalid.", "error")
        return redirect(url_for("item_detail", item_id=item_id))

    db.collection("rent_requests").add({
        "item_id":         item_id,
        "requester_email": requester_email,
        "rental_days":     rental_days,
        "status":          "pending",
        "requested_at":    firestore.SERVER_TIMESTAMP
    })

    flash("Your request has been sent successfully!", "success")
    return redirect(url_for("item_detail", item_id=item_id)) 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/howitworks")
def how_it_works():
    return render_template("howitworks.html")

if __name__ == "__main__":
    app.run(debug=True)