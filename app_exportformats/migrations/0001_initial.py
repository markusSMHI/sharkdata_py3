# Generated by Django 2.2 on 2019-04-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExportFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(default='', max_length=63)),
                ('datatype', models.CharField(default='', max_length=63)),
                ('year', models.CharField(default='', max_length=4)),
                ('approved', models.BooleanField(default=False)),
                ('status', models.CharField(default='', max_length=63)),
                ('export_name', models.CharField(db_index=True, default='', max_length=255)),
                ('export_file_name', models.CharField(default='', max_length=255)),
                ('export_file_path', models.CharField(default='', max_length=1023)),
                ('error_log_file', models.CharField(default='', max_length=255)),
                ('error_log_file_path', models.CharField(default='', max_length=1023)),
                ('generated_by', models.CharField(default='', max_length=255)),
                ('generated_datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
