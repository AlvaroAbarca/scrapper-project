from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.notifications import send_updates_mail

class UpdateNote(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    note = models.TextField(max_length=6000)
    date = models.DateTimeField(null=True, blank=True)

class Store(models.Model):
    base_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.base_url

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=True)
    updates_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    price_internet = models.IntegerField(null=True, blank=True)
    price_event = models.IntegerField(null=True, blank=True)
    price_card = models.IntegerField(null=True, blank=True)
    seller = models.CharField(max_length=200, null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    specs = models.TextField(max_length=2000, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    url_image = models.CharField(max_length=200, null=True, blank=True)
    users = models.ManyToManyField(User)
    stock = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def min_price(self):
        aux1 = [self.price, self.price_internet, self.price_event, self.price_card]
        aux = list(filter(lambda a: a != 0, aux1))
        if len(aux) == 0:
            aux = [0]
        return min(aux, key=float)

    def min_is_cmr(self):
        return int(self.min_price()) == self.price_card

    def is_offer(self):
        historic = self.producthistory_set.all().order_by("-created_at")
        if len(historic) < 2:
            return False
        price_1 = historic[0]
        price_2 = historic[1]
        if price_1.min_price() < price_2.min_price():
            return True
        else:
            return False
    def __str__(self):
        return "{} - {}".format(self.name, self.price)


class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    price_internet = models.IntegerField(null=True, blank=True)
    price_event = models.IntegerField(null=True, blank=True)
    price_card = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def min_price(self):
        aux1 = [self.price, self.price_internet, self.price_event, self.price_card]
        aux = list(filter(lambda a: a != 0, aux1))
        if len(aux) == 0:
            aux = [0]
        return min(aux, key=float)

    def __str__(self):
        fecha = self.created_at.strftime("%d-%m-%Y (%H:%M:%S.%f)")
        return ("{} - {}".format(self.product.name, fecha))


@receiver(post_save, sender=Product)
def save_product_history(sender, instance, created, update_fields, **kwargs):
    if not created and update_fields:
        product_history = ProductHistory.objects.create(
            product=instance,
            price=instance.price,
            price_internet=instance.price_internet,
            price_event=instance.price_event,
            price_card=instance.price_card
        )
        if instance.min_price() == 0:
            instance.stock = False
        else:
            instance.stock = True
        instance.save()
        product_history.save()


@receiver(post_save, sender=UpdateNote)
def sent_updates_email(sender, instance, created, **kwargs):
    if created:
        users_emails = [user.email for user in User.objects.all() if user.email and user.profile.updates_notifications]
        for email in users_emails:
            send_updates_mail.delay(instance.title, instance.note, email)
