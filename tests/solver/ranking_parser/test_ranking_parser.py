from solver import RankingParser


def test_can_create_rule_parser():
    rp = RankingParser()
    assert(isinstance(rp, RankingParser))


