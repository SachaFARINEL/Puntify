function addSourceToAudio(id) {
    const audio = document.querySelector('audio')
    audio.load()
    audio.innerHTML = `<source src=${`/tracks/${id}`}>`
    audio.play()
}