import {changeIconColor, formatDuration, isAudioFile, updateComponent, preventDefaultBehavior} from "../utils/utils.js";

const dropZone = document.getElementById('dropZone');
const error = document.getElementById('error');
const iconDropZone = document.getElementById('iconDropZone');
const submitButton = document.getElementById('submitButton');
const coverFM = document.getElementById('coverFM');

let fileName = document.querySelector('input[name="fileName"]')
let musicTitle = document.querySelector('input[name="musicTitle"]')
let artistName = document.querySelector('input[name="artistName"]')
let trackDuration = document.querySelector('input[name="trackDuration"]')
let duration = document.querySelector('input[name="duration"]')
let imgElementUrl = null
let mp3 = null
let tags = null

dropZone.addEventListener('dragover', addDragOverClass);
dropZone.addEventListener('dragleave', removeDragOverClass);
dropZone.addEventListener('drop', handleDropZone);
dropZone.addEventListener('click', handleDropClick);

submitButton.addEventListener('click', handleSubmit);

coverFM.addEventListener('click', getCoverAndTags);

async function handleSubmit(event) {
    preventDefaultBehavior(event);
    if (canSubmit()) {
        const formData = new FormData();
        formData.append('file', mp3);
        formData.append('fileName', fileName.value);
        formData.append('trackName', musicTitle.value.charAt(0).toUpperCase() + musicTitle.value.slice(1));
        formData.append('artistName', artistName.value.charAt(0).toUpperCase() + artistName.value.slice(1));
        formData.append('duration', duration.value);
        formData.append('cover', imgElementUrl);
        formData.append('tags', tags);

        const response = await fetch("/tracks/add", {
            method: "POST",
            body: formData
        });

        const message = await response.text();
        if (response.ok) {
            resetInput()
            updateComponent(error, ['successful'], message,)
            updateComponent(iconDropZone, ['fa-solid', 'fa-file-arrow-up', 'fa-2xl'])
            changeIconColor(iconDropZone, "");
            resetCoverFM()
        } else {
            handleDropError(message)
        }
    } else {
        updateComponent(error, ['error'], 'Please complete all fields (include cover image)')
    }
}

async function getCoverAndTags() {
    if (musicTitle.value !== '' && artistName.value !== '') {
        updateComponent(error, ['is-invisible'])
        let apiKey = '6b690048ba5bd85baa1563b8c8048a8f'
        let artist = artistName.value
        let track = musicTitle.value
        let lastFMUrl = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=' + apiKey + '&artist=' + artist + '&track=' + track + '&format=json'
        const response = await fetch(lastFMUrl, {
            method: 'GET'
        }).then(response => response.json())

        if (response?.track?.album?.image[3]) {
            const coverUrl = response.track.album.image[3]['#text']
            coverFM.innerHTML = `<img src="${coverUrl}" alt="Cover Image">`;
        } else {
            const shadowImg = 'https://t4.ftcdn.net/jpg/05/14/20/15/360_F_514201525_bdJOhRiJjHOwPc7I0Dg3VFxSsI0FHoOq.jpg'
            coverFM.innerHTML = `<img src="${shadowImg}" alt="No image">`;
            updateComponent(error, ['information'], 'Track not found')
        }
        imgElementUrl = document.querySelector('#coverFM img').src;

        if (response?.track?.toptags?.tag) {

            let tagsList = []
            for (let i = 0; i < response.track.toptags.tag.length; i++) {
                tagsList.push(response.track.toptags.tag[i].name)
            }
            tags = tagsList
        }

    } else {
        resetCoverFM()
        updateComponent(error, ['error'], 'Please complete artist and track name fields')
    }
}

async function processSelectedAudioFile(file) {
    if (isAudioFile(file)) {
        updateComponent(error, ['is-invisible'])
        updateComponent(iconDropZone, ['fa-solid', 'fa-check', 'fa-bounce', 'fa-2xl'])
        changeIconColor(iconDropZone, "#1f5120");

        fileName.value = file.name;
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/tracks/getDuration', {
            method: 'POST',
            body: formData,
        });

        let responseDuration = await response.json()
        trackDuration.value = formatDuration(responseDuration)
        duration.value = responseDuration
        mp3 = file
    } else {
        let value = 'Only audio files (mp3, wav, ogg) are allowed.'
        handleDropError(value)
    }
}

async function handleDropZone(event) {
    preventDefaultBehavior(event);
    const file = event.dataTransfer.files[0];
    if (file) {
        await processSelectedAudioFile(file)
    }
}

async function handleDropClick(event) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'audio/*';

    fileInput.addEventListener('change', async () => {
        const file = fileInput.files[0];
        if (file) {
            await processSelectedAudioFile(file)
        }
    });
    fileInput.click();
}

function handleDropError(value) {
    mp3 = null
    resetInput()
    updateComponent(error, ['error'], value)
    updateComponent(iconDropZone, ['fa-solid', 'fa-xmark', 'fa-2xl', 'fa-beat'])
    changeIconColor(iconDropZone, "#d42121");

    setTimeout(() => {
        iconDropZone.classList.remove("fa-xmark", "fa-beat")
        iconDropZone.classList.add('fa-solid', 'fa-file-arrow-up', 'fa-2xl')
        changeIconColor(iconDropZone, "");
    }, 1000);
}

function resetCoverFM() {
    coverFM.innerHTML = '<span class="icon is-large"><i class="fa-solid fa-hand-point-up fa-2xl"></i></span>'
    imgElementUrl = null
}

function addDragOverClass(event) {
    preventDefaultBehavior(event);
    this.classList.add('dragover');
}

function removeDragOverClass(event) {
    preventDefaultBehavior(event);
    this.classList.remove('dragover');
}

function canSubmit() {
    return fileName.value !== '' &&
        musicTitle.value !== '' &&
        artistName.value !== '' &&
        trackDuration.value !== '' &&
        duration.value !== '' &&
        imgElementUrl &&
        mp3 !== null;
}

function resetInput() {
    fileName.value = ''
    musicTitle.value = ''
    artistName.value = ''
    trackDuration.value = ''
    duration.value = ''
}