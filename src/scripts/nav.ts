// Slides one pill to the nav link for the section you're reading.
const nav = document.querySelector<HTMLElement>("[data-nav]");
const pill = nav?.querySelector<HTMLElement>("[data-nav-pill]");

if (nav && pill) {
  const targets = [
    ...nav.querySelectorAll<HTMLAnchorElement>("[data-nav-link]"),
  ].flatMap((link) => {
    const section = document.querySelector<HTMLElement>(link.hash);
    return section ? [{ link, section }] : [];
  });

  // A section counts as active once its top passes this point in the viewport.
  const ACTIVE_LINE = 0.45;
  let tops: number[] = [];
  let active: HTMLAnchorElement | null = null;
  let frame = 0;

  const measure = () => {
    tops = targets.map(
      ({ section }) => section.getBoundingClientRect().top + window.scrollY,
    );
  };

  const place = (link: HTMLAnchorElement) => {
    pill.style.width = `${link.offsetWidth}px`;
    pill.style.height = `${link.offsetHeight}px`;
    pill.style.transform = `translate(${link.offsetLeft}px, ${link.offsetTop}px)`;
  };

  const setActive = (next: HTMLAnchorElement | null) => {
    if (next === active) return;
    const wasHidden = !active;
    active?.removeAttribute("aria-current");
    active = next;

    if (!next) {
      pill.style.opacity = "0";
      return;
    }

    next.setAttribute("aria-current", "location");
    if (wasHidden) {
      // Appear in place instead of sliding in from the last position.
      pill.style.transition = "none";
      place(next);
      void pill.offsetWidth;
      pill.style.transition = "";
    } else {
      place(next);
    }
    pill.style.opacity = "1";
  };

  const update = () => {
    frame = 0;
    const line = window.scrollY + window.innerHeight * ACTIVE_LINE;
    const atBottom =
      window.scrollY + window.innerHeight >=
      document.documentElement.scrollHeight - 2;

    let next: HTMLAnchorElement | null = null;
    targets.forEach(({ link }, index) => {
      const top = tops[index];
      if (top !== undefined && line >= top) next = link;
    });
    // On tall screens the last section can't reach the line, so the end of the page selects it.
    if (atBottom) next = targets.at(-1)?.link ?? next;
    setActive(next);
  };

  const schedule = () => {
    frame ||= requestAnimationFrame(update);
  };

  window.addEventListener("scroll", schedule, { passive: true });

  // Sizes change on resize and when fonts load, so re-measure and keep the pill aligned.
  const resizes = new ResizeObserver(() => {
    measure();
    if (active) place(active);
    schedule();
  });
  resizes.observe(document.body);
  resizes.observe(nav);
}
