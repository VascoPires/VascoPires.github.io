import { chainCreep, packageState, packageMotion } from "./do-it-models.mjs";

async function initGrain() {
  const root = document.querySelector("[data-grain-viewer]");
  if (!root) return;
  try {
    const response = await fetch(root.dataset.url);
    if (!response.ok) throw new Error("Grain data unavailable");
    const data = await response.json();
    const shape = root.querySelector("#grain-shape");
    const arrangement = root.querySelector("#grain-state");
    const point = ([x, y]) => `${(290 + x * 9).toFixed(2)},${(130 - y * 9).toFixed(2)}`;
    const chartX = (step, max) => 45 + (285 * step) / max;
    const chartY = (load) => 210 - 14 * load;
    const update = () => {
      const model = data[shape.value];
      const state = model.states[Number(arrangement.value)];
      const row = model.history.find((row) => row.iteration === state.step);
      root.querySelector("[data-grain-lines]").innerHTML = state.lines.map((line) => `<polyline points="${line.map(point).join(" ")}"/>`).join("");
      root
        .querySelector("[data-grain-outline]")
        .setAttribute("d", model.outline.map((edge) => `M${point(edge[0])}L${point(edge[1])}`).join(" ") + " M47 40H533 M47 220H533");
      const max = model.history.at(-1).iteration;
      root.querySelector("[data-grain-grid]").innerHTML =
        [0, 5, 10]
          .map(
            (load) =>
              `<path d="M45 ${chartY(load)}H330" class="doit-grain-gridline"/><text x="35" y="${chartY(load) + 4}" text-anchor="end">${load}</text>`
          )
          .join("") + [0, max].map((step) => `<text x="${chartX(step, max)}" y="228" text-anchor="middle">${step}</text>`).join("");
      root
        .querySelector("[data-grain-curve]")
        .setAttribute(
          "d",
          model.history.map((row, index) => `${index ? "L" : "M"}${chartX(row.iteration, max)},${chartY(row.failure_load)}`).join(" ")
        );
      const marker = root.querySelector("[data-grain-marker]");
      marker.setAttribute("cx", chartX(state.step, max));
      marker.setAttribute("cy", chartY(row.failure_load));
      root.querySelector("[data-grain-caption]").textContent = `${arrangement.selectedOptions[0].text} · model step ${state.step}`;
      root.querySelector("[data-grain-result]").textContent = `First failure: ${row.failure_load.toFixed(
        1
      )} MPa. Peak fiber shear: ${row.tau_LR_max.toFixed(1)} MPa.`;
      root.querySelector("[data-grain-finding]").textContent =
        shape.value === "circle"
          ? "The rounded hole gains strength, but the first reorientation is stronger than the final grain arrangement. Following stress is not the same as finding the strongest design."
          : "Around the sharp hole, fiber shear drops—but transverse tension remains. The final arrangement gains almost no first-failure strength.";
    };
    shape.addEventListener("change", update);
    arrangement.addEventListener("change", update);
    update();
    root.querySelector("[data-grain-content]").hidden = false;
  } catch {
    root.querySelector("[data-grain-error]").hidden = false;
  }
}

