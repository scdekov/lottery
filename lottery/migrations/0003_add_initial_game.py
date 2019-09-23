from django.db import migrations


def create_default_game(apps, schema_editor):
    Game = apps.get_model('lottery', 'Game')
    if not Game.objects.count():
        Game.objects.create()


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_auto_20190921_1413'),
    ]

    operations = [
        migrations.RunPython(code=create_default_game,
                             reverse_code=lambda *args, **kwargs: True)
    ]
