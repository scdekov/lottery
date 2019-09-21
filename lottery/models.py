from django.contrib.postgres.fields import ArrayField
from django.db import models


class TicketsMeta(models.base.ModelBase):
    def __new__(cls, clsname, bases, dct):
        newclass = super(TicketsMeta, cls).__new__(cls, clsname, bases, dct)
        for ix in range(1, newclass.BIGGEST_NUMBER + 1):
            field = models.SmallIntegerField(null=False)
            newclass.add_to_class('is_{}_selected'.format(ix), field)

        return newclass


class Ticket(models.Model, metaclass=TicketsMeta):
    BIGGEST_NUMBER = 49

    nickname = models.CharField(max_length=256)
    numbers = ArrayField(models.SmallIntegerField(), size=6)
