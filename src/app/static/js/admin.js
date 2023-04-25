const modal = document.querySelector('#confirm-delete-modal > .modal')

function deleteUser(id) {
    fetch('/users', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id}),
    }).then(() => {
        document.querySelector('#confirm-delete-modal .box').innerHTML = `User ${id} has been deleted`
        openModal()
    }).catch(() => {
        document.querySelector('#confirm-delete-modal .box').innerHTML = `User ${id} hasn't been deleted`
    })
}

function openModal() {
    modal.classList.add('is-active');
}

function closeModal($el) {
    modal.classList.remove('is-active');
}

// Add a click event on various child elements to close the parent modal
(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach((close) => {
    const target = close.closest('.modal');

    close.addEventListener('click', () => {
      closeModal(target);
    });
});