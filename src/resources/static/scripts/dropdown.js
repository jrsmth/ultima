//Multiple options dropdown
//https://codepen.io/gatoledo1/pen/QWmpWjK

const optionMenu = document.querySelector(".game-dropdown"),
    selectBtn = optionMenu.querySelector(".select-btn"),
    options = optionMenu.querySelectorAll(".option"),
    sBtn_text = optionMenu.querySelector(".select-btn-text");

selectBtn.addEventListener("click", () =>
    optionMenu.classList.toggle("active")
);

options.forEach((option) => {
    option.addEventListener("click", () => {
        selectBtn.classList.remove("touched")
        const newOption = option.querySelector(".option-text").innerText;
        const radio = $('.radio');
        let gameId;

        if (newOption === 'New Game') {
            radio.removeClass("hide");
            gameId = '';
        } else {
            radio.addClass("hide");
            gameId = newOption;
        }

        $('#game-id')[0].value = gameId;
        sBtn_text.innerText = newOption;

        optionMenu.classList.remove("active");
        selectBtn.classList.add("touched")
    });
});
