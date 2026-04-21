function toggleCrafting(el) {
    const container = el.closest(".crafting-collapsible");
    const content = container.querySelector(".crafting-collapsible-content");
    const textSpan = container.querySelector(".toggle-text");

    const isHidden = content.style.display === "none";

    content.style.display = isHidden ? "block" : "none";
    if (textSpan) textSpan.textContent = isHidden ? "Collapse" : "Expand";
}