# Generated by Django 2.0.2 on 2018-02-20 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeycloakOpenIDProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('expires_before', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('refresh_expires_before', models.DateTimeField(null=True)),
                ('sub', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('state', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('redirect_uri', models.CharField(max_length=255)),
                ('next_path', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('expires_before', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('refresh_expires_before', models.DateTimeField(null=True)),
                ('server_url', models.CharField(max_length=255)),
                ('internal_server_url', models.CharField(
                    help_text='URL on internal netwerk calls. For example when '
                              'used with Docker Compose. Only supply when '
                              'internal calls should go to a different url as '
                              'the end-user will communicate with.',
                    max_length=255, null=True, blank=True)),
                ('name', models.CharField(
                    help_text='Name as known on the Keycloak server. This name '
                              'is used in the API paths of this Realm.',
                    max_length=255, unique=True)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('_certs', models.TextField()),
                ('_well_known_oidc', models.TextField(blank=True)),
                ('_well_known_uma', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50)),
                ('permission', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='auth.Permission')),
                ('realm', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='roles', to='django_keycloak.Realm')),
            ],
        ),
        migrations.AddField(
            model_name='keycloakopenidprofile',
            name='realm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='openid_profiles',
                                    to='django_keycloak.Realm'),
        ),
        migrations.AddField(
            model_name='keycloakopenidprofile',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='oidc_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('realm', 'permission')},
        ),
    ]
