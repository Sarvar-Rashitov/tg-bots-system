"""Users app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BotUser
from downloads.models import DownloadHistory

class UserListView(LoginRequiredMixin, ListView):
    model = BotUser
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by ban status
        ban_filter = self.request.GET.get('ban')
        if ban_filter == 'banned':
            queryset = queryset.filter(is_banned=True)
        elif ban_filter == 'active':
            queryset = queryset.filter(is_banned=False)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(telegram_id__icontains=search)
            )

        return queryset.order_by('-joined_at')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = BotUser
    template_name = 'users/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['download_history'] = self.object.download_history.all()[:20]
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = BotUser
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'User removed successfully!')
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Toggle ban instead of delete
        user = self.get_object()
        user.is_banned = not user.is_banned
        user.save()
        messages.success(request, f'User {"banned" if user.is_banned else "unbanned"} successfully!')
        return redirect('users:list')
