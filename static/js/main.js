"use strict";

const logoutConfirm = () => {
  const logout = document.getElementById("logout");

  logout.addEventListener("click", () => {
    const answer = confirm("ログアウトしますか？");
    if (answer) {
      window.location.href = "/logout/";
    }
  });
};
logoutConfirm();

const ClickMenu = () => {
  const menu = document.getElementById("menu");
  const menu_btn = document.getElementById("menu_btn");

  menu.addEventListener("click", () => {
    menu_btn.click();
  });
};
ClickMenu();
