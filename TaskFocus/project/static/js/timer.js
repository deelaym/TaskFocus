let initialTotalTime = document.getElementById('totalTime').value;
let timer = document.getElementById('timer');
let startBtn = document.getElementById('startBtn');
let pauseBtn = document.getElementById('pauseBtn');

let totalTime = initialTotalTime.replace(',', ':').split(':');
let days;
let hours;
let minutes;
let seconds;

if (totalTime.length === 4) {
    days = parseInt(totalTime[0]);
    hours = parseInt(totalTime[1]) + days * 24;
    minutes = parseInt(totalTime[2]);
    seconds = parseInt(totalTime[3]);
} else {
    hours = parseInt(totalTime[0]);
    minutes = parseInt(totalTime[1]);
    seconds = parseInt(totalTime[2]);
};

let current_time;

let interval;

function updateTime() {
    seconds++;
    if (seconds === 60) {
        minutes++;
        seconds = 0;
    }
    if (minutes === 60) {
        hours++;
        minutes = 0;
    }

    timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

startBtn.addEventListener('click', () => {
    interval = setInterval(updateTime, 1000);
    startBtn.disabled = true;
    pauseBtn.disabled = false;
});

pauseBtn.addEventListener('click', () => {
    clearInterval(interval);
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    current_time = timer.textContent;

    fetch('timer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(current_time)
        })
        .then(response => response.json())
        .then(current_time => {
                console.log(current_time);
        });

});


function getCookie(name) {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
    return cookieValue;
}