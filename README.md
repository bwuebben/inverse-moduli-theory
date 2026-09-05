# Inverse Moduli Theory

**Realizability of Degeneration Data by Compactified Moduli Spaces**

Bernd Johannes Wuebben, 2026

[Read the paper (PDF, 106 pages)](paper/inverse-moduli-theory.pdf)

Donaldson, Seiberg–Witten, Floer, and Gromov–Witten theories extract
invariants or algebraic structures from compactified moduli spaces. This
paper studies the inverse problem: which prescribed gluing data and
algebraic identities admit geometric realizations, and when can those
realizations arise from Fredholm problems?

The principal result is an obstruction to extending prescribed compatible
stabilizing bundles across the pentagon associahedron. A reflection in one
endpoint identification produces a nonorientable boundary bundle and
prevents that datum from extending. This is an obstruction for the
specified datum: its direct sum with itself can extend.

The paper also treats chain and higher associativity identities as
oriented filling conditions in dimension one, higher extensions in
ordinary smooth bordism, realization categories over gluing data, and
descent over overlapping color sets. Geometric targets and hypotheses are
specified in the statements. The analytic realization criteria are
conditional; the paper presents a framework of realization and
obstruction problems, with open questions, rather than a universal
existence theorem.

## Contents

| Path | Contents |
| --- | --- |
| [paper/inverse-moduli-theory.pdf](paper/inverse-moduli-theory.pdf) | Compiled manuscript |
| [paper/main.tex](paper/main.tex) | Complete LaTeX source, including the figures |
| [paper/references.bib](paper/references.bib) | Bibliography |
| [src/check_finite_examples.py](src/check_finite_examples.py) | Self-contained finite calculations |
| [build.sh](build.sh) | Manuscript build command |
| [CITATION.cff](CITATION.cff) | Citation metadata |

## Build the paper

Install a LaTeX distribution with `latexmk`, pdfLaTeX, and BibTeX (for
example, a full TeX Live or MacTeX installation). From the repository root:

```bash
./build.sh
```

The result is `paper/inverse-moduli-theory.pdf`. The source uses standard
LaTeX packages, including TikZ, `newtx`, `libertine`, and `natbib`. No
external figures or data files are required. A direct build is also possible:

```bash
cd paper
latexmk -pdf main.tex
```

That direct command produces `main.pdf`.

## Reproduce the finite calculations

Use Python 3.10 or later. No third-party packages, network access, or data
downloads are needed:

```bash
python3 src/check_finite_examples.py
```

The script checks:

- Both planar corner identities over all 256 parity assignments for each
  of the 64 linear and eight displayed quadratic sign candidates. All
  linear candidates fail; `(u,v,w)=(1,1,1)` is the unique survivor in the
  displayed quadratic family.
- Determinant signs in the rank-one pentagon example and the finite
  overlap-type counts for two quartets.
- Grading and stable-map dimension formulas on the bounded integer ranges
  specified in the source.

These calculations supplement the manuscript's proofs. They do not check
the geometric, categorical, or analytic theorems, or classify sign formulas
outside the displayed families. A successful run prints
`Finite calculations: PASS` and exits with status zero.

## Citation and license

Please cite the paper as:

> Bernd Johannes Wuebben. *Inverse Moduli Theory: Realizability of
> Degeneration Data by Compactified Moduli Spaces*. 2026.

The calculations in `src/` and the build script are distributed under the
MIT License. The manuscript sources, bibliography, and PDF in `paper/` are
copyright Bernd Johannes Wuebben; all rights reserved. See [LICENSE](LICENSE).
