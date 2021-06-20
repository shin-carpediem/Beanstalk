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
