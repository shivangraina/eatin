from django.db import models
from base.models import Item, Person
# Create your models here.

# DESCRIPTION -> models related to the Vendors


class Vendor(models.Model):
    objects = models.Manager()

    person_info = models.OneToOneField(Person, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    rating = models.IntegerField(null=True)
    categories = models.TextField(null=True)

    def get_vendor_name(self):
        return self.person_info.getPersonName()

    def get_coords(self):
        return self.person_info.getCoords()


# DESCRIPTION -> Menu for a particular time added by the vendor
class Menu(models.Model):
    objects = models.Manager()

    MENU_TYPE = [
        ('1', 'full'),
        ('2', 'half'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)
    time_stamp = models.DateField(auto_created=True, auto_now_add=True)
    type = models.CharField(max_length=1, choices=MENU_TYPE)
    rating = models.IntegerField(null=True)


'''
DESCRIPTION -> Related to base Item class so we can fetch name of that base Item, also relates to Menu which will
contain items added by vendor
'''


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} - {}".format(self.item_name.item_name, self.quantity)
