from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Jurusan(models.Model):
    kode_jurusan = models.CharField(max_length=10, unique=True)
    nama_jurusan = models.CharField(max_length=100)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_jurusan

class Kelas(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    nama_kelas = models.CharField(max_length=50)
    tingkat = models.IntegerField()
    wali_kelas = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'guru'},related_name='kelas_diampu')

    def __str__(self):
        return f"{self.nama_kelas} - {self.jurusan.nama_jurusan}"

class TahunAjaran(models.Model):
    tahun_ajaran = models.CharField(max_length=9)
    semester = models.CharField(max_length=5)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tahun_ajaran} - {self.semester}"

class Siswa(models.Model):
    nis = models.CharField(max_length=20, unique=True)
    nama_lengkap = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=10)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    alamat = models.TextField()
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun_masuk = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='siswa/', blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nis} - {self.nama_lengkap}"

class JenisAbsensi(models.Model):
    kode_absensi = models.CharField(max_length=10)
    nama_absensi = models.CharField(max_length=50)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_absensi

class Absensi(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jenis_absensi = models.ForeignKey(JenisAbsensi, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    keterangan = models.TextField(blank=True)
    dibuat_oleh = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.siswa} - {self.jenis_absensi}"

class JenisPelanggaran(models.Model):
    kode_pelanggaran = models.CharField(max_length=10)
    nama_pelanggaran = models.CharField(max_length=100)
    poin = models.IntegerField()
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nama_pelanggaran} ({self.poin} poin)"

class Pelanggaran(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jenis_pelanggaran = models.ForeignKey(JenisPelanggaran, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    keterangan = models.TextField(blank=True)
    dibuat_oleh = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.siswa} - {self.jenis_pelanggaran}"