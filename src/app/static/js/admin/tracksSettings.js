function deleteTrack(id) {
    fetch('/tracks', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id}),
    }).then(() => {
        location.reload()
    }).catch(() => {
    })
}