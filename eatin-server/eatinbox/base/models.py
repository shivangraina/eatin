from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# User = get_user_model()

# Create your models here.

'''DESCRIPTION - This model is for storing the Base Classes which will be either related or Inherited in
other classes'''

'''
PURPOSE -> Store all the items that will be added by all the different vendors
Now whatever items we are adding, we will associate them with different vendors so we have used ManyToMany
eg. Bendi Item should have same name in database and should have multiple vendors associated with it

PROBLEMS -> cases with items like roti will have large number of vendor ids assciated with it and should be general

FUTURE CHANGES -> have to handle general items case
'''


class Item(models.Model):
    item_name = models.CharField(max_length=50)
    vendor = models.ManyToManyField("vendors.vendor")  # ?? unnecessary complexity??


''' 
PURPOSE -> Base model for Customers, Vendors, Partners oneToOne with User

PROBLEMS -> accessing user data from vendors etc has uneccesary extra calls all User fields should be 
present in Person and Not some other model

FUTURE CHANGES -> Should Convert Person model into single User model
'''


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, default=18.453626)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, default=73.8508222)
    contact = models.CharField(max_length=10, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.getPersonName()

    def getPersonName(self):
        return self.user.first_name

    def getCoords(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


class UserManager(BaseUserManager):
    def create_user(self, email,
                    password=None,
                    is_superuser=False,
                    is_staff=False,
                    first_name=None,
                    is_active=True,
                    is_vendor=False,
                    is_customer=False,
                    is_partner=False,
                    is_user=None,
                    ):
        if not email:
            raise ValueError("User must provide Email")
        if not password:
            raise ValueError("User must provide a password")
        if not is_user:
            raise ValueError("is_user is required")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            # last_name=last_name,
        )

        user_obj.set_password(password)
        user_obj.admin = is_superuser
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.customer = is_customer
        user_obj.vendor = is_vendor
        user_obj.partner = is_partner

        '''logic for making appropriate flag true'''
        setattr(user_obj,
                is_user,
                True
                )

        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            is_superuser=True,
            is_staff=True,
            password=password,
            is_active=True,
            is_vendor=True,
            is_customer=True,
            is_partner=True,
            is_user="admin")

        return user

    # def create_vendor(self, email, password=None, first_name=None, last_name=None):
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         first_name=first_name,
    #         # last_name=last_name,
    #         is_active=True,
    #         is_vendor=True,
    #         is_customer=False,
    #         is_partner=False,
    #     )
    #
    #     return user
    #
    # def create_customer(self, email, password=None, first_name=None, last_name=None):
    #     user = self.create(
    #         email,
    #         password=password,
    #         first_name=first_name,
    #         last_name=last_name,
    #         is_active=True,
    #         is_vendor=False,
    #         is_customer=True,
    #         is_partner=False,
    #     )
    #
    #     return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    vendor = models.BooleanField(default=False)
    customer = models.BooleanField(default=True)
    partner = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj=None):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_vendor(self):
        return self.vendor

    @property
    def is_customer(self):
        return self.customer

    @property
    def is_partner(self):
        return self.partner
