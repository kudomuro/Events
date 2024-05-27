function zero_first_format(value)
{
    if (value < 10)
    {
        value='0'+value;
    }
    return value;
}                            
let current_datetime = new Date();
let day = zero_first_format(current_datetime.getDate());
let month = zero_first_format(current_datetime.getMonth()+1);
let year = current_datetime.getFullYear();   
let dateCrnt = `${year}-${month}-${day}`;
let time = document.getElementById('time');
time.innerHTML = `События на ${day}.${month}.${year} <span style="text-transform: lowercase;">(по местному времени)</span>`;   

async function load(url) {
    return await (await fetch(url)).json();
}


let date = new Date();
let weekday = 2**(date.getDay());

const start = async function() {
    let url='https://192.168.11.29/api/result'; 
    const json = await load(url);
        document.getElementById('blkDiv').innerHTML = json.filter(e => ((e.day&weekday)>0 || (e.date==dateCrnt))).map(json => 
            `
            <p><b>${new Date("1970-01-01T" + json.time + "+05:00").toLocaleTimeString("ru").replace(/(.*)\D\d+/, '$1')}</b> ${json.lead} «${json.theme}». ${json.actors}</p>
            `
        ).join('');
}

start();

window.setInterval(function () {
    start();
}, 10000);