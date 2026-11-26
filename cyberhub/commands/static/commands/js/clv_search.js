// CLV scripts:
// 1. Search boxes on the landing page (categories, and commands under "Advanced").
//    Same idea as core/js/search.js. Each form names its data with data-source.
// 2. On a tab page, a link ending in #command-<pk> scrolls to that command and opens it.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".clv-search").forEach(setupSearch);
  openCommandFromLink();
});

function setupSearch(form) {
  const dataElement = document.getElementById(form.dataset.source);
  if (!dataElement) return;

  const input = form.querySelector("input[name='q']");
  const results = form.querySelector(".ch-search-results");
  const items = JSON.parse(dataElement.textContent);

  // An item matches if the text appears in its name or description.
  function findMatches(query) {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return items.filter((item) => [item.name, item.description].some((text) => text.toLowerCase().includes(q)));
  }

  // textContent (never innerHTML), so text from the database can't become HTML.
  function buildResult(item) {
    const link = document.createElement("a");
    link.className = "ch-result";
    link.href = item.url;

    if (item.location) {
      // Command result: name as code on the left, "Tab › Category" on the right.
      link.classList.add("clv-command-result");
      const name = document.createElement("code");
      name.className = "clv-cmd";
      name.textContent = item.name;
      const location = document.createElement("span");
      location.className = "ch-result-desc";
      location.textContent = item.location;
      link.append(name, location);
    } else {
      const title = document.createElement("div");
      title.className = "ch-result-title";
      title.textContent = item.name;
      link.append(title);
    }
    return link;
  }

  function render() {
    results.replaceChildren();
    if (!input.value.trim()) {
      results.hidden = true;
      return;
    }

    const matches = findMatches(input.value);
    if (matches.length === 0) {
      const empty = document.createElement("div");
      empty.className = "ch-result-empty";
      empty.textContent = "Nothing matches.";
      results.append(empty);
    } else {
      matches.forEach((item) => results.append(buildResult(item)));
    }
    results.hidden = false;
  }

  input.addEventListener("input", render);
  input.addEventListener("focus", render);

  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") results.hidden = true;
  });

  // Enter opens the first match.
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const first = findMatches(input.value)[0];
    if (first) window.location.href = first.url;
  });

  document.addEventListener("click", (event) => {
    if (!form.contains(event.target)) results.hidden = true;
  });
}

function openCommandFromLink() {
  // getElementById (not querySelector) so an odd hash in the URL can't cause an error.
  const id = window.location.hash.slice(1);
  if (!id.startsWith("command-")) return;
  const details = document.getElementById(id);
  if (!details || !details.classList.contains("collapse")) return;

  bootstrap.Collapse.getOrCreateInstance(details).show();
  details.closest(".clv-row").scrollIntoView({ block: "center" });
}
