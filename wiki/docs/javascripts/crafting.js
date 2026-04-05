document.addEventListener("DOMContentLoaded", () => {
  const slots = document.querySelectorAll(".slot.tag");

  slots.forEach(slot => {
    const items = slot.dataset.items?.split(",");
    if (!items || items.length <= 1) return;

    let index = 0;

    setInterval(() => {
      index = (index + 1) % items.length;
      const itemId = items[index];

      const img = slot.querySelector("img");
      img.src = `/images/items/${itemId}.png`;
    }, 1000);
  });
});