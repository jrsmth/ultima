let userId;
let gameId;

async function init(gameId) { // TODO :: convert all to JQuery?
    let gameState;
    userId = $('#user-id')[0].value; // Question :: better way?

    // Retrieve game state
    await $.get(`/game/state/${gameId}`).then(res => {
        console.debug("Initialising game state");
        console.debug(res);
        gameState = res;

    }).catch(err => {
        console.error(err);
    });

    // Init user info
    const thisUser = [gameState['player_one'], gameState['player_two']].filter(obj => {
        return obj.name === userId
    })

    const playerOne = gameState['player_one']['name'];
    const playerTwo = gameState['player_two']['name'];
    $('#player-one-name')[0].innerText = playerOne;
    $('#player-two-name')[0].innerText = playerTwo;

    const playerTurn = gameState['player_turn'];
    $('#player-one')
        .addClass(playerTurn === 1 ? ' active' : '')
        .addClass(userId === playerOne ? ' this-user' : '');
    $('#player-two')
        .addClass(playerTurn === 2 ? ' active' : '')
        .addClass(userId === playerTwo ? ' this-user' : '');
    $('#cross')
        .addClass(playerTurn === 1 ? ' active' : '')
        .addClass(userId === playerOne ? ' this-user' : '');
    $('#circle')
        .addClass(playerTurn === 2 ? ' active' : '')
        .addClass(userId === playerTwo ? ' this-user' : '');

    // Init board
    if (gameState['game_mode'] === "standard") createStandardBoard(userId, thisUser['symbol'], gameState['board']);
    if (gameState['game_mode'] === "ultimate") createUltimateBoard(userId, thisUser['symbol'], gameState['board']);

}

function createStandardBoard(userId, thisSymbol, board) {
    const threeboard = $('#three-board');

    threeboard.empty();
    for (let i = 0; i < 9; i++) {
        const classList = (board[i] === thisSymbol) ? 'this-user' : (board[i] !== 0) ? 'opponent' : '';
        const markup =
        `
            <div class="shadow" id="three-${i}">
                <div class="square ${classList}" onClick="placeStandardMove(${i})">${markupSymbol(board[i])}</div>
            </div>
        `;

        threeboard.append(markup);
    }
}

function createUltimateBoard(userId, thisSymbol) {
    const innerStates = JSON.parse(document.getElementById("inner-states").value);
    const playableSquare = document.getElementById("playable-square").value;
    console.log(playableSquare)

    for (let i = 0; i < 9; i++) {
        const outerSquare = document.getElementById(`nine-square-${i}`);

        if (innerStates[i] === 2) { outerSquare.classList.add("draw") }
        if (innerStates[i] === 3) { outerSquare.classList.add(thisSymbol === '1' ? "this-user" : "opponent-user"); console.log(i) }
        if (innerStates[i] === 4) { outerSquare.classList.add(thisSymbol === '2' ? "this-user" : "opponent-user") }

        if (
            (playableSquare === "-1" || playableSquare === i.toString()) &&
            (!outerSquare.classList.contains("this-user") && !outerSquare.classList.contains("opponent-user") && !outerSquare.classList.contains("draw"))
        ) { outerSquare.classList.add("playable") }

        let outerBoard = []
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

            outerBoard.push(innerState)
        }

        // // if outerSquare has a win or lose status, apply colouring and prevent selection...
        // // how to obtain status? outer_board array? or can we generate that here(!)
        // // make a request to the backend to tell if the board is complete?
        // // if count of 1 > 3 or count 2 > 3, make the call to get game state for that square
        // $.get(`/game/${gameId}/state//${outerSquare}`)
        //     .then((res) => {
        //         if (res === "Status.PLAYER_ONE_WINS") {
        //             // Add class to the outer square, depending on thisPlayer
        //         } else if (res === "Status.PLAYER_TWO_WINS") {
        //             // Add class to the outer square, depending on thisPlayer
        //         }
        //     })
        //     .catch((e) => {
        //         console.log(`Error getting the [${outerSquare}] game state for game with ID [${gameId}]`);
        //         console.log(e);
        //     })
        //
        // // Question :: would an outer board array we more performant?
    }
}

function placeStandardMove(square) {
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

    $.get(`/game/${gameId}/place-move/${userId}/${square}`); // TODO :: err handle
    // location.reload();
}

// Place Ultimate Move
function placeUltimateMove(outerSquare, innerSquare) {
    const userSymbol = document.getElementById('this-user-symbol').value;
    const playerOneActive = document.getElementById('player-one-active').value;
    const playerTwoActive = document.getElementById('player-two-active').value;
    const gameComplete = document.getElementById('game-complete').value;

    if (gameComplete === 'True') return;
    if (userSymbol === '1' && playerTwoActive === 'True') return;
    if (userSymbol === '2' && playerOneActive === 'True') return;

    // Disallow if square not playable
    const outerSquareClasses = document.getElementById(`nine-square-${outerSquare}`).classList;
    if (!outerSquareClasses.contains('playable')) return

    // Disallow if inner square complete
    if (document.getElementById(`nine-square-${outerSquare}-${innerSquare}`).getElementsByClassName("square")[0].innerHTML !== '') {
        return;
    }

    // Disallow if outer square complete
    if (outerSquareClasses.contains('this-user') || outerSquareClasses.contains('opponent-user') || outerSquareClasses.contains('draw')) {
        return;
    }

    $.get(`/game/${gameId}/place-move/${userId}/${outerSquare}/${innerSquare}`);
    location.reload();
}

function enableCopy() { // TODO :: switch to jquery
    const copyGameId = document.getElementById("copy-game-id");
    const span = copyGameId.querySelector("span");
    span.onclick = function () {
        document.execCommand("copy");
    }

    // TODO :: revisit the animation and styling
    span.addEventListener("copy", function (event) {
        event.preventDefault();
        if (event.clipboardData) {
            event.clipboardData.setData("text/plain", span.textContent);
            const copy = copyGameId.getElementsByClassName("fa-copy")[0];
            const check = copyGameId.getElementsByClassName("fa-check")[0];

            copy.style.display = 'none';
            $(check).addClass("ticked");
            setTimeout((function () {
                $(check).removeClass('ticked');
                copy.style.display = 'block';
                $(copy).addClass("fade-in");
            }), 1000);
        }
    });
}

function restart() {
    const formData = {
        name: document.getElementById("this-user-id").value,
        gameId: gameId,
        gameMode: document.getElementById("game-mode").value,
        playerMode: document.getElementById("player-mode").value,
        restart: true
    }

    $.post('/', formData);
    location.reload();
}

function connectSocket(gameId) {
    // const socket = io();
    const socket = io.connect('http://localhost:8080'); // ??

    // const socket = io();
    console.log(socket);

    socket.on('connect', function() {
        console.log('connected');
        socket.emit('my event', {data: 'I\'m connected!'}); // TODO :: user specific msg? 'James has joined'?
    });

    // socket.on('connect', function() {
    //     socket.emit('my event', {data: 'I\'m connected!'});
    // });
    //
    socket.on('my_response', function(msg) {
        console.log(msg.data);
    });

    socket.on('update_game_state', function(message) {
        console.debug('Game state update received');
        init(message['game_id']);
    });
}

function markupSymbol(value) {
    if (value === 0) return '';
    if (value === 1) return '<i class="fa fa-times symbol"></i>';
    if (value === 2) return '<i class="fa-regular fa-circle symbol"></i>';
}