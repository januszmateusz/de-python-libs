from collections.abc import Mapping


def assert_same_flight(
    actual: Mapping[str, object], expected: Mapping[str, object]
) -> None:
    assert actual == expected
