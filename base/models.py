from django.db import models
from django.contrib.auth.models import User

class Transaksi(models.Model):
    TIPE_TRANSAKSI_CHOICES = [
        ('Pemasukan', 'Pemasukan'),
        ('Pengeluaran', 'Pengeluaran'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal = models.DateField()
    tipe_transaksi = models.CharField(max_length=50, choices=TIPE_TRANSAKSI_CHOICES)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tanggal} - {self.tipe_transaksi} - {self.jumlah}"
