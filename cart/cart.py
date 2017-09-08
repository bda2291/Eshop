from decimal import Decimal
from django.conf import settings
from django.contrib import auth
from products.models import Product, Offer
# from discount.models import Discount

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.discount_id = self.session.get('discount_id')
        if request.user.is_authenticated():
            self.points = self.session.get('points')
            self.points_quant = auth.get_user(request).profile.user_points
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, offer, price_per_itom, quantity=1, update_quantity=False):
        offer_slug = offer.slug
        if offer_slug not in self.cart:
            self.cart[offer_slug] = {'quantity': 0,
                                     'price': str(price_per_itom)}
        if update_quantity:
            self.cart[offer_slug]['quantity'] = int(quantity)
        else:
            self.cart[offer_slug]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, offer_slug):
        # product_id = str(product.id)
        if offer_slug in self.cart:
            del self.cart[offer_slug]
            self.save()

    def __iter__(self):
        offers_ids = self.cart.keys()
        offers = Offer.objects.filter(slug__in=offers_ids)

        for offer in offers:
            self.cart[str(offer.slug)]['offer'] = offer

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    # @property
    # def discount(self):
    #     if self.discount_id:
    #         return Discount.objects.get(id=self.discount_id)
    #     return None

    # def get_discount(self):
    #     if self.discount:
    #         return (self.discount.discount / Decimal('100')) * self.get_total_price()
    #     return Decimal('0')

    # def get_total_price_after_discount(self):
    #     return self.get_total_price() - self.get_discount()

    def get_total_deduct_points(self):
        return self.get_total_price() - Decimal(self.points_quant)

