"""Subscriptions app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SubscriptionChannel

class ChannelListView(LoginRequiredMixin, ListView):
    model = SubscriptionChannel
    template_name = 'subscriptions/list.html'
    context_object_name = 'channels'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by required status
        req = self.request.GET.get('required')
        if req == 'yes':
            queryset = queryset.filter(is_required=True)
        elif req == 'no':
            queryset = queryset.filter(is_required=False)

        # Filter by active status
        active = self.request.GET.get('active')
        if active == 'active':
            queryset = queryset.filter(is_active=True)
        elif active == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('-added_at')


class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = SubscriptionChannel
    template_name = 'subscriptions/form.html'
    fields = ['channel_id', 'channel_username', 'title', 'invite_link', 'is_required', 'is_active']
    success_url = reverse_lazy('subscriptions:list')

    def form_valid(self, form):
        messages.success(self.request, 'Channel added successfully!')
        return super().form_valid(form)


class ChannelUpdateView(LoginRequiredMixin, UpdateView):
    model = SubscriptionChannel
    template_name = 'subscriptions/form.html'
    fields = ['channel_id', 'channel_username', 'title', 'invite_link', 'is_required', 'is_active']
    success_url = reverse_lazy('subscriptions:list')

    def form_valid(self, form):
        messages.success(self.request, 'Channel updated successfully!')
        return super().form_valid(form)


class ChannelDeleteView(LoginRequiredMixin, DeleteView):
    model = SubscriptionChannel
    template_name = 'subscriptions/confirm_delete.html'
    success_url = reverse_lazy('subscriptions:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Channel deleted successfully!')
        return super().delete(request, *args, **kwargs)
