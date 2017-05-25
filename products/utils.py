def get_variant_picker_data(product):
    variants = product.variants.all()
    variant_attributes = product.product_class.variant_attributes.all()
    data = {'variants': [], 'variantAttributes': []}

    for attribute in variant_attributes:
        data['variantAttributes'].append({
            'name': attribute.name,
            'slug': attribute.slug,
            'values': [{'name': value.name, 'slug': value.slug} for value in attribute.values.all()]
        })

    for variant in variants:
        price = variant.price

        variant_data = {
            'id': variant.id,
            'name': variant.name,
            'price': price,
            'attributes': variant.attributes,

        }

        data['variants'].append(variant_data)

    return data


