import django_filters
from .models import Absensi

class AbsensiFilter(django_filters.FilterSet):
    # Filter range tanggal, dari - sampai
    tanggal = django_filters.DateFromToRangeFilter()
    
    # Filter nama siswa dengan pencarian case-insensitive contains
    siswa__nama_lengkap = django_filters.CharFilter(field_name='siswa__nama_lengkap', lookup_expr='icontains')
    
    # Jika siswa__kelas adalah ForeignKey, bisa pakai ModelChoiceFilter (optional)
    # siswa__kelas = django_filters.ModelChoiceFilter(field_name='siswa__kelas', queryset=Kelas.objects.all())
    
    class Meta:
        model = Absensi
        fields = ['jenis_absensi', 'tanggal', 'siswa__kelas', 'siswa__nama_lengkap']
