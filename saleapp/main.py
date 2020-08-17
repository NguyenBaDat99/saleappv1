import json

from flask import render_template, request, redirect, url_for, send_file, jsonify, session
from saleapp import app
from saleapp import dao, utils, decorate


@app.route("/")
def index():
    return render_template("index2.html")


@app.route("/products")
def product_list():
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    from_price = float(request.args["from_price"]) if request.args.get("from_price") else None
    to_price = float(request.args["to_price"]) if request.args.get("to_price") else None

    return render_template("product-list.html", products=dao.read_products(keyword=keyword, from_price=from_price, to_price=to_price))


@app.route("/products/<int:category_id>")
def product_list_by_cate(category_id):
    return render_template("product-list.html", products=dao.read_products_by_cate_id(category_id))


@app.route("/products/add", methods=["get", "post"])
@decorate.login_required
def product_add():
    err_msg = None
    if request.method == "POST":
        if request.args["product_id"] and int(request.args["product_id"]) > 0:
            p = dict(request.form.copy())
            p["id"] = request.args["product_id"]

            if dao.update_product(**p):
                return redirect(url_for('product_list'))
            else:
                pass
        else:
            if dao.add_product(**dict(request.form)):
                return redirect(url_for('product_list'))
            else:
                err_msg = "Add failed!!!"

    product = None
    if request.args["product_id"]:
        if int(request.args["product_id"]) > 0:
            product = dao.read_product_by_id(int(request.args["product_id"]))

    categories = dao.read_categories()
    return render_template("product-add.html", categories=categories, err_msg=err_msg, product=product)


@app.route("/api/products/<int:product_id>", methods=["delete"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({"status": 200, "product_id": product_id})

    return jsonify({"status": 500, "error_message": "Something Wrong!!!"})


@app.route("/product/export")
def export_product():
    p = utils.export()

    return send_file(filename_or_fp=p)


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            session["user"] = user
            if "next" in request.args:
                return redirect(request.args["next"])
            else:
                return redirect(url_for('index'))
        else:
            err_msg = "Something wrong!!!"
    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None
    return redirect(url_for("index"))


@app.route("/register",  methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)
    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Password wrong!!!"
        else:
            if dao.add_user(name=name, username=username, password=password):
                return redirect(url_for("login"))
            else:
                err_msg = "Something wrong!!!"
    return render_template("register.html", err_msg=err_msg)


@app.route("/api/cart", methods=["post"])
def add_to_cart():
    data = json.loads(request.data)
    product_id = data.get("product_id")
    name = data.get("name")
    price = data.get("price")
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    product_key = str(product_id)
    if product_key in cart:
        cart[product_key]["quantity"] = cart[product_key]["quantity"] + 1
    else:
        cart[product_key] = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session["cart"] = cart

    return jsonify({"success": 1, "quantity": sum([c["quantity"] for c in list(session["cart"].values())])})


@app.route('/cart')
def cart():
    return render_template('payment.html')


if __name__ == "__main__":
    app.run(debug=True)

