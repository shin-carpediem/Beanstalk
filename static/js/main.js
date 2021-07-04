"use strict";

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

const cartPlusMinus = () => {
  let cartNum = document.getElementById("cart-num");
  let cartNumVal = cartNum.value;
  console.log(cartNumVal);
  const cartMinus = document.getElementById("cart-minus");
  const cartPlus = document.getElementById("cart-plus");

  cartMinus.addEventListener("click", () => {
    if (cartNumVal > 1) {
      cartNumVal = cartNumVal - 1;
      console.log(cartNumVal);
    }
  });

  cartPlus.addEventListener("click", () => {
    cartNumVal = cartNumVal + 1;
    console.log(cartNumVal);
  });
};
cartPlusMinus();
