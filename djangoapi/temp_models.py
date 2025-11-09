# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class Agencies(models.Model):
    nombre = models.CharField(unique=True, max_length=150)
    long_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agencies'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cities(models.Model):
    pk = models.CompositePrimaryKey('country', 'city')
    country = models.ForeignKey('Countries', models.DO_NOTHING, db_column='country')
    city = models.CharField(max_length=100)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'
        unique_together = (('country', 'city'),)


class CitiesTmp(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities_tmp'


class Countries(models.Model):
    country = models.CharField(primary_key=True, max_length=100)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class CountriesTmp(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries_tmp'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Events(models.Model):
    date = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    agency = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.CharField(max_length=100, blank=True, null=True)
    country_e = models.ForeignKey(Cities, models.DO_NOTHING, db_column='country_e')
    city_e = models.CharField(max_length=100)
    event_title = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'events'


class EventsAgencies(models.Model):
    pk = models.CompositePrimaryKey('id_event', 'id_agencia')
    id_event = models.ForeignKey(Events, models.DO_NOTHING, db_column='id_event')
    id_agencia = models.ForeignKey(Agencies, models.DO_NOTHING, db_column='id_agencia')

    class Meta:
        managed = False
        db_table = 'events_agencies'
        unique_together = (('id_event', 'id_agencia'),)


class PresentationSpeakers(models.Model):
    pk = models.CompositePrimaryKey('id_presentation', 'id_speaker')
    id_presentation = models.ForeignKey('Presentations', models.DO_NOTHING, db_column='id_presentation')
    id_speaker = models.ForeignKey('Speakers', models.DO_NOTHING, db_column='id_speaker')

    class Meta:
        managed = False
        db_table = 'presentation_speakers'
        unique_together = (('id_presentation', 'id_speaker'),)


class Presentations(models.Model):
    title = models.TextField()
    event_title = models.ForeignKey(Events, models.DO_NOTHING, db_column='event_title', to_field='event_title')
    language = models.CharField(max_length=50, blank=True, null=True)
    url_document = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'presentations'


class Speakers(models.Model):
    name = models.CharField(max_length=200)
    country_s = models.ForeignKey(Countries, models.DO_NOTHING, db_column='country_s')
    agency_s = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'speakers'
