import random

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


class Game(models.Model):
    winning_numbers = ArrayField(models.SmallIntegerField(), size=6, null=True)
    is_active = models.BooleanField(default=True)

    def draw(self):
        if not self.is_active:
            return

        self.winning_numbers = []
        while len(self.winning_numbers) < 6:
            number = random.randint(1, 49)
            if number not in self.winning_numbers:
                self.winning_numbers.append(number)

        # self.is_active = False
        self.save()

    @property
    def winners(self):
        if not self.winning_numbers:
            return []

        winners_filter = ' + '.join(['is_{}_selected'.format(winning_number)
                                     for winning_number in self.winning_numbers])

        return list(Ticket.objects.raw("""
            SELECT id, nickname, numbers, {winners_filter} as matching_numbers FROM lottery_ticket
            where {winners_filter} > 2
        """.format(winners_filter=winners_filter)))

    @property
    def submitted_tickets_count(self):
        return self.ticket_set.count()


class TicketsMeta(models.base.ModelBase):
    def __new__(cls, clsname, bases, dct):
        newclass = super(TicketsMeta, cls).__new__(cls, clsname, bases, dct)
        for ix in range(1, newclass.BIGGEST_NUMBER + 1):
            field = models.SmallIntegerField(null=False, default=0)
            newclass.add_to_class('is_{}_selected'.format(ix), field)

        return newclass


class Ticket(models.Model, metaclass=TicketsMeta):
    BIGGEST_NUMBER = 49

    nickname = models.CharField(max_length=256)
    numbers = ArrayField(models.SmallIntegerField(), size=6)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        for selected_number in self.numbers:
            setattr(self, 'is_{}_selected'.format(selected_number), 1)

        super().save(*args, **kwargs)

    def clean(self):
        if len(set(self.numbers)) != 6 or any([n not in range(1, self.BIGGEST_NUMBER + 1) for n in self.numbers]):
            raise ValidationError('numbers should be 6 and unique and in range 1-{}'.format(self.BIGGEST_NUMBER))
