const pptxgen = require("/opt/homebrew/lib/node_modules/pptxgenjs");
const fs = require("fs");

const reviewDir = "/Users/richardcapobianco/Desktop/Work_Offline.nosync/SIDIS_Analysis_CLAS12_RichCap/Prepare_Next_Iteration/Fit_Refinement/plots/3D_BC_RC_acc020_review";
const summary = JSON.parse(fs.readFileSync(reviewDir + "/comparison/summary.json", "utf8"));
const pages = JSON.parse(fs.readFileSync(reviewDir + "/comparison/phi_pages.json", "utf8"));

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
pres.author = "Richard Capobianco";
pres.title = "3D BC+RC acc020 fit review";
pres.subject = "Fully corrected 3D unfolding fits and comparison with the July 2026 5D weights";

const C = {
  bg: "F7F5F2",
  ink: "1C2833",
  header: "1B3A4B",
  accent: "B85C38",
  card: "FFFCF8",
  muted: "5E6A71",
  line: "D9D3C9",
  white: "FFFFFF",
  good: "1F7A4D",
};

function footer(slide, label) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 7.22, w: 13.333, h: 0.28,
    fill: { color: C.header },
  });
  slide.addText(label, {
    x: 0.4, y: 7.24, w: 10.2, h: 0.22,
    fontFace: "Calibri", fontSize: 11, color: "E7EEF2", margin: 0,
  });
  slide.addText("3D BC+RC acc020", {
    x: 10.4, y: 7.24, w: 2.5, h: 0.22,
    fontFace: "Calibri", fontSize: 11, color: "E7EEF2", align: "right", margin: 0,
  });
}

function headerBar(slide, title) {
  slide.background = { color: C.bg };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.333, h: 0.72,
    fill: { color: C.header },
  });
  slide.addText(title, {
    x: 0.4, y: 0.14, w: 12.4, h: 0.46,
    fontFace: "Georgia", fontSize: 24, color: C.white, margin: 0,
  });
}

function statCard(slide, x, y, w, h, value, label) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: w, h: h,
    fill: { color: C.card },
    shadow: { type: "outer", color: "000000", blur: 8, offset: 1, angle: 135, opacity: 0.08 },
  });
  slide.addText(value, {
    x: x + 0.12, y: y + 0.12, w: w - 0.24, h: 0.62,
    fontFace: "Calibri", fontSize: 28, color: C.header, margin: 0,
  });
  slide.addText(label, {
    x: x + 0.12, y: y + 0.78, w: w - 0.24, h: 0.48,
    fontFace: "Calibri", fontSize: 13, color: C.muted, margin: 0,
  });
}

function plotSlide(title, imagePath, caption) {
  const slide = pres.addSlide();
  headerBar(slide, title);
  const imgW = 12.2;
  const imgH = imgW * (452 / 1096);
  const imgX = (13.333 - imgW) / 2;
  const imgY = 0.95;
  slide.addImage({
    path: imagePath,
    x: imgX, y: imgY, w: imgW, h: imgH,
  });
  slide.addText(caption, {
    x: 0.45, y: imgY + imgH + 0.1, w: 12.4, h: 0.7,
    fontFace: "Calibri", fontSize: 14, color: C.ink, margin: 0,
  });
  footer(slide, "5D comparison");
}

const title = pres.addSlide();
title.background = { color: C.header };
title.addText("Fully corrected 3D φ_h fits", {
  x: 0.6, y: 1.7, w: 12, h: 0.7,
  fontFace: "Georgia", fontSize: 40, color: C.white, margin: 0,
});
title.addText("BC + RC Bayesian  ·  acc020 Zeroth Order  ·  26 October 2026", {
  x: 0.6, y: 2.55, w: 12, h: 0.4,
  fontFace: "Calibri", fontSize: 18, color: "D5E2E8", margin: 0,
});
title.addText("Refinement, native φ_h overlays, and a quantitative comparison with the July 2026 5D weights.\nThe next Monte Carlo iteration was not started.", {
  x: 0.6, y: 3.4, w: 10.5, h: 0.9,
  fontFace: "Calibri", fontSize: 18, color: C.white, margin: 0,
});

