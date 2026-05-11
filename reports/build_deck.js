/* Build the MMAI 869 final presentation.
 * Run with: node reports/build_deck.js
 * Output:   reports/Team-Union_MMAI869_Final.pptx
 */

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const FIG = path.join(__dirname, "figures");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3" × 7.5"
pres.author = "Team-Union";
pres.title = "Steve's Luxury Resort — Churn Prediction";

// ============================
// Palette
// ============================
const NAVY = "0F2A47";        // primary dark
const NAVY_DARK = "081C33";   // title slides
const GOLD = "C9A24E";        // accent
const CORAL = "C0392B";       // alarm/eureka
const CREAM = "F6F1E7";       // light bg
const WHITE = "FFFFFF";
const SLATE = "4A5468";       // body text
const LIGHT_BG = "F2EFE7";

const FONT_TITLE = "Georgia";
const FONT_BODY = "Calibri";

// ============================
// Helpers
// ============================
function slideHeader(slide, kicker, title) {
  // Top accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.3, h: 0.18,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  // Kicker
  slide.addText(String(kicker).toUpperCase(), {
    x: 0.5, y: 0.32, w: 12, h: 0.32,
    fontFace: FONT_BODY, fontSize: 11, bold: true,
    color: GOLD, charSpacing: 6, margin: 0,
  });
  // Title
  slide.addText(title, {
    x: 0.5, y: 0.62, w: 12.3, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 32, bold: true,
    color: NAVY, margin: 0,
  });
}

function slideFooter(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 12.3, y: 7.05, w: 0.8, h: 0.3,
    fontFace: FONT_BODY, fontSize: 9, color: SLATE, align: "right", margin: 0,
  });
  slide.addText("Steve's Luxury Resort · MMAI 869 · Team-Union", {
    x: 0.5, y: 7.05, w: 8, h: 0.3,
    fontFace: FONT_BODY, fontSize: 9, color: SLATE, margin: 0,
  });
}

const TOTAL = 12;

// ============================
// Slide 1: TITLE (open fast — brief says don't dwell here)
// ============================
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DARK };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 6.25, w: 13.3, h: 0.05,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });
  s.addText("THE ALL-INCLUSIVE PARADOX", {
    x: 0.5, y: 1.7, w: 12.3, h: 0.5,
    fontFace: FONT_BODY, fontSize: 14, bold: true, color: GOLD, charSpacing: 8, margin: 0,
  });
  s.addText("Predicting Churn at Steve's Luxury Resort", {
    x: 0.5, y: 2.3, w: 12.3, h: 1.6,
    fontFace: FONT_TITLE, fontSize: 56, bold: true, color: WHITE, margin: 0,
  });
  s.addText("Why premium guests leave — and what we can do about it", {
    x: 0.5, y: 4.1, w: 12.3, h: 0.6,
    fontFace: FONT_TITLE, italic: true, fontSize: 22, color: GOLD, margin: 0,
  });
  s.addText("Team-Union · MMAI 869 · Final Project", {
    x: 0.5, y: 6.5, w: 12.3, h: 0.5,
    fontFace: FONT_BODY, fontSize: 12, color: WHITE, margin: 0,
  });
}