async function initTrunk() {
  const root = document.querySelector("[data-trunk-viewer]");
  if (!root) return;
  if ("IntersectionObserver" in window) {
    await new Promise((resolve) => {
      const observer = new IntersectionObserver(
        (entries) => {
          if (entries.some((entry) => entry.isIntersecting)) {
            observer.disconnect();
            resolve();
          }
        },
        { rootMargin: "600px" }
      );
      observer.observe(root);
    });
  }
  const status = root.querySelector("[data-trunk-status]");
  status.hidden = false;
  try {
    const response = await fetch(root.dataset.url);
    if (!response.ok) throw new Error("Trunk data unavailable");
    const data = (await response.json()).cases;
    const view = root.querySelector("#trunk-view");
    const state = root.querySelector("#trunk-state");
    const point = ([x, y]) => `${(160 + 0.9 * y).toFixed(2)},${(230 - 0.9 * x).toFixed(2)}`;
    const colors = [
      [245, 241, 232],
      [236, 171, 77],
      [155, 24, 57],
    ];
    const color = (index) => {
      const t = Math.sqrt(Math.max(0, Math.min(1, index))) * 2;
      const base = Math.min(1, Math.floor(t));
      const f = t - base;
      return `rgb(${colors[base].map((v, i) => Math.round(v + f * (colors[base + 1][i] - v))).join(",")})`;
    };
    const update = () => {
      const index = Number(state.value);
      const showIndex = view.value === "index";
      for (const figure of root.querySelectorAll("[data-trunk-case]")) {
        const model = data[figure.dataset.trunkCase];
        const selected = model.states[index];
        const lines = figure.querySelector("[data-trunk-lines]");
        const map = figure.querySelector("[data-trunk-map]");
        lines.innerHTML = showIndex ? "" : selected.lines.map((line) => `<polyline points="${line.map(point).join(" ")}"/>`).join("");
        if (showIndex) {
          // Merge equally colored faces to keep the detailed FE map lightweight in the DOM.
          const bands = new Map();
          model.triangles.forEach((triangle, i) => {
            const fill = color(selected.index[i]);
            const face = `M${triangle.map(point).join("L")}Z`;
            bands.set(fill, (bands.get(fill) || "") + face);
          });
          map.innerHTML = [...bands]
            .map(([fill, path]) => `<path d="${path}" fill="${fill}" stroke="${fill}" stroke-width="0.4" stroke-linejoin="round"/>`)
            .join("");
        } else map.innerHTML = "";
        figure.classList.toggle("doit-trunk-map", showIndex);
        figure
          .querySelector("[data-trunk-outline]")
          .setAttribute(
            "d",
            model.outline.map((edge) => `M${point(edge[0])}L${point(edge[1])}`).join(" ") + " M25 50H295 M25 410H295 M25 50V410 M295 50V410"
          );
        figure.querySelector("[data-trunk-index]").textContent = `Peak failure index: ${selected.metrics.tsai_hill_max.toFixed(2)}`;
        figure.querySelector("[data-trunk-transverse]").textContent = `Transverse tension: ${selected.metrics.sig_R_max.toFixed(2)} MPa`;
        figure.querySelector("[data-trunk-desc]").textContent = `${state.selectedOptions[0].text}, model step ${selected.step}. ${
          showIndex
            ? "Failure index on a common zero-to-one color scale."
            : "Computed trunk fiber axes; the branch core has fixed fibers out of the surface."
        }`;
      }
      root.querySelector("[data-trunk-legend]").hidden = !showIndex;
      root.querySelector("[data-trunk-finding]").textContent =
        "The filled region is branch material; the opening is empty. Compare the local response using the same color scale. The opening and branch have different diameters.";
    };
    view.addEventListener("change", update);
    state.addEventListener("change", update);
    update();
    root.querySelector("[data-trunk-content]").hidden = false;
    status.hidden = true;
  } catch {
    status.hidden = true;
    root.querySelector("[data-trunk-error]").hidden = false;
  }
}

