from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    nama_lengkap = models.CharField(max_length=100)
    jurusan = models.ForeignKey('core.Jurusan', on_delete=models.SET_NULL, null=True, blank=True)
    kelas = models.ForeignKey('core.Kelas', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username