from .models import Product

def get_variant_picker_data(product):
    variants = product.variants.all()
    variant_attributes = product.attributes.all()
    data = {'variants': [], 'variantAttributes': [], 'discount_policy': product.discount_policy}

    for attribute in sorted(variant_attributes, key=lambda x: x.main_attribute, reverse=True):
        data['variantAttributes'].append({
            'name': attribute.name,
            'public_name': attribute.name.split('_')[1],
            'slug': attribute.slug,
            'values': [{'name': value.name, 'slug': value.slug} for value in attribute.values.all()]
        })

    for variant in variants:
        price = variant.price

        variant_data = {
            'id': variant.id,
            'slug': variant.slug,
            'name': variant.name,
            'price': int(price),
            'attributes': variant.attributes,

        }

        data['variants'].append(variant_data)

    return data

def expand_categories(categories):
    products = None
    for e in categories:
        if e.name.startswith('None'):
            products = Product.objects.filter(category=e)
    return [x for x in categories if not x.name.startswith('None')], products


