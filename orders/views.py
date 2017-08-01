from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductsInBasket, ProductsInOrder, Order
from .forms import OrderCreateForm
from .tasks import OrderCreated
from cart.cart import Cart

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
    if not user.username:
        return redirect('auth:login')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            order = form.save(commit=False)
            if cart.discount:
                order.discount = cart.discount
                order.discount_value = cart.discount.discount

            if cart.points:
                order.points_quant = cart.points_quant

            order.save()

            for item in cart:
                ProductsInOrder.objects.create(order=order, product=item['product'],
                                         price_per_itom=item['price'],
                                         number=item['quantity'])
            cart.clear()

            # # Asinc mail sending
            # OrderCreated.delay(order.id)
            request.session['order_id'] = order.id

            return redirect(reverse('payment:process'))
            #return render(request, 'orders/created.html', {'order': order})
        else:
            return render_to_response('orders/create.html', {'username': user.username, 'cart': cart, 'form': form})

    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'username': user.username, 'cart': cart, 'form': form})

@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/detail.html', {'order': order})

@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'static_dev/css/bootstrap.min.css')])
    return response