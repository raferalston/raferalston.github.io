let background = document.querySelector('body');
let clicker = document.querySelector('#clicker');
let clickerText = document.querySelector('#clicker span');
let gameBox = document.querySelector('#game_box');
let score = document.querySelector('#score #count');
let colors = ['#1eff00', '#83ff0f', '#ffd30f', '#ff9f0f', '#ff670f', '#ff3f0f', '#ff130f'];
let gameScore = 0;
let gameLen = colors.length * 5 + 5;

clickerText.textContent = gameLen;

clicker.addEventListener('click', gameEvent);

function gameEvent(event) {
    gameScore++
    gameLen--
    clickerText.textContent = gameLen;
    score.textContent = gameScore
    if (gameScore % 5 == 0) {
        changeColor()
    }
}

function changeColor() {
    let color = colors.pop();
    if (color == undefined) {
        gameOver()
    }
    background.style.backgroundColor = color;
}

function gameOver() {
    gameBox.remove();
    let done = document.createElement('div');
    done.className = 'gameOver';
    done.textContent = 'Congratulations you win the game! Your final score: ' + gameScore;
    background.append(done);
}