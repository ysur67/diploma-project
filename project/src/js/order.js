import request from './components/tools.js';
import { displayErrors, clearErrors } from './components/form.js';


function changeState(buttons){
    buttons.forEach(button => {
        var wrapper = button.parentNode;
        if(button.checked){
            wrapper.classList.toggle('checked');
        }else{
            wrapper.classList.remove('checked')
        }
    })
}

async function sendOrderForm(event){
    event.preventDefault();
    var form = event.target.closest('form');
    clearErrors(form);
    var data = new FormData(form);
    var url = form.action;
    var response_data = await request('post', url, data)
    if(response_data.redirect)
        window.location.href = response_data.redirect;

    if(response_data.errors){
        displayErrors(form, response_data.fields);
        return;
    }
}

var shippingButtons = document.querySelectorAll('.radio-btn-shipping');
var paymentButtons = document.querySelectorAll('.radio-btn-payment');

shippingButtons.forEach(btn => {
    btn.addEventListener('click', function(){changeState(shippingButtons)})
})
paymentButtons.forEach(btn => {
    btn.addEventListener('click', function(){changeState(paymentButtons)})
})

var sendOrderButtons = document.querySelectorAll('.sn-order-form');
sendOrderButtons.forEach(btn => {
    btn.addEventListener('click', sendOrderForm)
})
document.addEventListener('DOMContentLoaded', function(){
    changeState(paymentButtons);
    changeState(shippingButtons);
})