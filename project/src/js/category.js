import request from './components/tools.js';


function changeDisplay(event){
    var panel = event.target.nextElementSibling;
    panel.classList.toggle('active');
    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
    }
}

function replaceCatalogData(event, data) {
    replaceFilters(data['template_filters']);
    replacePagination(data['pagination']);
    replaceProductList(data['products']);
}

function replaceProductList(data) {
    $('.products-content__list').html(data);
}

function replaceFilters(data) {
    $('#filtering').replaceWith(data);
}

function replacePagination(data) {
    $('.pagination').html(data);
}

function submitFilters(event, updatePagin=false){
    event.preventDefault();
    var form = $(event.target)
    var data = form.serialize();
    $.ajax({
        url: window.location.href,
        type: 'GET',
        dataType: 'json',
        data: data,
        success: function (data) {
            replaceProductList(data['products']);
            if(updatePagin)
                replacePagination(data['pagination']);
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function changePage(event) {
    event.preventDefault();
    var target = event.target;
    var page = target.dataset.href;
    var form = $('#sn-filter');
    var formData = form.serialize();
    var requestData = formData + `&page=${page}`;
    $.ajax({
        url: window.location.href,
        type: 'GET',
        dataType: 'json',
        data: requestData,
        success: function(data) {
            replacePagination(data['pagination']);
            replaceProductList(data['products']);
        },
        error: function(error) {
            console.log(error);
        }
    })
}

function updateCatalog(event, page=null) {
    let requestData = {}
    if(page)
        requestData.page = page;
    $.ajax({
        url: window.location.pathname,
        type: 'GET',
        dataType: 'json',
        data: {page: page},
        success: function (data) {
            replaceCatalogData(event, data);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function submitDisplay(event, page=null){
    event.preventDefault();
    var target = event.target;
    var value = target.value;
    var form = $('#sn-filter');
    var formData = $(form).serialize();
    if(page){
        formData = formData + `&page=${page}`;
    }
    formData = formData + `&display_type=${value}`;
    console.log(formData)
    $.ajax({
        url: window.location.href,
        type: 'GET',
        dataType: 'json',
        data: formData,
        success: function (data) {
            replaceProductList(data['products']);
            var productListWrapper = document.querySelector('.products-content__list');
            if(data['display_tile']){
                productListWrapper.classList.remove('column');
                productListWrapper.classList.add('row');
                var button = document.querySelector('.wide');
                button.classList.remove('active');
                button = document.querySelector('.tile');
                button.classList.add('active')
                return
            }
            productListWrapper.classList.remove('row');
            productListWrapper.classList.add('column');
            var button = document.querySelector('.tile');
            button.classList.remove('active');
            button = document.querySelector('.wide');
            button.classList.add('active');

        },
        error: function (error) {
            console.log(error);
        }
    })

    
}

window.addEventListener("DOMContentLoaded", function() {
    updateCatalog();
    $('body').on('click', '.value-title', function(event) {
        changeDisplay(event);
    });
    $('body').on('submit', '#sn-filter', function(event){
        submitFilters(event, true);
    });
    $('body').on('reset', '#sn-filter', function(event){
        var pageElement = document.querySelector('#current-page');
        var page = null;
        if(pageElement)
            page = pageElement.dataset.href;
        updateCatalog(event, page);
    });
    $('body').on('click', '.active-page', function(event) {
        changePage(event);
    })
    var displayBtns = document.querySelectorAll('.display-btn');
    if(displayBtns){
        displayBtns.forEach(btn => {
            btn.addEventListener('click', function(event){
                var pageElement = document.querySelector('#current-page');
                var page = null;
                if(pageElement)
                    page = pageElement.dataset.href;
                submitDisplay(event, page);
            })
        })
    }
    
});

console.log('ass')