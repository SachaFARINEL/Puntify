function changeFavorite(div, id) {
    let {isFavorite} = div.dataset

    let action = isFavorite === 'true' ? {action: "remove"} : {action: "add"}

    fetch(`/tracks/${id}/favorite`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(action)
    }).then(() => {
        div.dataset.isFavorite = isFavorite === 'true' ? "false" : "true"
        changeIcon(div.dataset.isFavorite, div)
    }).catch(error => {

    })
}

function changeIcon(isFavorite, div) {
    if (isFavorite === "true") {
        div.classList.remove('fa-regular')
        div.classList.add('fa-solid')
    } else {
        console.log('false')
        div.classList.remove('fa-solid')
        div.classList.add('fa-regular')
    }
}