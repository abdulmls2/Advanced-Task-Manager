# Generated by Django 3.2.18 on 2023-03-13 13:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('nature_of_task', models.CharField(max_length=2000, null=True)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('ending_date', models.DateField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile')),
            ],
            options={
                'ordering': ['creation_date'],
            },
        ),
    ]
