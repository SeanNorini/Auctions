# Generated by Django 4.2.5 on 2023-10-16 21:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="date_ends",
            field=models.DateField(
                default=datetime.datetime(2023, 10, 23, 17, 36, 25, 244760)
            ),
        ),
    ]
