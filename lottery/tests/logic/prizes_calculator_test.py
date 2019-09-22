from decimal import Decimal, ROUND_HALF_UP

from lottery.logic.prizes_calculator import PrizesCalculator


class TestPrizesCalculator:
    def test_add_prizes__no_winners(self):
        assert not PrizesCalculator.add_prizes([])

    def test_add_prizes__super_jacpot(self):
        assert PrizesCalculator.add_prizes([{'matching_numbers': 6}]) == [
            {'matching_numbers': 6, 'prize': PrizesCalculator.jacpot}
        ]

    @staticmethod
    def _get_decimal_price(price):
        return Decimal(price).quantize(Decimal('.01'), ROUND_HALF_UP)

    def test_add_prizes__single_winner_3(self):
        assert PrizesCalculator.add_prizes([{'matching_numbers': 3}]) == [
            {'matching_numbers': 3, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.1))}
        ]

    def test_add_prizes__single_winners_3_6(self):
        assert PrizesCalculator.add_prizes([
            {'matching_numbers': 6},
            {'matching_numbers': 3},
        ]) == [
            {'matching_numbers': 6, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.5))},
            {'matching_numbers': 3, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.1))}
        ]

    def test_add_prizes__single_winners_3_3_4_6(self):
        assert PrizesCalculator.add_prizes([
            {'matching_numbers': 4},
            {'matching_numbers': 3},
            {'matching_numbers': 6},
            {'matching_numbers': 3}
        ]) == [
            {'matching_numbers': 4, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.15))},
            {'matching_numbers': 3, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.05))},
            {'matching_numbers': 6, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.5))},
            {'matching_numbers': 3, 'prize': self._get_decimal_price(PrizesCalculator.jacpot * Decimal(0.05))}
        ]
