

export function displayErrors(form, fields) {
    for (const key in fields) {
        if (fields.hasOwnProperty(key)) {
            const control = form.querySelector('[name="' + key + '"]')
            const group = control.parentElement;
            let feedback = group.querySelector('.error');
            control.classList.add("is-invalid")
            feedback.classList.add("is-invalid")
            feedback.innerHTML = fields[key]
        }
    }
}

export function clearErrors(form) {
    var fields = form.querySelectorAll('.is-invalid');

    if(!fields)
        return

    fields.forEach(field => {
        field.classList.remove('is-invalid');
    })
}