// ============================
// Slide 2: THE PROBLEM
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "The problem", "Half of Steve's premium guests don't come back.");

  // Big stat callout
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.9, w: 5.8, h: 4.7,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("50.4%", {
    x: 0.5, y: 2.4, w: 5.8, h: 1.8,
    fontFace: FONT_TITLE, fontSize: 110, bold: true, color: GOLD,
    align: "center", margin: 0,
  });
  s.addText("of guests churn", {
    x: 0.5, y: 4.2, w: 5.8, h: 0.6,
    fontFace: FONT_TITLE, italic: true, fontSize: 22, color: WHITE,
    align: "center", margin: 0,
  });
  s.addText([
    { text: "6,954 ", options: { bold: true, color: GOLD } },
    { text: "training guests · ", options: { color: WHITE } },
    { text: "1,739 ", options: { bold: true, color: GOLD } },
    { text: "test guests", options: { color: WHITE } },
  ], {
    x: 0.5, y: 5.0, w: 5.8, h: 0.5,
    fontFace: FONT_BODY, fontSize: 16, align: "center", margin: 0,
  });
  s.addText("Class balance: 49.6% retained · 50.4% churned", {
    x: 0.5, y: 5.6, w: 5.8, h: 0.6,
    fontFace: FONT_BODY, italic: true, fontSize: 13, color: CREAM, align: "center", margin: 0,
  });

  // Right column: bullets framing the question
  s.addText("THE BUSINESS QUESTION", {
    x: 6.8, y: 1.9, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText("Which guests will leave — and why?", {
    x: 6.8, y: 2.3, w: 6.0, h: 1.0,
    fontFace: FONT_TITLE, fontSize: 26, bold: true, color: NAVY, margin: 0,
  });
  s.addText([
    { text: "Goal:", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Build a churn classifier · target retention campaigns at the at-risk cohort.", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Metric:", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Macro F1 · evaluated on held-out Kaggle test set.", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Surprise:", options: { bold: true, color: CORAL, breakLine: true } },
    { text: "Brief warned of imbalance — data is balanced. No resampling needed.", options: { color: SLATE } },
  ], {
    x: 6.8, y: 3.4, w: 6.0, h: 3.4,
    fontFace: FONT_BODY, fontSize: 16, paraSpaceAfter: 6, margin: 0,
  });

  slideFooter(s, 2, TOTAL);
}

// ============================
// Slide 3: DATA TOUR
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Data tour", "21 features, 13 with missing values, one near-unique field.");

  // Left: feature groups card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.9, w: 6.0, h: 4.9,
    fill: { color: LIGHT_BG }, line: { color: NAVY, width: 0 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.9, w: 0.08, h: 4.9,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });
  s.addText("WHAT WE GET", {
    x: 0.85, y: 2.05, w: 5.6, h: 0.35,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: NAVY, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "Booking", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "BookingDate · PromoCode · Region · Channel", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Stay & Demographics", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "AllInclusive · Room (Wing/Floor/View) · Package · Age · VIP", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "On-site Spending  ($)", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "RoomService · Dining · Retail · Spa · Entertainment", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Loyalty Signals", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "LoyaltyPoints · SurveyScore · DaysSinceEmail · Referral", options: { color: SLATE } },
  ], {
    x: 0.85, y: 2.45, w: 5.6, h: 4.3,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 4, margin: 0,
  });

  // Right: missing values plot
  s.addImage({
    path: path.join(FIG, "07_missing_pattern.png"),
    x: 6.9, y: 1.95, w: 6.0, h: 4.0,
    sizing: { type: "contain", w: 6.0, h: 4.0 },
  });
  s.addText("Missingness as a feature.", {
    x: 6.9, y: 6.0, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, bold: true, color: NAVY, margin: 0,
  });
  s.addText("PromoCode 47% null = no promo (kept as category). For the other 12 columns we add explicit missingness flags.", {
    x: 6.9, y: 6.4, w: 6.0, h: 0.6,
    fontFace: FONT_BODY, italic: true, fontSize: 12, color: SLATE, margin: 0,
  });

  slideFooter(s, 3, TOTAL);
}

