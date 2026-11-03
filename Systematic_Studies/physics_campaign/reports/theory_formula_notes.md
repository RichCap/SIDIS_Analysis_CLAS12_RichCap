# Published formulas for unpolarized π+ cosine moments

Checked against the papers named below. No number in this note was taken from this thesis, and no curve was digitized from a figure. A partial term is not the full model of the paper that contains it.

Beam energy: none of these papers publishes a π+ proton curve or table at 10.6 GeV. A CLAS12 comparison has to be recomputed at the thesis bins from the formulas and parameters quoted here.

## 1. Cahn effect

Sources:

- R. N. Cahn, Phys. Lett. B78 (1978) 269–273, DOI 10.1016/0370-2693(78)90020-5. Also R. N. Cahn, Phys. Rev. D40 (1989) 3107.
- Gaussian hadron-level form used in SIDIS phenomenology: M. Anselmino et al., Phys. Rev. D71 (2005) 074006, hep-ph/0501196, eqs. (38), (39), (47). The same O(k⊥/Q) bracket is in Anselmino et al., hep-ph/0507157, eq. (2), and in the review D’Alesio and Murgia, Prog. Part. Nucl. Phys. 61 (2008) 394, arXiv:0712.4328.

Cahn 1978 is a naive parton-model letter for ℓp → ℓ′hX. The struck parton, not the detected hadron, carries the intrinsic transverse momentum. The letter gives ŝ and −û with a term linear in (P⊥/Q) cos φ, and the electroproduction cross section proportional to ŝ² + û², eqs. (11) and (12) of that letter. Fragmentation is estimated only as a reduction of the parton asymmetry. The letter does not give a Gaussian width, a hadron PT, or a z-dependent closed form.

The standard Gaussian form keeps O(k⊥/Q) and integrates flavor-blind Gaussians. Anselmino et al., Phys. Rev. D71 (2005) 074006, eq. (38):

d⁵σ / (dxB dQ² dzh d²PT) ∝ Σq eq² fq(xB) Dq^h(zh) × [ 1 + (1−y)² − 4 (2−y)√(1−y) ⟨k⊥²⟩ zh PT / (⟨PT²⟩ Q) cos φh ] × exp(−PT²/⟨PT²⟩) / (π ⟨PT²⟩),

with ⟨PT²⟩ = ⟨p⊥²⟩ + zh² ⟨k⊥²⟩. Their fit to EMC and E665 charged-hadron data, not identified π+ at CLAS12, is ⟨k⊥²⟩ = 0.25 (GeV/c)² and ⟨p⊥²⟩ = 0.20 (GeV/c)², eq. (47). PDFs and FFs cancel in the cos φh / flat ratio only if those widths are flavor-independent.

The equivalent structure-function ratio, with the same Gaussians, is in Barone, Boglione, Gonzalez Hernandez, and Melis, Phys. Rev. D91 (2015) 074019, arXiv:1502.04214, eqs. (25) and (26):

F_UU^{cos φ}|_Cahn / F_UU = −2 (PT/Q) (zh ⟨k⊥²⟩ / ⟨PT²⟩).

Their asymmetry, eq. (38), multiplies that ratio by 2(2−y)√(1−y) / [1+(1−y)²]. That product reproduces the coefficient in Anselmino eq. (38). There is also an O(1/Q²) Cahn piece of cos 2φ, their eq. (29),

F_UU^{cos 2φ}|_Cahn / F_UU = 2 (PT²/Q²) (zh² ⟨k⊥²⟩² / ⟨PT²⟩²),

which is not the cos φh modulation.

An absolute moment, meaning that ratio times the lepton prefactor, does not need a new fit to this thesis’s A0: A0 cancels. It is not an absolute SIDIS yield. The numerical size is the published width choice. Barone et al. 2015, Sec. III, state that the multiplicity extraction ⟨k⊥²⟩ ≈ 0.6 GeV² makes the Cahn piece of ⟨cos φ⟩ of order 50%, larger than the measured asymmetry, which does not exceed 10%. Their own fits, with dynamical twist-3 omitted and with the cos 2φ Cahn term set to zero, return ⟨k⊥²⟩ = C = 0.031 ± 0.006 GeV² (COMPASS, Table I) and 0.037 ± 0.004 GeV² (HERMES, Table II). Those are different published curves, still not a fit to this thesis.