async function initSeasons() {
  const root = document.querySelector("[data-season-viewer]");
  if (!root) return;
  const status = root.querySelector("[data-season-status]");
  status.hidden = false;
  try {
    const response = await fetch(root.dataset.url);
    if (!response.ok) throw new Error("Growth data unavailable");
    const data = (await response.json()).cases;
    const modelInput = root.querySelector("#season-case");
    const requestedCase = new URLSearchParams(window.location.search).get("growth");
    if (Object.hasOwn(data, requestedCase)) modelInput.value = requestedCase;
    const slider = root.querySelector("#growth-season");
    const sliderLayout = window.matchMedia("(min-width: 901px)");
    const setSliderOrientation = () => slider.setAttribute("aria-orientation", sliderLayout.matches ? "vertical" : "horizontal");
    setSliderOrientation();
    sliderLayout.addEventListener("change", setSliderOrientation);
    const view = root.querySelector("#season-view");
    root.dataset.panel = view.value;
    view.addEventListener("change", () => {
      root.dataset.panel = view.value;
    });
    const play = root.querySelector("[data-season-play]");
    let model,
      playing = false,
      request = 0,
      last = 0,
      elapsed = 0;
    const fieldPoint = ([x, y]) => `${(180 + 0.8 * y).toFixed(2)},${(220 - 0.8 * x).toFixed(2)}`;
    const path = (points) => points.map((point, i) => `${i ? "L" : "M"}${fieldPoint(point)}`).join(" ");
    const update = () => {
      const k = Number(slider.value),
        current = model.states[k];
      root.dataset.model = modelInput.value;
      const render = root.querySelector("[data-season-render]");
      render.hidden = false;
      const isHole = modelInput.value === "trunk_hole";
      const saved = (isHole ? [0, 5, 10, 20, 40] : [0, 5, 10, 20]).filter((step) => step <= current.step).at(-1);
      const base = isHole ? render.dataset.base : render.dataset.branchBase;
      render.querySelector("img").src = `${base}${String(saved).padStart(2, "0")}.webp${isHole ? "" : "?v=joined-section-1"}`;
      render.querySelector("img").alt = `Cutaway of the ${isHole ? "hole" : "loaded 40° branch"} growth model at saved model step ${saved}`;
      slider.setAttribute("aria-valuetext", `Model season ${current.step}`);
      root.querySelector("[data-season-label]").textContent = `${current.step} of ${model.states.at(-1).step}`;
      root.querySelector("[data-season-footprint]").setAttribute("d", path(model.footprint) + "Z");
      root.querySelector("[data-season-fronts]").innerHTML = model.states
        .slice(0, k + 1)
        .map(
          (row, i) =>
            `<path d="${row.fronts.map(path).join(" ")}" stroke="${i === k ? "var(--doit-accent)" : "var(--doit-muted)"}" stroke-width="${
              i === k ? 2.5 : 0.8
            }" opacity="${i === k ? 1 : 0.2}"/>`
        )
        .join("");
      const maxStep = model.states.at(-1).step;
      const chartX = (step) => 65 + (500 * step) / maxStep;
      const vMax = Math.max(0.01, ...model.states.map((row) => row.per_season_cm3)) * 1.1;
      const fMax = Math.max(1, ...model.states.map((row) => row.failure_index)) * 1.05;
      const chartY = (value) => 365 - (300 * value) / fMax;
      const volumeY = (value) => 365 - (300 * value) / vMax;
      root.querySelector("[data-season-response-axis]").innerHTML =
        `<text x="65" y="25" class="doit-season-volume-label">Wood added / cm³</text><text x="565" y="48" text-anchor="end" class="doit-season-index-label">Failure index</text>` +
        [0, 0.5, 1]
          .map((fraction) => {
            const y = 365 - 300 * fraction;
            return `<path d="M65 ${y}H565" class="doit-season-grid"/><text x="55" y="${
              y + 5
            }" text-anchor="end" class="doit-season-volume-label">${Number((vMax * fraction).toFixed(2))}</text><text x="575" y="${
              y + 5
            }" class="doit-season-index-label">${Number((fMax * fraction).toFixed(2))}</text>`;
          })
          .join("") +
        `<path d="M65 65V365H565V65" class="doit-season-axis"/>` +
        [0, maxStep / 2, maxStep].map((step) => `<text x="${chartX(step)}" y="393" text-anchor="middle">${step}</text>`).join("");
      root.querySelector("[data-season-bars]").innerHTML = model.states
        .slice(1)
        .map((row, i) => {
          const height = (300 * row.per_season_cm3) / vMax,
            width = Math.max(2, 380 / maxStep);
          return `<rect x="${chartX(row.step) - width / 2}" y="${volumeY(
            row.per_season_cm3
          )}" width="${width}" height="${height}" fill="var(--doit-wood)" opacity="${i + 1 > k ? 0.25 : 1}"/>`;
        })
        .join("");
      root.querySelector("[data-season-volume]").textContent = `Season ${current.step}: ${current.per_season_cm3.toFixed(
        2
      )} cm³ · total ${current.added_cm3.toFixed(2)} cm³.`;
      root.querySelector("[data-season-threshold]").setAttribute("d", `M65 ${chartY(1)}H565`);
      root.querySelector("[data-season-cursor]").setAttribute("d", `M${chartX(current.step)} 65V365`);
      root
        .querySelector("[data-season-failure-line]")
        .setAttribute("d", model.states.map((row, i) => `${i ? "L" : "M"}${chartX(row.step)},${chartY(row.failure_index)}`).join(" "));
      const marker = root.querySelector("[data-season-failure-marker]");
      marker.setAttribute("cx", chartX(current.step));
      marker.setAttribute("cy", chartY(current.failure_index));
      root.querySelector("[data-season-failure]").textContent = `Index ${current.failure_index.toFixed(2)} · dashed: threshold 1.`;
    };
    const pause = () => {
      playing = false;
      cancelAnimationFrame(request);
      play.textContent = "Play";
      last = 0;
      elapsed = 0;
    };
    const tick = (time) => {
      if (!playing) return;
      if (last) elapsed += time - last;
      last = time;
      if (elapsed >= 250) {
        slider.value = Math.min(Number(slider.value) + 1, model.states.length - 1);
        elapsed = 0;
        update();
        if (Number(slider.value) === model.states.length - 1) {
          pause();
          return;
        }
      }
      request = requestAnimationFrame(tick);
    };
    const changeModel = () => {
      pause();
      model = data[modelInput.value];
      slider.max = model.states.length - 1;
      slider.value = Math.min(5, model.states.length - 1);
      update();
    };
    slider.addEventListener("input", () => {
      pause();
      update();
    });
    modelInput.addEventListener("change", changeModel);
    play.addEventListener("click", () => {
      if (playing) {
        pause();
        return;
      }
      if (Number(slider.value) === model.states.length - 1) slider.value = 0;
      playing = true;
      play.textContent = "Pause";
      update();
      request = requestAnimationFrame(tick);
    });
    root.querySelector("[data-season-reset]").addEventListener("click", () => {
      pause();
      slider.value = 0;
      update();
    });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) pause();
    });
    if ("IntersectionObserver" in window)
      new IntersectionObserver((entries) => {
        if (!entries[0].isIntersecting) pause();
      }).observe(root);
    changeModel();
    root.querySelector("[data-season-content]").hidden = false;
    status.hidden = true;
  } catch {
    status.hidden = true;
    root.querySelector("[data-season-error]").hidden = false;
  }
}

