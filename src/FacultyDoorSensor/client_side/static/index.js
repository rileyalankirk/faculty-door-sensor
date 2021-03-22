'use strict';


function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function updateTime() {
    let time = new Date();
    let hours = time.getHours();
    let meridian = (hours > 12) ? ' PM' : ' AM'
    if (hours > 12) { hours -= 12; }
    let  minutes = time.getMinutes();
    if (minutes < 10) { minutes = '0' + minutes; }
    document.getElementById('time').textContent = hours + ':' + minutes + meridian;
}

window.onload = function() { updateTime(); }  

window.addEventListener('load', function init() {
    setInterval( () => {
        updateDashboardData();
    }, 5000);
})

const updateDashboardData = () => {
    fetch(window.location.href + '/data')
    .then(response => response.json())
    .then(doorStatuses => {
        const { 
                color4, status4, name4, color3, status3, name3,
                color2, status2, name2, color1, status1, name1 
              } = doorStatuses;

        document.getElementById('left-top').style.backgroundColor = color1;
        document.getElementById('left-top-name').textContent = 'Dr. ' + capitalize(name1);
        document.getElementById('left-top-status').textContent = status1;
        document.getElementById('right-top').style.backgroundColor = color2;
        document.getElementById('right-top-name').textContent = 'Dr. ' + capitalize(name2);
        document.getElementById('right-top-status').textContent = status2;
        document.getElementById('left-bottom').style.backgroundColor = color3;
        document.getElementById('left-bottom-name').textContent = 'Dr. ' + capitalize(name3);
        document.getElementById('left-bottom-status').textContent = status3;
        document.getElementById('right-bottom').style.backgroundColor = color4;
        document.getElementById('right-bottom-name').textContent = 'Dr. ' + capitalize(name4);
        document.getElementById('right-bottom-status').textContent = status4;

        updateTime();
    })
    .catch((err) => console.log(err));
}
