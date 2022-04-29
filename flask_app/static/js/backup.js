//Define vars to hold time values
let miliSeconds = 0;
let seconds = 0;
let minutes = 0;

//Define vars to hold "display" value
let displayMiliSeconds = 0;
let displaySeconds = 0;
let displayMinutes = 0;

//Define var to hold setInterval() function
let interval = null;

//Define var to hold stopwatch status
let status = "stopped";

//Stopwatch function (logic to determine when to increment next value, etc.)
function stopWatch(){

    miliSeconds++;

    //Logic to determine when to increment next value
    if(miliSeconds / 100 === 1){
        miliSeconds = 0;
        seconds++;

        if(seconds / 60 === 1){
            seconds = 0;
            minutess++;
        }

    }

    //If seconds/minutes/hours are only one digit, add a leading 0 to the value
    if(miliSeconds < 10){
        displayMiliSeconds = "0" + miliSeconds.toString();
    }
    else{
        displayMiliSeconds = miliSeconds;
    }

    if(seconds < 10){
        displaySeconds = "0" + seconds.toString();
    }
    else{
        displaySeconds = seconds;
    }

    if(minutes < 10){
        displayMinutes = "0" + minutes.toString();
    }
    else{
        displayMinutes = minutes;
    }

    //Display updated time values to user
    document.getElementById("display").innerHTML = displayMinutes + ":" + displaySeconds + ":" + displayMiliSeconds;

}



function startStop(){

    if(status === "stopped"){

        //Start the stopwatch (by calling the setInterval() function)
        interval = window.setInterval(stopWatch, 10);
        document.getElementById("startStop").innerHTML = "Stop";
        status = "started";

    }
    else{

        window.clearInterval(interval);
        document.getElementById("startStop").innerHTML = "Start";
        status = "stopped";

    }

}

//Function to reset the stopwatch
function reset(){
    console.log(document.getElementById("display").innerHTML)
    console.log(document.getElementById("time").value)
    document.getElementById("time").value = document.getElementById("display").innerHTML
    window.clearInterval(interval);
    miliSeconds = 0;
    seconds = 0;
    minutes = 0;
    document.getElementById("display").innerHTML = "00:00:00";
    document.getElementById("startStop").innerHTML = "Start";

}

function save() {
    document.getElementById("time").value = document.getElementById("display").innerHTML
}