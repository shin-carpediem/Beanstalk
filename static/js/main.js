"use strict";

lazyload();

// loading
const loading_show = () => {
  const loading_icon = document.getElementById("loading_icon");
  const fullWrapper = document.getElementById("fullWrapper");

  loading_icon.classList.remove("prop_hide");
  fullWrapper.classList.add("el__deactivate");
};
loading_show();

const loading_hide = () => {
  const loading_icon = document.getElementById("loading_icon");
  const fullWrapper = document.getElementById("fullWrapper");

  loading_icon.classList.add("prop_hide");
  fullWrapper.classList.remove("el__deactivate");
};
loading_hide();

let path = window.location.href;

if (path == "/order_manage/") {
  const manageMenuConfirm = () => {
    const manageMenu = document.getElementById("manageMenu");

    manageMenu.addEventListener("click", () => {
      const answer = confirm("この画面から離れますが問題ありませんか？");
      if (answer) {
        window.location.href = "/manage/menu/";
      }
    });
  };
  manageMenuConfirm();
}

if (path.indexOf("detail") > -1) {
  let cartPlusMinus = () => {
    let cartNum = document.getElementById("cartNum");
    let NumVal = cartNum.value;
    let num = parseInt(NumVal);

    const cartMinus = document.getElementById("cartMinus");
    const cartPlus = document.getElementById("cartPlus");

    cartMinus.addEventListener("click", () => {
      if (num > 1) {
        num = num - 1;
        cartNum.value = num;
      }
    });

    cartPlus.addEventListener("click", () => {
      num = num + 1;
      cartNum.value = num;
    });
  };
  cartPlusMinus();
}
