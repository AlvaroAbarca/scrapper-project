from core.models import Product, Store
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from remote.falabella import get_product_info

def validate_url_with_stores(url):
    for store in Store.objects.all():
        if store.base_url in url:
            return True
    return False

def create_or_link_product(url, request):
    try:
        product_info = get_product_info(url)
        if len(Product.objects.filter(url=url)) == 0:
            product = Product.objects.create(
                name=product_info["name"],
                price=product_info["normal-price"],
                price_internet=product_info["internet-price"],
                price_event=product_info["event-price"],
                price_card=product_info["card-price"],
                url_image=product_info["image"],
                url=product_info["url"],
                specs=product_info["specs"],
                brand=product_info["brand"],
                seller=product_info["seller"]
            )
            product.save()
            if product.min_price() == 0:
                product.stock = False
            else:
                product.stock = True
            product.save()
        else:
            product = Product.objects.filter(url=url)[0]
        product.users.add(request.user)
        return True
    except:
        return False

def create_or_find_product(url):
    try:
        product_info = get_product_info(url)
        if len(Product.objects.filter(url=url)) == 0:
            product = Product.objects.create(
                name=product_info["name"],
                price=product_info["normal-price"],
                price_internet=product_info["internet-price"],
                price_event=product_info["event-price"],
                price_card=product_info["card-price"],
                url_image=product_info["image"],
                url=product_info["url"],
                specs=product_info["specs"],
                brand=product_info["brand"],
                seller=product_info["seller"]
            )
            product.save()
        else:
            product = Product.objects.filter(url=url)[0]
        return product
    except:
        return False


def send_notification_mail(products):
    subject = 'Algunos Productos que sigues bajaron de precio!'
    html_message = render_to_string(
        'emails/notification_email.html',
        {'products': products})
    plain_message = strip_tags(html_message)
    from_email = 'no-reply@example.com'
    to = 'marcelocavieresd@gmail.com'
    send_mail(
        subject, plain_message, from_email, [to],
        html_message=html_message)
    return True


def create_chart_data(product):
    labels = []
    prices = []
    cont = 1
    for history in product.producthistory_set.all():
        labels.append(history.created_at.strftime("%d-%m-%Y"))
        prices.append("{}".format(int(history.min_price())))
        cont+=1
    return(labels, prices)
