import request from './components/tools.js';
import { clearErrors, displayErrors} from './components/form.js';



function getTotalString(totalPrice){
    return totalPrice > 0 ? parseFloat(totalPrice) + " ₽" : "Корзина";
}

function setCart(response){
    var total = getTotalString(response.total);
    setTotalCost(total);
    setCartAmount(response);
}

function setTotalCost(price_string){
    var cartBlock = document.querySelectorAll('.cart-count')
    cartBlock.forEach(element => {
        element.innerText = price_string;
    })
}

function setCartAmount(response){
    var cartAmount = response.amount;
    var amountBlock = document.querySelector('.count-value');
    var amountWrapper = amountBlock.parentNode;
    var isAmountBlockShowen = amountWrapper.classList.contains('display');

    if(cartAmount < 1){
        var amountWrapper = amountBlock.parentNode;
        var isAmountBlockShowen = amountWrapper.classList.contains('display');
        if(isAmountBlockShowen){
            amountWrapper.classList.remove('display');
            amountBlock.innerText = cartAmount;
        }
        return
    }

    if(isAmountBlockShowen && cartAmount){
        amountBlock.innerText = cartAmount;
    }
    if(!isAmountBlockShowen){
        amountWrapper.classList.add('display');
        amountBlock.innerText = cartAmount;
    }
}

function addItemToCart(event){
    event.preventDefault();
    var form = event.target.closest('form');
    var productId = form.dataset.id;
    var data = {'productId': productId}
    var url = form.action;
    request('post', url, data)
    .then(response => {
        setCart(response)
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
        setCart(response);
        var cartTotalSpan = document.querySelector('#cart-total-price');
        cartTotalSpan.innerText = response.total;
        var cartAmount= response.amount;
        if(cartAmount<1){
            var cartItemsBlock = document.querySelector('.cart-content')
            cartItemsBlock.style.display = 'none';
            var emptyCart = document.querySelector('.cart-empty');
            emptyCart.style.display = 'flex';
        }
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

    setCart(response_data);
    
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
