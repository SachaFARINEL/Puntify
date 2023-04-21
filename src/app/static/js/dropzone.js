const dropZone = document.getElementById('dropZone');
const coverZone = document.getElementById('coverZone');
const error = document.getElementById('error');
const iconDropZone = document.getElementById('iconDropZone');
let track = null;

function preventDefaultBehavior(event) {
    event.preventDefault();
    event.stopPropagation();
}

function addDragOverClass(event) {
    preventDefaultBehavior(event);
    this.classList.add('dragover');
}

function removeDragOverClass(event) {
    preventDefaultBehavior(event);
    this.classList.remove('dragover');
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

dropZone.addEventListener('dragover', addDragOverClass);
dropZone.addEventListener('dragleave', removeDragOverClass);
dropZone.addEventListener('drop', handleDropZone);
dropZone.addEventListener('click', handleDropClick);

coverZone.addEventListener('dragover', addDragOverClass);
coverZone.addEventListener('dragleave', removeDragOverClass);
/*coverZone.addEventListener('drop', handleDrop);*/

/*coverZone.addEventListener('click', handleClick);*/

async function processSelectedAudioFile(file) {
    if (isAudioFile(file)) {
        removeError()
        replaceIconClasses(iconDropZone, "fa-file-arrow-up", "fa-check", "fa-bounce");
        changeIconColor(iconDropZone, "#1f5120");
        setInputValue('input[name="fileName"]', file.name);
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch('/tracks/getDuration', {
            method: 'POST',
            body: formData,
        });
        let duration = await response.json()
        setInputValue('input[name="trackDuration"]', formatDuration(duration));
        setInputValue('input[name="duration"]', duration)
        track = file
    } else {
        let value = 'Only audio files (mp3, wav, ogg) are allowed.'
        handleError(value)
    }
}

function handleError(value) {
    console.log(track)
    error.textContent = value;
    error.classList.remove('is-invisible');
    replaceIconClasses(iconDropZone, "fa-file-arrow-up", "fa-xmark", "fa-beat");
    changeIconColor(iconDropZone, "#d42121");
    setTimeout(() => {
        iconDropZone.classList.remove("fa-xmark", "fa-beat")
        iconDropZone.classList.add('fa-solid', 'fa-file-arrow-up', 'fa-2xl')
        changeIconColor(iconDropZone, "");
    }, 5000);
}

function removeError() {
    error.textContent = '';
    error.classList.add('is-invisible');
}

function isAudioFile(file) {
    const fileExtension = file.name.split('.').pop();
    return fileExtension === 'mp3' || fileExtension === 'wav' || fileExtension === 'ogg';
}

function replaceIconClasses(element, classToRemove, classToAdd, classToAdd2 = null) {
    element.classList.replace(classToRemove, classToAdd);
    if (classToAdd2) {
        element.classList.add(classToAdd2);
    }
}

function changeIconColor(element, color) {
    element.style.color = color;
}

function setInputValue(selector, value) {
    document.querySelector(selector).value = value;
}

function formatDuration(totalSeconds) {
    let hours = Math.floor(totalSeconds / 3600);
    let minutes = Math.floor((totalSeconds % 3600) / 60);
    let seconds = Math.floor(totalSeconds % 60);

    let formattedHours = hours < 10 ? "0" + hours : hours;
    let formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
    let formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

    return formattedHours + ":" + formattedMinutes + ":" + formattedSeconds;
}

