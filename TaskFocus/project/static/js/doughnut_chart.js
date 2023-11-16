let username = document.getElementById('username').value;
let hours = parseFloat(document.getElementById('total_hours').value);

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
    Chart.pluginService.register({
      beforeDraw: function(chart) {
        var width = chart.chart.width,
            height = chart.chart.height,
            ctx = chart.chart.ctx;

        ctx.restore();
        var fontSize = (height / 112).toFixed(2);
        ctx.font = fontSize + "em sans-serif";
        ctx.textBaseline = "middle";

        var text = `${hours}h`,
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = height / 1.8;

        ctx.fillText(text, textX, textY);
        ctx.save();
      }
    });
    }
    };
    xhr.send();
})();