function initPackage() {
  const root = document.querySelector("[data-package-experiment]");
  if (!root) return;
  const ratio = root.querySelector("#package-ratio");
  const acceleration = root.querySelector("#package-acceleration");
  const progress = root.querySelector("#package-progress");
  const play = root.querySelector("[data-package-play]");
  const status = root.querySelector("[data-package-status]");
  const body = root.querySelector("[data-package-body]");
  const rollers = [...root.querySelectorAll("[data-belt-roller]")];
  const plots = root.closest("section").querySelector("[data-package-plots]");
  const mapX = (ratio) => 50 + ((ratio - 1) / 2.5) * 400;
  const mapY = (acceleration) => 260 - (acceleration / 9) * 205;
  const criticalRatio = 1 / 0.6;
  const boundary = Array.from({ length: 81 }, (_, i) => {
    const ratio = criticalRatio + ((3.5 - criticalRatio) * i) / 80;
    return [mapX(ratio), mapY(9.81 / ratio)];
  });
  const pointString = (points) => points.map(([x, y], i) => `${i ? "L" : "M"}${x} ${y}`).join(" ");
  plots
    .querySelector('[data-package-zone="stable"]')
    .setAttribute("d", pointString([[50, 260], [450, 260], ...boundary.toReversed(), [50, mapY(0.6 * 9.81)]]) + " Z");
  plots.querySelector('[data-package-zone="sliding"]').setAttribute(
    "d",
    pointString([
      [50, 55],
      [mapX(criticalRatio), 55],
      [mapX(criticalRatio), mapY(0.6 * 9.81)],
      [50, mapY(0.6 * 9.81)],
    ]) + " Z"
  );
  plots
    .querySelector('[data-package-zone="tipping"]')
    .setAttribute("d", pointString([[mapX(criticalRatio), 55], [450, 55], ...boundary.toReversed()]) + " Z");
  plots.querySelector("[data-package-boundary]").setAttribute("d", pointString([[50, mapY(0.6 * 9.81)], ...boundary]));

  let simulation,
    running = false,
    animation,
    start,
    elapsed = 0;
  const pause = () => {
    running = false;
    cancelAnimationFrame(animation);
    play.textContent = Number(progress.value) === 1000 ? "Replay simulation" : "Run simulation";
  };
  const draw = () => {
    const end = simulation.frames.at(-1).time;
    elapsed = (Number(progress.value) / 1000) * end;
    let i = simulation.frames.findIndex((frame) => frame.time >= elapsed);
    if (i < 0) i = simulation.frames.length - 1;
    const upper = simulation.frames[i],
      lower = simulation.frames[Math.max(0, i - 1)];
    const fraction = upper.time === lower.time ? 0 : (elapsed - lower.time) / (upper.time - lower.time);
    const theta = lower.angle + (upper.angle - lower.angle) * fraction;
    const distance = lower.distance + (upper.distance - lower.distance) * fraction;
    const beltDistance = 0.5 * Number(acceleration.value) * elapsed * elapsed;
    const beltTravel = beltDistance * 140;
    // Ground view initially, then track the belt so the package stays readable.
    const camera = Math.max(0, beltTravel - 90);
    const relativeTravel = beltTravel - camera;
    const packageTravel = relativeTravel - distance * 140;
    body.setAttribute("transform", `translate(${packageTravel} 0) rotate(${(-theta * 180) / Math.PI} 220 270)`);
    root.querySelector("[data-belt-markings]").setAttribute("transform", `translate(${relativeTravel % 60} 0)`);
    rollers.forEach((roller, index) => {
      const x = -100 + index * 90 - (camera % 90);
      // Top of each clockwise-turning roller moves right with the belt.
      const rotation = ((beltTravel / 13) * 180) / Math.PI;
      roller.setAttribute("transform", `translate(${x} 287) rotate(${rotation % 360})`);
    });
    root.querySelector("[data-belt-speed]").textContent = `${(Number(acceleration.value) * elapsed).toFixed(2)} m/s`;
    root.querySelector("[data-belt-travel]").textContent = `${beltDistance.toFixed(2)} m travelled`;
    root.querySelector("[data-package-pivot]").setAttribute("cx", 220 + relativeTravel);
    // Keep a tall fallen block and a sliding block inside the diagram viewport.
    const left = Math.min(0, 220 + packageTravel - 70 * Number(ratio.value) - 20, 220 + packageTravel - 20);
    root.querySelector("svg").setAttribute("viewBox", `${left} 0 ${520 - left} 340`);
    root.querySelector(".doit-diagram-ground").setAttribute("x1", left + 8);
    root.querySelector("[data-package-resultant]").setAttribute("visibility", elapsed > 0 ? "hidden" : "visible");
    root.querySelector("[data-package-projection]").setAttribute("visibility", elapsed > 0 ? "hidden" : "visible");
    root.querySelector("[data-package-pivot]").setAttribute("visibility", theta > 0 ? "visible" : "hidden");
    root.querySelector("[data-package-time]").textContent = `${elapsed.toFixed(2)} s`;
    progress.setAttribute("aria-valuetext", `${elapsed.toFixed(2)} seconds; ${Math.round((theta * 180) / Math.PI)} degrees tilted`);
    status.textContent =
      Number(acceleration.value) === 0
        ? "The belt is at rest. Increase acceleration to set it in motion."
        : Number(progress.value) === 1000
          ? simulation.finished
          : elapsed === 0
            ? `${simulation.mode}. Press Run simulation to see the motion.`
            : simulation.mode === "Stable"
              ? "The package moves with the belt and stays upright."
              : simulation.mode === "Tipping starts first"
                ? "The package rotates about its lower left corner."
                : "The package slides left as the belt accelerates right.";
  };
  const configure = () => {
    pause();
    progress.value = 0;
    const r = Number(ratio.value),
      a = Number(acceleration.value),
      result = packageState(r, a);
    simulation = packageMotion(r, a);
    const marker = plots.querySelector("[data-package-map-point]");
    marker.setAttribute("cx", mapX(r));
    marker.setAttribute("cy", mapY(a));

    const height = 70 * r,
      center = 270 - height / 2,
      projected = 255 - 70 * result.projection;
    const box = root.querySelector("[data-package-box]");
    box.setAttribute("y", 270 - height);
    box.setAttribute("height", height);
    root.querySelector("[data-package-center]").setAttribute("cy", center);
    root.querySelector("[data-package-projection]").setAttribute("cx", projected);
    root.querySelector("[data-package-resultant]").setAttribute("d", `M255 ${center} L${projected} 270`);
    root.querySelector("[data-package-ratio]").textContent = r.toFixed(1);
    root.querySelector("[data-package-acceleration]").textContent = `${a.toFixed(1)} m/s²`;
    ratio.setAttribute("aria-valuetext", `${r.toFixed(1)} times as tall as it is wide`);
    acceleration.setAttribute("aria-valuetext", `${a.toFixed(1)} metres per second squared`);
    draw();
  };
  const tick = (now) => {
    if (!running) return;
    const end = simulation.frames.at(-1).time;
    progress.value = Math.min(1000, ((now - start) / (end * 3000)) * 1000);
    draw();
    if (Number(progress.value) === 1000) pause();
    else animation = requestAnimationFrame(tick);
  };
  play.addEventListener("click", () => {
    if (running) {
      pause();
      return;
    }
    if (Number(progress.value) === 1000) progress.value = 0;
    start = performance.now() - (Number(progress.value) / 1000) * simulation.frames.at(-1).time * 3000;
    running = true;
    play.textContent = "Pause simulation";
    animation = requestAnimationFrame(tick);
  });
  progress.addEventListener("input", () => {
    pause();
    draw();
  });
  root.querySelector("[data-package-reset]").addEventListener("click", () => {
    pause();
    progress.value = 0;
    draw();
  });
  [ratio, acceleration].forEach((input) => input.addEventListener("input", configure));
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause();
  });
  if ("IntersectionObserver" in window)
    new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) pause();
    }).observe(root);
  root.querySelector(".doit-experiment-controls").hidden = false;
  configure();
}

