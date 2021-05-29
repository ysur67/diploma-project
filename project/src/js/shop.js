import request from './components/tools.js';
import { clearErrors, displayErrors} from './components/form.js';



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
        // button.closest('tr').remove()
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

        var productItem = button.closest('tr');
        var isLast = productItem.classList.contains('last') ? true : false;
        var isFirst = productItem.classList.contains('first') ? true : false;

        var borderItem = document.querySelector(`.border_${ itemId }`);
        if(borderItem){
            borderItem.remove()
        }
        productItem.remove();
    })

}

console.log('jopa')
        

async function submitProduct(event){
    event.preventDefault();
    const form = event.target;
    const url = form.action;
    const data = new FormData(form)
    clearErrors(form);
    var response_data = await request('post', url, data);
    if(response_data.errors){
        displayErrors(form, response_data.fields)
        return
    }

    if(response_data.message){
        console.log(response_data.message);
    }

    var total = getTotalString(response_data.total);
    var cartBlock = document.querySelectorAll('.cart-count')
    cartBlock.forEach(element => {
        element.innerText = total;
    })
    
}

var productForm = document.querySelector('.product-form')
if(productForm){
    productForm.addEventListener('submit', submitProduct)
}

$(document).on('click', '.sn-product', function() {
    addItemToCart(event)
})

var itemRemoveButtons = document.querySelectorAll('.sn-remove');
itemRemoveButtons.forEach(btn => {
    btn.addEventListener('click', removeItem);
})
