import requests
from bs4 import BeautifulSoup

url = "https://www.falabella.com/falabella-cl/product/8077802/Pc-Gamer-Amd-Ryzen-R5-8Gb-Ram-240Gb-Ssd/8077802"
url = "https://www.falabella.com/falabella-cl/product/8077802/Pc-Gamer-Amd-Ryzen-R5-8Gb-Ram-240Gb-Ssd/8077802"
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
    "name": "",
    "normal-price": "",
    "event-price": "",
    "internet-price": "",
    "card-price": "",
    "image": "",
    "url": url,
    "seller": seller,
    "brand": brand
}

for x in aux:
    if "data-normal-price" in x.attrs:
        product["normal-price"] = x.attrs["data-normal-price"]
    elif "data-event-price" in x.attrs:
        product["event-price"] = x.attrs["data-event-price"]
    elif "data-internet-price" in x.attrs:
        product["internet-price"] = x.attrs["data-internet-price"]
    elif "data-cmr-price" in x.attrs:
        product["card-price"] = x.attrs["data-cmr-price"]

if product["normal-price"] == "":
    product["normal-price"] = product["internet-price"]

name = soup.find("div", {"class": "fa--product-name"})
image = "https://falabella.scene7.com/is/image/Falabella/{}".format(id)
product["name"] = name.attrs["data-name"]
product["image"] = image
print(str(specs))
