// Educational, quasi-static thresholds for a rigid block on a level belt.
export function packageState(ratio, acceleration, friction = 0.6) {
  const gravity = 9.81;
  const tipAt = gravity / ratio;
  const slideAt = friction * gravity;
  const firstAt = Math.min(tipAt, slideAt);
  const mode =
    acceleration < firstAt
      ? "Stable"
      : tipAt < slideAt
        ? "Tipping starts first"
        : slideAt < tipAt
          ? "Sliding starts first"
          : "Sliding and tipping thresholds coincide";
  return { mode, tipAt, slideAt, projection: (acceleration * ratio) / (2 * gravity) };
}

// Inextensible, uniform chain; equal-height supports. No creep or elasticity.
export function chainShape(length, span = 3, samples = 101) {
  if (!(length > span)) throw new RangeError("Chain length must exceed its span.");
  let lower = span / 100,
    upper = span;
  const arc = (a) => 2 * a * Math.sinh(span / (2 * a));
  while (arc(upper) > length) upper *= 2;
  for (let i = 0; i < 90; i++) {
    const midpoint = (lower + upper) / 2;
    if (arc(midpoint) > length) lower = midpoint;
    else upper = midpoint;
  }
  const a = (lower + upper) / 2;
  const end = Math.cosh(span / (2 * a));
  const points = Array.from({ length: samples }, (_, i) => {
    const x = -span / 2 + (span * i) / (samples - 1);
    return [x, a * (end - Math.cosh(x / a))];
  });
  return { a, sag: a * (end - 1), points };
}

// Constant-acceleration teaching cases: fixed-corner tipping or flat sliding.
// Rotation uses I_corner / m = (width² + height²) / 3, not an area moment.
export function packageMotion(ratio, acceleration, { dt = 0.002, duration = 3 } = {}) {
  const state = packageState(ratio, acceleration);
  const width = 0.5,
    height = width * ratio,
    gravity = 9.81;
  const inertiaPerMass = (width * width + height * height) / 3;
  const mode = state.mode;
  const frames = [{ time: 0, angle: 0, distance: 0 }];
  let angle = 0,
    omega = 0;
  const alpha = (theta) =>
    (acceleration * (width * Math.sin(theta) + height * Math.cos(theta)) - gravity * (width * Math.cos(theta) - height * Math.sin(theta))) /
    (2 * inertiaPerMass);
  const tipping = mode === "Tipping starts first";
  const sliding = mode === "Sliding starts first";
  for (let i = 1; i <= Math.round(duration / dt); i++) {
    const time = i * dt;
    let distance = 0;
    if (tipping) {
      const a1 = alpha(angle),
        v1 = omega;
      const a2 = alpha(angle + (dt * v1) / 2),
        v2 = omega + (dt * a1) / 2;
      const a3 = alpha(angle + (dt * v2) / 2),
        v3 = omega + (dt * a2) / 2;
      const a4 = alpha(angle + dt * v3),
        v4 = omega + dt * a3;
      const next = angle + (dt * (v1 + 2 * v2 + 2 * v3 + v4)) / 6;
      omega += (dt * (a1 + 2 * a2 + 2 * a3 + a4)) / 6;
      if (next >= Math.PI / 2) {
        const fraction = (Math.PI / 2 - angle) / (next - angle);
        frames.push({ time: (i - 1 + fraction) * dt, angle: Math.PI / 2, distance: 0 });
        break;
      }
      angle = next;
    } else if (sliding) {
      // Kinetic friction opposes leftward motion relative to the belt.
      distance = 0.5 * (acceleration - 0.5 * gravity) * time * time;
      if (distance >= 1.5) {
        frames.push({ time: Math.sqrt(3 / (acceleration - 0.5 * gravity)), angle: 0, distance: 1.5 });
        break;
      }
    }
    frames.push({ time, angle, distance });
  }
  return {
    mode,
    frames,
    finished:
      tipping && frames.at(-1).angle === Math.PI / 2
        ? "Side contact: the simulation stops before impact."
        : sliding
          ? "The package slides backwards relative to the belt."
          : mode === "Stable"
            ? "The package stays upright and moves with the belt."
            : "The package has not reached side contact within this run.",
  };
}

// Supplied MATLAB structural length-change scenario, with time in years.
// Coefficients are assumed inputs, not calibrated material creep data.
export function chainCreep(length, years, span = 3, samples = 101) {
  const load = 1.1 * 9.81,
    axialStiffness = 2e11 * 5e-5;
  const creepStrain = 5e-4 + 2e-4 * Math.log1p(years);
  const residual = (a) => 2 * a * Math.sinh(span / (2 * a)) - length * (1 + (load * a * Math.cosh(span / (2 * a))) / axialStiffness + creepStrain);
  let lower = span / 100,
    upper = span;
  while (residual(upper) > 0) upper *= 2;
  for (let i = 0; i < 90; i++) {
    const mid = (lower + upper) / 2;
    if (residual(mid) > 0) lower = mid;
    else upper = mid;
  }
  const a = (lower + upper) / 2,
    end = Math.cosh(span / (2 * a));
  const points = Array.from({ length: samples }, (_, i) => {
    const x = -span / 2 + (span * i) / (samples - 1);
    return [x, a * (end - Math.cosh(x / a))];
  });
  return { a, points, sag: a * (end - 1), length: 2 * a * Math.sinh(span / (2 * a)), creepStrain };
}
