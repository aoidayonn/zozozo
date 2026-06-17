/* ============================================
   ZOZO風 動的サイト JavaScript
   ============================================ */

document.addEventListener("DOMContentLoaded", () => {
  initThemeSwitcher();
  initToast();
  initScrollTop();
  initSmoothScroll();
  initCartAnimation();
  initDeleteConfirm();
  initQuantitySelector();
  initSearchHighlight();
  initTableHover();
  initFadeInOnScroll();
  initPriceFormat();
  initFormValidation();
  initImagePreview();
  initDarkMode();
  initLoadingOverlay();
});

/* ============================================
   1. トースト通知（カート追加時など）
   ============================================ */
function initToast() {
  const container = document.createElement("div");
  container.id = "toast-container";
  container.style.cssText =
    "position:fixed; top:20px; right:20px; z-index:9999;";
  document.body.appendChild(container);

  const cartForms = document.querySelectorAll(
    'form[action*="cart"] button[type="submit"]'
  );
  cartForms.forEach((btn) => {
    btn.addEventListener("click", () => {
      showToast("\u{1F6D2} カートに追加しました！");
    });
  });
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast toast-" + type;
  toast.textContent = message;
  toast.style.cssText =
    "background:" + (type === "success" ? "#111" : "#c0392b") + ";" +
    "color:#fff;" +
    "padding:14px 28px;" +
    "border-radius:6px;" +
    "margin-bottom:10px;" +
    "font-size:14px;" +
    "font-weight:500;" +
    "box-shadow:0 4px 16px rgba(0,0,0,0.2);" +
    "opacity:0;" +
    "transform:translateX(100px);" +
    "transition:all 0.4s ease;" +
    "cursor:pointer;";

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.opacity = "1";
    toast.style.transform = "translateX(0)";
  });

  toast.addEventListener("click", () => removeToast(toast));
  setTimeout(() => removeToast(toast), 3000);
}

function removeToast(toast) {
  toast.style.opacity = "0";
  toast.style.transform = "translateX(100px)";
  setTimeout(() => toast.remove(), 400);
}

/* ============================================
   2. スクロールトップボタン
   ============================================ */
function initScrollTop() {
  const btn = document.createElement("button");
  btn.id = "scroll-top";
  btn.innerHTML = "\u2191";
  btn.title = "ページトップへ";
  btn.style.cssText =
    "position:fixed;" +
    "bottom:30px;" +
    "right:30px;" +
    "width:48px;" +
    "height:48px;" +
    "border-radius:50%;" +
    "background:#111;" +
    "color:#fff;" +
    "border:none;" +
    "font-size:20px;" +
    "cursor:pointer;" +
    "opacity:0;" +
    "transform:scale(0);" +
    "transition:all 0.3s ease;" +
    "z-index:9998;" +
    "box-shadow:0 4px 12px rgba(0,0,0,0.3);";

  document.body.appendChild(btn);

  window.addEventListener("scroll", () => {
    if (window.scrollY > 200) {
      btn.style.opacity = "1";
      btn.style.transform = "scale(1)";
    } else {
      btn.style.opacity = "0";
      btn.style.transform = "scale(0)";
    }
  });

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ============================================
   3. スムーズスクロール
   ============================================ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
}

/* ============================================
   4. カート追加アニメーション
   ============================================ */
function initCartAnimation() {
  const cartBtns = document.querySelectorAll(
    'button[type="submit"], input[type="submit"]'
  );

  cartBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const ripple = document.createElement("span");
      ripple.style.cssText =
        "position:absolute;" +
        "border-radius:50%;" +
        "background:rgba(255,255,255,0.4);" +
        "width:100px;" +
        "height:100px;" +
        "transform:scale(0);" +
        "animation:ripple 0.6s ease-out;" +
        "pointer-events:none;";
      this.style.position = "relative";
      this.style.overflow = "hidden";
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  const style = document.createElement("style");
  style.textContent = "@keyframes ripple { to { transform: scale(4); opacity: 0; } }";
  document.head.appendChild(style);
}

/* ============================================
   5. 削除確認ダイアログ（カスタム）
   ============================================ */
