/* ============================================
   neko.js - 画面をうろうろする猫
   ============================================ */

(function() {
  var CATS = [
    { emoji: "\uD83D\uDC31", name: "みけ" },
    { emoji: "\uD83D\uDC08", name: "たま" },
    { emoji: "\uD83D\uDE3D", name: "しろ" },
    { emoji: "\uD83D\uDE3B", name: "ちゃちゃ" },
    { emoji: "\uD83D\uDC36", name: "ぽち" },
    { emoji: "\uD83D\uDC15", name: "らっきー" },
    { emoji: "\uD83D\uDC29", name: "こたろう" },
    { emoji: "\uD83D\uDC29", name: "ここあ" },
  ];

  
  /* ★ 猫をクリックした時のリンク先 */
  var NAV_LINKS = [
    { label: "\uD83D\uDC31 レビューを見る！",   url: "/soso/reviews/" },
    { label: "\uD83D\uDC08 カートを見る！",     url: "/soso/cart/" },
    { label: "\uD83D\uDE3D 購入履歴にゃ！",     url: "/soso/purchaseHistory/" },
    { label: "\uD83D\uDE3B 会員情報を確認！",   url: "/soso/userInfo/" },
    { label: "\uD83D\uDC36 会員情報を変更！",   url: "/soso/updateUser/" },
    { label: "\uD83D\uDC15 ログアウトにゃ",     url: "/soso/logout/" },
    { label: "\uD83D\uDC29 管理者ログイン！",   url: "/soso/adminLogin/" },
    { label: "\uD83D\uDC29 管理者ログイン！",   url: "/soso/tetris/" },
  ];


  var SOUNDS = [
  "ぷるわん!","ぷるにゃ！","こんにちは！！！！","よろしくお願いします。","お疲れさまでした。"
  ];

 
  
 var catElements = [];
 var isActive = localStorage.getItem("nekoCats") !== "false";
 var rafId = null;

 function init() {
   addStyles();
   createToggleButton();
   if (isActive) spawnCats();
 }

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
     "  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));" +
     "  will-change: left, top;" +
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
     ".neko-speech.nav-speech {" +
     "  background: #111;" +
     "  color: #fff;" +
     "  border-color: #111;" +
     "}" +
     ".neko-speech.nav-speech::after {" +
     "  border-top-color: #111;" +
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
     "}" +
     "#neko-toggle.off {" +
     "  opacity: 0.5;" +
     "}";
   document.head.appendChild(style);
 }

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

 function spawnCats() {
   for (var i = 0; i < CATS.length; i++) {
     createCat(CATS[i], i);
   }
   startLoop();
 }

 function removeCats() {
   for (var i = 0; i < catElements.length; i++) {
     if (catElements[i].el.parentNode) {
       catElements[i].el.parentNode.removeChild(catElements[i].el);
     }
   }
   catElements = [];
   if (rafId) {
     cancelAnimationFrame(rafId);
     rafId = null;
   }
 }

 function createCat(catData, index) {
   var el = document.createElement("div");
   el.className = "neko-cat idle";

   var emoji = document.createElement("span");
   emoji.className = "neko-emoji";
   emoji.textContent = catData.emoji;
   el.appendChild(emoji);

   var startX = Math.random() * (window.innerWidth - 60) + 20;
   var startY = Math.random() * (window.innerHeight - 60) + 20;
   el.style.left = startX + "px";
   el.style.top = startY + "px";

   /* ★ クリックで喋る＋ページ遷移 */
   el.addEventListener("click", function(e) {
     e.stopPropagation();
     speakAndNavigate(el);
   });

   document.body.appendChild(el);

   catElements.push({
     el: el,
     x: startX,
     y: startY,
     targetX: startX,
     targetY: startY,
     state: "idle",
     stateTimer: Date.now() + 1000 + index * 800,
     zzz: null,
     navIndex: index % NAV_LINKS.length  /* ★ 各猫に割り当てるリンクの開始位置 */
   });
 }

 /* ★ 喋ってからページ遷移 */
 function speakAndNavigate(el) {
   /* この猫のデータを探す */
   var cat = null;
   for (var i = 0; i < catElements.length; i++) {
     if (catElements[i].el === el) {
       cat = catElements[i];
       break;
     }
   }

   /* リンク先を取得（順番に回す） */
   var link = NAV_LINKS[cat ? cat.navIndex : 0];

   /* 次回クリック用に次のリンクへ */
   if (cat) {
     cat.navIndex = (cat.navIndex + 1) % NAV_LINKS.length;
   }

   /* 既存の吹き出しを消す */
   var existing = el.querySelector(".neko-speech");
   if (existing) existing.parentNode.removeChild(existing);

   /* ★ 行き先を表示する吹き出し */
   var bubble = document.createElement("div");
   bubble.className = "neko-speech nav-speech";
   bubble.textContent = link.label;
   el.appendChild(bubble);

   /* ★ 0.8秒後にページ遷移 */
   setTimeout(function() {
     window.location.href = link.url;
   }, 1500);
 }

 /* ── 通常の吹き出し（歩行中にたまに喋る） ── */
 function speakRandom(el) {
   var existing = el.querySelector(".neko-speech");
   if (existing) return;

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

 function startLoop() {
   var lastTime = Date.now();

   function loop() {
     if (!isActive) return;

     var now = Date.now();
     if (now - lastTime < 60) {
       rafId = requestAnimationFrame(loop);
       return;
     }
     lastTime = now;

     for (var i = 0; i < catElements.length; i++) {
       updateCat(catElements[i], now);
     }

     rafId = requestAnimationFrame(loop);
   }

   rafId = requestAnimationFrame(loop);
 }

 function updateCat(cat, now) {
   if (now >= cat.stateTimer) {
     if (cat.zzz && cat.zzz.parentNode) {
       cat.zzz.parentNode.removeChild(cat.zzz);
       cat.zzz = null;
     }

     var action = Math.random();

     if (action < 0.6) {
       cat.state = "walking";
       var angle = Math.random() * Math.PI * 2;
       var distance = 80 + Math.random() * 200;
       cat.targetX = cat.x + Math.cos(angle) * distance;
       cat.targetY = cat.y + Math.sin(angle) * distance;

       var maxX = window.innerWidth - 50;
       var maxY = window.innerHeight - 50;
       if (cat.targetX < 10) cat.targetX = 10;
       if (cat.targetX > maxX) cat.targetX = maxX;
       if (cat.targetY < 10) cat.targetY = 10;
       if (cat.targetY > maxY) cat.targetY = maxY;

       if (cat.targetX < cat.x) {
         cat.el.className = "neko-cat walking face-left";
       } else {
         cat.el.className = "neko-cat walking";
       }

       var dist = Math.sqrt(
         Math.pow(cat.targetX - cat.x, 2) +
         Math.pow(cat.targetY - cat.y, 2)
       );
       cat.stateTimer = now + dist * 8 + 500;

       /* ★ 歩き始めにたまに喋る（20%の確率） */
       if (Math.random() < 0.4) {
         speakRandom(cat.el);
       }

     } else if (action < 0.85) {
       cat.state = "idle";
       cat.el.className = "neko-cat idle";
       cat.stateTimer = now + 2000 + Math.random() * 3000;

     } else {
       cat.state = "sleeping";
       cat.el.className = "neko-cat sleeping";
       var zzz = document.createElement("span");
       zzz.style.cssText = "position:absolute; top:-16px; right:-8px; font-size:12px;";
       zzz.textContent = "zzZ";
       cat.el.appendChild(zzz);
       cat.zzz = zzz;
       cat.stateTimer = now + 3000 + Math.random() * 5000;
     }
   }

   if (cat.state === "walking") {
     var dx = cat.targetX - cat.x;
     var dy = cat.targetY - cat.y;
     var dist = Math.sqrt(dx * dx + dy * dy);

     if (dist > 2) {
       var speed = 2;
       cat.x += (dx / dist) * speed;
       cat.y += (dy / dist) * speed;
       cat.el.style.left = cat.x + "px";
       cat.el.style.top = cat.y + "px";
     }
   }
 }

 if (document.readyState === "loading") {
   document.addEventListener("DOMContentLoaded", init);
 } else {
   init();
 }
})();
