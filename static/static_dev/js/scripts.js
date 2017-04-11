$(document).ready(function(){
    var form = $('#form-buying-product');
    console.log(form);
    form.on('submit', function(e){
        e.preventDefault();
        $('#number').val();
        var nmb = $('#number').val();
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data('product-id');
        var product_name = submit_btn.data('product-name');
        var product_price = submit_btn.data('product-price');
        console.log(product_id, product_name);

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
                console.log("OK");
                console.log(data.products_total_nmb);
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

     //$('.basket-container').mouseout(function(){
     //    showingBasket();
     //});

     $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         $(this).closest('li').remove();
     })
});