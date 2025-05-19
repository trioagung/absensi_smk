from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users.views import login_view, tambah_user
from .views import (
    JurusanListView, JurusanCreateView, JurusanUpdateView, JurusanDeleteView,
    SiswaListView, SiswaCreateView, SiswaUpdateView, SiswaDeleteView,
    AbsensiListView, AbsensiCreateView, AbsensiUpdateView,
    PelanggaranListView, PelanggaranCreateView, PelanggaranUpdateView,
)

urlpatterns = [
    path('', views.home, name='home'),

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Master Data URLs
    path('admin/master/jurusan/', JurusanListView.as_view(), name='jurusan-list'),
    path('admin/master/jurusan/tambah/', JurusanCreateView.as_view(), name='jurusan-create'),
    path('admin/master/jurusan/<int:pk>/edit/', JurusanUpdateView.as_view(), name='jurusan-update'),
    path('admin/master/jurusan/<int:pk>/hapus/', JurusanDeleteView.as_view(), name='jurusan-delete'),

    # Data Siswa URLs
    path('admin/siswa/', SiswaListView.as_view(), name='siswa-list'),
    path('admin/siswa/tambah/', SiswaCreateView.as_view(), name='siswa-create'),
    path('admin/siswa/<int:pk>/edit/', SiswaUpdateView.as_view(), name='siswa-update'),
    path('admin/siswa/<int:pk>/hapus/', SiswaDeleteView.as_view(), name='siswa-delete'),

    # Absensi URLs
    path('admin/absensi/', AbsensiListView.as_view(), name='absensi-list'),
    path('admin/absensi/tambah/', AbsensiCreateView.as_view(), name='absensi-create'),
    path('admin/absensi/<int:pk>/edit/', AbsensiUpdateView.as_view(), name='absensi-update'),

    # Pelanggaran URLs
    path('admin/pelanggaran/', PelanggaranListView.as_view(), name='pelanggaran-list'),
    path('admin/pelanggaran/tambah/', PelanggaranCreateView.as_view(), name='pelanggaran-create'),
    path('admin/pelanggaran/<int:pk>/edit/', PelanggaranUpdateView.as_view(), name='pelanggaran-update'),

    # Rekap URLs
    path('admin/rekap/absensi/', views.rekap_absensi, name='rekap-absensi'),

    # Setting URLs
    path('admin/setting/kenaikan-kelas/', views.kenaikan_kelas, name='kenaikan-kelas'),

    # login
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Tambah User
    path('admin/user/tambah/', tambah_user, name='tambah_user'),
]