"use strict";

// common
lazyload();

let path = window.location.href;

// loading
const loading_icon = document.getElementById("loading_icon");

const loading_show = () => {
  loading_icon.classList.remove("el__hide");
};
loading_show();

const loading_hide = () => {
  loading_icon.classList.add("el__hide");
};
loading_hide();

// restaurant
if (path.indexOf("login") > -1) {
  const loginBtnDisable = () => {
    const loginBtn = document.getElementById("loginBtn");
    loginBtn.addEventListener("click", () => {
      loginBtn.classList.add("el__dactivate");
    });
  };
  loginBtnDisable();
}

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

// customer
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
