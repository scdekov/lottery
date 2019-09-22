import pytest

from django.core.exceptions import ValidationError

from lottery.models import Ticket


@pytest.mark.django_db
class TestTicket:
    def test_save(self, game):
        numbers = [1, 2, 3, 4, 5, 6]
        ticket = Ticket.objects.create(numbers=numbers, game=game, nickname='comar')
        for i in range(1, 50):
            if i in numbers:
                assert getattr(ticket, 'is_{}_selected'.format(i))
            else:
                assert not getattr(ticket, 'is_{}_selected'.format(i))

    def test_save__not_unique_numbers(self, game):
        with pytest.raises(ValidationError):
            Ticket.objects.create(numbers=[1, 1, 3, 4, 5, 6], game=game)

    def test_save__not_enough_numbers(self, game):
        with pytest.raises(ValidationError):
            Ticket.objects.create(numbers=[1, 1, 3, 4, 5], game=game)


@pytest.mark.django_db
class TestGame:
    def test_draw(self, game):
        game.draw()
        assert not game.is_active
        assert len(set(game.winning_numbers)) == 6
        assert all([num <= 49 and num >= 1 for num in game.winning_numbers])

    def test_draw__already_drawn(self, game):
        game.draw()
        winning_numbers = game.winning_numbers
        game.draw()
        assert game.winning_numbers == winning_numbers

    def test_winners__game_not_finished(self, game):
        assert not game.winners

    @pytest.mark.usefixtures('loosers')
    def test_winners__no_winner(self, finished_game):
        assert not finished_game.winners

    @pytest.mark.usefixtures('loosers')
    def test_winners__single_winner(self, finished_game, winner_ticket_6):
        winners = finished_game.winners
        assert len(winners) == 1
        assert winners[0].id == winner_ticket_6.id
        assert winners[0].matching_numbers == 6

    @pytest.mark.usefixtures('loosers')
    def test_winners__multiple_winners(self, finished_game, winner_ticket_6, winner_ticket_3):
        winners = finished_game.winners
        assert len(winners) == 2
        winners_by_id = {winner.id: winner for winner in winners}
        assert winner_ticket_3.id in winners_by_id.keys()
        assert winners_by_id[winner_ticket_3.id].matching_numbers == 3
        assert winner_ticket_6.id in winners_by_id.keys()
        assert winners_by_id[winner_ticket_6.id].matching_numbers == 6
