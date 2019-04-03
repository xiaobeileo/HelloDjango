from django.db import models

# Create your models here.
class User(models.Model):
    gender = (('male', 'M'), ('female', 'F'),)

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='M')
    c_time = models.DateTimeField(auto_now_add=True)

    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]
        verbose_name = 'User'
        verbose_name_plural = 'User'

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + " :   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "ConfirmCode"
        verbose_name_plural = "ConfirmCode"