function initChain() {
  const root = document.querySelector("[data-chain-experiment]");
  if (!root) return;
  const length = 4; // Supplied MATLAB scenario: fixed initial chain length.
  const yearsInput = root.querySelector("#chain-years");
  const magnify = root.querySelector("#chain-magnify");
  const update = () => {
    const years = Number(yearsInput.value);
    const baseline = chainCreep(length, 0),
      result = chainCreep(length, years);
    const amplification = magnify.checked ? 500 : 1,
      verticalScale = magnify.checked ? 90 : 440 / 3;
    const displayed = result.points.map(([x, y], i) => [x, baseline.points[i][1] + amplification * (y - baseline.points[i][1])]);
    const path = (points) =>
      points.map(([x, y], i) => `${i ? "L" : "M"}${(260 + (x * 440) / 3).toFixed(2)} ${(65 + y * verticalScale).toFixed(2)}`).join(" ");
    root.querySelector("[data-chain-line]").setAttribute("d", path(displayed));
    root.querySelector("[data-chain-baseline]").setAttribute("d", path(baseline.points));
    const shownSag = baseline.sag + amplification * (result.sag - baseline.sag);
    root.querySelector("[data-chain-sag]").setAttribute("d", `M260 65 V${65 + shownSag * verticalScale}`);
    root.querySelector("[data-chain-sag-label]").setAttribute("y", 72 + (shownSag * verticalScale) / 2);
    root.querySelector("[data-chain-years]").textContent = `${years.toFixed(1)} years`;
    root.querySelector("[data-chain-status]").textContent = `Sag: ${result.sag.toFixed(3)} m · creep adds ${(
      (result.sag - baseline.sag) *
      1000
    ).toFixed(2)} mm`;
    root.querySelector("[data-chain-scale]").textContent = magnify.checked
      ? "Creep change shown ×500; readouts use actual values."
      : "Actual scale; dashed curve shows the initial shape.";
    yearsInput.setAttribute("aria-valuetext", `${years} years under load`);
  };
  const play = root.querySelector("[data-chain-play]");
  let running = false,
    animation,
    start;
  const pause = () => {
    running = false;
    cancelAnimationFrame(animation);
    play.textContent = Number(yearsInput.value) === 30 ? "Replay years" : "Play years";
  };
  const tick = (now) => {
    if (!running) return;
    yearsInput.value = Math.min(30, ((now - start) / 8000) * 30);
    update();
    if (Number(yearsInput.value) === 30) pause();
    else animation = requestAnimationFrame(tick);
  };
  play.addEventListener("click", () => {
    if (running) {
      pause();
      return;
    }
    if (Number(yearsInput.value) === 30) yearsInput.value = 0;
    start = performance.now() - (Number(yearsInput.value) / 30) * 8000;
    running = true;
    play.textContent = "Pause years";
    animation = requestAnimationFrame(tick);
  });
  yearsInput.addEventListener("input", () => {
    pause();
    update();
  });
  magnify.addEventListener("input", update);
  root.querySelector("[data-chain-reset]").addEventListener("click", () => {
    pause();
    yearsInput.value = 0;
    update();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause();
  });
  if ("IntersectionObserver" in window)
    new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) pause();
    }).observe(root);
  root.querySelector(".doit-experiment-controls").hidden = false;
  update();
}

