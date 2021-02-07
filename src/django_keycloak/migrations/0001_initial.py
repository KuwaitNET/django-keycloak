from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteUserOpenIdConnectProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('expires_before', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('refresh_expires_before', models.DateTimeField(null=True)),
                ('sub', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
                'swappable': 'KEYCLOAK_OIDC_PROFILE_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('redirect_uri', models.CharField(max_length=255)),
                ('next_path', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name as known on the Keycloak server. This name is used in the API paths of this Realm.', max_length=255, unique=True)),
                ('_certs', models.TextField()),
                ('_well_known_oidc', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('internal_url', models.CharField(blank=True, help_text='URL on internal netwerk calls. For example when used with Docker Compose. Only supply when internal calls should go to a different url as the end-user will communicate with.', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remote_clients', to='django_keycloak.realm')),
            ],
        ),
        migrations.AddField(
            model_name='realm',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='realms', to='django_keycloak.server'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255)),
                ('secret', models.CharField(max_length=255)),
                ('realm', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='django_keycloak.realm')),
                ('service_account_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.KEYCLOAK_OIDC_PROFILE_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='remoteuseropenidconnectprofile',
            name='realm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openid_profiles', to='django_keycloak.realm'),
        ),
        migrations.CreateModel(
            name='OpenIdConnectProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('expires_before', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('refresh_expires_before', models.DateTimeField(null=True)),
                ('sub', models.CharField(max_length=255, unique=True)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openid_profiles', to='django_keycloak.realm')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='oidc_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'swappable': 'KEYCLOAK_OIDC_PROFILE_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='django_keycloak.client')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.permission')),
            ],
            options={
                'unique_together': {('client', 'permission')},
            },
        ),
        migrations.CreateModel(
            name='ExchangedToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('expires_before', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('refresh_expires_before', models.DateTimeField(null=True)),
                ('oidc_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.KEYCLOAK_OIDC_PROFILE_MODEL)),
                ('remote_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanged_tokens', to='django_keycloak.remoteclient')),
            ],
            options={
                'unique_together': {('oidc_profile', 'remote_client')},
            },
        ),
    ]
