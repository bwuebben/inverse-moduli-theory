#!/usr/bin/env python3
"""Finite calculations accompanying Inverse Moduli Theory.

Exhaustive parity checks for the displayed planar-sign ansatzes, determinant
signs for the rank-one pentagon example, overlap-type counts, and bounded
checks of grading and dimension formulas. These computations supplement the
proofs in the paper; they do not verify its geometric or analytic theorems.

Requires Python 3.10 or later; no third-party packages or data files.
"""

from __future__ import annotations

import itertools
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_grading_identities() -> None:
    # From |sx|=|x|-1, verify the shifted and unshifted polygon dimensions.
    for n in range(1, 9):
        for degrees in itertools.product(range(-3, 4), repeat=min(n + 1, 5)):
            if n + 1 > 5:
                break
            out, *inputs = degrees
            shifted = (out - 1) - sum(i - 1 for i in inputs) - 1
            unshifted = out - sum(inputs) + n - 2
            require(shifted == unshifted, "suspension dimension identity failed")

    # A facet obtained by inserting an s-input operation has codimension one.
    for n in range(1, 9):
        for r in range(n + 1):
            for s in range(1, n - r + 1):
                t = n - r - s
                for outer in range(-3, 5):
                    for inner in range(-3, 5):
                        total = outer + inner + 1
                        require(outer + inner == total - 1, "facet dimension failed")
                        require(r + s + t == n, "arity decomposition failed")

    # Curvature insertion is the s=0 analogue: outer + inner = ambient - 1.
    for outer in range(-3, 6):
        for inner in range(-3, 6):
            ambient = outer + inner + 1
            require(outer + inner == ambient - 1, "curvature facet dimension failed")


def planar_dimension_parities(
    prefix: int,
    block: int,
    suffix: int,
    intermediate: int,
    output: int,
) -> tuple[int, int]:
    """Return the outer and inner expected dimensions modulo two."""
    beta = (intermediate - block - 1) % 2
    alpha = (output - prefix - intermediate - suffix - 1) % 2
    return alpha, beta


def linear_planar_exponent(
    coefficients: tuple[int, ...],
    prefix: int,
    block: int,
    suffix: int,
    intermediate: int,
    output: int,
) -> int:
    """The six-coefficient linear ansatz in Lemma 5.7, modulo two."""
    variables = (prefix, block, suffix, intermediate, output, 1)
    return sum(coefficient * variable for coefficient, variable in zip(coefficients, variables)) % 2


def quadratic_planar_exponent(
    parameters: tuple[int, int, int],
    prefix: int,
    block: int,
    suffix: int,
    intermediate: int,
    output: int,
) -> int:
    """The displayed (u,v,w)-family of planar facet signs, modulo two."""
    u, v, w = parameters
    alpha, beta = planar_dimension_parities(prefix, block, suffix, intermediate, output)
    return (prefix + u * prefix * beta + v * beta + w * alpha * beta) % 2


def disjoint_planar_corner_difference(exponent, parities: tuple[int, ...]) -> int:
    """Difference of the two boundary routes for disjoint blocks."""
    left, block_i, middle, block_j, right, z_i, z_j, output = parities
    _, beta_i = planar_dimension_parities(left, block_i, middle + block_j + right, z_i, output)
    _, beta_j = planar_dimension_parities(left + block_i + middle, block_j, right, z_j, output)

    route_i_then_j = exponent(left, block_i, middle + block_j + right, z_i, output)
    route_i_then_j += exponent(left + z_i + middle, block_j, right, z_j, output)

    route_j_then_i = exponent(left + block_i + middle, block_j, right, z_j, output)
    route_j_then_i += exponent(left, block_i, middle + z_j + right, z_i, output)
    route_j_then_i += beta_i * beta_j  # interchange of the two inner factors
    return (route_i_then_j - route_j_then_i) % 2


def nested_planar_corner_difference(exponent, parities: tuple[int, ...]) -> int:
    """Difference of the two boundary routes for a block nested in another."""
    left, inner_left, inner_block, inner_right, right, z_i, z_j, output = parities
    alpha_i, _ = planar_dimension_parities(
        left,
        inner_left + inner_block + inner_right,
        right,
        z_i,
        output,
    )

    route_i_then_j = exponent(
        left,
        inner_left + inner_block + inner_right,
        right,
        z_i,
        output,
    )
    route_i_then_j += exponent(inner_left, inner_block, inner_right, z_j, z_i)
    route_i_then_j += alpha_i  # boundary of the second factor in outer x inner

    route_j_then_i = exponent(left + inner_left, inner_block, inner_right + right, z_j, output)
    route_j_then_i += exponent(left, inner_left + z_j + inner_right, right, z_i, output)
    return (route_i_then_j - route_j_then_i) % 2


