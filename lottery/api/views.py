from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets, mixins, decorators
from rest_framework.response import Response

from lottery.models import Ticket, Game
from lottery.logic.prizes_calculator import PrizesCalculator


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'nickname', 'numbers', 'game')

    def validate(self, attrs):
        instance = Ticket(**attrs)
        instance.clean()
        return attrs


class TicketsView(APIView):
    def get(self, request):
        return Response(data=TicketSerializer(Ticket.objects.all(), many=True).data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Ticket.objects.create(nickname=serializer.validated_data['nickname'],
                              numbers=serializer.validated_data['numbers'],
                              game=serializer.validated_data['game'])

        return Response(status=status.HTTP_201_CREATED)


class WinnerTicketSerializer(TicketSerializer):
    class Meta(TicketSerializer.Meta):
        fields = ('id', 'nickname', 'numbers', 'matching_numbers')
        read_only_fields = ('matching_numbers',)

    matching_numbers = serializers.IntegerField()


class GameSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'winning_numbers', 'is_active', 'winners')
        read_only_fields = ('winning_numbers', 'winners')

    winners = WinnerTicketSerializer(many=True, read_only=True)


class GameViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSeriazlier

    def retrieve(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = self.get_serializer(game)
        data = serializer.data
        data['winners'] = PrizesCalculator.add_prizes(data['winners'])
        return Response(data)

    @decorators.action(methods=['POST'], url_path='@draw', detail=True)
    def draw(self, request, *args, **kwargs):
        game = self.get_object()
        game.draw()
        return Response(status=status.HTTP_202_ACCEPTED)

    @decorators.action(methods=['GET'], url_path='@latest', detail=False)
    def latest(self, reuqest):
        latest_game = Game.objects.filter(is_active=True).order_by('-id').first()
        if latest_game:
            return Response(GameSeriazlier(latest_game).data)

        return Response(status=status.HTTP_404_NOT_FOUND)
