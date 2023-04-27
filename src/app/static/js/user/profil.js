import {preventDefaultBehavior, updateComponent} from '../utils/utils.js'

const inputFirstName = document.querySelector('input[name="firstName"]')
const inputLastName = document.querySelector('input[name="lastName"]')
const inputPasswd = document.querySelector('input[name="passwd"]')
const inputPasswConfirmation = document.querySelector('input[name="passwConfirmation"]')

const buttonSubmit = document.getElementById('submitBtn')
const error = document.getElementById('error');

const canSubmit = () => {
    return inputFirstName.value !== '' && inputLastName.value !== ''
}

const arePasswordsIdentical = () => {
    return inputPasswd.value === inputPasswConfirmation.value
}

const arePasswordsFilled = () => {
    return inputPasswd.value !== '' && inputPasswConfirmation.value !== ''
}

buttonSubmit.addEventListener('click', (event) => {
    preventDefaultBehavior(event)
    if (canSubmit()) {
        updateComponent(error, ['is-invisible'])
        let user = {
            'firstName': inputFirstName.value,
            'lastName': inputLastName.value,

        }
        if (arePasswordsIdentical() && arePasswordsFilled()) {
            console.log('add pass')
            user.passwd = inputPasswd.value
            user.passwConfirmation = inputPasswConfirmation.value
        } else if (!arePasswordsFilled() && !arePasswordsIdentical()) {
            console.log('mdp vide')
            updateComponent(error, ['error'], 'Passwords are not identical')
            return
        }

        fetch('/users/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user),
        }).then(() => location.reload())
    } else {
        updateComponent(error, ['error'], 'Please complete at least Firstname, lastname & email')
    }
})