function initDeleteConfirm() {
  const deleteLinks = document.querySelectorAll('a[href*="Delete"]');
  deleteLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      if (!confirm("本当に削除しますか？この操作は取り消せません。")) {
        e.preventDefault();
      }
    });
  });

  const withdrawLinks = document.querySelectorAll('a[href*="withdraw"]');
  withdrawLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      if (!confirm("本当に退会しますか？全てのデータが削除されます。")) {
        e.preventDefault();
      }
    });
  });
}

/* ============================================
   6. 数量セレクター（+/- ボタン付き）
   ============================================ */
function initQuantitySelector() {
  const selects = document.querySelectorAll('select[name="num"]');

  selects.forEach((select) => {
    const wrapper = document.createElement("div");
    wrapper.style.cssText = "display:inline-flex; align-items:center; gap:8px;";

    const minusBtn = document.createElement("button");
    minusBtn.type = "button";
    minusBtn.textContent = "\u2212";
    minusBtn.style.cssText =
      "width:32px; height:32px; border:1px solid #ccc; border-radius:4px;" +
      "background:#f5f5f5; font-size:16px; cursor:pointer; color:#111;";

    const plusBtn = document.createElement("button");
    plusBtn.type = "button";
    plusBtn.textContent = "\uFF0B";
    plusBtn.style.cssText = minusBtn.style.cssText;

    minusBtn.addEventListener("click", () => {
      const idx = select.selectedIndex;
      if (idx > 0) select.selectedIndex = idx - 1;
    });

    plusBtn.addEventListener("click", () => {
      const idx = select.selectedIndex;
      if (idx < select.options.length - 1) select.selectedIndex = idx + 1;
    });

    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(minusBtn);
    wrapper.appendChild(select);
    wrapper.appendChild(plusBtn);
  });
}

/* ============================================
   7. 検索ハイライト
   ============================================ */
function initSearchHighlight() {
  const params = new URLSearchParams(window.location.search);
  const keyword = params.get("keyword");

  if (keyword && keyword.trim()) {
    const cells = document.querySelectorAll("table td");
    const regex = new RegExp("(" + escapeRegExp(keyword) + ")", "gi");

    cells.forEach((cell) => {
      if (cell.querySelector("a, input, select, img")) return;
      if (regex.test(cell.textContent)) {
        cell.innerHTML = cell.innerHTML.replace(
          regex,
          '<mark style="background:#fff3cd; padding:2px 4px; border-radius:2px;">$1</mark>'
        );
      }
    });
  }
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* ============================================
   8. テーブル行ホバーエフェクト
   ============================================ */
function initTableHover() {
  const rows = document.querySelectorAll("table[border] tr");
  rows.forEach((row, index) => {
    if (index === 0) return;
    row.style.transition = "all 0.2s ease";
    row.addEventListener("mouseenter", () => {
      row.style.transform = "scale(1.01)";
      row.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
    });
    row.addEventListener("mouseleave", () => {
      row.style.transform = "scale(1)";
      row.style.boxShadow = "none";
    });
  });
}

/* ============================================
   9. フェードインアニメーション
   ============================================ */
function initFadeInOnScroll() {
  const content = document.querySelector(".content");
  if (content) {
    content.style.opacity = "0";
    content.style.transform = "translateY(20px)";
    content.style.transition = "all 0.6s ease";

    requestAnimationFrame(() => {
      content.style.opacity = "1";
      content.style.transform = "translateY(0)";
    });
  }

  const cards = document.querySelectorAll(".recommend-card");
  cards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";
    card.style.transition = "all 0.5s ease " + (index * 0.1) + "s";

    setTimeout(() => {
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 100);
  });
}

/* ============================================
   10. 価格フォーマット（カンマ区切り）
   ============================================ */
function initPriceFormat() {
  const cells = document.querySelectorAll("td, p, strong");
  cells.forEach((cell) => {
    if (cell.querySelector("a, input, select, button, img")) return;

    cell.innerHTML = cell.innerHTML.replace(
      /(\d{1,3}(?:,\d{3})*|\d+)(円)/g,
      function (match, num, yen) {
        var formatted = parseInt(num.replace(/,/g, "")).toLocaleString();
        return formatted + yen;
      }
    );
  });

  cells.forEach((cell) => {
    if (cell.querySelector("a, input, select, button, img")) return;
    cell.innerHTML = cell.innerHTML.replace(/¥(\d+)/g, function (match, num) {
      return "¥" + parseInt(num).toLocaleString();
    });
  });
}

