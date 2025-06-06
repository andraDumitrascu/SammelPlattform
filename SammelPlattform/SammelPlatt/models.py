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
class Foto(models.Model):
    beschreibung = models.CharField(db_column='Beschreibung', max_length=60, blank=True, null=True)
    kategorieid = models.ForeignKey(
    'Kategorie',
    on_delete=models.SET_NULL,
    db_column='KategorieID',
    null=True,
    blank=True
)
    fotoid = models.AutoField(db_column='FotoID', primary_key=True)
    hochladedatum = models.DateField(db_column='HochladeDatum', blank=True, null=True)
    gesamtbewertung = models.FloatField(db_column='Gesamtbewertung')
    ordid = models.ForeignKey('Ordner', models.DO_NOTHING, db_column='OrdID')
    foto = models.ImageField(upload_to='uploads/')
    def is_image(self):
        return self.foto.url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))

    def is_video(self):
        return self.foto.url.lower().endswith(('.mp4', '.mov', '.avi'))

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
    slug = models.SlugField(unique=True, max_length=60, blank=True)

    class Meta:
        db_table = 'ordner'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titel)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titel
