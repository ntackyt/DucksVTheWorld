import { onSnake, expandSnake } from './snake.js'
import { randomGridPosition } from './game.js'

//call function to randomize next location of food
let food = getRandomFoodPosition()
const EXPANSION_RATE = 1    //the amount of segments the snake increases by when it eats

//updating food location to a random xy coordinate within gameboard
export function update() {
  if (onSnake(food)) {  //add segment if a part of the snake touches the food
    expandSnake(EXPANSION_RATE)
    food = getRandomFoodPosition()
  }
}

export function draw(gameBoard) {   
  const foodElement = document.createElement('div')
  foodElement.style.gridRowStart = food.y
  foodElement.style.gridColumnStart = food.x
  foodElement.classList.add('food')
  gameBoard.appendChild(foodElement)
}


//create new food if current food goes "into the snake"
function getRandomFoodPosition() {
  let newFoodPosition
  while (newFoodPosition == null || onSnake(newFoodPosition)) {
    newFoodPosition = randomGridPosition()
  }
  return newFoodPosition
}