# Generated by Django 4.1 on 2023-01-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getit_api', '0005_rename_live_livedb_alter_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='livedb',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='', upload_to='product_images/'),
        ),
    ]