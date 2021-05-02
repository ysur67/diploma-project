import request from './components/tools.js';


function getTotalString(totalPrice){
    return totalPrice > 0 ? parseFloat(totalPrice) + " ₽" : "Корзина";
}

function addItemToCart(event){
    event.preventDefault();
    var form = event.target.closest('form');
    var productId = form.dataset.id;
    var data = {'productId': productId}
    var url = form.action;
    request('post', url, data)
    .then(response => {
        var total = getTotalString(response.total);
        var cartAmount = response.amount;
        var cartBlock = document.querySelectorAll('.cart-count')
        cartBlock.forEach(element => {
            element.innerText = total;
        })
    })
}

function removeItem(event){
    event.preventDefault();
    var button = event.target;
    var url = button.dataset.href;
    var itemId = button.dataset.id;
    var data = {'itemId': itemId}
    request('post', url, data)
    .then(response => {
        button.closest('tr').remove()
        var total = getTotalString(response.total);
        var cartAmount= response.amount;
        if(cartAmount<1){
            var cartItemsBlock = document.querySelector('.cart-content')
            cartItemsBlock.style.display = 'none';
            var emptyCart = document.querySelector('.cart-empty');
            emptyCart.style.display = 'flex';
        }
        var cartBlock = document.querySelectorAll('.cart-count')
        cartBlock.forEach(element => {
            element.innerText = total;
        })
        var cartPrice = document.querySelectorAll('.cart-total')
        cartPrice.forEach(title => {
            title.innerHTML = total;
        })
    })

}

var cartAddButtons = document.querySelectorAll('.sn-product');
cartAddButtons.forEach(btn => {
    btn.addEventListener('click', addItemToCart);
})


var itemRemoveButtons = document.querySelectorAll('.sn-remove');
itemRemoveButtons.forEach(btn => {
    btn.addEventListener('click', removeItem);
})
