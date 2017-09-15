from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
import weasyprint
import pytils
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductsInBasket, ProductsInOrder, Order
from .forms import OrderCreateForm
from .tasks import OrderCreated
from cart.cart import Cart

SUPPLIER_INFO = '''ООО "Русские Программы", ИНН 7713409230, КПП 771301001,
                127411, Москва г, Дмитровское ш., дом № 157, корпус 7, тел.: +74957258950'''

requisites = {'name': 'ООО "Русские Программы"', 'bank': 'АО "СМП БАНК" Г. МОСКВА', 'INN': '7713409230',
              'KPP': '771301001', 'BIK': '44525503', 'bank_acc': '30101810545250000503', 'acc': '40702810300750000177',
              'sup_info': SUPPLIER_INFO}

def basket_adding(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    new_product, created = ProductsInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, defaults={'number':nmb})
    if not created:
        new_product.number += int(nmb)
        new_product.save(force_update=True)

    products_in_basket = ProductsInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = []

    for item in products_in_basket:
        product_dict = {}
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_itom
        product_dict["nmb"] = item.number
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def basket_remove(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")


def OrderCreate(request):
    cart = Cart(request)
    user = auth.get_user(request)
    profile = user.profile
    if not user.username:
        return redirect('auth:login')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            # if cart.discount:
            #     order.discount = cart.discount
            #     order.discount_value = cart.discount.discount

            if cart.points:
                print(cart.points_quant)
                order.points_quant = cart.points_quant
                profile.user_points -= cart.points_quant
            profile.save()
            order.save()

            for item in cart:
                ProductsInOrder.objects.create(order=order, product=item['offer'],
                                         price_per_itom=item['price'],
                                         number=item['quantity'])
            cart.clear()

            # Asinc mail sending
            OrderCreated.delay(order.id)
            request.session['order_id'] = order.id

            # return redirect(reverse('payment:process'))
            return render(request, 'orders/created.html', {'username': user.username, 'order': order})
        else:
            return render('orders/create.html', {'username': user.username, 'cart': cart, 'form': form})

    form = OrderCreateForm(instance=profile)
    return render(request, 'orders/create.html', {'username': user.username, 'cart': cart, 'form': form})


@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/detail.html', {'order': order})


@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    verb_price = pytils.numeral.in_words(round(order.total_price))
    verb_cur = pytils.numeral.choose_plural(round(order.total_price), ("рубль", "рубля", "рублей"))
    html = render_to_string('orders/pdf.html', {**requisites, 'order': order,
                                                'verb_cur': verb_cur, 'verb_price': verb_price})
    rendered_html = html.encode(encoding="UTF-8")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=rendered_html, base_url=request.build_absolute_uri()).write_pdf(response,
                        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/bootstrap.min.css')])
    return response