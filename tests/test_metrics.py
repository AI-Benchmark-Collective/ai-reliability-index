from __future__ import annotations

import pytest

from airi.metrics import outcome_consistency, rate, wilson_interval


def test_rate_and_empty_denominator() -> None:
    assert rate(3, 4) == 0.75
    assert rate(0, 0) is None


def test_invalid_rate_rejected() -> None:
    with pytest.raises(ValueError):
        rate(5, 4)


def test_wilson_interval_known_case() -> None:
    lower, upper = wilson_interval(8, 10) or (None, None)
    assert lower == pytest.approx(0.4902, abs=0.001)
    assert upper == pytest.approx(0.9433, abs=0.001)


def test_outcome_consistency_is_modal_share() -> None:
    assert outcome_consistency(["success", "success", "failure", "success"]) == 0.75
    assert outcome_consistency([]) is None
