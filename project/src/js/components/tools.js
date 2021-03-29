export default async function request(method, url, data) {
    let response;
    const CSRF_TOKEN = getCookie('csrftoken');
    if (method.toUpperCase() === 'GET') {
        if (!data instanceof String) {
            data = new URLSearchParams(data).toString();
        }
        response = await fetch(url + '?' + data, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': CSRF_TOKEN
            }
        });
    } else if (method.toUpperCase() === 'POST') {
        data = new URLSearchParams(data);
        let form_data = new FormData();
        for (const [title, value] of data.entries()){
            form_data.set(title, value)
        }
        response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: form_data
        });
    }
    return await response.json();
}

export function getCookie(name) {
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
