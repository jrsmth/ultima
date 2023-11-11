$(document).ready(function() {
    // Toggle radio selection
    $('.field > .selection').click(function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');

        $('#game-mode')[0].value = $('.selected')[0].innerHTML.toUpperCase();
    });

    // Toggle game mode display
    $('#game-id').on('input', function() {
        const inputLength = $(this)[0].value.length;

        if (inputLength === 0) {
            $('.form-control.radio').removeClass('hide');
            $('#game-mode')[0].value = ""

            $('.field.radio > .selection').removeClass('selected');
        }

        if (inputLength > 0) {
            $('.form-control.radio').addClass('hide');
            $('#game-mode')[0].value = ""
        }
    });

});
