// Eye buttons: switch a password input between hidden and visible text.
const toggles = document.querySelectorAll("[data-password-toggle]");

function setVisible(button, visible) {
  const input = document.getElementById(button.dataset.passwordToggle);
  const icon = button.querySelector("i");
  const label = button.getAttribute("aria-label").replace(/^(Show|Hide)/, visible ? "Hide" : "Show");

  input.type = visible ? "text" : "password";
  icon.classList.toggle("fa-eye", !visible);
  icon.classList.toggle("fa-eye-slash", visible);
  button.setAttribute("aria-label", label);
}

toggles.forEach((button) => {
  button.addEventListener("click", () => {
    const input = document.getElementById(button.dataset.passwordToggle);
    setVisible(button, input.type === "password");
  });
});

// Hide passwords again on submit so the browser doesn't remember them as plain text fields.
document.querySelector("main form").addEventListener("submit", () => {
  toggles.forEach((button) => setVisible(button, false));
});
