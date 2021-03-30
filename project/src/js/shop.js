import request from './components/tools.js';


function addItemToCart(event){
    event.preventDefault();
    var form = event.target.closest('form');
    var productId = form.dataset.id;
    var data = {'productId': productId}
    var url = form.action;
    request('post', url, data)
    .then(response => {
        var total = response.total > 0 ? response.total + " ₽" : "Корзина";
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
        console.log(response)
        button.closest('tr').remove()
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
