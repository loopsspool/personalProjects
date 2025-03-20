// timer.js
// Allows user to set time until an alarm sound goes off

// Ethan Jones
// 11:24pm, Thursday 12-20-18
// 3 hours

var WW, WH; // For windowWidth and Height
var chooseSound, timerSound; // UI sound file selection and sound variable
var chooseHours, chooseMinute, chooseSecond, hours = 0, minutes = 0, seconds = 0, hourString, minuteString, secondString;
var selectXPosBuffer = 60;
var selectYPos;
var startButton, pauseButton, stopButton;
var isCounting = false;

function setup()
{
    // ENVIORNMENT SETTINGS
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    frameRate(1);
    colorMode(HSB, 360, 100 , 100, 100);
    fill(0);
    noStroke();

    // VARIABLE INITIALIZERS
    chooseSound = createFileInput(prepareSound);
    chooseSound.position(0, 0); 
    
    selectYPos = WH/6;
    textYPos = WH/6 + 30;

    chooseHours = createSelect();
    chooseHours.position(WW/2 - selectXPosBuffer, selectYPos);
    for (let h = 0; h <= 24; h++)
        chooseHours.option(h);
    chooseHours.changed(updateHours);
    text("Hours", WW/2 - selectXPosBuffer, textYPos);

    chooseMinutes = createSelect();
    chooseMinutes.position(WW/2, selectYPos);
    for (let m = 0; m < 60; m++)
        chooseMinutes.option(m);
    chooseMinutes.changed(updateMinutes);
    text("Minutes", WW/2, textYPos);

    chooseSeconds = createSelect();
    chooseSeconds.position(WW/2 + selectXPosBuffer, selectYPos)
    for (let s = 0; s < 60; s++)
        chooseSeconds.option(s);
    chooseSeconds.changed(updateSeconds);
    text("Seconds", WW/2 + selectXPosBuffer, textYPos);

    startButton = createButton('START');
    startButton.position(WW/2, WH/2);
    startButton.mousePressed(startTiming);

    pauseButton = createButton('PAUSE');
    pauseButton.position(WW/3, 5*WH/6);
    pauseButton.mousePressed(pauseTiming);
    pauseButton.hide();
}

function draw()
{
    background(100);
    displayRemainingTime();
    checkChangeTime();
    // TODO: stop (reset button)
    // If timer time selected and play is hit, play default sound unless file was input (attach listener to file selector?) at end of time
}

function displayRemainingTime()
{
    fill(0);
    textSize(48);
    textAlign(CENTER);
    if (!isCounting && frameCount%2==0)
        fill(100);
    hourString = hours.toString();
    minuteString = minutes.toString();
    secondString = seconds.toString();
    if (hours < 10)
        hourString = '0' + hours.toString();
    if (minutes < 10)
        minuteString = '0' + minutes.toString();
    if (seconds < 10)
        secondString = '0' + secondString.toString();
    text(hourString + ' : ' + minuteString + ' : ' + secondString, WW/2, WH/2);
}

function checkChangeTime()
{
    if (isCounting)
    {
        if (seconds > 0)
            seconds--;
        else if (seconds == 0)
        {
            if (minutes > 0)
            {
                minutes--;
                seconds = 59;
            }
            else if (minutes == 0)
            {
                if (hours > 0)
                {
                    hours--;
                    minutes = 59;
                    seconds = 59;
                }
                //else if (hours == 0)
                    //TODO: play alarm sound
            }
        }
    }
}

function startTiming()
{
    isCounting = true;
    startButton.hide();
    pauseButton.show();
    chooseHours.hide();
    chooseMinutes.hide();
    chooseSeconds.hide();
}

function pauseTiming()
{
    isCounting = false;
    startButton.show();
    pauseButton.hide();
    chooseHours.show();
    chooseMinutes.show();
    chooseSeconds.show();
    updateSelectors();
}

function prepareSound()
{
    // TODO: Check if it's a sound file.
    // Assign to timerSound variable
}

function updateSelectors()
{
    chooseHours.value(hours);
    chooseMinutes.value(minutes);
    chooseSeconds.value(seconds);
}

function updateHours()
{
    hours = chooseHours.value();
}

function updateMinutes()
{
    minutes = chooseMinutes.value();
}

function updateSeconds()
{
    seconds = chooseSeconds.value();
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}