// Quick-jump search: filters the component list as the user types.
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".ch-search");
  const dataElement = document.getElementById("ch-components");
  if (!form || !dataElement) return;

  const input = form.querySelector("input[name='q']");
  const results = document.getElementById("ch-search-results");
  const components = JSON.parse(dataElement.textContent);

  // A component matches if the text appears in its code, name or description.
  function findMatches(query) {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return components.filter((c) =>
      [c.code, c.name, c.description].some((text) => text.toLowerCase().includes(q))
    );
  }

  // Build one result row. textContent (never innerHTML) so text can't become HTML.
  function buildResult(c) {
    const item = document.createElement(c.url ? "a" : "div");
    item.className = c.url ? "ch-result" : "ch-result is-disabled";
    if (c.url) item.href = c.url;

    const tile = document.createElement("div");
    tile.className = `ch-tile ch-tile-sm ${c.tile}`;
    const icon = document.createElement("i");
    icon.className = `fa-solid ${c.icon}`;
    tile.append(icon);

    const text = document.createElement("div");
    const title = document.createElement("div");
    title.className = "ch-result-title";
    title.textContent = `${c.name} (${c.code})`;
    const description = document.createElement("div");
    description.className = "ch-result-desc";
    description.textContent = c.description;
    text.append(title, description);

    item.append(tile, text);

    if (!c.url) {
      const badge = document.createElement("span");
      badge.className = "ch-badge ms-auto";
      badge.textContent = "Coming soon";
      item.append(badge);
    }
    return item;
  }

  function render() {
    results.replaceChildren();
    if (!input.value.trim()) {
      results.hidden = true;
      return;
    }

    const matches = findMatches(input.value);
    const heading = document.createElement("div");
    heading.className = "ch-results-heading";
    heading.textContent = "Components";
    results.append(heading);

    if (matches.length === 0) {
      const empty = document.createElement("div");
      empty.className = "ch-result-empty";
      empty.textContent = "No components match.";
      results.append(empty);
    } else {
      matches.forEach((c) => results.append(buildResult(c)));
    }
    results.hidden = false;
  }

  input.addEventListener("input", render);
  input.addEventListener("focus", render);

  // Escape closes the dropdown.
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") results.hidden = true;
  });

  // Enter or the Search button opens the first match that exists.
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const first = findMatches(input.value).find((c) => c.url);
    if (first) window.location.href = first.url;
  });

  // Clicking anywhere outside the search closes the dropdown.
  document.addEventListener("click", (event) => {
    if (!form.contains(event.target)) results.hidden = true;
  });
});
