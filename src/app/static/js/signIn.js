const signInForm = document.getElementById('registerForm');
const submitBtn = document.getElementById('submitBtn');

submitBtn.addEventListener('click', async (event) => {
    event.preventDefault();

    const user = {
        username: signInForm.username.value,
        firstName: signInForm.firstName.value,
        lastName: signInForm.lastName.value,
        email: signInForm.email.value,
        passwd: signInForm.passwd.value,
        passwConfirmation: signInForm.passwConfirmation.value,
    }
    console.log(user)

    const response = await fetch('/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user),
    });

    console.log(await response.json())

    /*if (response.ok) {
       window.location.href = '/dashboard';
    } else {
      const errorData = await response.json();
      alert(errorData.detail);
    }*/
});