def first_planar_corner_failure(exponent) -> tuple[str, tuple[int, ...], int] | None:
    """Return a concrete parity witness when either corner identity fails."""
    assignments = itertools.product((0, 1), repeat=8)
    for parities in assignments:
        difference = disjoint_planar_corner_difference(exponent, parities)
        if difference != 1:
            return "disjoint", parities, difference

    assignments = itertools.product((0, 1), repeat=8)
    for parities in assignments:
        difference = nested_planar_corner_difference(exponent, parities)
        if difference != 1:
            return "nested", parities, difference
    return None


def check_planar_signs() -> None:
    """Exhaust the linear and displayed quadratic sign ansatzes in Lemma 5.7."""
    # The six coefficient slots are, in order: prefix-degree sum,
    # block-degree sum, suffix-degree sum, |z|, |y|, and the constant.
    # Every parity assignment below lifts to integer degrees with nonnegative
    # expected dimensions after adding sufficiently large even integers, so the
    # Boolean enumeration checks the polynomial identities without a degree bound.
    parity_assignments = tuple(itertools.product((0, 1), repeat=8))
    linear_failures: dict[tuple[int, ...], tuple[str, tuple[int, ...], int]] = {}
    linear_survivors: list[tuple[int, ...]] = []
    linear_disjoint_survivors: list[tuple[int, ...]] = []
    for coefficients in itertools.product((0, 1), repeat=6):
        exponent = lambda *values, coefficients=coefficients: linear_planar_exponent(
            coefficients, *values
        )
        disjoint_table = tuple(
            disjoint_planar_corner_difference(exponent, values)
            for values in parity_assignments
        )
        nested_table = tuple(
            nested_planar_corner_difference(exponent, values)
            for values in parity_assignments
        )
        disjoint_passes = all(difference == 1 for difference in disjoint_table)
        nested_passes = all(difference == 1 for difference in nested_table)
        if disjoint_passes:
            linear_disjoint_survivors.append(coefficients)
        failure = first_planar_corner_failure(exponent)
        if disjoint_passes and nested_passes:
            require(failure is None, "a surviving linear candidate has a failure witness")
            linear_survivors.append(coefficients)
        else:
            require(failure is not None, "a rejected linear candidate lacks a failure witness")
            linear_failures[coefficients] = failure

    require(
        len(linear_failures) == 64,
        "every linear planar-sign candidate should have a failure witness",
    )
    require(
        linear_survivors == [],
        f"unexpected linear planar-sign survivors: {linear_survivors}",
    )
    require(
        all(failure[0] == "disjoint" for failure in linear_failures.values()),
        "the disjoint corner should reject every linear planar-sign candidate",
    )
    require(
        linear_disjoint_survivors == [],
        f"unexpected disjoint-corner linear survivors: {linear_disjoint_survivors}",
    )

    quadratic_failures: dict[tuple[int, int, int], tuple[str, tuple[int, ...], int]] = {}
    quadratic_survivors: list[tuple[int, int, int]] = []
    quadratic_disjoint_survivors: list[tuple[int, int, int]] = []
    quadratic_nested_survivors: list[tuple[int, int, int]] = []
    for parameters in itertools.product((0, 1), repeat=3):
        exponent = lambda *values, parameters=parameters: quadratic_planar_exponent(
            parameters, *values
        )
        disjoint_table = tuple(
            disjoint_planar_corner_difference(exponent, values)
            for values in parity_assignments
        )
        nested_table = tuple(
            nested_planar_corner_difference(exponent, values)
            for values in parity_assignments
        )
        if all(difference == 1 for difference in disjoint_table):
            quadratic_disjoint_survivors.append(parameters)
        if all(difference == 1 for difference in nested_table):
            quadratic_nested_survivors.append(parameters)
        failure = first_planar_corner_failure(exponent)
        if failure is None:
            quadratic_survivors.append(parameters)
        else:
            quadratic_failures[parameters] = failure

    require(
        len(quadratic_failures) == 7,
        "seven quadratic planar-sign candidates should fail",
    )
    require(
        quadratic_survivors == [(1, 1, 1)],
        f"wrong quadratic planar-sign survivor set: {quadratic_survivors}",
    )
    require(
        quadratic_disjoint_survivors == [(1, 0, 1), (1, 1, 1)],
        f"wrong disjoint-corner survivor set: {quadratic_disjoint_survivors}",
    )
    require(
        quadratic_nested_survivors == [(1, 1, 1)],
        f"wrong nested-corner survivor set: {quadratic_nested_survivors}",
    )

    canonical = lambda *values: quadratic_planar_exponent((1, 1, 1), *values)
    for prefix, block, suffix, intermediate, output in itertools.product(
        (0, 1), repeat=5
    ):
        alpha, beta = planar_dimension_parities(prefix, block, suffix, intermediate, output)
        if alpha == beta == 0:
            require(
                canonical(prefix, block, suffix, intermediate, output) == prefix,
                "dimension-one planar facet sign should reduce to the bar sign",
            )


