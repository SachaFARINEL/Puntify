export function updateComponent(element, classesToAdd = [], message = null) {
    element.className = ''
    element.classList.add(...classesToAdd)
    if (message) {
        element.textContent = message
    }
}

export function isAudioFile(file) {
    const fileExtension = file.name.split('.').pop();
    return fileExtension === 'mp3' || fileExtension === 'wav' || fileExtension === 'ogg';
}

export function changeIconColor(element, color) {
    element.style.color = color;
}

export function formatDuration(totalSeconds) {
    let hours = Math.floor(totalSeconds / 3600);
    let minutes = Math.floor((totalSeconds % 3600) / 60);
    let seconds = Math.floor(totalSeconds % 60);

    let formattedHours = hours < 10 ? "0" + hours : hours;
    let formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
    let formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

    if (formattedHours === "00") {
        return formattedMinutes + ":" + formattedSeconds;
    } else {
        return formattedHours + ":" + formattedMinutes + ":" + formattedSeconds;
    }
}

export function preventDefaultBehavior(event) {
    event.preventDefault();
    event.stopPropagation();
}