const scope = pres.addSlide();
headerBar(scope, "What was refined");
scope.addText([
  { text: "Input", options: { bold: true, breakLine: true } },
  { text: "Unfolded_Simple_3D_Final_Thesis_Bank_", options: { breakLine: true } },
  { text: "rho0_new_acc020_Zeroth_Order_Full.root", options: { breakLine: true } },
  { text: "Family", options: { bold: true, breakLine: true } },
  { text: "3D BC_RC_Bayesian only. Acceptance-only, RC-only, and 5D were not refit.", options: { breakLine: true } },
  { text: "Coverage", options: { bold: true, breakLine: true } },
  { text: "All 452 Q²-y and z-pT bins that have a 3D BC+RC φ_h histogram.", options: { breakLine: true } },
  { text: "Fit", options: { bold: true, breakLine: true } },
  { text: "A(1 + B cos φ_h + C cos 2φ_h), histogram uncertainties, spline initialization.", options: { breakLine: true } },
  { text: "Passes", options: { bold: true, breakLine: true } },
  { text: "One full remake, then one Q²-y 9 remake after a tagged guide for bin (9, 32).", options: { breakLine: false } },
], {
  x: 0.5, y: 1.05, w: 7.6, h: 5.6,
  fontFace: "Calibri", fontSize: 16, color: C.ink, paraSpaceAfter: 8, margin: 0,
});
scope.addShape(pres.shapes.RECTANGLE, {
  x: 8.4, y: 1.15, w: 4.4, h: 4.7,
  fill: { color: C.card },
});
scope.addText("Preserved in the same ROOT file\n\n452 Bayesian φ_h histograms\n452 RC φ_h histograms\n452 BC+RC φ_h histograms\n\nFit objects were written only for BC+RC (452). No extra working copy of the ROOT file.", {
  x: 8.6, y: 1.35, w: 4.0, h: 4.3,
  fontFace: "Calibri", fontSize: 15, color: C.ink, margin: 0,
});
footer(scope, "Selective write. Unselected families were not refit.");

const norm = pres.addSlide();
headerBar(norm, "Where each correction is applied");
norm.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 1.05, w: 6.15, h: 5.85,
  fill: { color: C.card },
});
norm.addShape(pres.shapes.RECTANGLE, {
  x: 6.75, y: 1.05, w: 6.15, h: 5.85,
  fill: { color: C.card },
});
norm.addText("Already in the stored histogram", {
  x: 0.6, y: 1.2, w: 5.75, h: 0.4,
  fontFace: "Georgia", fontSize: 18, color: C.header, margin: 0,
});
norm.addText("3D Bayesian unfolding\nRadiative corrections\nBin-centering corrections\n\nThe fit uses this native histogram and its TH1 uncertainties. Luminosity, photon flux, and bin volume are not applied again during the fit.", {
  x: 0.6, y: 1.75, w: 5.75, h: 3.4,
  fontFace: "Calibri", fontSize: 16, color: C.ink, margin: 0,
});
norm.addText("The φ_h figures in this deck are these unnormalized distributions.", {
  x: 0.6, y: 5.5, w: 5.75, h: 0.9,
  fontFace: "Calibri", fontSize: 15, color: C.muted, margin: 0,
});
norm.addText("Applied only to spline A", {
  x: 6.95, y: 1.2, w: 5.75, h: 0.4,
  fontFace: "Georgia", fontSize: 18, color: C.header, margin: 0,
});
norm.addText("A → A / (bin area × luminosity × Γ_γ)\n\nLuminosity includes the Klimenko beam-blocker and tracking correction. B and C are not rescaled. A is stored in log space.\n\nBin (9, 32): area 0.00384, L = 4.58×10¹⁰ μb⁻¹, Γ_γ = 4.00×10⁻⁴. Beam-on / beam-off luminosity = 0.981.", {
  x: 6.95, y: 1.75, w: 5.75, h: 4.6,
  fontFace: "Calibri", fontSize: 16, color: C.ink, margin: 0,
});
footer(norm, "Each factor is applied once. Histogram fits stay unnormalized.");

