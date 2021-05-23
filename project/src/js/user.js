import request from './components/tools.js';
import { displayErrors, clearErrors} from './components/form.js';


async function submitForm(event) {
    event.preventDefault();
    var form = event.target.closest('form');
    clearErrors(form)
    var data = new FormData(form);
    var response = await request('post', window.location.href, data)
    console.log(response)
    if(response.errors){
        displayErrors(form, response.fields)
        return
    }

    if(response.redirect)
        window.location.href = response.redirect;

    displaySuccess()

    if(response.username){
        var username = document.querySelector("#username");
        username.innerHTML = response.username;
    }
}

function displaySuccess() {
    var elem = document.querySelector('.success-note');
    elem.style.padding = '10px';
    elem.style.border = '1px';
    elem.style.maxHeight = '50px';
    elem.style.opacity = '100';
    setTimeout(function(){
        elem.style.padding = '0px';
        elem.style.border = '0px';
        elem.style.maxHeight = '0px';
        elem.style.opacity = '0';
    }, 2500)
}

function toggleOrderInfo(event){
    var target = event.target;
    var info = target.querySelector('.info');
    var state = info.classList.contains('active');
    var maxheight = state ? '0px' : '1000px'
    info.style.maxHeight = maxheight;
    info.classList.toggle('active');

}

var snButtons = document.querySelectorAll('.sn-form')
snButtons.forEach(button => {
    button.addEventListener('click', submitForm)
})

var orders = document.querySelectorAll('.order-row');
orders.forEach(button => {
    button.addEventListener('click', toggleOrderInfo)
})