// ============================
// Slide 4: EUREKA #1 — ALLINCLUSIVE PARADOX
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Eureka #1", "Premium guests churn 2.5× more often.");

  s.addImage({
    path: path.join(FIG, "02_allinclusive_paradox.png"),
    x: 0.5, y: 1.85, w: 7.4, h: 4.8,
    sizing: { type: "contain", w: 7.4, h: 4.8 },
  });

  // Right: insight callout
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.4, y: 1.9, w: 4.5, h: 4.8,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("THE PARADOX", {
    x: 8.6, y: 2.05, w: 4.1, h: 0.35,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText("82% vs 33%", {
    x: 8.6, y: 2.5, w: 4.1, h: 1.0,
    fontFace: FONT_TITLE, fontSize: 36, bold: true, color: WHITE, margin: 0,
  });
  s.addText("All-Inclusive guests churn at 81.9% — Non-AI at 32.8%.", {
    x: 8.6, y: 3.6, w: 4.1, h: 1.0,
    fontFace: FONT_BODY, fontSize: 14, color: CREAM, margin: 0,
  });
  s.addText("HYPOTHESIS", {
    x: 8.6, y: 4.7, w: 4.1, h: 0.35,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText("All-Inclusive is sold as a one-shot experience. Without micro-purchases (dining, activities), no everyday loyalty habits form.", {
    x: 8.6, y: 5.05, w: 4.1, h: 1.6,
    fontFace: FONT_BODY, italic: true, fontSize: 12, color: WHITE, margin: 0,
  });

  slideFooter(s, 4, TOTAL);
}

// ============================
// Slide 5: EUREKA #2 — AI × REGION HEATMAP
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Eureka #2", "All-Inclusive in Europe is essentially a churn certainty.");

  s.addImage({
    path: path.join(FIG, "03_ai_x_region_heatmap.png"),
    x: 0.5, y: 1.85, w: 7.5, h: 4.8,
    sizing: { type: "contain", w: 7.5, h: 4.8 },
  });

  // Stat callouts
  const callout = (x, y, big, label, color) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.5, h: 1.4, fill: { color }, line: { color, width: 0 },
    });
    s.addText(big, {
      x: x + 0.2, y: y + 0.1, w: 4.1, h: 0.7,
      fontFace: FONT_TITLE, fontSize: 36, bold: true, color: WHITE, margin: 0,
    });
    s.addText(label, {
      x: x + 0.2, y: y + 0.85, w: 4.1, h: 0.5,
      fontFace: FONT_BODY, fontSize: 12, color: CREAM, margin: 0,
    });
  };
  callout(8.4, 1.9, "98.6%", "All-Inclusive + Europe (n=722)", CORAL);
  callout(8.4, 3.5, "91.5%", "All-Inclusive + AsiaPacific (n=528)", "B25E36");
  callout(8.4, 5.1, "28-41%", "Non-All-Inclusive · all regions", NAVY);

  s.addText("→ The interaction is far more predictive than either feature alone.", {
    x: 0.5, y: 6.65, w: 12.3, h: 0.3,
    fontFace: FONT_BODY, italic: true, fontSize: 13, color: SLATE, align: "left", margin: 0,
  });

  slideFooter(s, 5, TOTAL);
}

// ============================
// Slide 6: OTHER SIGNALS + NULL FINDINGS
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "What works · what doesn't", "Promotions cut churn in half. Surveys tell us nothing.");

  // Left: Promo plot
  s.addImage({
    path: path.join(FIG, "04_promo_impact.png"),
    x: 0.4, y: 1.95, w: 6.4, h: 4.4,
    sizing: { type: "contain", w: 6.4, h: 4.4 },
  });

  // Right: Survey plot
  s.addImage({
    path: path.join(FIG, "06_survey_useless.png"),
    x: 7.0, y: 1.95, w: 5.9, h: 4.4,
    sizing: { type: "contain", w: 5.9, h: 4.4 },
  });

  s.addText("Promotions retain customers — promos halve churn (67% → 36%).", {
    x: 0.4, y: 6.45, w: 6.4, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: NAVY, align: "center", margin: 0,
  });
  s.addText("SurveyScore is essentially useless — every score sits at ~50%.", {
    x: 7.0, y: 6.45, w: 5.9, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: CORAL, align: "center", margin: 0,
  });

  slideFooter(s, 6, TOTAL);
}