/* ============================================
   11. フォームバリデーション（リアルタイム）
   ============================================ */
function initFormValidation() {
  const pw1 = document.querySelector('input[name="password_1"]');
  const pw2 = document.querySelector('input[name="password_2"]');

  if (pw1 && pw2) {
    const hint = document.createElement("span");
    hint.style.cssText = "font-size:12px; margin-left:8px;";

    pw2.parentNode.appendChild(hint);

    pw2.addEventListener("input", () => {
      if (pw2.value === "") {
        hint.textContent = "";
        pw2.style.borderColor = "";
      } else if (pw1.value === pw2.value) {
        hint.textContent = "\u2705 パスワードが一致しています";
        hint.style.color = "#27ae60";
        pw2.style.borderColor = "#27ae60";
      } else {
        hint.textContent = "\u274C パスワードが一致しません";
        hint.style.color = "#c0392b";
        pw2.style.borderColor = "#c0392b";
      }
    });
  }

  const priceInput = document.querySelector('input[name="price"]');
  const stockInput = document.querySelector('input[name="stock"]');

  [priceInput, stockInput].forEach((input) => {
    if (!input) return;
    input.addEventListener("input", () => {
      const val = parseInt(input.value);
      if (isNaN(val) || val < 0) {
        input.style.borderColor = "#c0392b";
        input.style.background = "#fdf0ef";
      } else {
        input.style.borderColor = "#27ae60";
        input.style.background = "#f0fdf4";
      }
    });
  });
}

/* ============================================
   12. 画像プレビュー（アップロード前に確認）
   ============================================ */
function initImagePreview() {
  const imageInput = document.querySelector('input[type="file"]');
  if (!imageInput) return;

  const preview = document.createElement("div");
  preview.style.cssText = "margin-top:12px;";
  imageInput.parentNode.appendChild(preview);

  imageInput.addEventListener("change", (e) => {
    preview.innerHTML = "";
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      showToast("\u26A0\uFE0F ファイルサイズは5MB以下にしてください", "error");
      imageInput.value = "";
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const img = document.createElement("img");
      img.src = event.target.result;
      img.style.cssText =
        "max-width:200px; border-radius:8px; border:1px solid #ddd; margin-top:8px;";

      const label = document.createElement("p");
      label.textContent = "プレビュー: " + file.name;
      label.style.cssText = "font-size:12px; color:#888; margin-top:4px;";

      preview.appendChild(img);
      preview.appendChild(label);
    };
    reader.readAsDataURL(file);
  });
}

/* ============================================
   13. ダークモード切替
   ============================================ */
