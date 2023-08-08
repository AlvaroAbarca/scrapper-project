from celery.decorators import task
from core.models import Product, UpdateNote
from django.contrib.auth.models import User
from remote.falabella import get_product_info
from core.utils import send_notification_mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@task(name="send_notification_mail", bind=True)
def send_notification_mail(self, html_message, user_email):
    subject = 'Algunos Productos que sigues bajaron de precio!'
    plain_message = strip_tags(html_message)
    from_email = 'no-reply@bajodeprecio.cl'
    to = user_email
    send_mail(
        subject, plain_message, from_email, [to],
        html_message=html_message)
    return True

@task(name="sent_notifications", bind=True)
def sent_notifications(self):
    users = User.objects.all()
    for user in users:
        offer_products = [product.pk for product in user.product_set.all() if product.is_offer()]
        products = Product.objects.filter(pk__in=offer_products)
        if len(products) != 0:
            html_message = render_to_string(
                'emails/notification_email.html',
                {'products': products})
            send_notification_mail.delay(html_message, user.email)
    return True

@task(name="product_update", bind=True)
def product_update(self):
    products = Product.objects.all()
    for product in products:
        new_product_info = get_product_info(product.url)
        product.price = new_product_info["normal-price"]
        product.price_internet = new_product_info["internet-price"]
        product.price_event = new_product_info["event-price"]
        product.price_card = new_product_info["card-price"]
        product.save(
            update_fields=['price', 'price_card', 'price_internet', 'price_event']
        )
    sent_notifications.delay()
    return True
