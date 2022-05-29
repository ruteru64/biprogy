# Generated by Django 4.0.4 on 2022-05-28 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_topic_partner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='topic1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='topic2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='topic3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='belongs',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=200),
        ),
    ]
