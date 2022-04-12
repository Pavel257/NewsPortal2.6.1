# Generated by Django 4.0 on 2022-04-09 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0004_alter_author_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='authorUser',
            field=models.OneToOneField(help_text='author name', on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Имя автора'),
        ),
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('NW', 'Новости'), ('AR', 'Статья')], default='AR', help_text='category name', max_length=2, verbose_name='Категория'),
        ),
    ]