export default class Modal {
    constructor(modal) {
        this.modal = modal
        this.initEventListener()
        this.openModal()
    }
    openModal() {
        this.modal.classList.add('is-active');
    }

    closeModal() {
        this.modal.classList.remove('is-active');
    }

    initEventListener() {
        // Add a click event on various child elements to close the parent modal
        (this.modal.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(close => {
            const $target = close.closest('.modal');

            close.addEventListener('click', () => {
              this.closeModal($target);
            });
        });
    }



}

