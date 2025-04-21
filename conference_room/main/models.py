from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'room_id')

    def __str__(self):
        return f"{self.room.name} - {self.date}"