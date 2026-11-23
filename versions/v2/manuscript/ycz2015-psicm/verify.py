import json
from fractions import Fraction
from math import comb
from pathlib import Path


def polynomial(parameter, point):
    return point**4 + parameter * point**2 + Fraction(7, 40) * parameter - Fraction(31, 336)


def polynomial_first(parameter, point):
    return 4 * point**3 + 2 * parameter * point


def polynomial_second(parameter, point):
    return 12 * point**2 + 2 * parameter


def lower_bound(parameter, point, remainder_lower=Fraction(11, 6)):
    return 24 * (
        remainder_lower * polynomial_second(parameter, point)
        - 128 * polynomial_first(parameter, point)
        + 4078 * polynomial(parameter, point)
    ) - 2


def asymptotic_coefficients():
    bernoulli = [Fraction(1)]
    for degree in range(1, 11):
        bernoulli.append(-sum(
            Fraction(comb(degree + 1, index)) * bernoulli[index]
            for index in range(degree)
        ) / (degree + 1))
    coefficients = [Fraction(0)] * 12
    for degree in range(1, 12):
        coefficients[degree] += Fraction((-1)**(degree + 1), degree * 2**degree)
        coefficients[degree] -= Fraction((-1)**(degree - 1), 2**degree)
    for order in range(2, 11, 2):
        for degree in range(order, 12):
            offset = degree - order
            coefficients[degree] -= (
                bernoulli[order] / order * (-1)**offset
                * comb(order + offset - 1, offset) / 2**offset
            )
    expected = [
        Fraction(1, 24), -Fraction(7, 960), Fraction(31, 8064),
        -Fraction(127, 30720), Fraction(511, 67584),
    ]
    assert coefficients[1::2] == [Fraction(0)] * 6
    assert coefficients[2::2] == expected
    return [Fraction(0)] + expected


def main():
    point = Fraction(1, 64)
    critical = Fraction(331467377585, 629168992256)
    simple = Fraction(5269, 10000)
    kang_parameter = Fraction(527, 1000)
    threshold = Fraction(155, 294)
    lean_parameter = threshold - Fraction(1, 10000)
    assert 0 < critical < simple < kang_parameter < lean_parameter < threshold
    assert polynomial(critical, point) == Fraction(236541533, 3775013953536) > 0
    assert polynomial_first(critical, point) > 0
    assert polynomial_second(critical, point) > 0
    slopes = [point**2 + Fraction(7, 40), 2 * point, Fraction(2)]
    assert slopes == [Fraction(3589, 20480), Fraction(1, 32), Fraction(2)]
    shift = Fraction(97, 64)
    telescoper = [shift**3 - 2, 3 * shift**2 - 3, 3 * shift - 1, Fraction(1)]
    assert telescoper == [
        Fraction(388385, 262144), Fraction(15939, 4096),
        Fraction(227, 64), Fraction(1),
    ]
    assert all(value > 0 for value in telescoper)
    cubic_upper = Fraction(64, 33)**3 + 1
    assert cubic_upper == Fraction(298081, 35937) < 9
    assert point**-2 - 18 == 4078
    assert 4 * Fraction(2, 3) - Fraction(5, 6) == Fraction(11, 6)
    slope = lower_bound(Fraction(1), point) - lower_bound(Fraction(0), point)
    assert slope == Fraction(21943673, 1280) > 0
    assert lower_bound(critical, point) == 0
    simple_lower = lower_bound(simple, point)
    assert simple_lower == Fraction(26102771679, 22937600000) > 1
    for parameter in [critical, simple, kang_parameter, lean_parameter, threshold, Fraction(1)]:
        assert lower_bound(parameter, point) == slope * (parameter - critical)
    assert lower_bound(lean_parameter, point, Fraction(5, 3)) == Fraction(252732646219, 481689600000)
    assert lower_bound(lean_parameter, point) == Fraction(2289608094539, 481689600000)
    remainder = asymptotic_coefficients()
    coefficient_slope = 24 * (remainder[3] + Fraction(7, 40) * remainder[2])
    coefficient_constant = 24 * (remainder[4] - Fraction(31, 336) * remainder[2])
    assert coefficient_slope == Fraction(2071, 33600) > 0
    assert coefficient_constant == -Fraction(319, 3840)
    endpoint = -coefficient_constant / coefficient_slope
    assert endpoint == Fraction(11165, 8284)
    constant_polynomial = Fraction(7, 40) * endpoint - Fraction(31, 336)
    assert constant_polynomial == Fraction(199849, 1391712) > 0
    source_vector = [24 * constant_polynomial, 24 * endpoint, Fraction(24)]
    for power in [1, 2]:
        assert sum(source_vector[index] * remainder[index + power] for index in range(3)) == 0
    assert source_vector[2] * remainder[1] == 1
    assert source_vector[1] * remainder[1] + source_vector[2] * remainder[2] == endpoint - Fraction(7, 40)
    leading = sum(source_vector[index] * remainder[index + 3] for index in range(3))
    assert leading == Fraction(627404761, 10287535104) > 0
    determinant = remainder[1] * remainder[3] - remainder[2]**2
    assert determinant == Fraction(2071, 19353600) != 0
    base_leading = 24 * (remainder[3] + Fraction(7, 40) * remainder[2])
    assert base_leading == Fraction(2071, 33600) > 0
    output = {
        'coverage': 'Exact rational calculations for Theorem 1 and the coefficient corollaries',
        'arithmetic': 'Python fractions.Fraction; exact rational arithmetic',
        'x': str(point),
        'a_c': str(critical),
        'a_bar': str(simple),
        'ordered_positive_parameters': list(map(str, [critical, simple, kang_parameter, lean_parameter, threshold])),
        'P_at_a_c': str(polynomial(critical, point)),
        'positive_parameter_slopes': list(map(str, slopes)),
        'telescoper_coefficients_ascending': list(map(str, telescoper)),
        'cubic_series_upper_bound': str(cubic_upper),
        'R_strict_lower_bound': '11/6',
        'R_second_strict_lower_bound': '4078',
        'affine_bound_at_a_c': '0',
        'affine_bound_parameter_slope': str(slope),
        'G_second_strict_lower_bound_at_a_bar': str(simple_lower),
        'margin_above_one': str(simple_lower - 1),
        'earlier_half_unit_range_lower_bound': str(lower_bound(lean_parameter, point)),
        'asymptotic_coefficients_x_minus_2_through_10': list(map(str, remainder[1:])),
        'quartic_cancellation_determinant': str(determinant),
        'quartic_endpoint': str(endpoint),
        'quartic_x_minus_6_coefficient_per_t': str(leading),
        'quadratic_x_minus_4_coefficient_per_t': str(base_leading),
        'all_finite_inequalities_satisfied': True,
        'analytic_scope': 'Series, derivative bounds, endpoint arguments and coefficient classification have written or cited proofs in note.tex',
    }
    rendered = json.dumps(output, indent=2) + '\n'
    Path(__file__).with_name('verify-output.json').write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
