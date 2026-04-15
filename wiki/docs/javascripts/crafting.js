function toggleCrafting(btn) {
    const container = btn.closest(".crafting-collapsible");
    const content = container.querySelector(".crafting-collapsible-content");
    const textSpan = btn.querySelector(".toggle-text");

    const isHidden = content.style.display === "none";

    if (isHidden) {
        content.style.display = "block";
        textSpan.textContent = "Collapse";
    } else {
        content.style.display = "none";
        textSpan.textContent = "Expand";
    }
}