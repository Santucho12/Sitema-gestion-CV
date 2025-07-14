// Solo función para mostrar nombre de archivo cargado
function updateFileName(input, infoSpanId, btnId) {
  const infoSpan = document.getElementById(infoSpanId);
  const btn = document.getElementById(btnId);
  if (input.files.length > 0) {
    btn.classList.add("cv-cargado");
    infoSpan.textContent = `✅`;
  }
}
