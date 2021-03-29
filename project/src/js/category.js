import request from './components/tools.js';

function sendAjax(){
    var filterSet = document.getElementById('filtering');
    return request('post', window.location.href, {})
    .then((response) => {
        var attributes = response['attributes'];
        console.log({attributes})
        attributes.forEach(attribute =>{
            function setAttributes(attribute){
                let values = attribute.values;
                let result = ``
                values.forEach(value => {
                    result += `<div class='value-item'><label class='value-item'>
                        <input type="checkbox" name="value" value='${value.id_1c}'>${value.value}</label>
                        </div>`
                })
                return result
            }
            filterSet.innerHTML += `<div class='filter-value'>
                <span class='value-title'>${attribute.title}</span>
                <div class='values-list'>${setAttributes(attribute)}`
        })
        filterSet.innerHTML += `<div class='filter-controls'>
        <button type="submit" class='filter-button submit sn-filters'>Показать</button>
        <button type="reset" class='filter-button cancel'>Сбросить</button></div>`
    })
}

function changeDisplay(event){
    var panel = event.target.nextElementSibling;
    panel.classList.toggle('active');
    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
    }
}

function submitFilters(event){
    event.preventDefault();
    var form = event.target.closest('form')
    var data = new FormData(form)
    request('post', window.location.href, data)
}

window.addEventListener("DOMContentLoaded", function() {
    sendAjax()
        .then(() =>{
                var fitlerTitles = document.querySelectorAll('.value-title');
                fitlerTitles.forEach(title =>{
                    title.addEventListener('click', function(event){
                        changeDisplay(event)
                    })
                })
            }
        )
        .then(() => {
            var snButtons = document.querySelectorAll('.sn-filters')
            snButtons.forEach(btn => {
                btn.addEventListener('click', submitFilters)
            })
        })
});

