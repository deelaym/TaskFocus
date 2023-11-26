const tasksListElement = document.querySelector('.drag-list');

tasksListElement.addEventListener('dragstart', (evt) => {
    evt.target.classList.add('selected');
})

tasksListElement.addEventListener('dragend', (evt) => {
    evt.target.classList.remove('selected');
});

tasksListElement.addEventListener('dragover', (evt) => {
    evt.preventDefault();

    const activeElement = tasksListElement.querySelector('.selected');
    const currentElement = evt.target;

    const isMoveable = activeElement !== currentElement && currentElement.classList.contains('drag-item');

    if (!isMoveable) {
        return;
    }
    const nextElement = getNextElement(evt.clientY, currentElement);

    if (nextElement && activeElement === nextElement.previousElementSibling || activeElement === nextElement) {
            return;
        }

    tasksListElement.insertBefore(activeElement, nextElement);
    let taskElements = tasksListElement.querySelectorAll('.task_id');
    let tasks_ids = [];

    taskElements.forEach(function(task) {
        tasks_ids.push(task.value);
    });


    fetch(`update_order/`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({tasks: tasks_ids})
    })
    .then(response => response.json())
    .then(data => {
            console.log(data.success);
    });
});

const getNextElement = (cursorPosition, currentElement) => {
    const currentElementCoord = currentElement.getBoundingClientRect();
    const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;

    const nextElement = (cursorPosition < currentElementCenter)
        ? currentElement : currentElement.nextElementSibling;
    return nextElement;
}






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