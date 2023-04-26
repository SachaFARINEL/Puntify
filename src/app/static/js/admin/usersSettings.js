
const updateFlag = async (id, flagStatus) => {
    flagStatus = flagStatus === 'True'

    console.log('clicked')
    fetch('/users', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id, flagStatus}),
    }).then(() => {
        location.reload()
    }).catch(() => {
    })
}

function deleteUser(id) {
    fetch('/users', {
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