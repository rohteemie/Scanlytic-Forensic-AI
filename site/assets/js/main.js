const revealNodes = document.querySelectorAll(".reveal");

if (!("IntersectionObserver" in window)) {
  revealNodes.forEach((node) => node.classList.add("visible"));
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 },
  );

  revealNodes.forEach((node) => observer.observe(node));
}
