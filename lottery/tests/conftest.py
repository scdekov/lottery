import pytest

from rest_framework.test import APIClient

from model_mommy import mommy


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def game():
    return mommy.make('lottery.Game')


@pytest.fixture()
def finished_game():
    game = mommy.make('lottery.Game')
    game.winning_numbers = [1, 3, 5, 7, 9, 11]
    game.is_active = False
    game.save()
    return game


@pytest.fixture()
def ticket(game):
    ticket = mommy.make('lottery.Ticket', game=game, nickname='pesho')
    ticket.numbers = [1, 2, 3, 4, 5, 6]
    ticket.save()
    return ticket


@pytest.fixture()
def winner_ticket_6(finished_game):
    return mommy.make('lottery.Ticket', game=finished_game, nickname='gosho',
                      numbers=finished_game.winning_numbers)


def get_looser_numbers(winning_numbers, count):
    n = 1
    looser_numbers = []
    while len(looser_numbers) < count:
        if n not in winning_numbers:
            looser_numbers.append(n)
        n += 1
    return looser_numbers


@pytest.fixture()
def winner_ticket_3(finished_game):
    return mommy.make('lottery.Ticket', game=finished_game, nickname='ivan',
                      numbers=finished_game.winning_numbers[:3] +
                      get_looser_numbers(finished_game.winning_numbers, 3))


@pytest.fixture()
def loosers(finished_game):
    ticket_0 = mommy.make('lottery.Ticket', game=finished_game, nickname='ivan',
                          numbers=get_looser_numbers(finished_game.winning_numbers, 6))
    ticket_1 = mommy.make('lottery.Ticket', game=finished_game, nickname='ivan1',
                          numbers=[finished_game.winning_numbers[0]] +
                          get_looser_numbers(finished_game.winning_numbers, 5))
    ticket_2 = mommy.make('lottery.Ticket', game=finished_game, nickname='ivan2',
                          numbers=finished_game.winning_numbers[:2] +
                          get_looser_numbers(finished_game.winning_numbers, 4))
    return [ticket_0, ticket_1, ticket_2]
