from rest_framework.views import APIView
from rest_framework import serializers, status, viewsets, mixins, decorators
from rest_framework.response import Response

from lottery.models import Ticket, Game


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'nickname', 'numbers')


class CreateTicketView(APIView):
    def get(self, request):
        return Response(data=TicketSerializer(Ticket.objects.all(), many=True).data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Ticket.objects.create(nickname=serializer.validated_data['nickname'],
                              numbers=serializer.validated_data['numbers'])

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


class GameViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSeriazlier

    @decorators.action(methods=['POST'], url_path='@draw', detail=True)
    def draw(self, request):
        game = self.get_object()
        game.draw()
        return Response(status=status.HTTP_202_ACCEPTED)

    @decorators.action(methods=['GET'], url_path='@latest', detail=False)
    def latest(self, reuqest):
        latest_game = Game.objects.filter(is_active=True).order_by('-id').first()
        if latest_game:
            return Response(GameSeriazlier(latest_game).data)

        return Response(status=status.HTTP_404_NOT_FOUND)