// ============================
// Slide 7: FEATURE ENGINEERING
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Feature engineering", "30 new features. 5 of them ended up in the top 10.");

  // Left: what we tried
  s.addText("WHAT WE TRIED", {
    x: 0.5, y: 1.9, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });

  const tried = [
    { what: "Room split", detail: "Wing / Floor / View ← 5298 unique → 8/numeric/2", helped: true },
    { what: "Date features", detail: "Year, Month, DayOfWeek, Quarter, IsWeekend", helped: true },
    { what: "Spend features", detail: "TotalSpend, log-transforms, ratios, categories-used", helped: true },
    { what: "Missingness flags", detail: "12 explicit binary cols ← captures null patterns", helped: true },
    { what: "Domain interactions", detail: "AI×Europe, AI×Adventure, HasPromo", helped: false },
    { what: "Native cat handling", detail: "CatBoost / LightGBM without OHE", helped: false },
  ];
  let yPos = 2.35;
  tried.forEach((row) => {
    s.addShape(pres.shapes.OVAL, {
      x: 0.55, y: yPos + 0.08, w: 0.22, h: 0.22,
      fill: { color: row.helped ? "2C7D4F" : NAVY },
      line: { color: row.helped ? "2C7D4F" : NAVY, width: 0 },
    });
    s.addText(row.helped ? "✓" : "—", {
      x: 0.55, y: yPos + 0.05, w: 0.22, h: 0.28,
      fontFace: FONT_BODY, fontSize: 10, bold: true, color: WHITE, align: "center", margin: 0,
    });
    s.addText(row.what, {
      x: 0.95, y: yPos, w: 1.7, h: 0.36,
      fontFace: FONT_BODY, fontSize: 14, bold: true, color: NAVY, margin: 0,
    });
    s.addText(row.detail, {
      x: 2.7, y: yPos, w: 3.9, h: 0.36,
      fontFace: FONT_BODY, fontSize: 12, color: SLATE, margin: 0,
    });
    yPos += 0.55;
  });

  // Right: importance plot
  s.addImage({
    path: path.join(FIG, "10_feature_importance.png"),
    x: 6.9, y: 1.85, w: 6.0, h: 4.7,
    sizing: { type: "contain", w: 6.0, h: 4.7 },
  });
  s.addText("Half of the model's top 10 features were engineered.", {
    x: 6.9, y: 6.55, w: 6.0, h: 0.35,
    fontFace: FONT_BODY, italic: true, fontSize: 12, color: NAVY, align: "center", margin: 0,
  });

  slideFooter(s, 7, TOTAL);
}

