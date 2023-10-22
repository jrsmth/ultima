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
        } else if (state !== "b'0'") {
            square.parentElement.classList.add( "opponent-user");
        }

        if (state === "b'0'") {
            square.innerHTML = '';
        } else if (state === "b'1'") {
            square.innerHTML = '<i class="fa-regular fa-circle symbol"></i>'
        } else if (state === "b'2'") {
            square.innerHTML = '<i class="fa fa-times symbol"></i>'
        }
    }

}

function placeMove(square) {
    const gameId = "ab12-3cd4-e5f6-78gh";

    $.get(`/game/${gameId}/place-move/${thisUserId}/${square}`);
    location.reload();
}

init();