"""Bots app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TelegramBot

class BotListView(LoginRequiredMixin, ListView):
    model = TelegramBot
    template_name = 'bots/list.html'
    context_object_name = 'bots'
    paginate_by = 20

class BotCreateView(LoginRequiredMixin, CreateView):
    model = TelegramBot
    template_name = 'bots/form.html'
    fields = ['username', 'token', 'is_active']
    success_url = reverse_lazy('bots:list')

    def form_valid(self, form):
        messages.success(self.request, 'Bot added successfully!')
        return super().form_valid(form)

class BotUpdateView(LoginRequiredMixin, UpdateView):
    model = TelegramBot
    template_name = 'bots/form.html'
    fields = ['username', 'token', 'is_active']
    success_url = reverse_lazy('bots:list')

    def form_valid(self, form):
        messages.success(self.request, 'Bot updated successfully!')
        return super().form_valid(form)

class BotDeleteView(LoginRequiredMixin, DeleteView):
    model = TelegramBot
    template_name = 'bots/confirm_delete.html'
    success_url = reverse_lazy('bots:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Bot deleted successfully!')
        return super().delete(request, *args, **kwargs)
