# inventory/migrations/0001_initial.py

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(db_column='Product Id', primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('class_index', models.IntegerField()),
                ('class_label_name', models.CharField(max_length=255)),
                ('made_in', models.CharField(max_length=255)),
                ('made_by', models.CharField(max_length=255)),
                ('sugar_content', models.CharField(max_length=100)),
                ('varietal', models.CharField(max_length=255)),
                ('alcohol_volume', models.FloatField()),
                ('product_details', models.TextField(blank=True, null=True)),
                ('product_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Alcohol Product',
                'verbose_name_plural': 'Alcohol Products',
                'db_table': 'alcohol_inventory',
            },
        ),
    ]
