from django.db import models


class Patient(models.Model):
    patient_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    address = models.TextField(default='')
    symptoms = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    bed = models.ForeignKey(
    'HospitalBed',
      on_delete=models.SET_NULL,
      null=True,
      blank=True
    )
    is_discharged = models.BooleanField(default=False)

    def __str__(self):
        return self.patient_name

class HospitalBed(models.Model):
    bed_number = models.CharField(max_length=20, unique=True)
    ward_name = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"{self.bed_number} - {status}"    