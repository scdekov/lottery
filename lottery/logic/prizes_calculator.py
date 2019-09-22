from decimal import Decimal, ROUND_HALF_UP


class PrizesCalculator:
    jacpot = Decimal(1000000)
    prize_percent_shares = {
        3: Decimal(0.1),
        4: Decimal(0.15),
        5: Decimal(0.25),
        6: Decimal(0.50)
    }

    @classmethod
    def add_prizes(cls, winners):
        winners = list(winners)
        prize_shares_per_winner = cls._get_prize_shares_per_winner(winners)
        for winner in winners:
            winner['prize'] = prize_shares_per_winner[winner['matching_numbers']]

        return winners

    @classmethod
    def _get_prize_shares_per_winner(cls, winners):
        winner_counts = {matching_numbers: 0 for matching_numbers in cls.prize_percent_shares.keys()}
        for winner in winners:
            winner_counts[winner['matching_numbers']] += 1

        if winner_counts[6] == len(winners):
            return {6: cls.jacpot}

        return {
            matching_numbers:
            (cls.prize_percent_shares[matching_numbers] *
                cls.jacpot / winner_counts[matching_numbers]).quantize(Decimal('.01'), ROUND_HALF_UP)
            for matching_numbers in cls.prize_percent_shares.keys() if winner_counts[matching_numbers]
        }
