// Snake Game Engine - Pure JavaScript Implementation

const GRID_SIZE = 20; // 20x20 cells
const CELL_SIZE = 20; // 20px per cell (Canvas: 400x400px)

const Canvas = document.getElementById('gameCanvas');
const ctx = Canvas.getContext('2d');

// UI Elements
const currentScoreEl = document.getElementById('currentScore');
const highScoreEl = document.getElementById('highScore');
const wallModeSelect = document.getElementById('wallMode');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const overlayEl = document.getElementById('overlay');
const overlayTitleEl = document.getElementById('overlayTitle');
const overlayTextEl = document.getElementById('overlayText');

// Game State Variables
let snake = [];
let food = { x: 0, y: 0 };
let direction = { x: 1, y: 0 }; // Initial direction: Right
let inputBuffer = []; // Queue for inputs to prevent self-collision
let score = 0;
let highScore = localStorage.getItem('snake_highscore') || 0;
let gameState = 'IDLE'; // 'IDLE', 'RUNNING', 'PAUSED', 'GAME_OVER'
let gameInterval = null;
let currentSpeed = 120; // Initial tick rate in ms

// Initialize Highscore UI
highScoreEl.textContent = highScore;

// Directions
const DIR = {
    UP: { x: 0, y: -1 },
    DOWN: { x: 0, y: 1 },
    LEFT: { x: -1, y: 0 },
    RIGHT: { x: 1, y: 0 }
};

// Initialize or Reset Game
function initGame() {
    snake = [
        { x: 5, y: 10 },
        { x: 4, y: 10 },
        { x: 3, y: 10 }
    ];
    direction = DIR.RIGHT;
    inputBuffer = [];
    score = 0;
    currentSpeed = 120;
    currentScoreEl.textContent = score;
    spawnFood();
    draw();
}

// Spawn food in an unoccupied cell
function spawnFood() {
    const emptyCells = [];
    for (let x = 0; x < GRID_SIZE; x++) {
        for (let y = 0; y < GRID_SIZE; y++) {
            const isOccupied = snake.some(segment => segment.x === x && segment.y === y);
            if (!isOccupied) {
                emptyCells.push({ x, y });
            }
        }
    }
    if (emptyCells.length > 0) {
        const randomIndex = Math.floor(Math.random() * emptyCells.length);
        food = emptyCells[randomIndex];
    }
}

// Main Game Loop Tick
function tick() {
    if (gameState !== 'RUNNING') return;

    // Process Next Input from Queue
    if (inputBuffer.length > 0) {
        const nextDir = inputBuffer.shift();
        direction = nextDir;
    }

    // Calculate New Head Position
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };
    const wallMode = wallModeSelect.value;

    // Wall Collision Check
    if (wallMode === 'die') {
        if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
            triggerGameOver('Du bist gegen die Wand gefahren!');
            return;
        }
    } else if (wallMode === 'wrap') {
        if (head.x < 0) head.x = GRID_SIZE - 1;
        if (head.x >= GRID_SIZE) head.x = 0;
        if (head.y < 0) head.y = GRID_SIZE - 1;
        if (head.y >= GRID_SIZE) head.y = 0;
    }

    // Self Collision Check
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        triggerGameOver('Du hast dich selbst gebissen!');
        return;
    }

    // Move Snake Head
    snake.unshift(head);

    // Check Food Collision
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        currentScoreEl.textContent = score;
        if (score > highScore) {
            highScore = score;
            highScoreEl.textContent = highScore;
            localStorage.setItem('snake_highscore', highScore);
        }
        spawnFood();
        adjustSpeed();
    } else {
        // Remove Tail
        snake.pop();
    }

    draw();
}

// Dynamic Speed Adjustment
function adjustSpeed() {
    // Increase speed slightly every 50 points (min 50ms interval)
    const newSpeed = Math.max(50, 120 - Math.floor(score / 50) * 10);
    if (newSpeed !== currentSpeed) {
        currentSpeed = newSpeed;
        clearInterval(gameInterval);
        gameInterval = setInterval(tick, currentSpeed);
    }
}

