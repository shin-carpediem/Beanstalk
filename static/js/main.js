"use strict";

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
