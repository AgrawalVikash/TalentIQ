
// window.onblur = () => fetch('/proctoring-focus-loss', {method: 'POST'});


// function reportFocusLoss() {
//   fetch('/proctoring-focus-loss', { method: 'POST' });
// }

// window.onblur = reportFocusLoss;

// document.addEventListener('visibilitychange', () => {
//   if (document.visibilityState === 'hidden') {
//     reportFocusLoss();
//   }
// });

let lostFocusStart = null;

window.addEventListener("blur", () => {
    lostFocusStart = new Date();
    fetch("/log_tab_switch", {method: "POST"});
});

window.addEventListener("focus", () => {
    if (lostFocusStart) {
        const duration = (new Date() - lostFocusStart) / 1000;
        console.log(`Focus lost for ${duration} seconds`);
        lostFocusStart = null;
    }
});

