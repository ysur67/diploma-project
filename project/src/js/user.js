import request from './components/tools.js';


function submitForm(event){
    event.preventDefault();
    var form = event.target.closest('form');
    var data = new FormData(form);
    request('post', window.location.href, data)
    .then(response=>{
        if(response.errors == true){
            var errors = response.fields;
            for(var error in errors){
                var field = document.getElementById("id_" + error);
                field.classList.add('error');
            } 
            var userMessage = document.querySelector('.display-errors');
            if(response.message != '' || response.message != null){
                userMessage.innerHTML = response.message;
            }else{
                userMessage.innerHTML = 'Проверьте выделенные поля!'
            }
            userMessage.style.opacity = 1;
        }
        else{
            window.location.href = response.redirect
        }
    })
}

var snButtons = document.querySelectorAll('.sn-form')
snButtons.forEach(button => {
    button.addEventListener('click', submitForm)
})
