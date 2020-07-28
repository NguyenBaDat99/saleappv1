from saleapp import app
import json
import os


def read_products(keyword=None, from_price=None, to_price=None):
    with open(os.path.join(app.root_path, "data/products.json"), encoding="utf-8") as f:
        products = json.load(f)
    if keyword:
        return [product for product in read_products() if product["name"].lower().find(keyword.lower()) >= 0]
    if from_price and to_price:
        return [product for product in read_products() if
                from_price <= float(product["price"]) <= to_price]
    return products


def read_products_by_cate_id(cate_id):
    return [product for product in read_products() if product["category_id"] == cate_id]


def add_product(name, description, price, image, category):
    products = read_products()
    products.append({
        "id": len(products) + 1,
        "name": name,
        "description": description,
        "price": float(price),
        "images": image,
        "category_id": int(category)
    })
    return update_product_json(products)


def update_product_json(products):
    try:
        f = open(os.path.join(app.root_path, "data/products.json"), "w", encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        return True
    except Exception as ex:
        print(ex)
        return False


def update_product(id, name, description, price, image, category):
    products = read_products()
    for pro in products:
        if pro["id"] == int(id):
            pro["name"] = name
            pro["description"] = description
            pro["price"] = price
            pro["image"] = image
            pro["category"] = category
            break
    return update_product_json(products)


def read_product_by_id(id):
    products = read_products()
    for pro in products:
        if (pro["id"] == id):
            return pro
    return None


def read_categories():
    with open(os.path.join(app.root_path, "data/categories.json"), encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print(read_products())
