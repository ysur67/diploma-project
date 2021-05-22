function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendSearchString(event){
    document.addEventListener('scroll', closeSearchResult)
    var target = event.target;
    var value = target.value;
    var form = target.closest('form')
    var url = form.getAttribute('action');
    console.log(value)
    $.ajax({
        method: 'POST',
        url: url,
        data: {search: value, csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(data){
            var resultBlock = form.querySelector('.search-result');
            var rect = target.getBoundingClientRect();
            var position = {
                left: rect.left + window.scrollX,
                top: rect.top + window.scrollY
            }
            resultBlock.style.left = position.left;
            resultBlock.style.top = position.top + 500;
            resultBlock.style.display = 'block';
            var resultList = resultBlock.querySelector('.result-list');
            resultList.innerHTML = data['template'];
        },
        error: function(error) {
            console.log(error);
        }
    })
}

function closeSearchResult(){
    var form = document.querySelector('#searchForm');
    var searchResult = form.querySelector('.search-result')
    searchResult.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function(event){
    var searchFields = document.getElementsByName('search');
    if(searchFields){
        searchFields.forEach(field => {
            field.addEventListener('input', sendSearchString);
            // body.addEventListener('click')
            // field.addEventListener('focusout', closeSearchResult)
        })
    }
    document.querySelector('#searchForm').addEventListener('submit', function(event) {
        event.preventDefault()
        var target = event.target;
        var url = target.dataset.href;
        window.location.href = url;
    })
})
