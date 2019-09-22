import pytest

from rest_framework import status

from django.shortcuts import reverse

from lottery.models import Ticket, Game


@pytest.mark.django_db
class TestTicketsView:
    def test_get(self, client, loosers):
        resp = client.get(reverse('tickets'))
        assert len(resp.data) == len(loosers)

    def test_post__invalid_data(self, client):
        resp = client.post(reverse('tickets'), data={})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_post(self, client, game):
        ticket_data = {
            'numbers': [1, 2, 3, 4, 5, 6],
            'game': game.id,
            'nickname': 'nick'
        }
        resp = client.post(reverse('tickets'), data=ticket_data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert Ticket.objects.count() == 1
        ticket = Ticket.objects.first()
        assert ticket.game_id == ticket_data['game']
        assert ticket.numbers == ticket_data['numbers']
        assert ticket.nickname == ticket_data['nickname']

    def test_post__invalid_numbers(self, client, game):
        ticket_data = {
            'numbers': [1, 2, 3, 4, 5],
            'game': game.id,
            'nickname': 'nick'
        }
        resp = client.post(reverse('tickets'), data=ticket_data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGameView:
    def test_get(self, client, game):
        resp = client.get(reverse('game-detail', kwargs={'pk': game.id}))
        assert resp.status_code == status.HTTP_200_OK

    def test_post(self, client):
        resp = client.post(reverse('game-list'))
        assert resp.status_code == status.HTTP_201_CREATED
        assert Game.objects.count() == 1

    @pytest.mark.usefixtures('finished_game')
    def test_latest(self, client, game):
        resp = client.get(reverse('game-latest'))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['id'] == game.id

    def test_latest__no_games(self, client):
        resp = client.get(reverse('game-latest'))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_draw(self, client, game, mocker):
        draw = mocker.patch('lottery.api.views.Game.draw')

        resp = client.post(reverse('game-draw', kwargs={'pk': game.id}))

        assert resp.status_code == status.HTTP_202_ACCEPTED
        draw.assert_called_once()
