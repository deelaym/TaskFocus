let initialTotalTime = document.getElementById('totalTime').value;
let timer = document.getElementById('timer');
let startBtn = document.getElementById('startBtn');
let pauseBtn = document.getElementById('pauseBtn');
let slug = document.getElementById('slug').value;
let username = document.getElementById('username').value;

let totalTime = initialTotalTime.replace(',', ':').split(':');
let days;
let hours;
let minutes;
let seconds;

let startTime;
let stopTime;

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
    startTime = new Date();
    interval = setInterval(updateTime, 1000);
    startBtn.disabled = true;
    startBtn.style.display = 'none';
    pauseBtn.disabled = false;
    pauseBtn.style.display = 'inline';

    let d = startTime.getDate();
    let m = startTime.getMonth() + 1;
    let y = startTime.getFullYear();
    let h = startTime.getHours();
    let min = startTime.getMinutes();
    let s = startTime.getSeconds();
    startTime = [d, m, y, h, min, s]
});

pauseBtn.addEventListener('click', () => {
    clearInterval(interval);
    startBtn.disabled = false;
    startBtn.style.display = 'inline';
    pauseBtn.disabled = true;
    pauseBtn.style.display = 'none'
    current_time = timer.textContent;
    stopTime = new Date();

    let d = stopTime.getDate();
    let m = stopTime.getMonth() + 1;
    let y = stopTime.getFullYear();
    let h = stopTime.getHours();
    let min = stopTime.getMinutes();
    let s = stopTime.getSeconds();
    stopTime = [d, m, y, h, min, s]


    fetch(`/${username}/project/${slug}/timer/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({current_time: current_time, duration: [startTime, stopTime]})
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