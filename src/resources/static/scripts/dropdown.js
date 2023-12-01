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
        sBtn_text.innerText = option.querySelector(".option-text").innerText;
        optionMenu.classList.remove("active");
    });
});