const quality = pres.addSlide();
headerBar(quality, "Fit quality after two passes");
statCard(quality, 0.4, 1.05, 2.4, 1.45, "452", "Bins fitted");
statCard(quality, 2.95, 1.05, 2.4, 1.45, "0", "Failed or empty");
statCard(quality, 5.5, 1.05, 2.4, 1.45, "1.087", "Median χ²/NDF");
statCard(quality, 8.05, 1.05, 2.4, 1.45, "2.18", "95th percentile");
statCard(quality, 10.6, 1.05, 2.3, 1.45, "5", "Bins above 3");
quality.addText("Bin (9, 32) was the one poor fit. The untagged guide left B = −0.046 and χ²/NDF = 7.09. A tagged (\"9\", \"32\", \"3D\", \"BC\") guide and a Q²-y 9 remake give B = −0.137, C = −0.005, χ²/NDF = 1.554 (NDF 21). The right-hand figure is that refit. The left-hand figure is the fit before the guide change.", {
  x: 0.45, y: 2.7, w: 12.4, h: 0.85,
  fontFace: "Calibri", fontSize: 15, color: C.ink, margin: 0,
});
const pairH = 3.35;
const beforeW = pairH * (696 / 472);
const afterW = pairH * (964 / 670);
if(summary.before_932) {
  quality.addImage({
    path: summary.before_932,
    x: 0.4, y: 3.62, w: beforeW, h: pairH,
  });
}
quality.addImage({
  path: reviewDir + "/phi_h_png/Q2y09_zpt32.png",
  x: 0.55 + beforeW, y: 3.62, w: afterW, h: pairH,
});
footer(quality, "Left: before the (9, 32) guide. Right: final fit.");

const poor = pres.addSlide();
headerBar(poor, "Bins that still sit above χ²/NDF = 3");
const poorRows = [
  [
    { text: "Q²-y", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "z-pT", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "χ²/NDF", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "χ²", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "NDF", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "B", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "C", options: { fill: { color: C.header }, color: C.white, bold: true } },
  ],
];
summary.poor.filter(function(row) { return row.red >= 3.0; }).forEach(function(row) {
  poorRows.push([String(row.q2y), String(row.zpt), row.red.toFixed(2), String(row.Chi2), String(row.NDF), row.B.toFixed(3), row.C.toFixed(3)]);
});
poor.addTable(poorRows, {
  x: 0.5, y: 1.15, w: 12.3, h: 2.6,
  colW: [1.5, 1.5, 1.8, 1.6, 1.4, 2.2, 2.3],
  border: { pt: 0.5, color: C.line },
  fontFace: "Calibri",
  fontSize: 14,
  color: C.ink,
  align: "center",
  valign: "middle",
});
poor.addText("These five were left in place. (1, 32) and (1, 26) are single high bins at the edge of φ_h. (3, 29), (12, 24), and (10, 17) are elevated but still describe the histogram. No bin has χ²/NDF above 5, and no fit was excluded from the spline.", {
  x: 0.5, y: 4.15, w: 12.3, h: 1.3,
  fontFace: "Calibri", fontSize: 16, color: C.ink, margin: 0,
});
poor.addText("The pull screen of all 452 histograms did not turn up another bin that needed a new guide.", {
  x: 0.5, y: 5.55, w: 12.3, h: 0.6,
  fontFace: "Calibri", fontSize: 16, color: C.ink, margin: 0,
});
footer(poor, "Unresolved fits. None were dropped from the spline.");

const setup = pres.addSlide();
headerBar(setup, "Comparison sample");
setup.addText([
  { text: "Nominal 5D file, left unchanged", options: { bold: true, breakLine: true } },
  { text: "Prepare_Next_Iteration/rho0_Subtracted_5D_V2_4D_xB_Fit_Pars_from_5D_BC_RC_Bayesian_Compute_SplineWeight.txt", options: { breakLine: true } },
  { text: "Generated 29 July 2026. This is the file named by the reweighting and response-matrix defaults.", options: { breakLine: true } },
  { text: "New 3D file", options: { bold: true, breakLine: true } },
  { text: "Prepare_Next_Iteration/acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt", options: { breakLine: true } },
  { text: "Same C++ signature: ComputeSplineWeight(Q², xB, y, z, pT, φ_h) = A(1 + B cos φ + C cos 2φ), coordinates (xB, y, z, pT).", options: { breakLine: true } },
  { text: "Matched kinematics", options: { bold: true, breakLine: true } },
  { text: "421 shared bin centers. 31 3D bins and 48 5D bins have no partner and are not in the differences. 3D and 5D are two reductions of related data, not independent measurements.", options: { breakLine: false } },
], {
  x: 0.5, y: 1.05, w: 12.3, h: 5.7,
  fontFace: "Calibri", fontSize: 16, color: C.ink, paraSpaceAfter: 8, margin: 0,
});
footer(setup, "Differences below use the common 421 centers.");

