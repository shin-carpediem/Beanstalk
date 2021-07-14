"use strict";

lazyload();

const loading_icon = document.getElementById("loading_icon");
const loading_show = () => {
  loading_icon.classList.remove("prop_hide");
};
loading_show();

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