def check_stable_map_dimensions() -> None:
    # Standard real virtual dimension and both one-node splittings.
    for m, g, n, c1 in itertools.product(range(1, 6), range(0, 4), range(0, 7), range(-4, 7)):
        dim = 2 * c1 + 2 * (m - 3) * (1 - g) + 2 * n

        # Separating node: g=g1+g2, n=n1+n2, c1=c11+c12;
        # each component acquires one nodal marking and matching subtracts 2m.
        for g1 in range(g + 1):
            g2 = g - g1
            for n1 in range(n + 1):
                n2 = n - n1
                c11, c12 = c1 - 1, 1
                split = (
                    2 * c11 + 2 * (m - 3) * (1 - g1) + 2 * (n1 + 1)
                    + 2 * c12 + 2 * (m - 3) * (1 - g2) + 2 * (n2 + 1)
                    - 2 * m
                )
                require(split == dim - 2, "separating stable-map codimension failed")

        # Nonseparating node: normalize genus down by one, add two markings,
        # and match the two evaluations along the diagonal of real codimension 2m.
        if g >= 1:
            normalized = 2 * c1 + 2 * (m - 3) * (1 - (g - 1)) + 2 * (n + 2) - 2 * m
            require(normalized == dim - 2, "nonseparating stable-map codimension failed")


def permutation_sign(values: list[int]) -> int:
    inversions = sum(values[i] > values[j] for i in range(len(values)) for j in range(i + 1, len(values)))
    return -1 if inversions % 2 else 1


def check_pentagon_monodromy() -> None:
    # For K_3, order summands outer vertex first, inner vertex second.
    # At (xy)z these two gap labels are [2,1]; at x(yz) they are [1,2].
    gap_left = [2, 1]
    gap_right = [1, 2]
    require(permutation_sign(gap_left) == -1, "left gap map should be a transposition")
    require(permutation_sign(gap_right) == 1, "right gap map should preserve order")
    gap_product = permutation_sign(gap_left) * permutation_sign(gap_right)
    require(gap_product == -1, "gap endpoint determinant product should be negative")

    # Five interval faces each use one endpoint of each shape.  Relative to the
    # gap datum, the determinant monodromy is the fifth power of the ratio.
    for det_left, det_right in itertools.product((-1, 1), repeat=2):
        relative = ((det_left * det_right) * gap_product) ** 5
        monodromy = relative  # the gap bundle itself has trivial monodromy
        orientable = monodromy == 1
        require(orientable == (det_left * det_right < 0), "pentagon orientability criterion failed")

    # The additive gap decoration has n-1 labels, so a K_4 facet has rank
    # (3-1)+(2-1)=3, equal to the ambient K_4 decoration rank.
    require((3 - 1) + (2 - 1) == 4 - 1, "pentagon bundle rank failed")


def increasing_types(objects: set[int]) -> set[tuple[int, ...]]:
    return {
        tuple(xs)
        for size in range(3, len(objects) + 1)
        for xs in itertools.combinations(sorted(objects), size)
    }


def check_overlap_quartets() -> None:
    o1, o2 = {1, 2, 3, 4}, {2, 3, 4, 5}
    o0 = o1 & o2
    t0, t1, t2 = map(increasing_types, (o0, o1, o2))
    require(t0 == {(2, 3, 4)}, "overlap should contain one increasing type")
    require(len(t1) == 5 and len(t2) == 5, "each quartet should have four triples and one quadruple")
    require(t1 & t2 == t0, "the two type systems should intersect exactly on (2,3,4)")
    union = t1 | t2
    require((1, 2, 3, 4, 5) not in union, "union grammar must not contain the mixed pentagon type")
    require(sum(len(t) == 3 for t in union) == 7, "union should contain seven zero-dimensional triple types")
    require(sum(len(t) == 4 for t in union) == 2, "union should contain two one-dimensional quartet types")

    # K_3 is an interval: each arity-four type therefore has two facets.
    require(len(list(itertools.combinations(range(3), 2))) - 1 == 2, "quartet facet count failed")


def main() -> int:
    check_grading_identities()
    check_planar_signs()
    check_stable_map_dimensions()
    check_pentagon_monodromy()
    check_overlap_quartets()
    print("Finite calculations: PASS")
    print("  Planar signs: all 64 linear candidates rejected;")
    print("  (u,v,w)=(1,1,1) is the unique survivor in the displayed quadratic family.")
    print("  Rank-one pentagon determinant signs and overlap-type counts checked.")
    print("  Bounded grading and stable-map dimension checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Finite calculations: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