plotSlide(
  "Modulation differences of the weight functions",
  reviewDir + "/comparison/delta_BC_hist.png",
  "Evaluated splines at the bin centers. Median |ΔB| = 0.0067 and median |ΔC| = 0.0048."
);
plotSlide(
  "B and C stay on the same line",
  reviewDir + "/comparison/BC_scatter.png",
  "Each point is one matched bin. The line is equality. Color is not used; the spread is the whole matched sample."
);
plotSlide(
  "No single y or pT band carries the change",
  reviewDir + "/comparison/delta_vs_kinematics.png",
  "ΔB versus y and ΔC versus pT. The larger B shifts sit at a few high-pT points, not in one y bin."
);
plotSlide(
  "Median |ΔB| and |ΔC| by Q²-y bin",
  reviewDir + "/comparison/median_abs_by_q2y.png",
  "Smoothed weight functions. The larger medians are Q²-y 8, 11, 12, and 15, still below 0.02."
);
plotSlide(
  "A after removing the photon-flux convention",
  reviewDir + "/comparison/A_convention_and_shape.png",
  "Left: (A_3D/A_5D)×Γ_γ. Median 0.976. Right: largest |Δ(1+B cos φ+C cos 2φ)| over φ. Median 0.012."
);
plotSlide(
  "What a drop-in file swap would do to the event weight",
  reviewDir + "/comparison/weight_ratios.png",
  "Left: log10(W_3D/W_5D) at φ_h = 0. Median ratio 1804. Right: the same ratio after multiplying out Γ_γ, in percent."
);

const largest = pres.addSlide();
headerBar(largest, "Largest fit-parameter differences");
largest.addText("Training values, before spline smoothing. |ΔB| never exceeds 0.10. |ΔC| never exceeds 0.10.", {
  x: 0.45, y: 0.85, w: 12.4, h: 0.35,
  fontFace: "Calibri", fontSize: 14, color: C.muted, margin: 0,
});
function paramTable(rows, kind) {
  const header = [
    { text: "Bin", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "y", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "z", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "pT", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "3D", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "5D", options: { fill: { color: C.header }, color: C.white, bold: true } },
    { text: "Δ", options: { fill: { color: C.header }, color: C.white, bold: true } },
  ];
  const body = [header];
  rows.slice(0, 5).forEach(function(row) {
    body.push([
      row.q2y + ", " + row.zpt,
      row.y.toFixed(2),
      row.z.toFixed(2),
      row.pT.toFixed(2),
      row[kind + "3"].toFixed(3),
      row[kind + "5"].toFixed(3),
      row["d" + kind].toFixed(3),
    ]);
  });
  return body;
}
largest.addText("B", {
  x: 0.45, y: 1.25, w: 6.0, h: 0.3,
  fontFace: "Georgia", fontSize: 16, color: C.header, margin: 0,
});
largest.addTable(paramTable(summary.largest_train_B, "B"), {
  x: 0.4, y: 1.6, w: 6.2, h: 2.5,
  border: { pt: 0.5, color: C.line },
  fontFace: "Calibri", fontSize: 12, color: C.ink, align: "center", valign: "middle",
});
largest.addText("C", {
  x: 6.85, y: 1.25, w: 6.0, h: 0.3,
  fontFace: "Georgia", fontSize: 16, color: C.header, margin: 0,
});
largest.addTable(paramTable(summary.largest_train_C, "C"), {
  x: 6.75, y: 1.6, w: 6.2, h: 2.5,
  border: { pt: 0.5, color: C.line },
  fontFace: "Calibri", fontSize: 12, color: C.ink, align: "center", valign: "middle",
});
largest.addText("Parameter |ΔB|: median 0.012, 95th percentile 0.039, maximum 0.088. 3.1% of matched bins exceed 0.05. Parameter |ΔC|: median 0.008, 95th percentile 0.033, maximum 0.068. The biggest B shifts are high-z or high-pT edges, especially (2, 6). They are spread across Q²-y rather than confined to one region.", {
  x: 0.45, y: 4.4, w: 12.4, h: 1.4,
  fontFace: "Calibri", fontSize: 15, color: C.ink, margin: 0,
});
footer(largest, "Fit parameters. The smoothed weight functions move less than these training values.");

