/**
 * L'état de la piste audio.
 * @type {Track}
 */
let currentSong = null;

let playerButtonIsEnabled = false

const playerButtons = document.querySelectorAll('.player-button')
playerButtons.forEach(playerButton => {
    playerButton.addEventListener('click', (e) => {
        if(!playerButtonIsEnabled) enablePlayerButton()
        const {trackId, trackDuration, trackName, trackArtist} = e.target.dataset
        if(currentSong) {
            currentSong.changeTrack(trackId, trackDuration)
        } else {
            currentSong = new Track(trackId, trackDuration)
        }
        document.getElementById('track-metadata').innerText = `${trackName} - ${trackArtist}`
    })
})

document.getElementById('play-pause-button').addEventListener('click', ({target}) => {
    currentSong.switchPlayPause()
    switchPlayPauseIcon()
})

const switchPlayPauseIcon = () => {
    const playStopButtonIcon = document.getElementById('play-pause-button-icon')
    if(currentSong.state === 'play') {
        playStopButtonIcon.classList.remove('fa-play')
        playStopButtonIcon.classList.add('fa-pause')
    } else {
        playStopButtonIcon.classList.remove('fa-pause')
        playStopButtonIcon.classList.add('fa-play')
    }
}

document.getElementById('stop-button').addEventListener('click', () => {
    currentSong.stop()
})

const enablePlayerButton = () => {
    document.getElementById('stop-button').disabled = false
    document.getElementById('play-pause-button').disabled = false

    const playStopButtonIcon = document.getElementById('play-pause-button-icon')
    playStopButtonIcon.classList.remove('fa-play')
    playStopButtonIcon.classList.add('fa-pause')

    playerButtonIsEnabled = true
}

/**
 * Représente une piste audio.
 * @class
 */
class Track {
    /**
     * L'état de la piste audio.
     * @type {Object}
     */
    #state = 'play'

    /**
     * L'élément audio HTML de la piste audio.
     * @type {HTMLAudioElement}
     */
    #track

    /**
     * L'élément audio HTML de la piste audio.
     * @type {number}
     */
    #duration

    /**
     * ID de l'interval qui refraichit la barre de progression
     * @type {number}
     */
    #progressBarInterval

    /**
     * Crée une instance de la classe Track.
     * @constructor
     * @param {string} idTrack - L'identifiant de la piste audio.
     * @param {string} duration - La durée de la musique
     */
    constructor(idTrack, duration) {
        this.#track = new Audio(`/tracks/${idTrack}`)
        const [minutes, seconds] = duration.split(':').map(part => parseInt(part))
        this.#duration = minutes * 60 + seconds
        this.#initEventListener()
    }

    #initEventListener() {
        this.#track.addEventListener('loadeddata', () => {
            this.play()
        })
        this.#track.addEventListener('pause', () => {
            clearInterval(this.#progressBarInterval)
        })
        this.#track.addEventListener('play', () => {
            this.#startProgressBar()
        })
    }

    /**
     * Démarre la lecture de la piste audio.
     */
    play() {
        this.#track.play().then(() => {})
    }

    /**
     * Initialise la barre de progression
     */
    #startProgressBar(){
        const refreshBar = () => {
            const percent = Math.round(((this.#track.currentTime / this.#duration) * 100) * 10) / 10
            const progressBar = document.getElementById('track-progress-bar')
            progressBar.value = percent
            progressBar.innerText = `${percent}%`
            if(percent >= 100) {
                this.stop()
                clearInterval(this.#progressBarInterval)
            }
        }
        this.#progressBarInterval = setInterval(refreshBar, 1000)
    }

    /**
     * Met en pause la lecture de la piste audio.
     */
    pause() {
        this.#track.pause()
    }

    /**
     * Stop la lecture de la piste audio.
     */
    stop() {
        this.#state = 'pause'
        this.pause()

        const playStopButtonIcon = document.getElementById('play-pause-button-icon')
        playStopButtonIcon.classList.remove('fa-pause')
        playStopButtonIcon.classList.add('fa-play')
    }

    switchPlayPause() {
        if (this.#state === 'play') {
            this.#state = 'pause'
            this.pause()
        } else if (this.#state === 'pause') {
            this.#state = 'play'
            this.play()
        } else {
            console.error('error on track state')
        }
    }

    get state () {
        return this.#state
    }

    changeTrack(id, duration) {
        this.#track.src = `/tracks/${id}`
        const [minutes, seconds] = duration.split(':').map(part => parseInt(part))
        this.#duration = minutes * 60 + seconds
        this.#track.load()
    }
}