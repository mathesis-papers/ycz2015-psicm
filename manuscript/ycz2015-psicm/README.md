# An alternative proof extending Kang's refutation of Yang–Chu–Zhang (2015), Conjecture 1(ii), p. 15

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang (National
University of Singapore; ChronoAI Pte Ltd, Singapore). November 7, 2026.
CC BY 4.0.

For the source's digamma remainder family, Theorem 1 proves
`G_a''(1/64) > (21943673/1280)(a-a_c) >= 0` for every
`a >= a_c = 331467377585/629168992256`. In particular,
`G_a''(1/64) > 26102771679/22937600000 > 1` for `a >= 5269/10000`.
Consequently `-G_a` is not completely monotone on this parameter half-line.
The exact admissible set below `a_c` is not characterized.

The prior refutation is Kang (2026), DOI 10.5281/zenodo.23718266,
Theorem 1; his supporting `PROOF.md` already gives a rational derivative
witness at `a=527/1000`, `x=1/50`. The posing source is Yang–Chu–Zhang,
*Journal of Inequalities and Applications* 2015:157, DOI
10.1186/s13660-015-0674-8, Conjecture 1(ii), p. 15; the earlier version is
Yang, arXiv:1409.6411v1, p. 14.

## Coefficient coverage

For Problem 1, p. 16, Corollary 2 proves the necessary condition `a_0>0`
in every degree. Corollary 3 characterizes all `n=1` solutions as
`t G_(11165/8284)`, `t>0`, with the required positive `x^-6` coefficient
`627404761t/10287535104`. Its complete-monotonicity sufficiency is the
source's Theorem 4; the coefficient classification follows from the written
asymptotic cancellation argument. The optional `n=0` base case uses its
Theorem 2. The general `n>=2` classification and Conjecture 1(i) are not
covered. The finite nonzero scaled limit in Problem 1 is essential.

## Build

Compile the single main source with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use a standard LaTeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; no external figures or inputs
are required. Packages: fontenc, lmodern, amsmath, amssymb, amsthm, booktabs,
array, geometry and hyperref.

## Mathematical evidence

```sh
python3 verify.py
```

Python 3 and its standard library suffice. The command writes
`verify-output.json`. It checks the affine lower bound, signs, margins,
translated digamma asymptotic coefficients and cancellation identities using
exact fractions. Infinite series, endpoint limits and monotonicity arguments
have written proofs or the precise cited theorems in the note.

The PDF links `Refutation.lean` at revision
`074df09ddbbef1843ddb383577bfaa827f753e36`. The declaration `result` negates
the source's universal equivalence. Its private `uniform_second_deriv`
lemma proves `G_a''(1/64)>1/2` for `a>=155/294-1/10000`. That declaration
does not include the stronger `a_c` range or the coefficient corollaries;
these have the written proofs in the note.

## Contents

- `note.tex`: statement, proofs, coverage table and bibliography.
- `metadata.json`: title, creators, license and source evidence link.
- `verify.py`, `verify-output.json`: finite exact calculations and values.
- `README.md`: mathematical scope and build instructions.
- `SHA256SUMS.txt`: checksums of these source files in the ZIP distribution.