async function initLanding() {
  const root = document.querySelector("[data-landing-experiment]");
  if (!root) return;
  try {
    const response = await fetch(root.dataset.responseUrl);
    if (!response.ok) throw new Error("Response unavailable");
    const data = await response.json();
    if (
      !Array.isArray(data.time) ||
      data.time.length !== 241 ||
      ["damped", "compression", "force"].some((key) => data[key]?.length !== data.time.length || data[key].some((value) => !Number.isFinite(value)))
    )
      throw new Error("Response incomplete");
    const input = root.querySelector("#landing-progress");
    const play = root.querySelector("[data-landing-play]");
    const output = root.querySelector("[data-landing-time]");
    const postContact = data.time.map((t, i) => ({ t, i })).filter(({ t }) => t >= 0);
    const plotX = (t) => 48 + (Math.max(0, t) / 2.3) * 342;
    for (const key of ["compression", "force"]) {
      const path = postContact.map(({ t, i }, j) => `${j ? "L" : "M"}${plotX(t).toFixed(2)} ${(270 - data[key][i] * 205).toFixed(2)}`).join(" ");
      root.querySelector(`[data-landing-${key}]`).setAttribute("d", path);
    }
    let running = false,
      animation,
      start;
    const update = () => {
      const frame = Number(input.value),
        t = data.time[frame];
      ["damped"].forEach((key) => {
        const panel = root.querySelector(`[data-landing-panel="${key}"]`);
        const chassis = 292 - data[key][frame] * 220;
        const foot = Math.min(292, chassis + data.rest * 220);
        panel.querySelector("[data-lander-body]").setAttribute("transform", `translate(0 ${chassis - 95})`);
        panel.querySelector("[data-lander-legs]").setAttribute("d", `M156 ${chassis} L106 ${foot} M264 ${chassis} L314 ${foot}`);
        panel.querySelector("[data-lander-feet]").setAttribute("d", `M86 ${foot} H126 M294 ${foot} H334`);
        panel.querySelector("[data-landing-state]").textContent =
          t < 0
            ? "Before touchdown"
            : foot < 291.5
              ? "Rebounding: footpads leave the ground"
              : key === "damped" && t > 1.1
                ? "Settled, with footpads on the ground"
                : "Footpads in contact";
      });
      const x = plotX(t);
      root.querySelector("[data-landing-cursor]").setAttribute("d", `M${x} 55 V270`);
      for (const key of ["compression", "force"]) {
        const point = root.querySelector(`[data-landing-${key}-point]`);
        point.setAttribute("cx", x);
        point.setAttribute("cy", 270 - data[key][frame] * 205);
      }
      const label = t < 0 ? "Approaching the surface" : `${t.toFixed(2)} s after touchdown`;
      output.textContent = label;
      input.setAttribute("aria-valuetext", label);
    };
    const pause = () => {
      running = false;
      cancelAnimationFrame(animation);
      play.textContent = Number(input.value) === 240 ? "Replay landing" : "Play landing";
    };
    const tick = (now) => {
      if (!running) return;
      const index = Math.min(240, Math.floor(((now - start) / 6000) * 240));
      input.value = index;
      update();
      if (index === 240) pause();
      else animation = requestAnimationFrame(tick);
    };
    play.addEventListener("click", () => {
      if (running) {
        pause();
        return;
      }
      if (Number(input.value) === 240) input.value = 0;
      start = performance.now() - (Number(input.value) / 240) * 6000;
      running = true;
      play.textContent = "Pause landing";
      animation = requestAnimationFrame(tick);
    });
    input.addEventListener("input", () => {
      pause();
      update();
    });
    root.querySelector("[data-landing-reset]").addEventListener("click", () => {
      pause();
      input.value = 0;
      update();
    });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) pause();
    });
    if ("IntersectionObserver" in window)
      new IntersectionObserver((entries) => {
        if (!entries[0].isIntersecting) pause();
      }).observe(root);
    root.querySelector(".doit-landing-controls").hidden = false;
    update();
  } catch {
    root.querySelector(".doit-landing-error").hidden = false;
  }
}

initSeasons();
initGrain();
initTrunk();
initPackage();
initChain();
initLanding();
