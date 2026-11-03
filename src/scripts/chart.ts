import meta from "@/assets/chart/meta.json";

type Island = [x: number, y: number, name: string, lat: number, lon: number];

const HOVER_RADIUS = 26;

const formatCoord = (value: number, positive: string, negative: string) => {
  const abs = Math.abs(value);
  const degrees = Math.floor(abs);
  const minutes = Math.floor((abs - degrees) * 60);
  const hemisphere = value >= 0 ? positive : negative;
  return `${degrees}°${String(minutes).padStart(2, "0")}′${hemisphere}`;
};

function setupHover(chart: HTMLElement) {
  const light = chart.querySelector<HTMLElement>("[data-chart-light]");
  const ring = chart.querySelector<HTMLElement>("[data-chart-ring]");
  const tip = chart.querySelector<HTMLElement>("[data-chart-tip]");
  const tipName = chart.querySelector<HTMLElement>("[data-chart-tip-name]");
  const tipCoords = chart.querySelector<HTMLElement>("[data-chart-tip-coords]");
  if (!light || !ring || !tip || !tipName || !tipCoords) return;

  let islands: Island[] = [];
  let pointer: { x: number; y: number } | null = null;
  let frame = 0;

  const render = () => {
    frame = 0;
    if (!pointer) return;
    const { x, y } = pointer;
    light.style.transform = `translate3d(${x}px, ${y}px, 0)`;

    let nearest: Island | null = null;
    let best = HOVER_RADIUS * HOVER_RADIUS;
    for (const island of islands) {
      const distance = (island[0] - x) ** 2 + (island[1] - y) ** 2;
      if (distance < best) {
        best = distance;
        nearest = island;
      }
    }

    if (!nearest) {
      delete chart.dataset.found;
      return;
    }

    const [ix, iy, name, lat, lon] = nearest;
    ring.style.transform = `translate(${ix}px, ${iy}px)`;
    tipName.textContent = name;
    tipCoords.textContent = `${formatCoord(lat, "N", "S")} ${formatCoord(lon, "E", "W")}`;
    // Sits on whichever side has room, away from the page content on the left.
    const offset = ix < 200 ? "16px" : "calc(-100% - 16px)";
    tip.style.transform = `translate(${ix}px, ${iy}px) translate(${offset}, -50%)`;
    chart.dataset.found = "";
  };

  chart.addEventListener(
    "pointerenter",
    async () => {
      const data = await import("@/assets/chart/islands.json");
      islands = data.default as unknown as Island[];
    },
    { once: true },
  );

  chart.addEventListener("pointermove", (event) => {
    const rect = chart.getBoundingClientRect();
    pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    chart.dataset.active = "";
    frame ||= requestAnimationFrame(render);
  });

  chart.addEventListener("pointerleave", () => {
    pointer = null;
    delete chart.dataset.active;
    delete chart.dataset.found;
  });
}

function setupScrollbar(chain: HTMLElement) {
  const marker = chain.querySelector<HTMLElement>("[data-chain-marker]");
  const readout = chain.querySelector<HTMLElement>("[data-chain-readout]");
  const track = marker?.parentElement;
  if (!marker || !readout || !track) return;

  const TRACK = 150;
  let frame = 0;

  const render = () => {
    frame = 0;
    const page = document.documentElement.scrollHeight;
    const view = window.innerHeight;
    const max = Math.max(page - view, 1);
    const ratio = Math.min(window.scrollY / max, 1);
    const height = Math.max((view / page) * TRACK, 16);
    marker.style.height = `${height}px`;
    marker.style.transform = `translateY(${ratio * (TRACK - height)}px)`;

    const centre = window.scrollY + view / 2;
    const lat = Math.max(meta.lat0 - centre / meta.scale, -0.78);
    readout.textContent = formatCoord(lat, "N", "S");
  };

  const schedule = () => {
    frame ||= requestAnimationFrame(render);
  };

  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule, { passive: true });

  track.addEventListener("click", (event) => {
    const rect = track.getBoundingClientRect();
    const ratio = (event.clientY - rect.top) / rect.height;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    window.scrollTo({ top: ratio * max });
  });

  schedule();
  document.documentElement.dataset.chainReady = "";
}

const chart = document.querySelector<HTMLElement>("[data-chart]");
if (chart && matchMedia("(hover: hover) and (pointer: fine)").matches) {
  setupHover(chart);
}

// The scrollbar only exists at desktop widths, so phones skip its scroll work.
const chain = document.querySelector<HTMLElement>("[data-chain]");
const desktop = matchMedia("(min-width: 80rem)");
const startScrollbar = () => {
  if (!chain || !desktop.matches) return;
  desktop.removeEventListener("change", startScrollbar);
  setupScrollbar(chain);
};
desktop.addEventListener("change", startScrollbar);
startScrollbar();
