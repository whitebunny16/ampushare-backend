from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.speciality}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    remark = models.TextField()

    def __str__(self):
        return self.remark


class Payment(models.Model):
    PAYMENT_FAILED_STATUS = 'F'
    PAYMENT_SUCCESS_STATUS = 'S'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_FAILED_STATUS, 'Failed'),
        (PAYMENT_SUCCESS_STATUS, 'Success')
    ]

    PAYMENT_KHALTI = 'K'
    PAYMENT_ESEWA = 'E'

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_KHALTI, 'Khalti'),
        (PAYMENT_ESEWA, 'Esewa')
    ]

    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES)
