from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from location_field.models.plain import PlainLocationField


SCORE = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
DD = ((1, "Simplified_DD"), (2, "Standard_DD"), (3, "Enhanced_DD"))


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    provider = models.ForeignKey('Provider', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_child_variants = models.BooleanField(default=False, null=True,
                                             blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    '''This class defines the review model'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="reviews")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    title = models.CharField(max_length=254)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    single_rating = models.IntegerField(choices=SCORE)
    verified_purchase = models.BooleanField(default=False)

    class Meta:
        '''Meta class defining the order of retrieved reviews'''
        ordering = ["created_on"]

    def __str__(self):
        '''Returns a string which facilitates a concise approach'''
        return f"Review ID {self.id} review-body {self.body}"\
               f" rated {self.single_rating} by {self.name}"


class Provider(models.Model):
    '''This class defines the provider model'''
    point_of_contact = models.CharField(max_length=50, null=False,
                                        blank=False)
    business_name = models.CharField(max_length=50)
    risk_lev = models.IntegerField(choices=DD)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'],
                                  zoom=5,
                                  default='40.015585972319,18.24176788330078')
    ship_abroad = models.BooleanField(default=False)
    slr_rating = models.IntegerField(choices=SCORE)

    class Meta:
        '''Meta class defining the order of retrieved providers'''
        ordering = ["-slr_rating"]

    def __str__(self):
        '''Returns a string which facilitates a concise approach'''
        return f"Provider {self.business_name} from {self.city}"
