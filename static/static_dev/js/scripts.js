$(document).ready(function(){
    var form = $('#form-buying-product');
    form.on('submit', function(e){
        e.preventDefault();
        $('#number').val();
        var nmb = $('#number').val();
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data('product-id');
        var product_name = submit_btn.data('product-name');
        var product_price = submit_btn.data('product-price');

        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token = $('#form-buying-product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = form.attr('action');

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                if (data.products_total_nmb){
                    $('#basket_total_nmb').text('('+data.products_total_nmb+')');
                    $('.basket-items ul').html("");
                    $.each(data.products, function(k, v){
                        $('.basket-items ul').append('<li>'+v.name+', ' + v.nmb + 'pc. ' + 'for ' + v.price_per_item + 'rub.  ' +
                            //'<a class="delete-item" href="">x</a>'+
                        '</li>');
                    });
                }
            },
            error: function(){
                 console.log("error")
             }
        });
    });

    calculate();

    function showingBasket(){
        $('.basket-items').removeClass('hidden');
    };

    //$('.basket-container').on('click', function(e){
    //    e.preventDefault();
    //    showingBasket();
    //});

     $('.basket-container').mouseover(function(){
         showingBasket();
     });

     $('.basket-container').mouseout(function(){
         showingBasket();
     });

     $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         $(this).closest('li').remove();
     })
});

function showOrHide(cb, cat) {
    cb = document.getElementById(cb);
    cat = document.getElementById(cat);
    if (cb.checked) cat.style.display = "block";
    else cat.style.display = "none";
}

function _discount(quantity, discount_policy){
    if (isNaN(discount_policy)) {
        return 1
    }
    else {
        var keys = Object.keys(discount_policy);
        for (var i = 0, len = keys.length; i < len; i++) {
            var split_entry = keys[i].split('-');
            if (parseInt(split_entry[0]) <= quantity && quantity < parseFloat(split_entry[1])){
                return parseFloat(discount_policy[keys[i]]);
            }
        }
    }

}

function calculate(){
    var count = document.getElementById("variant_length").value;
    var quantity = document.getElementById("quantity").value;
    var result = document.getElementById("result");
    var price_per_itom = document.getElementById("price_per_itom");
    var erw = document.getElementById("erw");
    var variants = JSON.parse(document.getElementById("variants").value.replace(/'/g, '"'));
    var discount_policy = JSON.parse(document.getElementById("discount_policy").value.replace(/'/g, '"'));
    var product_slug = document.getElementById("product_slug");
    var result_itog = document.getElementById("result_itog");
    var tmp_price = 0;


    if (count == 0) {
        tmp_price = Math.round(variants[0]['price'] * _discount(quantity, discount_policy));
        result.innerHTML = tmp_price;
        price_per_itom.value = tmp_price;
        tmp_price = tmp_price * quantity;
        result_itog.innerHTML = tmp_price;
        erw.innerHTML = Math.round(tmp_price * 0.05);
        product_slug.value = variants[0].slug;
    }

    if (count > 1) {
        var quant0 = document.getElementById("id_0");
        var quant1 = document.getElementById("id_1");
        var quant0_val = JSON.parse(quant0.value.replace(/'/g, '"'));
        var quant1_val = JSON.parse(quant1.value.replace(/'/g, '"'));
        for (var i = 0, len = variants.length; i < len; i++) {
            if (variants[i]['attributes'][quant0.name] == quant0_val['name'] &&
                variants[i]['attributes'][quant1.name] == quant1_val['name']) {
                    tmp_price = Math.round(variants[i]['price'] * _discount(quantity, discount_policy));
                    result.innerHTML = tmp_price;
                    price_per_itom.value = tmp_price;
                    tmp_price = tmp_price * quantity;
                    result_itog.innerHTML = tmp_price;
                    erw.innerHTML = Math.round(tmp_price * 0.05);
                    product_slug.value = variants[i].slug;
                }
        }
    }
    else {
        var quant0 = document.getElementById("id_0");
        var quant0_val = JSON.parse(quant0.value.replace(/'/g, '"'));
        for (var i = 0, len = variants.length; i < len; i++) {
            if (variants[i]['attributes'][quant0.name] == quant0_val['name']) {
                    tmp_price = Math.round(variants[i]['price'] * _discount(quantity, discount_policy));
                    result.innerHTML = tmp_price;
                    price_per_itom.value = tmp_price;
                    tmp_price = tmp_price * quantity;
                    result_itog.innerHTML = tmp_price;
                    erw.innerHTML = Math.round(tmp_price * 0.05);
                    product_slug.value = variants[i].slug;
                }
        }
    }
}