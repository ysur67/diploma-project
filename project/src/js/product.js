
// import request from './components/tools.js';
// import { displayErrors, clearErrors } from './components/form.js';

// async function submitProduct(event){
//     event.preventDefault();
//     const form = event.target;
//     const url = form.action;
//     const data = new FormData(form)
//     clearErrors(form);
//     var response_data = await request('post', url, data);
//     if(response_data.errors){
//         displayErrors(form, response_data.fields)
//         return
//     }

//     if(response_data.message){
//         console.log(response_data.message)
//     }
    
// }

// var productForm = document.querySelector('.product-form')
// if(productForm){
//     productForm.addEventListener('submit', submitProduct)
// }
