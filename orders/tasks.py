from django.conf import settings
from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from io import BytesIO
import weasyprint
import pytils
from .models import Order

SUPPLIER_INFO = '''ООО "Русские Программы", ИНН 7713409230, КПП 771301001,
                127411, Москва г, Дмитровское ш., дом № 157, корпус 7, тел.: +74957258950'''

requisites = {'name': 'ООО "Русские Программы"', 'bank': 'АО "СМП БАНК" Г. МОСКВА', 'INN': '7713409230',
              'KPP': '771301001', 'BIK': '44525503', 'bank_acc': '30101810545250000503', 'acc': '40702810300750000177',
              'sup_info': SUPPLIER_INFO}

@task
def OrderCreated(order_id):
    """
    Sending Email of order creating
    """
    order = Order.objects.get(id=order_id)
    verb_price = pytils.numeral.in_words(round(order.total_price))
    verb_cur = pytils.numeral.choose_plural(round(order.total_price), ("рубль", "рубля", "рублей"))
    subject = 'Order {}'.format(order.id)
    message = 'Dear, {}, You have successfully placed an order.\
                   Your order number {}'.format(order.customer_name, order.id)
    mail_send = EmailMessage(subject, message, 'admin@myshop.ru', [order.customer_email, 'bda2291@mail.ru'])

    # html = render_to_string('orders:AdminOrderPDF', args=[order_id])

    html = render_to_string('orders/pdf.html', {**requisites, 'order': order,
                                                'verb_cur': verb_cur, 'verb_price': verb_price})
    rendered_html = html.encode(encoding="UTF-8")
    out = BytesIO()
    weasyprint.HTML(string=rendered_html).write_pdf(out,
                        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])

    # weasyprint.HTML(string=rendered_html, base_url=request.build_absolute_uri()).write_pdf(response,
    #                             stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/bootstrap.min.css')])
    mail_send.attach('order_{}.pdf'.format(order_id), out.getvalue(), 'application/pdf')
    mail_send.send()
    return mail_send