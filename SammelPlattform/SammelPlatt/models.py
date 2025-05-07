# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bewertung(models.Model):
    sternezahl = models.IntegerField(db_column='sterneZahl')  # Field name made lowercase.
    bewertungid = models.AutoField(db_column='BewertungID', primary_key=True)  # Field name made lowercase.
    titel = models.CharField(db_column='Titel', max_length=25)  # Field name made lowercase.
    beschreibung = models.CharField(db_column='Beschreibung', max_length=60, blank=True, null=True)  # Field name made lowercase.
    nutzerid = models.ForeignKey('Nutzer', models.DO_NOTHING, db_column='NutzerID')  # Field name made lowercase.
    fotoid = models.ForeignKey('Foto', models.DO_NOTHING, db_column='FotoID')  # Field name made lowercase.

    class Meta:
        db_table = 'bewertung'


class Foto(models.Model):
    beschreibung = models.CharField(db_column='Beschreibung', max_length=60, blank=True, null=True)  # Field name made lowercase.
    kategorieid = models.ForeignKey('Kategorie', models.DO_NOTHING, db_column='KategorieID')  # Field name made lowercase.
    fotoid = models.AutoField(db_column='FotoID', primary_key=True)  # Field name made lowercase.
    hochladedatum = models.DateField(db_column='HochladeDatum', blank=True, null=True)  # Field name made lowercase.
    gesamtbewertung = models.FloatField(db_column='Gesamtbewertung')  # Field name made lowercase.
    ordid = models.ForeignKey('Ordner', models.DO_NOTHING, db_column='OrdID')  # Field name made lowercase.
    foto = models.TextField(db_column='Foto')  # Field name made lowercase.

    class Meta:
        db_table = 'foto'


class Kategorie(models.Model):
    kategorieid = models.AutoField(db_column='KategorieID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        db_table = 'kategorie'


class Nutzer(models.Model):
    email = models.CharField(db_column='Email', unique=True, max_length=30)  # Field name made lowercase.
    passwort = models.CharField(db_column='Passwort', max_length=45)  # Field name made lowercase.
    eingeloggt = models.IntegerField(db_column='Eingeloggt')  # Field name made lowercase.
    gesperrt = models.IntegerField(db_column='Gesperrt')  # Field name made lowercase.
    nutzerid = models.AutoField(db_column='NutzerID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'nutzer'


class Ordner(models.Model):
    ordid = models.AutoField(db_column='OrdID', primary_key=True)  # Field name made lowercase.
    titel = models.CharField(unique=True, max_length=45)
    pfad = models.CharField(max_length=45)
    inordner = models.ForeignKey('self', models.DO_NOTHING, db_column='inOrdner', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'ordner'
