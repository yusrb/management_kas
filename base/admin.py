from django.contrib import admin
from .models import Transaksi

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'tipe_transaksi', 'jumlah', 'deskripsi')
    list_filter = ('tipe_transaksi', 'tanggal')
    search_fields = ('deskripsi',)
    date_hierarchy = 'tanggal'
