var elevationData;
var canvas;
var width;
var height;
var seaLevelOutput;

const LOW_ELEVATION_COLOR = [204, 204, 92]; // #cccc5c
const HIGH_ELEVATION_COLOR = [38, 120, 13]; // #26780d
const SEA_COLOR = [89, 158, 255]; // #599eff
const HIGHLIGHT_COLOR = [235, 64, 52]; // #eb4034

const MAX_ELEVATION = 255;

function setColor(imageData, x, y, r, g, b, a) {
    const width = imageData.width;
    const startIndex = (y * width + x) * 4;
    imageData.data[startIndex] = r;
    imageData.data[startIndex + 1] = g;
    imageData.data[startIndex + 2] = b;
    imageData.data[startIndex + 3] = a;
}

function update() {
    const level = document.querySelector('#sea-level').value;
    const output = document.querySelector('.sea-level-output');
    const highlight = document.querySelector('#highlight-submerged').checked;

    output.textContent = level + " meter(s)";

    if (canvas.getContext) {
        const ctx = canvas.getContext('2d');
        
        if (elevationData !== undefined) {
            const imageData = ctx.createImageData(width, height);
            for (let y = 0; y < height; y++) {
                for (let x = 0; x < width; x++) {
                    const elevation = elevationData[y * width + x];
                    if (elevation > level) {
                        const color = [0, 0, 0];
                        for (let i = 0; i < 3; i++) {
                            color[i] = LOW_ELEVATION_COLOR[i] + elevation * (HIGH_ELEVATION_COLOR[i] - LOW_ELEVATION_COLOR[i]) / MAX_ELEVATION;
                        }
                        setColor(imageData, x, y, ...color, 255);
                    } else {
                        // const mixedColor = [0, 0, 0];
                        // for (let i = 0; i < 3; i++) {
                        //     mixedColor[i] = color[i] + (level.value - elevation + 130) * (SEA_COLOR[i] - color[i]) / 255;
                        // }
                        // setColor(imageData, x, y, ...mixedColor, 255);
                        setColor(imageData, x, y, ...((highlight && elevation > 0) ? HIGHLIGHT_COLOR : SEA_COLOR), 255);
                    }
                }
            }
            ctx.putImageData(imageData, 0, 0);
        } else {
            // TODO: display loading...
            // Fill background black
            ctx.fillStyle = 'rgb(0, 0, 0)';
            ctx.fillRect(0, 0, width, height);
        }
    } // TODO: handle error and print message
}

function fetchElevationData() {
    const req = new XMLHttpRequest();
    req.responseType = "arraybuffer";
    req.onload = function(e) {
        if (req.status === 200) {
            const arraybuffer = req.response;
            elevationData = new Uint8Array(arraybuffer);
            update();
        } else {
            // TODO: user friendly error message on canvas
            console.error("Request failed");
        }
    }
    req.open("GET", "/elevation.dat");
    req.send();
}

function load() {
    console.log("Page fully Loaded!");
    canvas = document.getElementById('map');
    width = canvas.width;
    height = canvas.height;

    update();

    const level = document.querySelector('#sea-level');
    level.addEventListener('input', function() {
        update();
    });
    document.querySelector('#highlight-submerged').addEventListener('click', function() {
        update();
    })

    fetchElevationData();
}

console.log("Javascript executed");