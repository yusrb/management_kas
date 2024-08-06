from django.urls import reverse_lazy
from typing import Any
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .models import Transaksi
from django.db import models
from .forms import FormTransaksi

class DaftarTransaksiView(LoginRequiredMixin, ListView):
    model = Transaksi
    template_name = 'base/daftar_transaksi.html'
    context_object_name = 'daftar_transaksi'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='user').exists():
            queryset = queryset.filter(pengguna=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["judul"] = "Daftar Transaksi"
        total_pemasukan = self.get_queryset().filter(tipe_transaksi='Pemasukan').aggregate(total=models.Sum('jumlah'))['total'] or 0
        total_pengeluaran = self.get_queryset().filter(tipe_transaksi='Pengeluaran').aggregate(total=models.Sum('jumlah'))['total'] or 0
        saldo = total_pemasukan - total_pengeluaran

        context['total_pemasukan'] = total_pemasukan
        context['total_pengeluaran'] = total_pengeluaran
        context['saldo'] = saldo

        return context

class TambahTransaksiView(LoginRequiredMixin, CreateView):
    model = Transaksi
    form_class = FormTransaksi
    template_name = 'base/form_transaksi.html'
    success_url = reverse_lazy('transaksi:daftar')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["judul"] = "Tambah Transaksi"
        return context
    

    def form_valid(self, form):
        print("Form adalah valid") 
        form.instance.pengguna = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Transaksi berhasil ditambahkan!')
        return response
    
    def form_invalid(self, form):
        print("Form adalah invalid")  
        print(form.errors)
        messages.error(self.request, 'Ada kesalahan dalam form.')
        return super().form_invalid(form)

class UbahTransaksiView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Transaksi
    form_class = FormTransaksi
    template_name = 'base/form_transaksi.html'
    permission_required = 'transaksi.change_transaksi'
    success_url = reverse_lazy('transaksi:daftar')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["judul"] = "Ubah Transaksi"
        return context
    

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Transaksi berhasil diperbarui!')
        return response

class HapusTransaksiView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Transaksi
    template_name = 'base/hapus_transaksi.html'
    success_url = reverse_lazy('transaksi:daftar')
    permission_required = 'transaksi.delete_transaksi'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["judul"] = "Confirm Delete"
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Transaksi berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

class FilterTransaksiView(LoginRequiredMixin, TemplateView):
    template_name = 'base/filter_transaksi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["judul"] = "Filter Transaksi"
        tanggal_awal = self.request.GET.get('tanggal_awal')
        tanggal_akhir = self.request.GET.get('tanggal_akhir')
        tipe_transaksi = self.request.GET.get('tipe_transaksi') 
        transaksi_queryset = Transaksi.objects.all()

        if tanggal_awal and tanggal_akhir:
            transaksi_queryset = transaksi_queryset.filter(tanggal__range=[tanggal_awal, tanggal_akhir])
        if tipe_transaksi:
            transaksi_queryset = transaksi_queryset.filter(tipe_transaksi=tipe_transaksi)
        if self.request.user.groups.filter(name='user').exists():
            transaksi_queryset = transaksi_queryset.filter(pengguna=self.request.user)

        total_pemasukan = transaksi_queryset.filter(tipe_transaksi='Pemasukan').aggregate(total=models.Sum('jumlah'))['total'] or 0
        total_pengeluaran = transaksi_queryset.filter(tipe_transaksi='Pengeluaran').aggregate(total=models.Sum('jumlah'))['total'] or 0
        saldo = total_pemasukan - total_pengeluaran

        context['daftar_transaksi'] = transaksi_queryset
        context['total_pemasukan'] = total_pemasukan
        context['total_pengeluaran'] = total_pengeluaran
        context['saldo'] = saldo

        return context