// ============================
// Slide 8: MODEL JOURNEY
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Model journey", "5 algorithms, 2 paradigms, one clear winner.");

  s.addImage({
    path: path.join(FIG, "08_model_leaderboard.png"),
    x: 0.5, y: 1.85, w: 7.4, h: 4.8,
    sizing: { type: "contain", w: 7.4, h: 4.8 },
  });

  // Right: CV vs LB note + rubric checks
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.3, y: 1.9, w: 4.6, h: 4.85,
    fill: { color: LIGHT_BG }, line: { color: LIGHT_BG, width: 0 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.3, y: 1.9, w: 0.08, h: 4.85,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 },
  });

  s.addText("RUBRIC CHECKS", {
    x: 8.55, y: 2.05, w: 4.2, h: 0.35,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: NAVY, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "✓ Non-tree model: ", options: { bold: true, color: NAVY } },
    { text: "Logistic Regression (0.8199)", options: { color: SLATE, breakLine: true } },
    { text: "✓ Tree-based:  ", options: { bold: true, color: NAVY } },
    { text: "Random Forest (0.8225)", options: { color: SLATE, breakLine: true } },
    { text: "✓ Boosting:  ", options: { bold: true, color: NAVY } },
    { text: "XGBoost · LightGBM · CatBoost", options: { color: SLATE, breakLine: true } },
    { text: "✓ Ensemble:  ", options: { bold: true, color: NAVY } },
    { text: "Weighted soft-vote of top 3", options: { color: SLATE } },
  ], {
    x: 8.55, y: 2.45, w: 4.2, h: 2.4,
    fontFace: FONT_BODY, fontSize: 13, paraSpaceAfter: 6, margin: 0,
  });

  s.addText("CV ↔ LB", {
    x: 8.55, y: 4.95, w: 4.2, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText("All scores are 5-fold stratified CV F1-macro. We expect LB ≈ CV ± 0.005 given OOF stability (std 0.005–0.008).", {
    x: 8.55, y: 5.3, w: 4.2, h: 1.4,
    fontFace: FONT_BODY, italic: true, fontSize: 12, color: SLATE, margin: 0,
  });

  slideFooter(s, 8, TOTAL);
}

// ============================
// Slide 9: HYPERPARAMETER TUNING
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Hyperparameter tuning", "Diminishing returns hit fast on a 7k-row dataset.");

  // Left: what we did
  s.addText("THE SEARCH", {
    x: 0.5, y: 1.95, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "12 ", options: { bold: true, color: NAVY } },
    { text: "CatBoost configs explored:", options: { color: SLATE, breakLine: true } },
    { text: "    depth ∈ {4, 5, 6, 7, 8}", options: { color: SLATE, breakLine: true } },
    { text: "    learning_rate ∈ {0.03, 0.05, 0.07, 0.10}", options: { color: SLATE, breakLine: true } },
    { text: "    l2_leaf_reg ∈ {3, 5, 7}", options: { color: SLATE, breakLine: true } },
    { text: "    iterations ∈ {300, 500, 700, 1000}", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Plus ", options: { color: SLATE } },
    { text: "Optuna ", options: { bold: true, color: NAVY } },
    { text: "infrastructure ready (in src/tune_catboost.py)", options: { color: SLATE } },
  ], {
    x: 0.5, y: 2.4, w: 6.0, h: 3.2,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 4, margin: 0,
  });

  // Right: result card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 1.95, w: 6.0, h: 4.7,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("THE RESULT", {
    x: 7.1, y: 2.1, w: 5.6, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText("Defaults already win.", {
    x: 7.1, y: 2.55, w: 5.6, h: 0.7,
    fontFace: FONT_TITLE, fontSize: 30, bold: true, color: WHITE, margin: 0,
  });
  s.addText([
    { text: "Best tuned config: ", options: { color: CREAM, breakLine: true } },
    { text: "CV F1 = 0.8497  (vs baseline 0.8513)", options: { color: WHITE, bold: true, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Threshold tuning: ", options: { color: CREAM, breakLine: true } },
    { text: "+0.07 pp · balanced data, 0.5 already optimal", options: { color: WHITE, bold: true, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Why?  Differences (±0.005–0.008) are within one σ — we're at the noise floor for a 7k-row dataset.", options: { italic: true, color: CREAM } },
  ], {
    x: 7.1, y: 3.4, w: 5.6, h: 3.1,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 4, margin: 0,
  });

  slideFooter(s, 9, TOTAL);
}

// ============================
// Slide 10: BEST MODEL DETAILS
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Best model", "0.5 × CatBoost + 0.3 × LightGBM + 0.2 × XGBoost.");

  // Top stat
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.85, w: 4.0, h: 1.55,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("0.8523", {
    x: 0.5, y: 1.9, w: 4.0, h: 0.95,
    fontFace: FONT_TITLE, fontSize: 50, bold: true, color: GOLD, align: "center", margin: 0,
  });
  s.addText("OOF F1-macro · weighted ensemble", {
    x: 0.5, y: 2.85, w: 4.0, h: 0.45,
    fontFace: FONT_BODY, fontSize: 12, color: WHITE, align: "center", margin: 0,
  });

  // Lift-vs-baseline mini-callouts
  const liftBox = (x, y, big, label) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 1.85, h: 1.55,
      fill: { color: LIGHT_BG }, line: { color: LIGHT_BG, width: 0 },
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.06, h: 1.55,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 },
    });
    s.addText(big, {
      x: x + 0.15, y: y + 0.15, w: 1.7, h: 0.7,
      fontFace: FONT_TITLE, fontSize: 22, bold: true, color: NAVY, margin: 0,
    });
    s.addText(label, {
      x: x + 0.15, y: y + 0.85, w: 1.7, h: 0.65,
      fontFace: FONT_BODY, fontSize: 11, color: SLATE, margin: 0,
    });
  };
  liftBox(4.7, 1.85, "+0.19 pp", "vs CatBoost\nsolo");
  liftBox(6.65, 1.85, "+3.2 pp", "vs Logistic\nRegression");

  // Confusion matrix figure
  s.addImage({
    path: path.join(FIG, "09_confusion_matrix.png"),
    x: 0.5, y: 3.6, w: 5.5, h: 3.2,
    sizing: { type: "contain", w: 5.5, h: 3.2 },
  });

  // Right side: classification report card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.6, y: 1.85, w: 4.3, h: 4.95,
    fill: { color: NAVY }, line: { color: NAVY, width: 0 },
  });
  s.addText("OOF METRICS", {
    x: 8.8, y: 2.0, w: 4.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "Retained class", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "Precision  ", options: { color: CREAM } }, { text: "0.84", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "Recall      ", options: { color: CREAM } }, { text: "0.86", options: { bold: true, color: WHITE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Churned class", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "Precision  ", options: { color: CREAM } }, { text: "0.86", options: { bold: true, color: WHITE, breakLine: true } },
    { text: "Recall      ", options: { color: CREAM } }, { text: "0.84", options: { bold: true, color: WHITE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Macro F1   ", options: { color: CREAM } }, { text: "0.85", options: { bold: true, color: GOLD, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Symmetric. No class neglected — balanced data behaves predictably.", options: { italic: true, color: CREAM } },
  ], {
    x: 8.8, y: 2.45, w: 4.0, h: 4.3,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 3, margin: 0,
  });

  slideFooter(s, 10, TOTAL);
}

// ============================
// Slide 11: 3 RIGHT + 3 WRONG
// ============================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  slideHeader(s, "Where the model gets it right · and wrong", "Confidently right on the cohort. Wrong on the noise.");

  // Two columns, two cards
  // CORRECT card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.85, w: 6.1, h: 4.95,
    fill: { color: LIGHT_BG }, line: { color: LIGHT_BG, width: 0 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.85, w: 6.1, h: 0.4,
    fill: { color: "2C7D4F" }, line: { color: "2C7D4F", width: 0 },
  });
  s.addText("3 CORRECT — high confidence", {
    x: 0.65, y: 1.88, w: 5.8, h: 0.34,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: WHITE, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "Profile · all 3 examples:  ", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "AllInclusive · Europe · Adventure · No promo · Dining $0", options: { color: SLATE, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Predicted churn probability:", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "  Guest 166287 → ", options: { color: SLATE } }, { text: "99.98%", options: { bold: true, color: "2C7D4F", breakLine: true } },
    { text: "  Guest 552514 → ", options: { color: SLATE } }, { text: "99.98%", options: { bold: true, color: "2C7D4F", breakLine: true } },
    { text: "  Guest 931435 → ", options: { color: SLATE } }, { text: "99.97%", options: { bold: true, color: "2C7D4F", breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Insight:", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Model has learned the deadly cohort exactly. The All-Inclusive Europe Adventure segment really is a churn machine.", options: { italic: true, color: SLATE } },
  ], {
    x: 0.7, y: 2.45, w: 5.7, h: 4.2,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 4, margin: 0,
  });

  // WRONG card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.8, y: 1.85, w: 6.1, h: 4.95,
    fill: { color: LIGHT_BG }, line: { color: LIGHT_BG, width: 0 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.8, y: 1.85, w: 6.1, h: 0.4,
    fill: { color: CORAL }, line: { color: CORAL, width: 0 },
  });
  s.addText("3 WRONG — confidently wrong", {
    x: 6.95, y: 1.88, w: 5.8, h: 0.34,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: WHITE, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "Guest 350637", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Looks like the deadly cohort (AI · EU · Adventure)", options: { color: SLATE, breakLine: true } },
    { text: "Pred 99.2% churn — actually retained.", options: { italic: true, color: CORAL, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Guest 303315", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Looks like a safe cohort (Americas · Promo · NotAI)", options: { color: SLATE, breakLine: true } },
    { text: "Pred 0.7% churn — actually churned.", options: { italic: true, color: CORAL, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Guest 748080", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Looks like a safe cohort (AsiaPacific · PromoB · NotAI)", options: { color: SLATE, breakLine: true } },
    { text: "Pred 1.0% churn — actually churned.", options: { italic: true, color: CORAL, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Insight:", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Real-world noise. Need life-event data to predict these.", options: { italic: true, color: SLATE } },
  ], {
    x: 7.0, y: 2.4, w: 5.7, h: 4.3,
    fontFace: FONT_BODY, fontSize: 13, paraSpaceAfter: 1, margin: 0,
  });

  slideFooter(s, 11, TOTAL);
}

// ============================
// Slide 12: NEXT STEPS + LESSONS LEARNED
// ============================
{
  const s = pres.addSlide();
  s.background = { color: NAVY_DARK };
  slideHeader(s, "If we had more time", "Next steps & lessons learned.");
  // Override header colors for dark slide
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 13.3, h: 1.5, fill: { color: NAVY_DARK }, line: { color: NAVY_DARK, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 13.3, h: 0.18, fill: { color: GOLD }, line: { color: GOLD, width: 0 } });
  s.addText("CLOSING", {
    x: 0.5, y: 0.32, w: 12, h: 0.32,
    fontFace: FONT_BODY, fontSize: 11, bold: true, color: GOLD, charSpacing: 6, margin: 0,
  });
  s.addText("Where this team would go next.", {
    x: 0.5, y: 0.62, w: 12.3, h: 0.85,
    fontFace: FONT_TITLE, fontSize: 32, bold: true, color: WHITE, margin: 0,
  });

  // Two columns
  // Next steps card
  s.addText("NEXT STEPS  →", {
    x: 0.5, y: 1.85, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "1.  Stacking with a meta-learner — typically +0.2–0.5 pp over blending.", options: { color: WHITE, breakLine: true } },
    { text: "2.  Optuna, 100+ trials per model — we ran ~12 manual configs.", options: { color: WHITE, breakLine: true } },
    { text: "3.  Pseudo-labeling confident test predictions to grow the train set.", options: { color: WHITE, breakLine: true } },
    { text: "4.  External data: macroeconomic conditions in Europe during booking month — the 98.6% Europe number begs for an explanation.", options: { color: WHITE, breakLine: true } },
    { text: "5.  Cluster analysis to formalize guest personas (the brief's optional ask).", options: { color: WHITE } },
  ], {
    x: 0.5, y: 2.3, w: 6.0, h: 4.5,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 7, margin: 0,
  });

  // Lessons learned card
  s.addText("LESSONS LEARNED  ✦", {
    x: 6.9, y: 1.85, w: 6.0, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, bold: true, color: GOLD, charSpacing: 4, margin: 0,
  });
  s.addText([
    { text: "1.  Counterintuitive insights win presentations. ", options: { bold: true, color: WHITE } },
    { text: "The All-Inclusive paradox is what executives remember.", options: { color: CREAM, breakLine: true } },
    { text: "2.  FE drove interpretation more than accuracy. ", options: { bold: true, color: WHITE } },
    { text: "Trees found the same splits, but engineered features made our story clear.", options: { color: CREAM, breakLine: true } },
    { text: "3.  Don't tune past the noise floor. ", options: { bold: true, color: WHITE } },
    { text: "Within ±1σ, you're chasing folds, not lift.", options: { color: CREAM, breakLine: true } },
    { text: "4.  Read the metric carefully. ", options: { bold: true, color: WHITE } },
    { text: "F1-macro on balanced data behaves nothing like F1 on imbalanced data.", options: { color: CREAM, breakLine: true } },
    { text: "5.  Simple ensembles win. ", options: { bold: true, color: WHITE } },
    { text: "A weighted soft-vote of 3 boosters gave us our final +0.19 pp.", options: { color: CREAM } },
  ], {
    x: 6.9, y: 2.3, w: 6.0, h: 4.5,
    fontFace: FONT_BODY, fontSize: 14, paraSpaceAfter: 5, margin: 0,
  });

  // Closing tagline
  s.addText("Thank you · Q&A", {
    x: 0.5, y: 6.85, w: 12.3, h: 0.4,
    fontFace: FONT_TITLE, italic: true, fontSize: 16, color: GOLD, align: "right", margin: 0,
  });
}

pres.writeFile({ fileName: path.join(__dirname, "Team-Union_MMAI869_Final.pptx") })
  .then((f) => console.log("Wrote", f));
