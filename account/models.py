from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, atype, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not atype:
            raise ValueError("Users must have an account type")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            atype=atype,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, atype, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            atype=atype,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    class AccountType(models.TextChoices):
        DOCTOR = 'Doctor'
        PATIENT = 'Patient'

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    atype = models.CharField(
        max_length=50, choices=AccountType.choices, default=AccountType.DOCTOR)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'atype']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(pre_save, sender=Account, dispatch_uid='active')
def active(sender, instance, **kwargs):
    if instance.is_active and Account.objects.filter(pk=instance.pk, is_active=False).exists():
        subject = 'Active account'
        mesagge = '%s your account is now active' % (instance.username)
        from_email = 'admin@medwise.in'
        send_mail(subject, mesagge, from_email, [
                  instance.email], fail_silently=False)


@receiver(pre_save, sender=Account, dispatch_uid='notactive')
def notactive(sender, instance, **kwargs):
    if instance.atype == 'Doctor' and instance.is_active == False:
        subject = 'Your application to medwise.in'
        mesagge = 'Dear Doctor %s\nThis is to double-check that you have applied as a volunteer doctor at medwise.in. Please confirm by replying to this and also give your specialization area\nRegards\nRishab Koul admin medwise' % (
            instance.username)
        from_email = 'admin@medwise.in'
        send_mail(subject, mesagge, from_email, [
            instance.email], fail_silently=False)


@receiver(pre_save, sender=Account, dispatch_uid='newdoctorcame')
def newdoctorcame(sender, instance, **kwargs):
    if instance.atype == 'Doctor' and instance.is_active == False:
        subject = 'New Doctor Arrived'
        mesagge = '%s wants to join the app Email - %s' % (
            instance.username, instance.email)
        from_email = 'admin@medwise.in'
        send_mail(subject, mesagge, from_email, [
            settings.EMAIL_HOST_USER], fail_silently=False)
