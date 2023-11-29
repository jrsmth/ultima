$(document).ready(function() {
    // Toggle radio selection
    $('.field > .selection').click(function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');

        $('#game-mode')[0].value = $('.selected')[0].innerHTML.toLowerCase();
        $('#player-mode')[0].value = $('.selected')[1].innerHTML.toLowerCase();
    });

    // Toggle game mode display
    $('#game-id').on('input', function() {
        const inputLength = $(this)[0].value.length;

        if (inputLength === 0) {
            $('.form-control.radio').removeClass('hide');
            $('#game-mode')[0].value = ""
            $('#player-mode')[0].value = ""

            $('.field.radio > .selection').removeClass('selected');
        }

        if (inputLength > 0) {
            $('.form-control.radio').addClass('hide');
            $('#game-mode')[0].value = ""
            $('#player-mode')[0].value = ""
        }
    });

});

function login() {
    setVelocity(1);
    setDensity(10000);
    setBrightness(10);
    makeStars();

    $('#login-section')[0].style.display = 'none';
    $('#login-loader')[0].style.display = 'block';

    setTimeout(() => {
        $('#login-form')[0].submit();
    }, 1000);
}