const conclude = pres.addSlide();
headerBar(conclude, "What the change means for the next iteration");
conclude.addText([
  { text: "The φ modulation is close.", options: { bold: true, breakLine: true } },
  { text: "Across 421 shared bins, B and C differ by about 0.01. The change is broad. Q²-y 8, 11, 12, and 15 move a little more. A few high-pT edges move by 0.05–0.09 in B.", options: { breakLine: true } },
  { text: "The absolute weight is not a drop-in.", options: { bold: true, breakLine: true } },
  { text: "The new A is divided by Γ_γ. The July A is not. At φ_h = 0 the new weight is larger by a median factor 1804, and that factor changes with Q² and y (95th percentile 7451). Γ_γ itself is about 5×10⁻⁴.", options: { breakLine: true } },
  { text: "Once that factor is removed, the remaining weight change is a few percent in the middle of the distribution and a few tens of percent in the tail. The July file also uses the pre-11 August 2026 target density, a flat 2.0% luminosity difference (0.07151 / 0.0701).", options: { breakLine: true } },
  { text: "Practical step", options: { bold: true, breakLine: true } },
  { text: "Keep the Monte Carlo and response-matrix defaults on the July 5D file until a 3D weight is built with the same A convention, or the consumer is taught to expect the flux division. The new file is the right cross-section spline. It is not the right drop-in event weight.", options: { breakLine: false } },
], {
  x: 0.5, y: 1.0, w: 12.3, h: 5.8,
  fontFace: "Calibri", fontSize: 16, color: C.ink, paraSpaceAfter: 6, margin: 0,
});
footer(conclude, "Defaults were not switched. Production was not run.");

const files = pres.addSlide();
headerBar(files, "Where the products are");
files.addText([
  { text: "ROOT and JSON, updated in place", options: { bold: true, breakLine: true } },
  { text: "Unfolded_Simple_3D_Final_Thesis_Bank_", options: { breakLine: true } },
  { text: "rho0_new_acc020_Zeroth_Order_Full.root", options: { breakLine: true } },
  { text: "Fit_Pars_from_Simple_RooUnfold_SelfContained_using_", options: { breakLine: true } },
  { text: "Unfolded_Simple_3D_Final_Thesis_Bank_", options: { breakLine: true } },
  { text: "rho0_new_acc020_Zeroth_Order_Full.json", options: { breakLine: true } },
  { text: "Spline, new names", options: { bold: true, breakLine: true } },
  { text: "Prepare_Next_Iteration/acc020_3D_BC_RC_4D_xB_Fit_Pars_from_3D_BC_RC_Bayesian_Compute_SplineWeight.txt", options: { breakLine: true } },
  { text: "Matching Fit_Par_A/B/C .npz and .pkl files sit beside it. 452 training points. No failed fits removed.", options: { breakLine: true } },
  { text: "Figures", options: { bold: true, breakLine: true } },
  { text: "phi_h_pdf/Q2y01 through Q2y17, 452 pages. Comparison tables and plots are in comparison/.", options: { breakLine: true } },
  { text: "The slides after this one are those 452 fits, grouped by Q²-y.", options: { breakLine: false } },
], {
  x: 0.5, y: 1.05, w: 12.3, h: 5.6,
  fontFace: "Calibri", fontSize: 16, color: C.ink, paraSpaceAfter: 6, margin: 0,
});
footer(files, "Full-resolution PDFs remain in phi_h_pdf/.");

let lastQ = null;
pages.forEach(function(page) {
  if(page.q2y !== lastQ) {
    lastQ = page.q2y;
    const divider = pres.addSlide();
    divider.background = { color: C.header };
    const count = pages.filter(function(item) { return item.q2y === page.q2y; }).length;
    divider.addText("Q²-y bin " + page.q2y, {
      x: 0.7, y: 2.6, w: 12, h: 0.7,
      fontFace: "Georgia", fontSize: 40, color: C.white, margin: 0,
    });
    divider.addText(count + " z-pT bins   ·   native BC+RC histogram and fit", {
      x: 0.7, y: 3.45, w: 12, h: 0.4,
      fontFace: "Calibri", fontSize: 20, color: "D5E2E8", margin: 0,
    });
  }
  const slide = pres.addSlide();
  slide.background = { color: C.bg };
  slide.addText("Q²-y " + page.q2y + "    z-pT " + page.zpt, {
    x: 0.4, y: 0.12, w: 9.5, h: 0.36,
    fontFace: "Georgia", fontSize: 20, color: C.header, margin: 0,
  });
  slide.addText("Unnormalized", {
    x: 10.2, y: 0.16, w: 2.7, h: 0.3,
    fontFace: "Calibri", fontSize: 14, color: C.muted, align: "right", margin: 0,
  });
  const imgH = 6.55;
  const imgW = imgH * (964 / 670);
  const imgX = (13.333 - imgW) / 2;
  slide.addImage({
    path: page.png,
    x: imgX, y: 0.52, w: imgW, h: imgH,
  });
});

pres.writeFile({ fileName: reviewDir + "/3D_BC_RC_acc020_Final_Review.pptx" })
  .then(function() { console.log("wrote deck", pages.length); })
  .catch(function(err) { console.error(err); process.exit(1); });
