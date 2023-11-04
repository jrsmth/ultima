let thisUserId;
let thisSymbol;

function init() {
    thisUserId = document.getElementById('this-user-id').value;
    thisSymbol = document.getElementById('this-user-symbol').value;

    for (let i = 1; i <= 9; i++) {
        const square = document.getElementById(`square-${i}`).getElementsByClassName("square")[0];
        const state = square.innerHTML;
        if (state === thisSymbol) {
            square.parentElement.classList.add( "this-user");
        } else if (state !== "0") {
            square.parentElement.classList.add( "opponent-user");
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

function placeMove(square) {
    const gameId = "ab12-3cd4-e5f6-78gh";

    const userSymbol = document.getElementById('this-user-symbol').value;
    const playerOneActive = document.getElementById('player-one-active').value;
    const playerTwoActive = document.getElementById('player-two-active').value;
    const gameComplete = document.getElementById('game-complete').value;

    if (gameComplete === 'True') return;
    if (userSymbol === '1' && playerTwoActive === 'True') return;
    if (userSymbol === '2' && playerOneActive === 'True') return;

    if (document.getElementById(`square-${square}`).getElementsByClassName("square")[0].innerHTML !== '') {
        return;
    }

    $.get(`/game/${gameId}/place-move/${thisUserId}/${square}`);
    location.reload();
}

init();