let username = document.getElementById('username').value;

(function () {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/${username}/reports/doughnut`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            let labels = response.labels;
            let data = response.data;
            let colors = response.colors;

    new Chart(document.getElementById("doughnut-chart"), {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderColor: "transparent"
            }]
        },
        options: {
            cutoutPercentage: 70,

        }
    });
    }
    };
    xhr.send();
})();