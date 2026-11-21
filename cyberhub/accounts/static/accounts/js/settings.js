const appearanceForm = document.getElementById("appearance-form");
const fontSizeInput = document.getElementById("font-size");
const SAVE_DELAY_MS = 700;
let saveTimer;

// Save the color mode as soon as it is clicked, so there is no separate Save button.
appearanceForm.querySelectorAll('input[name="color_mode"]').forEach((radio) => {
  radio.addEventListener("change", () => appearanceForm.requestSubmit());
});

// Resize the page right away, but wait for a pause before saving,
// because saving reloads the page and would interrupt typing or repeated clicks.
fontSizeInput.addEventListener("input", () => {
  clearTimeout(saveTimer);
  if (!fontSizeInput.checkValidity()) return;

  document.documentElement.style.fontSize = `${fontSizeInput.value}px`;
  saveTimer = setTimeout(() => appearanceForm.requestSubmit(), SAVE_DELAY_MS);
});
