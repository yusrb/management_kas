from django.urls import path
from .views import DaftarTransaksiView, TambahTransaksiView, HapusTransaksiView, UbahTransaksiView, FilterTransaksiView

app_name = 'transaksi'

urlpatterns = [
    path('', DaftarTransaksiView.as_view(), name='daftar'),
    path('tambah/', TambahTransaksiView.as_view(), name='tambah'),
    path('<int:pk>/ubah/', UbahTransaksiView.as_view(), name='ubah'),
    path('<int:pk>/hapus/', HapusTransaksiView.as_view(), name='hapus'),
    path('filter/', FilterTransaksiView.as_view(), name='filter'),
]
