"use strict";

const fileInput = document.getElementById("fileInput");
const chooseButton = document.getElementById("chooseButton");
const dropZone = document.getElementById("dropZone");
const statusBanner = document.getElementById("statusBanner");
const statusText = document.getElementById("statusText");
const markdownEditor = document.getElementById("markdownEditor");
const markdownPreview = document.getElementById("markdownPreview");
const previewState = document.getElementById("previewState");
const charCounter = document.getElementById("charCounter");
const fileName = document.getElementById("fileName");
const fileMeta = document.getElementById("fileMeta");
const fileType = document.getElementById("fileType");
const copyButton = document.getElementById("copyButton");
const resetButton = document.getElementById("resetButton");
const downloadButton = document.getElementById("downloadButton");

let outputFilename = "converted.md";
let renderTimer = null;
let renderSequence = 0;

chooseButton.addEventListener("click", (event) => {
  event.stopPropagation();
  fileInput.click();
});
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    fileInput.click();
  }
});
fileInput.addEventListener("change", () => {
  if (fileInput.files.length) convertFile(fileInput.files[0]);
});

for (const eventName of ["dragenter", "dragover"]) {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add("dragover");
  });
}
for (const eventName of ["dragleave", "drop"]) {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
  });
}
dropZone.addEventListener("drop", (event) => {
  const [file] = event.dataTransfer.files;
  if (file) convertFile(file);
});

markdownEditor.addEventListener("input", () => {
  updateCounter();
  scheduleRender();
});
copyButton.addEventListener("click", copyMarkdown);
resetButton.addEventListener("click", resetWorkspace);
downloadButton.addEventListener("click", downloadMarkdown);
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s" && !downloadButton.disabled) {
    event.preventDefault();
    downloadMarkdown();
  }
});

async function convertFile(file) {
  setBusy(true, `正在轉換 ${file.name}…`);
  fileName.textContent = file.name;
  fileMeta.textContent = `${formatBytes(file.size)} · 準備轉換`;
  fileType.textContent = extensionLabel(file.name);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/api/convert", { method: "POST", body: formData });
    const payload = await readJson(response);
    if (!response.ok) throw new Error(payload.detail || "轉換失敗。 ");

    outputFilename = payload.output_filename || "converted.md";
    markdownEditor.value = payload.markdown || "";
    markdownEditor.disabled = false;
    copyButton.disabled = false;
    resetButton.disabled = false;
    downloadButton.disabled = false;
    fileName.textContent = payload.filename;
    fileMeta.textContent = `${formatBytes(payload.source_bytes)} · ${Number(payload.elapsed_ms).toLocaleString()} ms · 輸出 ${Number(payload.markdown_chars).toLocaleString()} 字元`;
    updateCounter();
    await renderPreview(markdownEditor.value);
    hideStatus();
    markdownEditor.focus();
  } catch (error) {
    showError(error.message || "無法完成轉換。 ");
    markdownEditor.disabled = true;
    copyButton.disabled = true;
    resetButton.disabled = false;
    downloadButton.disabled = true;
    previewState.textContent = "轉換失敗";
  } finally {
    chooseButton.disabled = false;
    fileInput.value = "";
  }
}

function scheduleRender() {
  window.clearTimeout(renderTimer);
  previewState.textContent = "更新中…";
  renderTimer = window.setTimeout(() => renderPreview(markdownEditor.value), 220);
}

async function renderPreview(markdown) {
  const sequence = ++renderSequence;
  try {
    const response = await fetch("/api/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ markdown }),
    });
    const payload = await readJson(response);
    if (!response.ok) throw new Error(payload.detail || "預覽失敗。 ");
    if (sequence !== renderSequence) return;

    markdownPreview.classList.remove("empty");
    markdownPreview.innerHTML = payload.html || '<div class="empty-state"><p>Markdown 內容為空。</p></div>';
    for (const link of markdownPreview.querySelectorAll("a")) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
    previewState.textContent = "已同步";
  } catch (error) {
    if (sequence !== renderSequence) return;
    previewState.textContent = "預覽錯誤";
    markdownPreview.classList.add("empty");
    markdownPreview.textContent = error.message || "預覽失敗。";
  }
}

async function copyMarkdown() {
  try {
    await navigator.clipboard.writeText(markdownEditor.value);
    const previous = copyButton.textContent;
    copyButton.textContent = "已複製";
    window.setTimeout(() => { copyButton.textContent = previous; }, 1200);
  } catch {
    markdownEditor.select();
    document.execCommand("copy");
  }
}

function downloadMarkdown() {
  const blob = new Blob([markdownEditor.value], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = outputFilename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function resetWorkspace() {
  outputFilename = "converted.md";
  markdownEditor.value = "";
  markdownEditor.disabled = true;
  copyButton.disabled = true;
  resetButton.disabled = true;
  downloadButton.disabled = true;
  fileName.textContent = "尚未選擇檔案";
  fileMeta.textContent = "轉換後可在下方直接編輯";
  fileType.textContent = "MD";
  charCounter.textContent = "0 字元";
  previewState.textContent = "等待內容";
  markdownPreview.classList.add("empty");
  markdownPreview.innerHTML = '<div class="empty-state"><div class="empty-glyph" aria-hidden="true">#</div><p>轉換後的排版效果會顯示在此處。</p></div>';
  hideStatus();
}

function setBusy(isBusy, message) {
  chooseButton.disabled = isBusy;
  statusBanner.hidden = !isBusy;
  statusBanner.classList.remove("error");
  statusText.textContent = message;
}

function showError(message) {
  statusBanner.hidden = false;
  statusBanner.classList.add("error");
  statusText.textContent = message;
}

function hideStatus() {
  statusBanner.hidden = true;
  statusBanner.classList.remove("error");
  statusText.textContent = "";
}

function updateCounter() {
  charCounter.textContent = `${markdownEditor.value.length.toLocaleString()} 字元`;
}

function extensionLabel(name) {
  const extension = name.includes(".") ? name.split(".").pop() : "FILE";
  return extension.slice(0, 5).toUpperCase();
}

function formatBytes(bytes) {
  const value = Number(bytes) || 0;
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}

async function readJson(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}
