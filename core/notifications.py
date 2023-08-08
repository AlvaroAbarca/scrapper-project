from celery.decorators import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@task(name="send_updates_mail", bind=True)
def send_updates_mail(self, title, text, user_email):
    html_message = render_to_string(
        'emails/update_notification_email.html',
        {'title': title, 'text': text})
    subject = 'Tenemos nuevas actualizaciones!'
    plain_message = strip_tags(html_message)
    from_email = 'no-reply@bajodeprecio.cl'
    to = user_email
    send_mail(
        subject, plain_message, from_email, [to],
        html_message=html_message)
    return True
