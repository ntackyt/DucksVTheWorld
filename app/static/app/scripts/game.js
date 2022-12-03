import { update as updateSnake, draw as drawSnake, SNAKE_SPEED, getSnakeHead, snakeIntersection } from './snake.js'
import { update as updateFood, draw as drawFood } from './food.js'


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//resetting game info at the beginning of every game
let lastRenderTime = 0
let gameOver = false
const gameBoard = document.getElementById('game-board') 

function main(currentTime) {

    //option to restart if you lose the game from browser popup
    if (gameOver){
        // For CSRF protection
        const csrftoken = getCookie('csrftoken');
        // POST data to Django server using AJAX
        $.ajax({
            type: "POST",
            url: "/game/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                "points_earned": 4
            },
            success: function (response) {
                if (response.success == True) {
                    console.log("success");
                } else {
                    console.log("failure");
                }
            },
            error: function (error) {
                console.log("Error: ", error);
            }
        });
        if (confirm('you lose :( Press Ok to restart!')){
            window.location = '/game'
        }
        return
    }

    //game loop
    window.requestAnimationFrame(main) 
    const secondsSinceLastRender = (currentTime - lastRenderTime) / 1000
    if (secondsSinceLastRender < 1 / SNAKE_SPEED ) return

    lastRenderTime = currentTime

    //reset game board
    //update game board snake & food status
    updateSnake()
    updateFood()
    checkBorder()

    //display snake & food updates
    gameBoard.innerHTML = ''
    drawSnake(gameBoard)
    drawFood(gameBoard)
}

window.requestAnimationFrame(main)

//game ends if snake goes past gameboard
function checkBorder() {
    gameOver = gridBoundary(getSnakeHead()) || snakeIntersection()
  }


//get random position within the 21x21 grid parameter (used for genrating new food position)
export function randomGridPosition() {
    return {
        x: Math.floor(Math.random() * 21) + 1,
        y: Math.floor(Math.random() * 21) + 1,
    }
}

//defining parameters for the playable grid
function gridBoundary(position) {
    return (
        position.x < 1 || position.x > 21 || position.y < 1 || position.y > 21
    )
}

