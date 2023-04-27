import Modal from "../utils/Modal.js";
export {deleteTrack, initUpdateButton, openTrackUpdateModel,initDeleteButton}

const initDeleteButton = () => {
    document.querySelectorAll('.delete-track').forEach(element => {
        element.addEventListener('click', () => deleteTrack(element.children[0].dataset.trackId))
    })
}
const initUpdateButton = () => {
    document.querySelectorAll('.update-track').forEach(element => {
        element.addEventListener('click', () => openTrackUpdateModel(element.children[0].dataset.trackId))
    })
}

const trackUpdateModal = document.getElementById('track-update-modal')
function deleteTrack(id) {
    fetch('/tracks', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id}),
    }).then(() => {
        location.reload()
    }).catch(err => {
        console.error(err)
    })
}

function openTrackUpdateModel(id) {
    fetch(`/tracks/${id}/modal`, {
        method: 'GET',
        headers: {
            'Content-Type': 'text/html'
        }
    }).then(response => {
        response.text().then(html => {
            trackUpdateModal.innerHTML = html
            const modal = new Modal(document.querySelector('#track-update-modal  .modal'))
            document.getElementById('update-track-form').addEventListener('submit', e => {
                e.preventDefault()
                const cover = document.querySelector('.modal input[name=cover]').value
                const trackName = document.querySelector('.modal input[name=trackName]').value
                const fileName = document.querySelector('.modal input[name=fileName]').value
                const artistName = document.querySelector('.modal input[name=artistName]').value
                const track = {
                    cover,
                    trackName,
                    fileName,
                    artistName
                }
                fetch(`/tracks/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(track)
                }).then(response => {
                    response.text().then(result => {
                        modal.closeModal()
                        modal.modal.remove()
                        location.reload()
                    })
                }).catch(err => {
                    console.error(err)
                })
            })
        })
    }).catch(err => {
        console.error(err)
    })
}

function updateTrack() {

}