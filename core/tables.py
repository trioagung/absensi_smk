import django_tables2 as tables
from .models import Siswa

class SiswaTable(tables.Table):
    action = tables.TemplateColumn(
        template_name='core/admin/siswa/action_buttons.html',
        orderable=False
    )
    
    class Meta:
        model = Siswa
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nis', 'nama_lengkap', 'jenis_kelamin', 'kelas', 'status')