function initDarkMode() {
  const toggle = document.createElement("button");
  toggle.id = "dark-mode-toggle";
  toggle.innerHTML = "\u{1F319}";
  toggle.title = "ダークモード切替";
  toggle.style.cssText =
    "position:fixed;" +
    "bottom:30px;" +
    "left:30px;" +
    "width:48px;" +
    "height:48px;" +
    "border-radius:50%;" +
    "background:#111;" +
    "color:#fff;" +
    "border:none;" +
    "font-size:20px;" +
    "cursor:pointer;" +
    "z-index:9998;" +
    "box-shadow:0 4px 12px rgba(0,0,0,0.3);" +
    "transition:all 0.3s ease;";

  document.body.appendChild(toggle);

  const darkCSS = document.createElement("style");
  darkCSS.id = "dark-mode-css";
  darkCSS.textContent =
    "body.dark-mode { background-color: #1a1a1a; color: #e0e0e0; }" +
    "body.dark-mode .content { background: #2a2a2a; box-shadow: 0 2px 16px rgba(0,0,0,0.3); }" +
    "body.dark-mode h1, body.dark-mode h3, body.dark-mode h4 { color: #f0f0f0; }" +
    "body.dark-mode h3 { border-bottom-color: #555; }" +
    "body.dark-mode h4 { border-left-color: #888; }" +
    "body.dark-mode th { background-color: #333 !important; color: #fff !important; }" +
    "body.dark-mode td { border-bottom-color: #444; }" +
    "body.dark-mode tr:nth-child(even) { background-color: #2f2f2f; }" +
    "body.dark-mode tr:hover { background-color: #383838; }" +
    "body.dark-mode input, body.dark-mode select { background: #333; color: #e0e0e0; border-color: #555; }" +
    "body.dark-mode input:focus, body.dark-mode select:focus { border-color: #888; box-shadow: 0 0 0 3px rgba(255,255,255,0.1); }" +
    "body.dark-mode a { color: #aaa; }" +
    "body.dark-mode .recommend-card { background: #333; border-color: #444; }" +
    "body.dark-mode .recommend-name { color: #f0f0f0; }" +
    "body.dark-mode strong { color: #f0f0f0; }" +
    "body.dark-mode form[style*='display:flex'], body.dark-mode form[style*='display: flex'] { background: #333 !important; border-color: #555 !important; color: #e0e0e0; }" +
    "body.dark-mode .form { background: transparent; }" +
    "body.dark-mode label { color: #e0e0e0; }" +
    "body.dark-mode input[type='submit'], body.dark-mode button[type='submit'] { background: #f0f0f0; color: #111; border-color: #f0f0f0; }" +
    "body.dark-mode input[type='submit']:hover, body.dark-mode button[type='submit']:hover { background: transparent; color: #f0f0f0; }" +
    "body.dark-mode p[style*='color:red'] { background: #3d1f1f; border-color: #5a2a2a; }" +
    "body.dark-mode #loading-overlay { background: rgba(0,0,0,0.7); }" +
    "body.dark-mode #loading-overlay p { color: #e0e0e0; }" +
    "body.dark-mode .recommend-info { color: #999; }" +
    "body.dark-mode .recommend-price { color: #e74c3c; }" +
    "body.dark-mode mark { background: #5a4a00; color: #fff; }";
  document.head.appendChild(darkCSS);

  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark-mode");
    toggle.innerHTML = "\u2600\uFE0F";
    toggle.style.background = "#f5f5f5";
    toggle.style.color = "#111";
  }

  toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", isDark);

    if (isDark) {
      toggle.innerHTML = "\u2600\uFE0F";
      toggle.style.background = "#f5f5f5";
      toggle.style.color = "#111";
    } else {
      toggle.innerHTML = "\u{1F319}";
      toggle.style.background = "#111";
      toggle.style.color = "#fff";
    }
  });
}

/* ============================================
   14. ローディングオーバーレイ
   ============================================ */
