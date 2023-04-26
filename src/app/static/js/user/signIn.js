import {updateComponent} from '../utils/utils.js';

const signInForm = document.getElementById('registerForm');
const submitBtn = document.getElementById('submitBtn');
const error = document.getElementById('error');

submitBtn.addEventListener('click', async (event) => {
    event.preventDefault();

    const user = {
        firstName: signInForm.firstName.value,
        lastName: signInForm.lastName.value,
        email: signInForm.email.value,
        passwd: signInForm.passwd.value,
        passwConfirmation: signInForm.passwConfirmation.value,
    }

    fetch('/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user),
        redirect: 'follow'
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url
        } else if (!response.ok) {
            response.text().then(errorMessage => {
                const errorObject = JSON.parse(errorMessage);
                updateComponent(error, ['error', 'is-visible'], errorObject.detail);
            });
        }
    })


});