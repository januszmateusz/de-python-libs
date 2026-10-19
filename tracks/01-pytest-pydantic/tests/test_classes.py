class TestAirport:
    def test_code(self) -> None:
        code = "WAW"
        assert len(code) == 3


class TestRoute:
    def __init__(self, origin: str, destination: str) -> None:
        self.origin = origin
        self.destination = destination

    def test_distance(self) -> None:
        assert self.origin != self.destination