from django import forms
from .models import Transaksi

class FormTransaksi(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'tipe_transaksi', 'jumlah', 'deskripsi']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'tipe_transaksi': forms.Select(choices=Transaksi.TIPE_TRANSAKSI_CHOICES),
        }