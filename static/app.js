/* ===================================================
   AI Pulse — News Scraper App Logic
   =================================================== */

const API_URL = "/articles";

let allArticles = [];
let currentCategory = "All";

// ── Category CSS class map ──────────────────────────
const catClass = {
  "AI Companies":   "cat-ai-companies",
  "AI Research":    "cat-ai-research",
  "Infrastructure": "cat-infrastructure",
  "AI Products":    "cat-ai-products",
};

// ── Source domain from URL ──────────────────────────
function getSource(url) {
  try {
    const host = new URL(url).hostname.replace("www.", "");
    if (host.includes("techcrunch")) return "🟠 TechCrunch";
    if (host.includes("ycombinator") || host.includes("news.y")) return "🟡 HackerNews";
    return "🌐 " + host;
  } catch {
    return "🌐 Unknown Source";
  }
}

// ── Relative timestamp ──────────────────────────────
function timeAgo(dateStr) {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  if (isNaN(date)) return "";
  const diff = (Date.now() - date) / 1000; // seconds
  if (diff < 60)    return "Just now";
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

// ── Animate count up ────────────────────────────────
function animateCount(el, target) {
  let current = 0;
  const step = Math.ceil(target / 30);
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current;
    if (current >= target) clearInterval(interval);
  }, 25);
}

// ── Update stats bar ────────────────────────────────
function updateStats(articles) {
  const counts = {
    total:   articles.length,
    company: articles.filter(a => a.category === "AI Companies").length,
    research:articles.filter(a => a.category === "AI Research").length,
    infra:   articles.filter(a => a.category === "Infrastructure").length,
    product: articles.filter(a => a.category === "AI Products").length,
  };
  animateCount(document.getElementById("totalCount"),   counts.total);
  animateCount(document.getElementById("companyCount"), counts.company);
  animateCount(document.getElementById("researchCount"),counts.research);
  animateCount(document.getElementById("infraCount"),   counts.infra);
  animateCount(document.getElementById("productCount"), counts.product);
}

// ── Render a single card ────────────────────────────
function renderCard(article, idx) {
  const template = document.getElementById("cardTemplate");
  const clone = template.content.cloneNode(true);
  const card = clone.querySelector(".card");

  card.style.animationDelay = `${idx * 0.04}s`;

  const catEl = card.querySelector(".card-category");
  catEl.textContent = article.category || "Other";
  catEl.className = "card-category " + (catClass[article.category] || "cat-other");

  card.querySelector(".card-time").textContent = timeAgo(article.scraped_at);
  card.querySelector(".card-title").textContent = article.title || "Untitled";

  const link = card.querySelector(".card-link");
  if (article.url) {
    link.href = article.url;
  } else {
    link.style.display = "none";
  }

  card.querySelector(".card-source").textContent = getSource(article.url || "");

  return clone;
}

// ── Filter + Sort + Render ──────────────────────────
function filterArticles() {
  const query   = document.getElementById("searchInput").value.toLowerCase().trim();
  const sort    = document.getElementById("sortSelect").value;
  const grid    = document.getElementById("articlesGrid");
  const empty   = document.getElementById("emptyState");

  let filtered = allArticles.filter(a => {
    const matchCat = currentCategory === "All" || a.category === currentCategory;
    const matchQ   = !query || (a.title || "").toLowerCase().includes(query);
    return matchCat && matchQ;
  });

  // Sort
  if (sort === "newest") {
    filtered.sort((a, b) => new Date(b.scraped_at) - new Date(a.scraped_at));
  } else if (sort === "oldest") {
    filtered.sort((a, b) => new Date(a.scraped_at) - new Date(b.scraped_at));
  } else if (sort === "title") {
    filtered.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
  }

  grid.innerHTML = "";

  if (filtered.length === 0) {
    empty.style.display = "block";
    return;
  }
  empty.style.display = "none";

  const frag = document.createDocumentFragment();
  filtered.forEach((article, idx) => frag.appendChild(renderCard(article, idx)));
  grid.appendChild(frag);
}

// ── Category tab handler ────────────────────────────
function setCategory(tabEl, cat) {
  currentCategory = cat;
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  tabEl.classList.add("active");
  filterArticles();
}

// ── Clear search ────────────────────────────────────
function clearSearch() {
  document.getElementById("searchInput").value = "";
  filterArticles();
}

// ── Fetch articles from Flask API ───────────────────
async function loadNews() {
  const loader  = document.getElementById("loader");
  const grid    = document.getElementById("articlesGrid");
  const errEl   = document.getElementById("errorState");
  const errMsg  = document.getElementById("errorMsg");
  const lastUpd = document.getElementById("lastUpdated");
  const refreshIcon = document.querySelector(".refresh-icon");

  loader.style.display = "flex";
  errEl.style.display  = "none";
  grid.innerHTML       = "";

  if (refreshIcon) {
    refreshIcon.style.animation = "spin 0.7s linear infinite";
  }

  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    allArticles = data.filter(a => a.title && a.title.trim().length > 0);
    updateStats(allArticles);

    const now = new Date();
    lastUpd.textContent = "Updated " + now.toLocaleTimeString();

    loader.style.display = "none";
    filterArticles();
  } catch (err) {
    loader.style.display = "none";
    errEl.style.display  = "block";
    errMsg.textContent   = "Error: " + err.message + ". Make sure the server is running.";
    console.error("Failed to fetch news:", err);
  } finally {
    if (refreshIcon) {
      refreshIcon.style.animation = "";
    }
  }
}

// ── Keyboard shortcut: / to focus search ───────────
document.addEventListener("keydown", e => {
  if (e.key === "/" && document.activeElement !== document.getElementById("searchInput")) {
    e.preventDefault();
    document.getElementById("searchInput").focus();
  }
  if (e.key === "Escape") {
    clearSearch();
    document.getElementById("searchInput").blur();
  }
});

// ── Init ────────────────────────────────────────────
loadNews();
