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

        $('.basket-items ul').append('<li>'+product_name+', ' + nmb + 'pc. ' + 'for ' + product_price + 'rub.  ' +
            '<a class="delete-item" href="">x</a>'+
            '</li>');

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