// Rendering Function
function draw() {
    // Clear Canvas
    ctx.fillStyle = '#1A1A1A';
    ctx.fillRect(0, 0, Canvas.width, Canvas.height);

    // Draw Grid Lines (Subtle)
    ctx.strokeStyle = '#222222';
    ctx.lineWidth = 1;
    for (let i = 0; i <= GRID_SIZE; i++) {
        ctx.beginPath();
        ctx.moveTo(i * CELL_SIZE, 0);
        ctx.lineTo(i * CELL_SIZE, Canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * CELL_SIZE);
        ctx.lineTo(Canvas.width, i * CELL_SIZE);
        ctx.stroke();
    }

    // Draw Food (Apple with leaf for accessibility)
    const foodCenterX = food.x * CELL_SIZE + CELL_SIZE / 2;
    const foodCenterY = food.y * CELL_SIZE + CELL_SIZE / 2;
    const radius = CELL_SIZE / 2 - 2;

    ctx.fillStyle = '#FF4444';
    ctx.beginPath();
    ctx.arc(foodCenterX, foodCenterY, radius, 0, Math.PI * 2);
    ctx.fill();

    // Leaf on top of Apple
    ctx.fillStyle = '#00FF66';
    ctx.beginPath();
    ctx.arc(foodCenterX + 2, foodCenterY - radius + 2, 3, 0, Math.PI * 2);
    ctx.fill();

    // Draw Snake
    snake.forEach((segment, index) => {
        const isHead = index === 0;

        if (isHead) {
            ctx.fillStyle = '#00FF66';
            ctx.fillRect(segment.x * CELL_SIZE + 1, segment.y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);

            // Draw Head Eyes for Direction Clarity
            ctx.fillStyle = '#121212';
            const eyeOffset = 4;
            let eye1X, eye1Y, eye2X, eye2Y;

            if (direction.x === 1) { // Right
                eye1X = (segment.x + 1) * CELL_SIZE - eyeOffset; eye1Y = segment.y * CELL_SIZE + 5;
                eye2X = (segment.x + 1) * CELL_SIZE - eyeOffset; eye2Y = (segment.y + 1) * CELL_SIZE - 7;
            } else if (direction.x === -1) { // Left
                eye1X = segment.x * CELL_SIZE + eyeOffset; eye1Y = segment.y * CELL_SIZE + 5;
                eye2X = segment.x * CELL_SIZE + eyeOffset; eye2Y = (segment.y + 1) * CELL_SIZE - 7;
            } else if (direction.y === -1) { // Up
                eye1X = segment.x * CELL_SIZE + 5; eye1Y = segment.y * CELL_SIZE + eyeOffset;
                eye2X = (segment.x + 1) * CELL_SIZE - 7; eye2Y = segment.y * CELL_SIZE + eyeOffset;
            } else { // Down
                eye1X = segment.x * CELL_SIZE + 5; eye1Y = (segment.y + 1) * CELL_SIZE - eyeOffset;
                eye2X = (segment.x + 1) * CELL_SIZE - 7; eye2Y = (segment.y + 1) * CELL_SIZE - eyeOffset;
            }

            ctx.beginPath();
            ctx.arc(eye1X, eye1Y, 2, 0, Math.PI * 2);
            ctx.arc(eye2X, eye2Y, 2, 0, Math.PI * 2);
            ctx.fill();
        } else {
            // Body Segments
            ctx.fillStyle = '#00CC52';
            ctx.fillRect(segment.x * CELL_SIZE + 2, segment.y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
        }
    });
}

// Handle User Controls & Input Queueing
function queueInput(newDir) {
    const lastDir = inputBuffer.length > 0 ? inputBuffer[inputBuffer.length - 1] : direction;

    // Prevent 180 degree instant reversal
    if (newDir.x + lastDir.x === 0 && newDir.y + lastDir.y === 0) return;

    if (inputBuffer.length < 2) {
        inputBuffer.push(newDir);
    }
}

// Event Listeners
document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
            if (gameState === 'RUNNING') queueInput(DIR.UP);
            break;
        case 'ArrowDown':
        case 's':
        case 'S':
            if (gameState === 'RUNNING') queueInput(DIR.DOWN);
            break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
            if (gameState === 'RUNNING') queueInput(DIR.LEFT);
            break;
        case 'ArrowRight':
        case 'd':
        case 'D':
            if (gameState === 'RUNNING') queueInput(DIR.RIGHT);
            break;
        case ' ':
            togglePause();
            break;
    }
});

// Button Controls
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', togglePause);

function startGame() {
    initGame();
    gameState = 'RUNNING';
    overlayEl.classList.add('hidden');
    startBtn.textContent = 'Neu starten';
    pauseBtn.disabled = false;

    if (gameInterval) clearInterval(gameInterval);
    gameInterval = setInterval(tick, currentSpeed);
}

function togglePause() {
    if (gameState === 'RUNNING') {
        gameState = 'PAUSED';
        clearInterval(gameInterval);
        overlayTitleEl.textContent = 'PAUSE';
        overlayTitleEl.style.color = '#00FF66';
        overlayTextEl.textContent = 'Drücke Drücke "Pause" oder [Leertaste], um fortzufahren.';
        overlayEl.classList.remove('hidden');
        pauseBtn.textContent = 'Weiter';
    } else if (gameState === 'PAUSED') {
        gameState = 'RUNNING';
        overlayEl.classList.add('hidden');
        pauseBtn.textContent = 'Pause';
        gameInterval = setInterval(tick, currentSpeed);
    }
}

function triggerGameOver(reason) {
    gameState = 'GAME_OVER';
    clearInterval(gameInterval);
    pauseBtn.disabled = true;

    overlayTitleEl.textContent = 'GAME OVER';
    overlayTitleEl.style.color = '#FF4444';
    overlayTextEl.textContent = `${reason} Endstand: ${score} Punkte.`;
    overlayEl.classList.remove('hidden');
}

// Initial draw on page load
initGame();
