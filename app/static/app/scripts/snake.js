// setting the snake speed and the initial block position
export const SNAKE_SPEED = 7
const snakeBody = [{ x: 11, y: 11 }]
let newSegments = 0
let snakeLength = 0

//setting current snake direction and previous direction
let inputDirection = { x: 0, y: 0}
let lastInputDirection = { x: 0, y: 0}

export function update() {
  addSegments()

  const inputDirection = getInputDirection()

  for (let i = snakeBody.length - 2; i >= 0; i--) {
    snakeBody[i + 1] = { ...snakeBody[i] }
  }

  snakeBody[0].x += inputDirection.x
  snakeBody[0].y += inputDirection.y
}

export function draw(gameBoard) {
  snakeBody.forEach(segment => {
    const snakeElement = document.createElement('div')
    snakeElement.style.gridRowStart = segment.y
    snakeElement.style.gridColumnStart = segment.x
    snakeElement.classList.add('snake')
    gameBoard.appendChild(snakeElement)
  })
}

//increase amount of snake segments
export function expandSnake(amount) {
  newSegments += amount
}

export function onSnake(position, { ignoreHead = false } = {}) {
  return snakeBody.some((segment, index) => {
    if (ignoreHead && index === 0) return false
    return equalPositions(segment, position)
  })
}

export function getSnakeHead() {
  return snakeBody[0]
}

//check that snake does not run into itself
export function snakeIntersection() { 
  return onSnake(snakeBody[0], { ignoreHead: true })
}

function equalPositions(pos1, pos2) {
  return pos1.x === pos2.x && pos1.y === pos2.y
}

function addSegments() {
  for (let i = 0; i < newSegments; i++) {
    snakeBody.push({ ...snakeBody[snakeBody.length - 1] })
    snakeLength = snakeLength + 1 
  }

  newSegments = 0
}

//updating the snakes direction based on user input if input is valid
//error checking to ensure new direction is not where the snake is coming from
window.addEventListener('keydown', e => {
    switch (e.key){
        case 'ArrowUp':
            if (lastInputDirection.y !== 0) break
            inputDirection = { x: 0, y: -1 }
            break
        case 'ArrowDown':
            if (lastInputDirection.y !== 0) break
            inputDirection = { x: 0, y: 1 }
            break
        case 'ArrowLeft':
            if (lastInputDirection.x !== 0) break
            inputDirection = { x: -1, y: 0 }
            break
        case 'ArrowRight':
            if (lastInputDirection.x !== 0) break
            inputDirection = { x: 1, y: 0 }
            break
    }
})

function getInputDirection(){
    lastInputDirection = inputDirection
    return inputDirection
}