from solver import RankingParser


def test_can_create_rule_parser():
    rp = RankingParser()
    assert(isinstance(rp, RankingParser))


def test_ranking_parser_multi_line_input():
    multi_line_input = """
    [Green] before [Red]
    [Yellow] before [Green]
    """

    expected_result = [
        ("Yellow", "Green", "Red")
    ]

    rp = RankingParser()
    rp.build()
    rp.parse(multi_line_input)

    assert(rp.solve() == expected_result)