- EVALUABLE: the flavor-blind Gaussian cos φh moment −2 (PT/Q) zh ⟨k⊥²⟩/⟨PT²⟩, times the lepton prefactor above, using a published width pair such as 0.25 and 0.20 (GeV/c)²; A0 is not an extra input

## 2. Boer–Mulders × Collins contribution to cos 2φh

Two papers. In both, Boer–Mulders × Collins is one term. It is not the whole calculated asymmetry.

### Barone, Prokudin, and Ma, 2008

V. Barone, A. Prokudin, and B.-Q. Ma, Phys. Rev. D78 (2008) 045022, arXiv:0804.3024 (Barone:2008tn).

Their ⟨cos 2φ⟩, eqs. (14)–(18), has three pieces: kinematic Cahn, eq. (4); leading-twist Boer–Mulders × Collins, eq. (5); and O(αs) gluon radiation, eqs. (10)–(13). Equation (5) is

d⁵σ_BM / (dx dy dz d²PT)|_{cos 2φ} = (4πα_em² s / Q⁴) Σa ea² x(1−y) × ∫ d²kT d²pT δ²(PT − z kT − pT) × [2 (h·kT)(h·pT) − kT·pT] / (z M Mh) × h1^{⊥a}(x,kT²) H1^{⊥a}(z,pT²) cos 2φ.

The plotted asymmetry is the sum. Figure 4 defines the lines: dot-dashed is O(αs), dotted is Boer–Mulders, dashed is Cahn, solid is the sum. Figures 8 and 9 are proton π+ and π− at their JLab 6 GeV and 12 GeV cuts, not at 10.6 GeV. The 12 GeV proton cuts, eq. (41), are Q² ≥ 1 GeV², W² ≥ 4 GeV², 0.02 ≤ PT ≤ 1.4 GeV, 0.05 ≤ x ≤ 0.7, 0.4 ≤ z ≤ 0.7, 0.2 ≤ y ≤ 0.85, 1 ≤ Eh ≤ 7 GeV. No table digitizes those curves.

Parameters of the Boer–Mulders × Collins piece, not of the sum:

- h1^{⊥u} ≃ 1.80 f1T^{⊥u}, h1^{⊥d} = −0.94 f1T^{⊥d}, eq. (24), from κu ≃ 1.67, κd ≃ −2.03, κT^u ≃ 3, κT^d ≃ 1.9.
- Sivers parameters copied into Table I: Au = −0.32 ± 0.11, Ad = 1.00 ± 0.12, au = 0.29 ± 0.35, ad = 1.16 ± 0.47, bu = 0.53 ± 3.58, bd = 3.77 ± 2.59, M0² = 0.32 ± 0.25 GeV². The shape is eqs. (25)–(27).
- ⟨kT²⟩ = 0.25 GeV², ⟨pT²⟩ = 0.20 GeV².
- Collins Table II, from their ref. [43]: A_fav^C = 0.41 ± 0.91, A_unf^C = −1.00 ± 0.96, γ = 1.04 ± 0.38, δ = 0.13 ± 0.25, ⟨pT²⟩ = 0.2 GeV², and the squared Collins mass parameter MC² = (0.71 ± 0.65) GeV². Shape: eqs. (31)–(34).
- Collinear inputs: GRV98 for f1 and Kretzer for D1.

At PT ≪ 1 GeV they drop O(αs), eq. (16), but the Cahn term remains in the numerator. The dotted curve is the Boer–Mulders × Collins piece; the solid curve is not.

### Barone et al., 2015

V. Barone, M. Boglione, J. O. Gonzalez Hernandez, and S. Melis, Phys. Rev. D91 (2015) 074019, arXiv:1502.04214. This is the calculation often cited as Phys. Rev. D91.

Up to O(1/Q) they fit

A^{cos φ} = A^{cos φ}|_Cahn + A^{cos φ}|_BM,    A^{cos 2φ} = A^{cos 2φ}|_BM.

The cos 2φ Cahn term, their eq. (14) and the Gaussian eq. (29), is set to zero in the fit (Table I and Table II captions). Their cos 2φ model is therefore the Boer–Mulders × Collins term only, eqs. (13) and (30), not a sum with Cahn or with O(αs). They say the Boer–Mulders function is marginal: Δfd is compatible with zero and Δfu is small, and the selected multidimensional cos 2φ points are compatible with zero. The paper does not publish a JLab or 10.6 GeV prediction.

