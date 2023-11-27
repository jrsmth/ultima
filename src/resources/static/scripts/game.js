let userId;
let gameState;
let socket;
let appUrl;

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
    threeboard.addClass('active');
    threeboard.empty();

    for (let i = 0; i < 9; i++) {
        const classList = getSquareClass(board[i], thisSymbol);
        const markup =
        `
            <div class="shadow" id="three-${i}">
                <div class="square ${classList}" onclick="placeStandardMove(${i})">${markupSymbol(board[i])}</div>
            </div>
        `;

        threeboard.append(markup);
    }
}

function initUltimateBoard(userId, thisSymbol, board) {
    const nineboard = $('#nine-board');
    nineboard.addClass('active');
    nineboard.empty();

    const outerStates = gameState["outer_states"];
    for (let i = 0; i < 9; i++) {
        let innerSquares = '';
        let outerClasses = '';
        if (outerStates[i] === 2) { outerClasses += "draw" }
        if (outerStates[i] === 3) { outerClasses += (thisSymbol === 1 ? "this-user" : "opponent") }
        if (outerStates[i] === 4) { outerClasses += (thisSymbol === 2 ? "this-user" : "opponent") }

        const playableSquare = (gameState["playable_square"] === -1) || (gameState["playable_square"] === i);
        const notTaken = (outerStates[i] === 1);
        const playable = playableSquare && notTaken;
        if (playable) outerClasses += 'playable';

        for (let j = 0; j < 9; j++) {
            let classList = '';
            if (!outerClasses.includes("this-user") && !outerClasses.includes("opponent")) {
                classList = getSquareClass(board[i][j], thisSymbol);
            }

            innerSquares +=
                `
                    <div class="shadow inner" id="nine-${i}-${j}">
                        <div class="square ${classList}" onclick="placeUltimateMove(${i}, ${j})">
                            ${markupSymbol(board[i][j])}
                        </div>
                    </div>
                `
        }

        const outerSquare =
            `
                <div class="shadow outer ${outerClasses}" id="nine-${i}">
                    <div class="square">
                        ${innerSquares}
                    </div>
                </div>
            `

        nineboard.append(outerSquare);
    }
}

function placeStandardMove(index) {
    if (allowedToPlace(index)) {
        $.get(`/game/${gameState['game_id']}/place-move/${userId}/${index}`)
            .catch(err => {
                    console.error(`[placeStandardMove] Error placing move for square with index [${index}]`);
                    console.error(err);
                }
            );
        // TODO :: disallow a second user click whilst first is processing...
    }
}

function placeUltimateMove(outerIndex, innerIndex) {
    const outerSquare = $(`#nine-${outerIndex}`);
    const innerSquare = $(`#nine-${outerIndex}-${innerIndex}`);

    const innerSquareComplete = innerSquare.find('.square')[0].innerHTML.trim() !== '';
    const outerSquareComplete = outerSquare.hasClass('this-user') ||
                                outerSquare.hasClass('opponent') ||
                                outerSquare.hasClass('draw');

    const canPlace = allowedToPlace(outerIndex, innerIndex) &&
                     outerSquare.hasClass('playable') &&
                     !innerSquareComplete &&
                     !outerSquareComplete

    if (canPlace) {
        $.get(`/game/${gameState['game_id']}/place-move/${userId}/${outerIndex}/${innerIndex}`)
            .catch(err => {
                    console.error(`[placeStandardMove] Error placing move for square with index [${index}]`);
                    console.error(err);
                }
            );
        // TODO :: disallow a second user click whilst first is processing...
    }
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
    socket = io.connect(appUrl);

    console.log(socket); // FixMe

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
    return '';
}

function allowedToPlace(outer, inner) {
    const gameStarted = (gameState['player_two']['name'] !== "");
    const gameIncomplete = !gameState['complete'];
    const alreadyPlayed = gameState['game_mode'] === "standard" ?
                          gameState['board'][outer] !== 0 :
                          gameState['board'][outer][inner] !== 0;
    return gameStarted && gameIncomplete && isUserTurn() && !alreadyPlayed;
}