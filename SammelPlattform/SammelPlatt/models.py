from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# -----------------------------
# Custom Nutzer Manager
# -----------------------------
class NutzerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashed password wird in 'Passwort' gespeichert
        user.save(using=self._db)
        return user


# -----------------------------
# Custom Nutzer Model
# -----------------------------
class Nutzer(AbstractBaseUser):
    nutzerid = models.AutoField(db_column='NutzerID', primary_key=True)
    email = models.EmailField(db_column='Email', unique=True, max_length=30)
    password = models.CharField(db_column='Passwort', max_length=128)

    last_login = None  # entfernt das Feld aus AbstractBaseUser

    eingeloggt = models.BooleanField(db_column='Eingeloggt', default=False)
    gesperrt = models.BooleanField(db_column='Gesperrt', default=False)

    @property
    def is_active(self):
        return not self.gesperrt

    @is_active.setter
    def is_active(self, value):
        self.gesperrt = not value

    objects = NutzerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'nutzer'

# -----------------------------
# Bewertung
# -----------------------------
class Bewertung(models.Model):
    sternezahl = models.IntegerField(db_column='sterneZahl')
    bewertungid = models.AutoField(db_column='BewertungID', primary_key=True)
    titel = models.CharField(db_column='Titel', max_length=25)
    beschreibung = models.CharField(db_column='Beschreibung', max_length=60, blank=True, null=True)
    nutzerid = models.ForeignKey('Nutzer', models.DO_NOTHING, db_column='NutzerID')
    fotoid = models.ForeignKey('Foto', models.DO_NOTHING, db_column='FotoID')

    class Meta:
        db_table = 'bewertung'


# -----------------------------
# Foto
# -----------------------------
from django.utils.timezone import now

class Foto(models.Model):
    beschreibung = models.CharField(db_column='Beschreibung', max_length=60, blank=True, null=True)
    kategorieid = models.ForeignKey('Kategorie', models.DO_NOTHING, db_column='KategorieID')
    fotoid = models.AutoField(db_column='FotoID', primary_key=True)
    hochladedatum = models.DateField(db_column='HochladeDatum', default=now)
    gesamtbewertung = models.FloatField(db_column='Gesamtbewertung', default=0.0)
    ordid = models.ForeignKey('Ordner', models.DO_NOTHING, db_column='OrdID')
    foto = models.ImageField(upload_to='uploads/')

    class Meta:
        db_table = 'foto'

# -----------------------------
# Kategorie
# -----------------------------
class Kategorie(models.Model):
    kategorieid = models.AutoField(db_column='KategorieID', primary_key=True)
    name = models.CharField(db_column='Name', unique=True, max_length=45)

    class Meta:
        db_table = 'kategorie'


# -----------------------------
# Ordner
# -----------------------------
class Ordner(models.Model):
    ordid = models.AutoField(db_column='OrdID', primary_key=True)
    titel = models.CharField(unique=True, max_length=45)
    pfad = models.CharField(max_length=45)
    inordner = models.ForeignKey('self', models.DO_NOTHING, db_column='inOrdner', blank=True, null=True)
    slug = models.SlugField(max_length=60, blank=True)

    class Meta:
        db_table = 'ordner'
        unique_together = ('slug', 'inordner')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titel)
        super().save(*args, **kwargs)

    def get_full_slug_path(self):
        parts = []
        current = self
        while current:
            parts.insert(0, current.slug)
            current = current.inordner
        return '/'.join(parts)

    @classmethod
    def get_by_slug_path(cls, slug_path):
        slugs = slug_path.strip('/').split('/')
        current = None
        for slug in slugs:
            try:
                current = cls.objects.get(slug=slug, inordner=current)
            except cls.DoesNotExist:
                return None
        return current

    def __str__(self):
        return self.get_full_slug_path()