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
// if (path.indexOf("login") > -1) {
//   const loginBtnDisable = () => {
//     const loginBtn = document.getElementById("loginBtn");
//     loginBtn.addEventListener("click", () => {
//       loginBtn.classList.add("el__dactivate");
//     });
//   };
//   loginBtnDisable();
// }

if (path.indexOf("order_manage") > -1) {
  // const manageMenu = () => {
  //   const manage = document.getElementById("manageMenu");
  //   manage.addEventListener("click", () => {
  //     const answer = confirm(
  //       "メニューの編集画面に移りますか？（営業時間内の変更はお客様に変更内容が即時反映されますので、極力お避けください）"
  //     );
  //     if (answer) {
  //       window.location.href = "/manage/menu/";
  //     }
  //   });
  // };
  // manageMenu();

  const statusChange = () => {
    try {
      const cooking = document.getElementById("cooking");
      // const chancel = document.getElementById("chancel");
      const done = document.getElementById("done");

      const cookingRadio = document.getElementById("cookingRadio");
      // const chancelRadio = document.getElementById("chancelRadio");
      const doneRadio = document.getElementById("doneRadio");

      cooking.addEventListener("click", () => {
        cookingRadio.click();
      });
      // chancel.addEventListener("click", () => {
      //   chancelRadio.click();
      // });
      done.addEventListener("click", () => {
        doneRadio.click();
      });
    } catch (e) {
      console.log(e);
    }
  };
  statusChange();
}

// if (path.indexOf("order_manage/history/total") > -1) {
//   const total = () => {
//     const subTotal = document.getElementById("subTotal");
//     const sumOfTable = document.getElementById("sumOfTable");

//     const subTotalVal = subTotal.value;

//   };
//   total();
// }

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

// if ((path.indexOf("cart") > -1) | (path.indexOf("history") > -1)) {
//   const orderConfirm = () => {
//     const orderStop = document.getElementById("orderConfirm");
//     orderStop.addEventListener("click", () => {
//       const answer = confirm("注文しますか？");
//       if (answer) {
//         if (path.indexOf("cart") > -1) {
//           // orderStop.click();
//           window.location.href = "/menu/";
//         }
//         if (path.indexOf("history") > -1) {
//           // orderStop.click();
//           window.location.href = "/history/";
//         }
//       }
//     });
//   };
//   orderConfirm();
// }

// if (path.indexOf("history") > -1) {
//   const orderStopConfirm = () => {
//     const orderStop = document.getElementById("orderStopConfirm");
//     orderStop.addEventListener("click", () => {
//       const answer = confirm("オーダーストップしてお会計に移りますか？");
//       if (answer) {
//         window.location.href = "/stop/";
//       }
//     });
//   };
//   orderStopConfirm();
// }

// if (path.indexOf("filter") > -1) {
//   const startNomihoConfirm = () => {
//     const startNomiho = document.getElementById("startNomiho");
//     startNomiho.addEventListener("click", () => {
//       const answer = confirm("飲み放題を開始しますか？");
//       if (answer) {
//         window.location.href = "/nomiho/";
//       }
//     });
//   };
//   startNomihoConfirm();
// }
