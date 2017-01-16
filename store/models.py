from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=600)

    def __str__(self):
        return self.name


class Staff(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    photo = ProcessedImageField(upload_to='staff_photo',
                                processors=[ResizeToFill(200, 120)],
                                format='PNG',
                                options={'quality': 90}
                                )

    def __str__(self):
        return self.name


class Comment(models.Model):
    user_id = models.IntegerField(default=-1)
    staff = models.ForeignKey(Staff)
    text = models.TextField(max_length=800)
    time_added = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text[:50]


class Order(models.Model):
    user_id = models.IntegerField(default=-1)
    item = models.ForeignKey(Staff)
    status = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return "Order#" + str(self.id) + " processed:" + self.order_status()

    def order_status(self):
        if self.status:
            return "yes"
        else:
            return "no"
