/* ============================================
   neko.js - 画面をうろうろする猫
   ============================================ */

(function() {
  var CATS = [
    { emoji: "\uD83D\uDC31", name: "みけ" },
    { emoji: "\uD83D\uDC08", name: "たま" },
    { emoji: "\uD83D\uDC31", name: "しろ" },
    { emoji: "\uD83D\uDC08", name: "ちゃちゃ" },
    { emoji: "\uD83D\uDC36", name: "ぽち" },
    { emoji: "\uD83D\uDC15", name: "らっきー" },
    { emoji: "\uD83D\uDC29", name: "こたろう" },
    { emoji: "\uD83E\uDDAE", name: "ここあ" }
  ];

  var SOUNDS = [
  "ぷるわん!","ぷるにゃ！","こんにちは！！！！","よろしくお願いします。","お疲れさまでした。"
  ];

 
  var catElements = [];
  var animationIds = [];
  var isActive = localStorage.getItem("nekoCats") !== "false";

  /* ── 初期化 ── */
  function init() {
    addStyles();
    createToggleButton();
    if (isActive) {
      spawnCats();
    }
  }

  /* ── CSS追加 ── */
  function addStyles() {
    var style = document.createElement("style");
    style.textContent =
      "@keyframes catBounce {" +
      "  0%, 100% { transform: translateY(0); }" +
      "  50% { transform: translateY(-6px); }" +
      "}" +
      "@keyframes catBounceMirror {" +
      "  0%, 100% { transform: translateY(0) scaleX(-1); }" +
      "  50% { transform: translateY(-6px) scaleX(-1); }" +
      "}" +
      "@keyframes catIdle {" +
      "  0%, 100% { transform: rotate(0deg); }" +
      "  25% { transform: rotate(-3deg); }" +
      "  75% { transform: rotate(3deg); }" +
      "}" +
      "@keyframes speechPop {" +
      "  0% { transform: translateX(-50%) scale(0); opacity: 0; }" +
      "  50% { transform: translateX(-50%) scale(1.2); opacity: 1; }" +
      "  100% { transform: translateX(-50%) scale(1); opacity: 1; }" +
      "}" +
      "@keyframes speechFade {" +
      "  to { opacity: 0; transform: translateX(-50%) translateY(-20px); }" +
      "}" +
      ".neko-cat {" +
      "  position: fixed;" +
      "  z-index: 99990;" +
      "  font-size: 32px;" +
      "  cursor: pointer;" +
      "  user-select: none;" +
      "  transition: left 0.05s linear, top 0.05s linear;" +
      "  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));" +
      "}" +
      ".neko-cat.walking .neko-emoji {" +
      "  display: inline-block;" +
      "  animation: catBounce 0.4s ease-in-out infinite;" +
      "}" +
      ".neko-cat.walking.face-left .neko-emoji {" +
      "  animation: catBounceMirror 0.4s ease-in-out infinite;" +
      "}" +
      ".neko-cat.idle .neko-emoji {" +
      "  display: inline-block;" +
      "  animation: catIdle 2s ease-in-out infinite;" +
      "}" +
      ".neko-cat.sleeping .neko-emoji {" +
      "  display: inline-block;" +
      "  opacity: 0.7;" +
      "}" +
      ".neko-cat.face-left .neko-emoji {" +
      "  display: inline-block;" +
      "  transform: scaleX(-1);" +
      "}" +
      ".neko-speech {" +
      "  position: absolute;" +
      "  bottom: 100%;" +
      "  left: 50%;" +
      "  transform: translateX(-50%);" +
      "  background: #fff;" +
      "  border: 2px solid #111;" +
      "  border-radius: 12px;" +
      "  padding: 4px 10px;" +
      "  font-size: 12px;" +
      "  font-weight: 700;" +
      "  white-space: nowrap;" +
      "  animation: speechPop 0.3s ease forwards;" +
      "  pointer-events: none;" +
      "}" +
      ".neko-speech.fade {" +
      "  animation: speechFade 0.5s ease forwards;" +
      "}" +
      ".neko-speech::after {" +
      "  content: '';" +
      "  position: absolute;" +
      "  top: 100%;" +
      "  left: 50%;" +
      "  transform: translateX(-50%);" +
      "  border: 6px solid transparent;" +
      "  border-top-color: #111;" +
      "}" +
      "#neko-toggle {" +
      "  position: fixed;" +
      "  bottom: 90px;" +
      "  left: 30px;" +
      "  width: 42px;" +
      "  height: 42px;" +
      "  border-radius: 50%;" +
      "  border: 2px solid #888;" +
      "  background: rgba(255,255,255,0.9);" +
      "  backdrop-filter: blur(10px);" +
      "  font-size: 18px;" +
      "  cursor: pointer;" +
      "  z-index: 99991;" +
      "  box-shadow: 0 2px 8px rgba(0,0,0,0.1);" +
      "  transition: all 0.3s ease;" +
      "  display: flex;" +
      "  align-items: center;" +
      "  justify-content: center;" +
      "}" +
      "#neko-toggle:hover {" +
      "  transform: scale(1.1);" +
      "  box-shadow: 0 4px 16px rgba(0,0,0,0.15);" +
      "}" +
      "#neko-toggle.off {" +
      "  opacity: 0.5;" +
      "}";
    document.head.appendChild(style);
  }

  /* ── ON/OFFボタン ── */
  function createToggleButton() {
    var btn = document.createElement("button");
    btn.id = "neko-toggle";
    btn.type = "button";
    btn.title = "ねこ ON/OFF";
    btn.textContent = "\uD83D\uDC31";
    if (!isActive) btn.classList.add("off");

    btn.addEventListener("click", function() {
      isActive = !isActive;
      localStorage.setItem("nekoCats", isActive);
      if (isActive) {
        btn.classList.remove("off");
        spawnCats();
      } else {
        btn.classList.add("off");
        removeCats();
      }
    });

    document.body.appendChild(btn);
  }

  /* ── 猫を生成 ── */
  function spawnCats() {
    for (var i = 0; i < CATS.length; i++) {
      createCat(CATS[i], i);
    }
  }

  /* ── 猫を削除 ── */
  function removeCats() {
    for (var i = 0; i < catElements.length; i++) {
      if (catElements[i] && catElements[i].parentNode) {
        catElements[i].parentNode.removeChild(catElements[i]);
      }
    }
    catElements = [];
    for (var j = 0; j < animationIds.length; j++) {
      clearTimeout(animationIds[j]);
    }
    animationIds = [];
  }

  /* ── 猫を1匹作成 ── */
  function createCat(catData, index) {
    var el = document.createElement("div");
    el.className = "neko-cat idle";

    var emoji = document.createElement("span");
    emoji.className = "neko-emoji";
    emoji.textContent = catData.emoji;
    el.appendChild(emoji);

    /* 初期位置（ランダム） */
    var startX = Math.random() * (window.innerWidth - 60) + 20;
    var startY = Math.random() * (window.innerHeight - 60) + 20;
    el.style.left = startX + "px";
    el.style.top = startY + "px";

    /* クリックで鳴く */
    el.addEventListener("click", function(e) {
      e.stopPropagation();
      speak(el);
    });

    document.body.appendChild(el);
    catElements.push(el);

    /* 行動開始（少しずらす） */
    var delay = index * 800 + Math.random() * 1000;
    var id = setTimeout(function() {
      catBehavior(el);
    }, delay);
    animationIds.push(id);
  }

  /* ── 猫の行動ループ ── */
  function catBehavior(el) {
    if (!isActive) return;
    if (!el.parentNode) return;

    var action = Math.random();

    if (action < 0.6) {
      /* 歩く */
      walk(el, function() {
        var id = setTimeout(function() { catBehavior(el); }, 100);
        animationIds.push(id);
      });
    } else if (action < 0.85) {
      /* 休憩 */
      el.className = "neko-cat idle";
      var idleTime = 2000 + Math.random() * 3000;
      var id = setTimeout(function() { catBehavior(el); }, idleTime);
      animationIds.push(id);
    } else {
      /* 寝る */
      el.className = "neko-cat sleeping";
      var zzz = document.createElement("span");
      zzz.style.cssText = "position:absolute; top:-16px; right:-8px; font-size:12px;";
      zzz.textContent = "zzZ";
      el.appendChild(zzz);
      var sleepTime = 3000 + Math.random() * 5000;
      var id = setTimeout(function() {
        if (zzz.parentNode) zzz.parentNode.removeChild(zzz);
        catBehavior(el);
      }, sleepTime);
      animationIds.push(id);
    }
  }

  /* ── 歩く ── */
  function walk(el, callback) {
    var currentX = parseFloat(el.style.left) || 0;
    var currentY = parseFloat(el.style.top) || 0;

    /* ランダムな方向に歩く */
    var angle = Math.random() * Math.PI * 2;
    var distance = 80 + Math.random() * 200;
    var targetX = currentX + Math.cos(angle) * distance;
    var targetY = currentY + Math.sin(angle) * distance;

    /* 画面内に収める */
    var maxX = window.innerWidth - 50;
    var maxY = window.innerHeight - 50;
    if (targetX < 10) targetX = 10;
    if (targetX > maxX) targetX = maxX;
    if (targetY < 10) targetY = 10;
    if (targetY > maxY) targetY = maxY;

    /* ★ 猫の絵文字だけ反転（吹き出しはそのまま） */
    if (targetX < currentX) {
      el.className = "neko-cat walking face-left";
    } else {
      el.className = "neko-cat walking";
    }

    /* 歩くアニメーション（少しずつ移動） */
    var steps = 30 + Math.floor(Math.random() * 30);
    var stepX = (targetX - currentX) / steps;
    var stepY = (targetY - currentY) / steps;
    var step = 0;

    function doStep() {
      if (!isActive || !el.parentNode) return;
      if (step >= steps) {
        if (callback) callback();
        return;
      }
      step++;
      currentX += stepX;
      currentY += stepY;
      el.style.left = currentX + "px";
      el.style.top = currentY + "px";
      var id = setTimeout(doStep, 40 + Math.random() * 20);
      animationIds.push(id);
    }
    doStep();
  }

  /* ── 鳴く（吹き出し） ── */
  function speak(el) {
    var existing = el.querySelector(".neko-speech");
    if (existing) existing.parentNode.removeChild(existing);

    var bubble = document.createElement("div");
    bubble.className = "neko-speech";
    bubble.textContent = SOUNDS[Math.floor(Math.random() * SOUNDS.length)];
    el.appendChild(bubble);

    setTimeout(function() {
      bubble.classList.add("fade");
      setTimeout(function() {
        if (bubble.parentNode) bubble.parentNode.removeChild(bubble);
      }, 500);
    }, 2000);
  }

  /* ── DOM読み込み後に初期化 ── */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
