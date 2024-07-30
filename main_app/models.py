from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
BEHAVIORS = (
    ('S', 'Skating'),
    ('L', 'Lewd'),
    ('O', 'Offensive')
)

class Trick(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trick-detail', kwargs={'pk': self.id})

class Skater(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    tricks = models.ManyToManyField(Trick)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # Define a method to get the URL for this particular cat instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('skater-detail', kwargs={'skater_id': self.id})

class Behavior(models.Model):
    date = models.DateField('Behavior Date')
    behavior = models.CharField(
        max_length=1,
        choices=BEHAVIORS,
        default=BEHAVIORS[0][0]
    )
    skater = models.ForeignKey(Skater, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_behavior_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']

