function leadingZero(inp){
    if (inp < 10) return `0${inp}`
    return inp
}

function millify(n){
    if (!n) return 0
    var millnames = ['','K','M','B','T','Qd']
    var digitCount = Math.floor(Math.log10(Math.abs(n))/3)
    var millidx = Math.max(0,Math.min(millnames.length -1, digitCount))

    return `${(n / 10**(3 * millidx)).toFixed(1)}${millnames[millidx]}`
}

Chart.defaults.font.size = 20
Chart.defaults.animation = false
Chart.defaults.color = "#818285"
let hourNum = new Date().getHours()
if (hourNum){
    hourNum -= 1
}else{
    hourNum = 23
}
const hour = leadingZero(hourNum)
const hourArray = Array.from(Array(61).keys())
const buffUptimeXAxis = Array.from(Array(601).keys())

function makeStackableBuffChart(element, datasets){
    
    for (let dataset of datasets){
        for(let i = dataset.data.length; i < 600; i++){
            dataset.data.unshift(0)
        }
    }

    new Chart(element, {
    type: 'line',
    data: {
        labels: buffUptimeXAxis,
        datasets: datasets
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        y: {
            grid: {
                color: "#1F1F20"
            },
            ticks: {
                maxTicksLimit: 3,
                autoSkip: false,
            },
            min: 0,
            max: 10,
        },
        x: {
            ticks: {
                callback: function(value, index, values) {
                    value = value/10
                    if (value == 60) return `${leadingZero(hourNum+1)}:00`
                    if (!(value%10)) return `${hour}:${leadingZero(value)}`
                },
                stepSize: 10
            }
        }
        },
        elements: {
            point: {
                pointStyle: false,
            }
        },
        plugins:{
            legend: {
                display: false
            }
        },
    }
    })
}