Gaussian Boer–Mulders × Collins structure function, eq. (30):

F_UU^{cos 2φ}|_BM = −e PT² Σq eq² xB [Δfq↑/p(xB) ΔDh/q↑(zh)] / (MBM MC) × exp(−PT²/⟨PT²⟩_BM) / (π ⟨PT²⟩_BM³) × zh ⟨k⊥²⟩_BM² ⟨p⊥²⟩_C² / (⟨k⊥²⟩ ⟨p⊥²⟩),

with ⟨PT²⟩_BM = ⟨p⊥²⟩_C + zh² ⟨k⊥²⟩_BM. The asymmetry multiplies F^{cos 2φ}/F_UU by 2(1−y)/[1+(1−y)²], eq. (39).

Published fit numbers, 2σ, αq = βq = 0, CTEQ6L and DSS, Collins fixed to eq. (46): N_fav^C = 0.49, N_dis^C = −1.00, γ = 1.06, δ = 0.07, MC² = 1.50 GeV². Widths ⟨p⊥²⟩ = A + B zh² and ⟨k⊥²⟩ = C.

- COMPASS Table I: A = 0.200 ± 0.002, B = 0.571 ± 0.018, C = 0.031 ± 0.006, MBM² = 0.09 ± 0.45, Nu = −0.45 ± 0.26, Nd = −1.00 ± 1.95.
- HERMES Table II: A = 0.126 ± 0.004, B = 0.506 ± 0.045, C = 0.037 ± 0.004, MBM² = 0.10 ± 0.20, Nu = −0.49 ± 0.15, Nd = −1.00 ± 0.20.

- EVALUABLE: the 2008 Boer–Mulders × Collins integrand, eq. (5), with Tables I and II, ⟨kT²⟩ = 0.25 GeV², ⟨pT²⟩ = 0.20 GeV², GRV98, and Kretzer; separately, the 2015 Boer–Mulders-only cos 2φ Gaussian, eq. (30), with Table I or Table II and the fixed Collins numbers in eq. (46). Neither published plot is a 10.6 GeV curve, and neither Boer–Mulders term is that paper’s full asymmetry

## 3. Bastami et al. 2019

S. Bastami et al., JHEP 06 (2019) 007, arXiv:1807.10606. Semi-inclusive deep-inelastic scattering in the Wandzura–Wilczek-type approximation.

They publish formulas and HERMES/COMPASS comparisons, not a CLAS12 or 10.6 GeV curve. Numerical widths used for their estimates, Appendix A.1: ⟨k⊥²⟩_f1 = 0.25 GeV² and ⟨P⊥²⟩_D1 = 0.20 GeV². Collinear f1 is MSTW LO and D1 is DSS, taken at Q² = 2.4 GeV² unless they say otherwise.

cos 2φh, leading twist only. Equation (2.17b) is the convolution of h1⊥ with H1⊥. The Gaussian result they plot is eq. (5.9a),

F_UU^{cos 2φh}(x, z, PhT) = x Σq eq² h1^{⊥(1)q}(x) H1^{⊥(1)q}(z) b_AB (z PhT / λ)² G(PhT),

with λ = z² ⟨k⊥²⟩_h⊥ + ⟨P⊥²⟩_H⊥, b_AB = 4 MN mh, and G(PhT) = exp(−PhT²/λ) / (π λ). This is only the Boer–Mulders term. Section 5.5 says they neglect O(1/Q²), including the Cahn contamination, and that this Boer–Mulders-only curve does not describe the data: COMPASS has the opposite sign. Figure 8 is that term versus x for a proton target, HERMES π± and COMPASS h±, not a PT curve at 10.6 GeV.

Boer–Mulders and Collins numbers are in the paper. Table 4 prints N_BM^u = 2.1 ± 0.1, N_BM^d = −1.111 ± 0.001, Nu = 0.35, αu = 0.73, βu = 3.46, Nd = −0.9, αd = 1.08, βd = 3.46, MBM² = 0.34 GeV². The sentence before the table cites their ref. [161], Phys. Rev. D82 (2010) 114025; the table caption cites ref. [156], Phys. Rev. D81 (2010) 114026. The arithmetic above is what Bastami prints. Collins Table 3, from their ref. [151], Anselmino et al., Phys. Rev. D87 (2013) 094019: NuT = 0.46, NdT = −1.00, α = 1.11, β = 3.64, ⟨k⊥²⟩_h1 = 0.25 GeV², N_fav^C = 0.49, N_dis^C = −1.00, γ = 1.06, δ = 0.07, MC² = 1.50 GeV², with the asymmetric errors given in that table. The implementation is Appendix A.4 and A.5. Transversity uses GRV98LO and DSS, which is not the same collinear pair as the unpolarized MSTW choice.

