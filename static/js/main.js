"use strict";

let path = window.location.pathname;

if ((path === "/menu/") | (path === "/filter/")) {
  const ClickMenu = () => {
    const menu = document.getElementById("menu");
    const menu_btn = document.getElementById("menu_btn");

    menu.addEventListener("click", () => {
      menu_btn.click();
    });
  };
  ClickMenu();
}

if (path === "/cart/") {
  const ClickCartTop = () => {
    const cart_top = document.getElementById("cart_top");
    const cart_top_btn = document.getElementById("cart_top_btn");

    cart_top.addEventListener("click", () => {
      cart_top_btn.click();
    });
  };
  ClickCartTop();
}

// TODO:
const ClickCart = () => {
  const cart = document.getElementById("cart");
  const cart_btn = document.getElementById("cart_btn");

  cart.addEventListener("click", () => {
    cart_btn.click();
  });
};
ClickCart();

// TODO:
const ClickOrder = () => {
  const order = document.getElementById("order");
  const order_btn = document.getElementById("order_btn");

  order.addEventListener("click", () => {
    order_btn.click();
  });
};
ClickOrder();
