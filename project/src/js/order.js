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

function toggleVisibility(target, display){
    if(display){
        target.classList.remove('disabled');
        return
    }
    target.classList.add('disabled');
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

async function getSuggestions(event){
    var target = event.target;
    var inputValue = target.value;
    var requestData = {'address': inputValue}
    var url = window.location.href;
    var response_data = await request('post', url, requestData);
    console.log(response_data)
    console.log(response_data.suggestions);
    displaySuggestions(response_data.suggestions);
}

function displaySuggestions(suggestions){
    var addressInput = document.querySelector('input[name=address]')
    var resultBlock = document.querySelector('.suggestions-result');
    var position = getBlockPosition(addressInput);
    resultBlock.style.left = position.left;
    resultBlock.style.top = position.top + 50 + 'px';
    resultBlock.innerHTML = '';
    suggestions.map(sugg => {
        var template = `<div class="sug-row" data-str='${sugg.value}'>${sugg.value}</div>`;
        resultBlock.innerHTML += template;
    })
    resultBlock.classList.remove('hidden');
}

function getBlockPosition(block){
    var rect = block.getBoundingClientRect();
    var position = {
        left: rect.left + window.scrollX,
        top: rect.top + window.scrollY
    }
    return position;
}

function insertAddressValue(event){
    var target = event.target;
    var targetValue = target.dataset.str;
    var addressInput = document.querySelector('input[name=address]');
    addressInput.value = targetValue;
    closeSuggestions();
}

function closeSuggestions(){
    var suggestionsBlock = document.querySelector('.suggestions-result');
    suggestionsBlock.classList.add('hidden');
}

async function calculateShipping(event){
    var addressInput = document.querySelector('input[name=address]');
    var typeShippingBtn = document.querySelector('input[name=shipping]:checked');
    var typeShippingCode = typeShippingBtn.id;
    var requestData = {'address': addressInput.value, 'shipping': typeShippingCode};
    var url = event.target.dataset.href;
    var responseData = await request('post', url, requestData);
    displayShippingPrice(responseData.price);
}

function displayShippingPrice(priceValue){
    var priceWrapper = document.querySelector('.price-value');
    var priceSpan = priceWrapper.querySelector('.value');
    priceSpan.innerHTML = priceValue + 'руб.';
    if(priceValue < 1000){
        priceWrapper.innerHTML = 'Стоимость доставки до дома: ';
        priceSpan.innerHTML = '1500 руб.';
        priceWrapper.appendChild(priceSpan);
        priceWrapper.classList.remove('hidden');
        return;
    }
    priceWrapper.innerHTML = 'Стоимость доставки: ';
    priceWrapper.appendChild(priceSpan);
    priceWrapper.classList.remove('hidden');
}

var shippingButtons = document.querySelectorAll('.radio-btn-shipping');
var paymentButtons = document.querySelectorAll('.radio-btn-payment');

console.log('joa')
shippingButtons.forEach(btn => {
    btn.addEventListener('click', function(event){
        changeState(shippingButtons);
        var addressBlock = document.querySelector('.address');
        if(event.target.classList.contains('calculate')){
            toggleVisibility(addressBlock, true);
            return
        }
        toggleVisibility(addressBlock, false);
    })
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

var addressInput = document.querySelector('input[name=address]');
if(addressInput){
    addressInput.addEventListener('change', getSuggestions);

}

var calcShippingBtn = document.querySelector('.calculate-shipping');
calcShippingBtn.addEventListener('click', function(event){
    calculateShipping(event);
})

$(document).on('click', '.sug-row', function(event){
    insertAddressValue(event);
})
