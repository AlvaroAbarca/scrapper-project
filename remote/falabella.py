import requests
from bs4 import BeautifulSoup
from core.models import Product

# url = "https://www.falabella.com/falabella-cl/product/8184177"


def get_product_info(url):
    r = requests.get(url)
    id = [x for x in url.split("/") if x.isdigit()][0]
    soup = BeautifulSoup(r.text, "lxml")
    div = soup.find_all("div", {"class": "price"})
    soup2 = BeautifulSoup(str(div), "lxml")
    aux = soup2.find_all("li")
    seller = "Fallabela"
    info_seller = soup.find("p", {"class": "sellerInfoContainer"})
    brand = soup.find("a", {"class": "product-brand-link"}).string
    if info_seller:
        seller = info_seller.find("span", {"class": "underline"}).string
    specs = soup.find("div", {"class": "specifications-container"})
    product = {
        "specs": "",
        "name": "",
        "normal-price": 0,
        "event-price": 0,
        "internet-price": 0,
        "card-price": 0,
        "image": "",
        "url": url,
        "seller": seller,
        "brand": brand
    }
    product["specs"] = str(specs)
    for x in aux:
        if "data-normal-price" in x.attrs:
            product["normal-price"] = int(x.attrs["data-normal-price"].replace(".", ""))
        elif "data-event-price" in x.attrs:
            product["event-price"] = int(x.attrs["data-event-price"].replace(".", ""))
        elif "data-internet-price" in x.attrs:
            product["internet-price"] = int(x.attrs["data-internet-price"].replace(".", ""))
        elif "data-cmr-price" in x.attrs:
            product["card-price"] = int(x.attrs["data-cmr-price"].replace(".", ""))

    if product["normal-price"] == 0:
        product["normal-price"] = product["internet-price"]

    name = soup.find("div", {"class": "fa--product-name"})
    image = "https://falabella.scene7.com/is/image/Falabella/{}".format(id)
    product["name"] = name.attrs["data-name"]
    product["image"] = image
    return product


def update_products():
    products = Product.objects.all()
    for product in products:
        new_product_info = get_product_info(product.url)
        product.price = new_product_info["normal-price"]
        product.price_internet = new_product_info["internet-price"]
        product.price_event = new_product_info["event-price"]
        product.name = new_product_info["name"]
        product.save()
