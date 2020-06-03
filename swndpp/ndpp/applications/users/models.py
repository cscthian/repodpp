# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):

        user = self.model(
            username=username,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    TYPE_CHOICES = (
            ('1', 'Almacen'),
            ('2', 'Caja'),
            ('5', 'Contabilidad'),
            ('3', 'adminitrativo'),
            ('4', 'Administrador'),
    )
    username = models.CharField('username', max_length=15, unique=True)
    type_user = models.CharField('tipo de usuario', max_length=2, choices=TYPE_CHOICES, null=True, blank=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
         swappable = 'AUTH_USER_MODEL'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
