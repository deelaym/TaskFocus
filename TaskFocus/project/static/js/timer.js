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

let isRunning = false;

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
    let data = {
        hours: hours,
        minutes: minutes,
        seconds: seconds,
        startTime: startTime,
    };
        window.localStorage.setItem('time', JSON.stringify(data));

    timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

window.addEventListener('load', () => {
    isRunning = JSON.parse(window.localStorage.getItem('isRunning'));
    if (window.localStorage.getItem('time') !== null && isRunning['isRunning']) {
        let data = JSON.parse(window.localStorage.getItem('time'));

        hours = data['hours'];
        minutes = data['minutes'];
        seconds = data['seconds'];

        timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        go_on();
    }
});

window.addEventListener('beforeunload', () => {
    if (window.localStorage.getItem('isRunning')['isRunning']) {
        pause();
    }
});


start = () => {
    startTime = new Date();
    interval = setInterval(updateTime, 1000);
    startBtn.disabled = true;
    startBtn.style.display = 'none';
    pauseBtn.disabled = false;
    pauseBtn.style.display = 'inline';

    let data = {
        hours: hours,
        minutes: minutes,
        seconds: seconds,
        startTime: startTime,
    };
    window.localStorage.setItem('time', JSON.stringify(data));

    isRunning = {isRunning: true}
    window.localStorage.setItem('isRunning', JSON.stringify(isRunning));
};

go_on = () => {
    interval = setInterval(updateTime, 1000);
    startBtn.disabled = true;
    startBtn.style.display = 'none';
    pauseBtn.disabled = false;
    pauseBtn.style.display = 'inline';

    startTime = JSON.parse(window.localStorage.getItem('time'))['startTime'];
    let data = {
        hours: hours,
        minutes: minutes,
        seconds: seconds,
        startTime: startTime,
    };
    window.localStorage.setItem('time', JSON.stringify(data));

    isRunning = {isRunning: true}
    window.localStorage.setItem('isRunning', JSON.stringify(isRunning));
};

pause = () => {
    clearInterval(interval);
    startBtn.style.display = 'inline';
    pauseBtn.style.display = 'none'
};

stop = () => {
    clearInterval(interval);
    startBtn.disabled = false;
    startBtn.style.display = 'inline';
    pauseBtn.disabled = true;
    pauseBtn.style.display = 'none'
    stopTime = new Date();

    let data = JSON.parse(window.localStorage.getItem('time'));
    startTime = new Date(data['startTime'])
    let d1 = startTime.getDate();
    let m1 = startTime.getMonth() + 1;
    let y1 = startTime.getFullYear();
    let h1 = startTime.getHours();
    let min1 = startTime.getMinutes();
    let s1 = startTime.getSeconds();
    startTime = [d1, m1, y1, h1, min1, s1]

    let d2 = stopTime.getDate();
    let m2 = stopTime.getMonth() + 1;
    let y2 = stopTime.getFullYear();
    let h2 = stopTime.getHours();
    let min2 = stopTime.getMinutes();
    let s2 = stopTime.getSeconds();
    stopTime = [d2, m2, y2, h2, min2, s2]

    isRunning = {isRunning: false}
    window.localStorage.setItem('isRunning', JSON.stringify(isRunning));

    fetch(`/${username}/project/${slug}/timer/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({duration: [startTime, stopTime]})
        })
        .then(response => response.json())
        .then(duration => {
                console.log(duration);
        });

};

startBtn.addEventListener('click', start);
pauseBtn.addEventListener('click', stop);

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