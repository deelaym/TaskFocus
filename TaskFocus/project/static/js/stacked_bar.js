let username1 = document.getElementById('username1').value;

(function () {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/${username1}/reports/stacked_bar/`, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            let months = response.months;
            let labels = response.labels;
            let data = response.data;
            let colors = response.colors;
            let datasets = []
            for (let i = 0; i < labels.length; i++) {
                 datasets.push({
                    label: labels[i],
                    data: data[i],
                    backgroundColor: colors[i],
                });

            }


    new Chart(document.getElementById("stacked-bar"), {
        type: "bar",
        data: {
            labels: months,
            datasets: datasets,
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
                }
            }

    });
    }
    }
    xhr.send();
})();