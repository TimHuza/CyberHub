const noteForm = document.getElementById("note-form");
const contentInput = noteForm.querySelector('textarea[name="content"]');
const csrfToken = noteForm.querySelector('input[name="csrfmiddlewaretoken"]').value;
const previewTab = document.getElementById("preview-tab");
const previewBox = document.getElementById("note-preview");
let latestRequest = 0;

// The server renders the preview, so it always matches the saved note and is always sanitized.
async function showPreview() {
  const thisRequest = ++latestRequest;
  previewBox.textContent = "Loading preview...";

  try {
    const response = await fetch(noteForm.dataset.previewUrl, {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: new URLSearchParams({ content: contentInput.value }),
      redirect: "error", // An expired login redirects to a page we must not show as a preview.
    });
    if (!response.ok) throw new Error("Preview request failed");

    const html = await response.text();
    if (thisRequest !== latestRequest) return; // A newer preview was requested meanwhile.

    if (html.trim()) {
      previewBox.innerHTML = html; // Safe only because the server sanitized it.
    } else {
      previewBox.textContent = "Nothing to preview.";
    }
  } catch {
    if (thisRequest === latestRequest) {
      previewBox.textContent = "Preview couldn't load. Your text is still in the Code tab.";
    }
  }
}

previewTab.addEventListener("shown.bs.tab", showPreview);
