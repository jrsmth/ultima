const canvasGame = $('#starfield-game')[0];
const contextGame = canvasGame.getContext("2d");
let widthGame;
let heightGame;
let velocityGame = 0.01;
let densityGame = 500;
let brightnessGame = 1;
let sizeGame = 2;

function getBrightnessGame() { return brightnessGame; }
function getDensityGame() { return densityGame; }
function getVelocityGame() { return velocityGame; }
function setBrightnessGame(value) { brightnessGame = value; }
function setDensityGame(value) { densityGame = value; }
function setVelocityGame(value) { velocityGame = value; }

const setCanvasLimitsGame = () => {
    widthGame = document.body.clientWidth;
    heightGame = document.body.clientHeight;
    canvasGame.width = widthGame;
    canvasGame.height = heightGame;
};

setCanvasLimitsGame();

window.onresize = () => {
    setCanvasLimitsGame();
};

const makeStarsGame = () => {
    const out = [];
    for (let i = 0; i < getDensityGame(); i++) {
        const s = {
            x: Math.random() * 1600 - 800,
            y: Math.random() * 900 - 450,
            z: Math.random() * 1000
        };
        out.push(s);
    }

    return out;
};

let starsGame = makeStarsGame();

const clearGame = () => {
    contextGame.fillStyle = "black"; // FixMe?
    contextGame.fillRect(0, 0, canvasGame.width, canvasGame.height);
};

const putPixelGame = (x, y, brightness) => {
    const intensity = brightness * 255;
    contextGame.fillStyle = "rgb(" + intensity + "," + intensity + "," + intensity + ")";
    contextGame.fillRect(x, y, sizeGame, sizeGame);
};

const moveStarsGame = distance => {
    const count = starsGame.length;
    for (let i = 0; i < count; i++) {
        const s = starsGame[i];
        s.z -= distance;
        while (s.z <= 1) {
            s.z += 1000;
        }
    }
};

let prevTimeGame;
const initGame = time => {
    prevTimeGame = time;
    requestAnimationFrame(tickGame);
};

const tickGame = time => {
    let elapsed = time - prevTimeGame;
    prevTimeGame = time;

    moveStarsGame(elapsed * getVelocityGame());
    clearGame();

    const cx = widthGame / 2;
    const cy = heightGame / 2;

    const count = starsGame.length;
    for (let i = 0; i < count; i++) {
        const star = starsGame[i];

        const x = cx + star.x / (star.z * 0.001);
        const y = cy + star.y / (star.z * 0.001);

        if (x < 0 || x >= widthGame || y < 0 || y >= heightGame) {
            continue;
        }

        const d = star.z / 1000.0;
        const b = getBrightnessGame() - d * d;

        putPixelGame(x, y, b);
    }

    requestAnimationFrame(tickGame);
};

requestAnimationFrame(initGame);
