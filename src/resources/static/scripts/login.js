$(document).ready(function() {
    $('.field > .selection').click(function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');

        const gameMode = document.getElementById('game-mode');
        gameMode.value = document.getElementsByClassName('selected')[0].innerHTML.toUpperCase();
    });
});