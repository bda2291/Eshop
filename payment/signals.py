from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
import weasyprint

from orders.models import Order

def PaymentNotification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

        # Отправка Email
        subject = 'E-shop - Order: {}'.format(order.id)
        message = 'In the application there is a PDF-file with information about your order'
        email = EmailMessage(subject, message, 'admin@mayshop.com', [order.customer_email])

        # Генерация PDF
        html = render_to_string('orders/pdf.html', {'order': order})
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(out,
                                stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'static_dev/css/bootstrap.min.css')])

        # Прикрепляем pdf
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()

valid_ipn_received.connect(PaymentNotification)