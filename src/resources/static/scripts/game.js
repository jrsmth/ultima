let userId;
let gameState;
let socket;

async function init(gameId) {
    // Retrieve game state
    await $.get(`/game/state/${gameId}`).then(res => {
        console.debug("Initialising game state");
        console.debug(res);
        gameState = res;

    }).catch(err => {
        console.error(err);
    });

    const thisPlayer = [gameState['player_one'], gameState['player_two']].filter(obj => {
        return obj.name === userId
    })[0];

    // Init user info
    initUserInfo(thisPlayer);

    // Init board
    if (gameState['game_mode'] === "standard") initStandardBoard(userId, thisPlayer['symbol'], gameState['board']);
    if (gameState['game_mode'] === "ultimate") initUltimateBoard(userId, thisPlayer['symbol'], gameState['board']);

}

function initUserInfo(thisPlayer) {
    const playerOneName = gameState['player_one']['name'];
    const playerTwoName = gameState['player_two']['name'];
    $('#player-one-name')[0].innerText = playerOneName;
    $('#player-two-name')[0].innerText = playerTwoName;

    const playerTurn = gameState['player_turn'];
    const playerOne = $('#player-one');
    const playerTwo = $('#player-two');
    const cross = $('#cross');
    const circle = $('#circle');

    playerOne.removeClass('active');
    playerTwo.removeClass('active');
    cross.removeClass('active');
    circle.removeClass('active');

    const gameStarted = (playerTwoName !== "");
    const gameInProgress = gameStarted && !gameState['complete'];
    if (gameInProgress) {
        playerOne
            .addClass(playerTurn === 1 ? ' active' : '')
            .addClass(userId === playerOneName ? ' this-user' : '');
        playerTwo
            .addClass(playerTurn === 2 ? ' active' : '')
            .addClass(userId === playerTwoName ? ' this-user' : '');
        cross
            .addClass(playerTurn === 1 ? ' active' : '')
            .addClass(userId === playerOneName ? ' this-user' : '');
        circle
            .addClass(playerTurn === 2 ? ' active' : '')
            .addClass(userId === playerTwoName ? ' this-user' : '');

    }

    initNotification(thisPlayer["notification"]);
}

function initNotification(playerNotification) {
    const playerTurn = $('#player-turn');
    const notification = $('#notification');
    const notificationContent = $('#notification-content');
    notificationContent.empty();

    if (playerNotification["active"]) {
        playerTurn.addClass('hide');
        notification.addClass('active');
        notification.addClass(playerNotification["mood"]);

        notificationContent.append(
            `
                <h3>${playerNotification["title"]}</h3>
                <p>${playerNotification["content"]}</p>
            `
        );

    } else {
        playerTurn.removeClass('hide');
        notification.removeClass();
    }
}

function initStandardBoard(userId, thisSymbol, board) {
    const threeboard = $('#three-board');

    threeboard.empty();
    for (let i = 0; i < 9; i++) {
        const classList = getSquareClass(board[i], thisSymbol);
        const markup =
        `
            <div class="shadow" id="three-${i}">
                <div class="square ${classList}" onClick="placeStandardMove(${i})">${markupSymbol(board[i])}</div>
            </div>
        `;

        threeboard.append(markup);
    }
}

function initUltimateBoard(userId, thisSymbol) {
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

function placeStandardMove(index) {
    const gameNotStarted = (gameState['player_two']['name'] === "");
    const gameComplete = gameState['complete'];
    const opponentTurn = !isUserTurn();
    const alreadyPlayed = gameState['board'][index] !== 0;
    if (gameNotStarted || gameComplete || opponentTurn || alreadyPlayed) return;

    $.get(`/game/${gameState['game_id']}/place-move/${userId}/${index}`)
        .catch(err => {
            console.error(`[placeStandardMove] Error placing move for square with index [${index}]`);
            console.error(err);
        }
    )
}

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
    socket.emit('restart', {
        gameId: gameState["game_id"],
        userId: userId
    });
}

function connectSocket(gameId) {
    // const socket = io();
    socket = io.connect('http://localhost:8080'); // ??

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

function isUserTurn() {
    return (gameState['player_turn'] === 1 && gameState['player_one']['name'] === userId) ||
           (gameState['player_turn'] === 2 && gameState['player_two']['name'] === userId);
}

function getSquareClass(square, thisSymbol) {
    if (square === thisSymbol) return 'this-user';
    if (square !== 0) return 'opponent';
    if (!isUserTurn() || (gameState['player_two']['name'] === "")) return 'inactive';
}