from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django.db.models import Count, Sum
from django.http import JsonResponse

from .models import Jurusan, Kelas, TahunAjaran, JenisAbsensi, JenisPelanggaran, Siswa, Absensi, Pelanggaran
from .tables import SiswaTable
from .filters import AbsensiFilter

def home(request):
    return render(request, 'core/home.html', {'title': 'Beranda'})

def admin_check(user):
    return user.role == 'admin'

@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    return render(request, 'core/admin/dashboard.html')

# Jurusan Views
class JurusanListView(ListView):
    model = Jurusan
    template_name = 'core/admin/master/jurusan_list.html'
    context_object_name = 'jurusan_list'

class JurusanCreateView(CreateView):
    model = Jurusan
    fields = '__all__'
    template_name = 'core/admin/master/jurusan_form.html'
    success_url = reverse_lazy('jurusan-list')

class JurusanUpdateView(UpdateView):
    model = Jurusan
    fields = '__all__'
    template_name = 'core/admin/master/jurusan_form.html'
    success_url = reverse_lazy('jurusan-list')

class JurusanDeleteView(DeleteView):
    model = Jurusan
    template_name = 'core/admin/master/jurusan_confirm_delete.html'
    success_url = reverse_lazy('jurusan-list')

# Siswa Views
class SiswaListView(SingleTableView):
    model = Siswa
    table_class = SiswaTable
    template_name = 'core/admin/siswa/siswa_list.html'

class SiswaCreateView(CreateView):
    model = Siswa
    fields = '__all__'
    template_name = 'core/admin/siswa/siswa_form.html'
    success_url = reverse_lazy('siswa-list')

class SiswaUpdateView(UpdateView):
    model = Siswa
    fields = '__all__'
    template_name = 'core/admin/siswa/siswa_form.html'
    success_url = reverse_lazy('siswa-list')

class SiswaDeleteView(DeleteView):
    model = Siswa
    template_name = 'core/admin/siswa/siswa_confirm_delete.html'
    success_url = reverse_lazy('siswa-list')

# Absensi Views
class AbsensiListView(FilterView):
    model = Absensi
    filterset_class = AbsensiFilter
    template_name = 'core/admin/absensi/absensi_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('siswa', 'jenis_absensi', 'dibuat_oleh')

class AbsensiCreateView(CreateView):
    model = Absensi
    fields = '__all__'
    template_name = 'core/admin/absensi/absensi_form.html'
    success_url = reverse_lazy('absensi-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['siswa'].queryset = Siswa.objects.filter(status=True)
        form.fields['dibuat_oleh'].initial = self.request.user
        form.fields['dibuat_oleh'].disabled = True
        return form

class AbsensiUpdateView(UpdateView):
    model = Absensi
    fields = '__all__'
    template_name = 'core/admin/absensi/absensi_form.html'
    success_url = reverse_lazy('absensi-list')

# Rekap dan Kenaikan Kelas
def rekap_absensi(request):
    jurusan_id = request.GET.get('jurusan')
    kelas_id = request.GET.get('kelas')
    
    queryset = Siswa.objects.filter(status=True)
    
    if jurusan_id:
        queryset = queryset.filter(jurusan_id=jurusan_id)
    if kelas_id:
        queryset = queryset.filter(kelas_id=kelas_id)
    
    siswa_list = []
    for siswa in queryset:
        absensi = Absensi.objects.filter(siswa=siswa)
        pelanggaran = Pelanggaran.objects.filter(siswa=siswa)
        
        siswa_list.append({
            'siswa': siswa,
            'total_hadir': absensi.filter(jenis_absensi__nama_absensi='Hadir').count(),
            'total_sakit': absensi.filter(jenis_absensi__nama_absensi='Sakit').count(),
            'total_izin': absensi.filter(jenis_absensi__nama_absensi='Izin').count(),
            'total_alpha': absensi.filter(jenis_absensi__nama_absensi='Alpha').count(),
            'total_pelanggaran': pelanggaran.count(),
            'total_poin': pelanggaran.aggregate(Sum('jenis_pelanggaran__poin'))['jenis_pelanggaran__poin__sum'] or 0
        })
    
    context = {
        'siswa_list': siswa_list,
        'jurusan_list': Jurusan.objects.all(),
        'selected_jurusan': int(jurusan_id) if jurusan_id else None,
        'kelas_list': Kelas.objects.filter(jurusan_id=jurusan_id) if jurusan_id else Kelas.objects.none(),
        'selected_kelas': int(kelas_id) if kelas_id else None
    }
    
    return render(request, 'core/admin/rekap/absensi.html', context)

def kenaikan_kelas(request):
    if request.method == 'POST':
        siswa_ids = request.POST.getlist('siswa_ids')
        tingkat_tujuan = request.POST.get('tingkat_tujuan')
        
        # Logika untuk memindahkan siswa ke kelas yang sesuai di tingkat tujuan
        # ...
        
        return JsonResponse({'status': 'success'})
    
    jurusan_id = request.GET.get('jurusan')
    kelas_id = request.GET.get('kelas')
    
    queryset = Siswa.objects.filter(status=True)
    
    if jurusan_id:
        queryset = queryset.filter(jurusan_id=jurusan_id)
    if kelas_id:
        queryset = queryset.filter(kelas_id=kelas_id)
        kelas = Kelas.objects.get(id=kelas_id)
    else:
        kelas = None
    
    context = {
        'siswa_list': queryset,
        'jurusan_list': Jurusan.objects.all(),
        'selected_jurusan': int(jurusan_id) if jurusan_id else None,
        'kelas_list': Kelas.objects.filter(jurusan_id=jurusan_id) if jurusan_id else Kelas.objects.none(),
        'selected_kelas': int(kelas_id) if kelas_id else None
    }
    
    return render(request, 'core/admin/kenaikan/kenaikan_kelas.html', context)


from django.views.generic import CreateView
from .models import Pelanggaran
from django.urls import reverse_lazy

class PelanggaranCreateView(CreateView):
    model = Pelanggaran
    fields = ['nama', 'poin', 'kategori']  # ganti sesuai field model kamu
    template_name = 'core/admin/pelangaran/pelanggaran_form.html'
    success_url = reverse_lazy('pelanggaran-list')


class PelanggaranListView(ListView):
    model = Pelanggaran
    template_name = 'core/admin/pelanggaran/pelanggaran_list.html'
    context_object_name = 'pelanggaran_list'

class PelanggaranUpdateView(UpdateView):
    model = Pelanggaran
    fields = ['nama', 'poin', 'kategori']
    template_name = 'core/admin/pelanggaran/pelanggaran_form.html'
    success_url = reverse_lazy('pelanggaran-list')