cos φh. After the WW-type reduction, eq. (4.2a) still has two convolutions, xh H1⊥ and xf⊥ D1. Section 7.8 keeps the f⊥ piece and treats the T-odd h as they treat fT. The expression they compare with data is eq. (7.9a),

F_UU^{cos φh}(x, z, PhT) = (2 MN / Q) x Σq eq² [−x f_⊥^{(1)q}(x)] D1^q(z) b_B (z PhT / λ) G(PhT),

with b_B = 2 MN and λ = z² ⟨k⊥²⟩_f⊥ + ⟨P⊥²⟩_D1. They set ⟨k⊥²⟩_f⊥ = ⟨k⊥²⟩_f1 and, from eq. (3.3b), x f_⊥^{(1)q}(x) = ⟨k⊥²⟩_f1 / (2 MN²) f1^q(x). With that choice the Gaussians cancel in F^{cos φh}/F_UU, and they warn that the ratio exceeds 100% for PhT ≳ 1 GeV, so the formula is only for PhT ≪ Q. Figure 20 compares this WW cos φh result with COMPASS h± and HERMES π± versus x. It is not a 10.6 GeV prediction. They say it overestimates COMPASS at small x and does not reproduce the HERMES flavor dependence.

HERMES asymmetries in the paper are the ⟨y⟩-weighted ratios; COMPASS ratios are F / F_UU. A CLAS12 overlay has to use the same moment definition as the thesis. That is a convention, not a missing function.

- EVALUABLE: Bastami’s WW f⊥ cos φh ratio from eqs. (7.9a) and (3.3b) with ⟨k⊥²⟩ = 0.25 GeV², ⟨P⊥²⟩ = 0.20 GeV², MSTW, and DSS, and, separately, their Boer–Mulders-only cos 2φh expression (5.9a) with Tables 3 and 4; neither is the full unpolarized structure function, and neither is a published 10.6 GeV curve

## 4. Balitsky and Prokudin 2026

I. Balitsky and A. Prokudin, JHEP 05 (2026) 265, arXiv:2601.18882, DOI 10.1007/JHEP05(2026)265.

The cross section is eq. (2.6): σ0 [ F_UU,T + p1 F_UU,L + cos(φh) p3 F_UU^{cos φh} + cos(2φh) p1 F_UU^{cos 2φh} ], with p1 = (1−y) / (1 − y + y²/2) and p3 = (2−y)√(1−y) / (1 − y + y²/2), eq. (2.8), up to O(1/Q²).

Their kinematic power corrections, keeping f1 D1 and h1⊥ H1⊥ and dropping the rest, are eqs. (3.17) and (3.18). For cos φh, eq. (4.13),

F_UU^{cos φh} = C[ −2 (ĥ·k⊥)/Q f1 D1 ] + C[ −2 k⊥² (ĥ·p⊥) / (zh M mh Q) κ h1⊥ H1⊥ ].

The first term is the Cahn term. The Gaussian result they plot is eq. (4.14): an f1 D1 piece −x Σ ea² f1 D1 × 2 ⟨k⊥²⟩_f1 Ph⊥ zh exp(−Ph⊥²/λ) / [ Q π λ² ], with λ = zh² ⟨k⊥²⟩_f1 + ⟨p⊥²⟩_D1, plus a Boer–Mulders × Collins piece written there with λ3 = 8 M mh zh Ph⊥ (⟨p⊥²⟩_H⊥² + zh² ⟨k⊥²⟩_h⊥ (Ph⊥² − zh² ⟨k⊥²⟩_h⊥)). The f1 D1 piece alone matches the Cahn ratio in Sec. 1.

