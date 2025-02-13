# inventory/migrations/0002_load_initial_data.py
from django.db import migrations

def load_initial_data(apps, schema_editor):
    # Get the Products model from the historical version provided by migrations.
    Products = apps.get_model('inventory', 'Products')
    initial_products = [
        {
            'product_id': 515262,
            'product_name': 'De Chancey Brut Crémant de Loire',
            'class_index': 0,
            'class_label_name': '515262_De_Chancey',
            'made_in': 'Loire, France',
            'made_by': 'Vintages Front Line Release',
            'sugar_content': '6 g/L',
            'varietal': 'Crémant',
            'product_type': 'Vintage',
            'alcohol_volume': 12.3,
            'product_details': 'Great rise in temperament, energy and quality here from the rich and generous 2021 vintage...',
        },
        {
            'product_id': 37687,
            'product_name': 'Teliani Valley Glekhuri Kisiskhevi Qvevri Saperavi',
            'class_index': 1,
            'class_label_name': '37687_Glekhuri',
            'made_in': 'Kakheti, Georgia',
            'made_by': 'Kakheti, Georgia',
            'sugar_content': '3 g/L',
            'varietal': 'Saperavi',
            'product_type': 'Vintage',
            'alcohol_volume': 13.5,
            'product_details': "['Qvevri' refers to the ceramic amphorae used in fermentation.] 100% Saperavi. Dense savoury blackberry aromas with touches of almonds and hints of earthy character.",
        },
        {
            'product_id': 37691,
            'product_name': 'Mildiani Alazani Valley Semi-Sweet Red 2021',
            'class_index': 2,
            'class_label_name': '37691_Alazani_Valley_SS_Red',
            'made_in': 'Kakheti, Georgia',
            'made_by': 'Kakheti, Georgia',
            'sugar_content': '39 g/L',
            'varietal': 'Red Blend',
            'product_type': 'Vintage',
            'alcohol_volume': 12,
            'product_details': 'This semi-sweet red is a blend of Saperavi and Cabernet farmed without synthetic chemicals. Tangy and savoury, it offers ripe fruit and baking spices with a pleasant, balanced sweetness on the finish.',
        }
    ]
    for product_data in initial_products:
        # Use get_or_create to avoid inserting duplicates
        Products.objects.get_or_create(**product_data)

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
