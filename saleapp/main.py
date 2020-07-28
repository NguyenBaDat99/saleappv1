from flask import render_template, request, redirect, url_for
from saleapp import app
from saleapp import dao

@app.route("/")
def index():
    return render_template("index.html")

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


if __name__ == "__main__":
    app.run(debug=True)

