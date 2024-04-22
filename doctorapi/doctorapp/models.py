from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='slots', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.start_time} to {self.end_time} ({self.doctor})"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='appointments', on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, related_name='appointments', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_contact = models.CharField(max_length=100)
    appointment_date = models.DateField()

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.appointment_date}"