For cos 2φh, eq. (4.18) is the leading Boer–Mulders × Collins convolution plus two O(1/Q²) terms, one f1 D1 and one h1⊥ H1⊥. The leading Gaussian piece is eq. (4.20), with λ4 = 4 M mh Ph⊥² zh². Their NNLP cos 2φh piece is not recomputed from scratch in the plots: they set it by eq. (3.19), F_UU,T^{NNLP} = F_UU^{cos 2φh, NNLP} = −(qT/Q) F_UU^{cos φh}. They state that this NNLP cos 2φh result differs from Piloneta and Vladimirov. The leading Boer–Mulders term agrees with the standard convolution. Equation (3.19) is their relation, not the Bacchetta or Barone twist-4 Cahn formula.

Numerical inputs, Sec. 4: the same Gaussian model as Bastami et al., ⟨k⊥²⟩_f1 = 0.25 GeV², ⟨p⊥²⟩_D1 = 0.20 GeV², MSTW and DSS, initial scale Q² = 2.4 GeV². Boer–Mulders first moments from Barone, Melis, and Prokudin, Phys. Rev. D81 (2010) 114026, arXiv:0912.5194. Collins first moments from Anselmino et al., Phys. Rev. D87 (2013) 094019, arXiv:1303.3822. They state that both u and d Boer–Mulders first moments are negative in SIDIS, and that H1⊥ for u → π+ is positive while d → π+ is negative. κ = −1 converts the Drell–Yan Boer–Mulders function to the SIDIS one, stated before eq. (3.15). They do not repeat the Boer–Mulders fit table; those numbers have to be read from the cited papers, which Bastami Table 4 already transcribes with the citation mismatch noted in Sec. 3.

What they actually plot for the cosine moments is not CLAS12. Figure 10 is p3 A_UU^{cos φh} for π+ at x = 0.1, zh = 0.3, Q² = 3 GeV², called characteristic HERMES kinematics, and a comparison to HERMES π+ and π−. Figure 11 is COMPASS. Figures 12 and 13 are the same for cos 2φh. They say the NNLP piece changes cos 2φh drastically and that the COMPASS trend comes out opposite to the data. The Jefferson Lab numbers in this paper are for R_SIDIS = F_UU,L / F_UU,T, which they estimate at about 20% in the JLab range, Figs. 5 and 6, not for cos φh or cos 2φh. Denominator of their plotted asymmetries is F_UU,T + p1 F_UU,L, eqs. (4.15) and (4.21), so the longitudinal structure function is part of the published moment, not an optional extra.

- EVALUABLE: F_UU^{cos φh} from eq. (4.14) and F_UU^{cos 2φh} from eq. (4.20) plus the NNLP relation (3.19), at a chosen (x, zh, Ph⊥, Q, y), with ⟨k⊥²⟩_f1 = 0.25 GeV², ⟨p⊥²⟩_D1 = 0.20 GeV², MSTW, DSS, and the cited Boer–Mulders and Collins first moments; the published cosine figures are HERMES and COMPASS comparisons, not a 10.6 GeV prediction

## Grid search for the Boer–Mulders collinear inputs

Searched this machine for grids that can be evaluated at the analysis bins. No GRV98 proton grid and no Kretzer fragmentation-function grid were found, including under EvGen_sidis_fork, the installed LHAPDF directory (index only, no member files), and the Pythia 8 pdfdata directories. The 2008 Boer–Mulders × Collins integrand, which needs GRV98 for f1 and Kretzer for D1, is therefore not evaluated. No curve was substituted for that missing pair.

The pair that can be read is MSTW 2008 LO and DSS. The MSTW file is EvGen_sidis_fork/sidis/share/sidis/sf_set/prokudin/mstw2008lo.00.dat, evaluated with the MSTWPDF interpolator (argument Q = √Q²; the returned value is x f). The same file also exists in the Pythia 8 pdfdata directories. The fragmentation functions are the DSS LO π+ LHAPDF set dsspipLO at EvGen_sidis_fork/sidis/share/sidis/sf_set/stf/dsspipLO, read with LHAPDF 6.5.6 (xfxQ returns z D). Both grids cover the 452 bin centers: x is about 0.16 to 0.55 and z is about 0.18 to 0.64, with the collinear scale fixed at Q² = 2.4 GeV² as in Bastami et al.

That pair is the one used for Bastami et al. eq. (5.9a), with their Table 4 Boer–Mulders parameters and Table 3 Collins parameters. The comparison is in Comparisons_to_Theory_Models.tex. It is the Boer–Mulders–Collins term only. The Cahn table is unchanged. CTEQ6L is present as a Pythia table (cteq6l.tbl) but is not the PDF of this formula, and it was not used.
