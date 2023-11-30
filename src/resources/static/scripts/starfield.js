const canvas = $('#starfield')[0];
const context = canvas.getContext("2d");
let width;
let height;
let velocity = 0.01;
let density = 500;
let brightness = 1;
let size = 2;

function getVelocity() {
    return velocity;
}

function setVelocity(value) {
    velocity = value;
}

function getDensity() {
    return density;
}

function setDensity(value) {
    density = value;
}

function getBrightness() {
    return brightness;
}

function setBrightness(value) {
    brightness = value;
}

function getSize() {
    return size;
}

function setSize(value) {
    size = value;
}

const setCanvasLimits = () => {
    width = document.body.clientWidth;
    height = document.body.clientHeight;
    canvas.width = width;
    canvas.height = height;
};

setCanvasLimits();

window.onresize = () => {
    setCanvasLimits();
};

const makeStars = () => {
    const out = [];
    for (let i = 0; i < getDensity(); i++) {
        const s = {
            x: Math.random() * 1600 - 800,
            y: Math.random() * 900 - 450,
            z: Math.random() * 1000
        };
        out.push(s);
    }

    return out;
};

let stars = makeStars();

const clear = () => {
    context.fillStyle = "black"; // FixMe?
    context.fillRect(0, 0, canvas.width, canvas.height);
};

const putPixel = (x, y, brightness) => {
    const intensity = brightness * 255;
    context.fillStyle = "rgb(" + intensity + "," + intensity + "," + intensity + ")";
    context.fillRect(x, y, getSize(), getSize());
};

const moveStars = distance => {
    const count = stars.length;
    for (let i = 0; i < count; i++) {
        const s = stars[i];
        s.z -= distance;
        while (s.z <= 1) {
            s.z += 1000;
        }
    }
};

let prevTime;
const init = time => {
    prevTime = time;
    requestAnimationFrame(tick);
};

const tick = time => {
    let elapsed = time - prevTime;
    prevTime = time;

    moveStars(elapsed * getVelocity());
    clear();

    const cx = width / 2;
    const cy = height / 2;

    const count = stars.length;
    for (let i = 0; i < count; i++) {
        const star = stars[i];

        const x = cx + star.x / (star.z * 0.001);
        const y = cy + star.y / (star.z * 0.001);

        if (x < 0 || x >= width || y < 0 || y >= height) {
            continue;
        }

        const d = star.z / 1000.0;
        const b = getBrightness() - d * d;

        putPixel(x, y, b);
    }

    requestAnimationFrame(tick);
};

requestAnimationFrame(init);
