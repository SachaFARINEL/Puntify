function changeFavorite(div, id) {
    const isFavorite = div.dataset.isFavorite

    let action = isFavorite === 'true' ? {action: "remove"} : {action: "add"}

    fetch(`/tracks/${id}/favorite`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(action)
    }).then(response => {
        changeIcon(isFavorite, div)
    }).catch(error => {

    })
}

function changeIcon(isFavorite, div) {
    if (isFavorite) {
        div.classList.remove('fa-solid')
        div.classList.add('fa-regular')
    } else {
        div.classList.remove('fa-regular')
        div.classList.add('fa-solid')
    }
}