function initLoadingOverlay() {
  const overlay = document.createElement("div");
  overlay.id = "loading-overlay";
  overlay.style.cssText =
    "position:fixed;" +
    "top:0; left:0;" +
    "width:100%; height:100%;" +
    "background:rgba(255,255,255,0.8);" +
    "display:flex;" +
    "align-items:center;" +
    "justify-content:center;" +
    "z-index:99999;" +
    "opacity:0;" +
    "pointer-events:none;" +
    "transition:opacity 0.3s ease;";

  const inner = document.createElement("div");
  inner.style.textContent = "text-align:center;";

  const spinner = document.createElement("div");
  spinner.className = "spinner";

  const label = document.createElement("p");
  label.textContent = "読み込み中...";
  label.style.cssText = "margin-top:16px; font-size:14px; color:#111;";

  inner.appendChild(spinner);
  inner.appendChild(label);
  overlay.appendChild(inner);
  document.body.appendChild(overlay);

  const style = document.createElement("style");
  style.textContent =
    ".spinner { width:40px; height:40px; border:4px solid #e0e0e0; border-top-color:#111; border-radius:50%; animation:spin 0.8s linear infinite; margin:0 auto; }" +
    "@keyframes spin { to { transform: rotate(360deg); } }";
  document.head.appendChild(style);

  const forms = document.querySelectorAll('form[method="POST"], form[method="post"]');
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      overlay.style.opacity = "1";
      overlay.style.pointerEvents = "auto";
    });
  });
}

  /* ============================================
     15. テーマ切替（CSS切替ボタン）
     ============================================ */
  function initThemeSwitcher() {
    var themes = [
      { id: "zozo",   label: "ZOZO",   file: "/static/soso/css/zozo.css"   },
      { id: "apple",  label: "Apple",  file: "/static/soso/css/apple.css"  },
      { id: "instagram", label: "Instagram", file: "/static/soso/css/instagram.css" },
      { id: "twitter", label: "Twitter", file: "/static/soso/css/twitter.css" }
    ];
  
    // 現在のテーマを取得（デフォルトは zozo）
    var currentTheme = localStorage.getItem("siteTheme") || "zozo";
  
    // テーマ用の <link> タグを作成
    var themeLink = document.querySelector('link[rel="stylesheet"]');
    if (!themeLink) {
      themeLink = document.createElement("link");
      themeLink.rel = "stylesheet";
      document.head.appendChild(themeLink);
    }
  
    // テーマ適用関数
    function applyTheme(themeId) {
      var theme = themes.find(function(t) { return t.id === themeId; });
      if (theme) {
        themeLink.href = theme.file;
        localStorage.setItem("siteTheme", themeId);
        currentTheme = themeId;
        updateButtonLabel();
      }
    }
  
    // ── ボタン本体 ──
    var switcher = document.createElement("div");
    switcher.id = "theme-switcher";
    switcher.style.cssText =
      "position:fixed;" +
      "top:20px;" +
      "right:20px;" +
      "z-index:10000;";
  
    var btn = document.createElement("button");
    btn.id = "theme-btn";
    btn.type = "button";
    btn.style.cssText =
      "padding:10px 20px;" +
      "border-radius:980px;" +
      "border:2px solid #888;" +
      "background:rgba(255,255,255,0.9);" +
      "backdrop-filter:blur(10px);" +
      "color:#333;" +
      "font-size:13px;" +
      "font-weight:700;" +
      "cursor:pointer;" +
      "transition:all 0.3s ease;" +
      "box-shadow:0 4px 16px rgba(0,0,0,0.1);";
  
    // ── ドロップダウン ──
    var dropdown = document.createElement("div");
    dropdown.id = "theme-dropdown";
    dropdown.style.cssText =
      "position:absolute;" +
      "top:50px;" +
      "right:0;" +
      "background:rgba(255,255,255,0.95);" +
      "backdrop-filter:blur(10px);" +
      "border-radius:12px;" +
      "box-shadow:0 8px 32px rgba(0,0,0,0.15);" +
      "overflow:hidden;" +
      "display:none;" +
      "min-width:160px;" +
      "border:1px solid #ddd;";
  
    themes.forEach(function(theme) {
      var item = document.createElement("button");
      item.type = "button";
      item.textContent = theme.label;
      item.dataset.theme = theme.id;
      item.style.cssText =
        "display:block;" +
        "width:100%;" +
        "padding:12px 20px;" +
        "border:none;" +
        "background:transparent;" +
        "color:#333;" +
        "font-size:14px;" +
        "font-weight:500;" +
        "cursor:pointer;" +
        "text-align:left;" +
        "transition:background 0.2s;";
  
      item.addEventListener("mouseenter", function() {
        this.style.background = "#f0f0f0";
      });
      item.addEventListener("mouseleave", function() {
        this.style.background = "transparent";
      });
      item.addEventListener("click", function() {
        applyTheme(this.dataset.theme);
        dropdown.style.display = "none";
      });
  
      dropdown.appendChild(item);
    });
  
    // ── ボタンラベル更新 ──
    function updateButtonLabel() {
      var theme = themes.find(function(t) { return t.id === currentTheme; });
      btn.textContent = "\uD83C\uDFA8 " + (theme ? theme.label : "Theme");
    }
  
    // ── 開閉トグル ──
    btn.addEventListener("click", function(e) {
      e.stopPropagation();
      dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
    });
  
    document.addEventListener("click", function() {
      dropdown.style.display = "none";
    });
  
    switcher.appendChild(btn);
    switcher.appendChild(dropdown);
    document.body.appendChild(switcher);
  
    // 初期テーマ適用
    updateButtonLabel();
    applyTheme(currentTheme);
  }
