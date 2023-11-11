let thisUserId;
let thisSymbol;

function init() { // TODO :: convert to JQuery?
    thisUserId = document.getElementById('this-user-id').value;
    thisSymbol = document.getElementById('this-user-symbol').value;
    const gameMode = document.getElementById('game-mode').value;

    if (gameMode === "STANDARD") initStandard(thisUserId, thisSymbol);
    if (gameMode === "ULTIMATE") initUltimate(thisUserId, thisSymbol);

}

function initStandard(thisUserId, thisSymbol) {
    for (let i = 0; i < 9; i++) {
        const square = document.getElementById(`three-square-${i}`).getElementsByClassName("square")[0];
        const state = square.innerHTML;
        if (state === thisSymbol) {
            square.parentElement.classList.add("this-user");
        } else if (state !== "0") {
            square.parentElement.classList.add("opponent-user");
        }

        if (state === "0") {
            square.innerHTML = '';
        } else if (state === "1") {
            square.innerHTML = '<i class="fa fa-times symbol"></i>'
        } else if (state === "2") {
            square.innerHTML = '<i class="fa-regular fa-circle symbol"></i>'
        }
    }
}

function initUltimate(thisUserId, thisSymbol) {
    for (let i = 0; i < 9; i++) {
        const outerSquare = document.getElementById(`nine-square-${i}`).getElementsByClassName("square")[0];

        for (let j = 0; j < 9; j++) {
            const innerSquare = document.getElementById(`nine-square-${i}-${j}`).getElementsByClassName("square")[0];

            const innerState = innerSquare.innerHTML;
            if (innerState === thisSymbol) {
                innerSquare.parentElement.classList.add("this-user");
            } else if (innerState !== "0") {
                innerSquare.parentElement.classList.add("opponent-user");
            }

            if (innerState === "0") {
                innerSquare.innerHTML = '';
            } else if (innerState === "1") {
                innerSquare.innerHTML = '<i class="fa fa-times symbol"></i>'
            } else if (innerState === "2") {
                innerSquare.innerHTML = '<i class="fa-regular fa-circle symbol"></i>'
            }
        }
    }
}

function placeStandardMove(square) {
    const gameId = "ab12-3cd4-e5f6-78gh";

    const userSymbol = document.getElementById('this-user-symbol').value;
    const playerOneActive = document.getElementById('player-one-active').value;
    const playerTwoActive = document.getElementById('player-two-active').value;
    const gameComplete = document.getElementById('game-complete').value;

    if (gameComplete === 'True') return;
    if (userSymbol === '1' && playerTwoActive === 'True') return;
    if (userSymbol === '2' && playerOneActive === 'True') return;

    if (document.getElementById(`three-square-${square}`).getElementsByClassName("square")[0].innerHTML !== '') {
        return;
    }

    $.get(`/game/${gameId}/place-move/${thisUserId}/${square}`);
    location.reload();
}

function placeMove(outerSquare, innerSquare) {
    const gameId = "ab12-3cd4-e5f6-78gh";

    const userSymbol = document.getElementById('this-user-symbol').value;
    const playerOneActive = document.getElementById('player-one-active').value;
    const playerTwoActive = document.getElementById('player-two-active').value;
    const gameComplete = document.getElementById('game-complete').value;

    if (gameComplete === 'True') return;
    if (userSymbol === '1' && playerTwoActive === 'True') return;
    if (userSymbol === '2' && playerOneActive === 'True') return;

    if (document.getElementById(`nine-square-${outerSquare}-${innerSquare}`).getElementsByClassName("square")[0].innerHTML !== '') {
        return;
    }

    $.get(`/game/${gameId}/place-move/${thisUserId}/${outerSquare}/${innerSquare}`);
    location.reload();
}

init();