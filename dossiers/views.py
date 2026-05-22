from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from datetime import date

from .models import Dossier, Client, Intervention, Audience, Document
from .forms import DossierForm, DocumentForm, ClientForm, InterventionForm, AudienceForm
from .mixins import AvocatRequiredMixin


# =============================================================================
# Dashboard
# =============================================================================

@login_required
def dashboard(request):
    context = {
        'total_dossiers': Dossier.objects.count(),
        'dossiers_en_cours': Dossier.objects.filter(statut='En cours').count(),
        'total_clients': Client.objects.count(),
        'total_audiences': Audience.objects.filter(date_audience__gte=date.today()).count(),
        'prochaine_intervention': (
            Intervention.objects
            .filter(date_intervention__gte=date.today())
            .order_by('date_intervention')
            .first()
        ),
        'dossiers_recents': Dossier.objects.order_by('-id')[:5],
        'prochaines_audiences': Audience.objects.filter(date_audience__gte=date.today()).order_by('date_audience')[:5],
    }
    return render(request, 'dashboard.html', context)


# =============================================================================
# Dossiers
# =============================================================================

class DossierListView(LoginRequiredMixin, ListView):
    model = Dossier
    template_name = 'dossiers/dossier_list.html'
    context_object_name = 'dossiers'
    paginate_by = 10

    def get_queryset(self):
        qs = Dossier.objects.order_by('-id')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(titre__icontains=q) |
                Q(client__nom__icontains=q) |
                Q(client__prenom__icontains=q) |
                Q(partie_adverse__icontains=q)
            )
        statut = self.request.GET.get('statut')
        if statut:
            qs = qs.filter(statut=statut)
        type_affaire = self.request.GET.get('type')
        if type_affaire:
            qs = qs.filter(type_affaire=type_affaire)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['selected_statut'] = self.request.GET.get('statut', '')
        ctx['selected_type'] = self.request.GET.get('type', '')
        ctx['type_choices'] = Dossier.TYPE_CHOICES
        return ctx


class DossierDetailView(LoginRequiredMixin, DetailView):
    model = Dossier
    template_name = 'dossiers/dossier_detail.html'
    context_object_name = 'dossier'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['intervention_form'] = InterventionForm()
        return ctx


class DossierCreateView(LoginRequiredMixin, CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'
    success_url = reverse_lazy('dossier_list')

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get('client')
        if client_id:
            initial['client'] = client_id
        return initial


class DossierUpdateView(LoginRequiredMixin, UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'

    def get_success_url(self):
        return reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_update'] = True
        return ctx


class DossierDeleteView(LoginRequiredMixin, AvocatRequiredMixin, DeleteView):
    model = Dossier
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('dossier_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_type'] = 'le dossier'
        ctx['object_name'] = self.object.titre
        ctx['cancel_url'] = reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})
        return ctx


# =============================================================================
# Clients
# =============================================================================

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'dossiers/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        qs = Client.objects.order_by('-id')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nom__icontains=q) |
                Q(prenom__icontains=q) |
                Q(telephone__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'dossiers/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_update'] = True
        return ctx


class ClientDeleteView(LoginRequiredMixin, AvocatRequiredMixin, DeleteView):
    model = Client
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_type'] = 'le client'
        ctx['object_name'] = str(self.object)
        ctx['cancel_url'] = reverse_lazy('client_detail', kwargs={'pk': self.object.pk})
        return ctx


# =============================================================================
# Documents
# =============================================================================

@login_required
def importer_document(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.dossier = dossier
            doc.save()
            messages.success(request, 'Document importé avec succès.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def supprimer_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    dossier_pk = document.dossier.pk
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé.')
    return redirect('dossier_detail', pk=dossier_pk)


# =============================================================================
# Interventions
# =============================================================================

@login_required
def ajouter_intervention(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = InterventionForm(request.POST, request.FILES)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.dossier = dossier
            intervention.save()
            messages.success(request, 'Intervention ajoutée avec succès.')
    return redirect('dossier_detail', pk=pk)


@login_required
def supprimer_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    dossier_pk = intervention.dossier.pk
    if request.method == 'POST':
        intervention.delete()
        messages.success(request, 'Intervention supprimée.')
    return redirect('dossier_detail', pk=dossier_pk)


# =============================================================================
# Audiences
# =============================================================================

class AudienceListView(LoginRequiredMixin, ListView):
    model = Audience
    template_name = 'dossiers/audience_list.html'
    context_object_name = 'audiences'
    paginate_by = 15

    def get_queryset(self):
        qs = Audience.objects.order_by('date_audience')
        filtre = self.request.GET.get('filtre', 'toutes')
        if filtre == 'a_venir':
            qs = qs.filter(date_audience__gte=date.today())
        elif filtre == 'passees':
            qs = qs.filter(date_audience__lt=date.today())
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(tribunal__icontains=q) |
                Q(dossier__titre__icontains=q) |
                Q(dossier__client__nom__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filtre'] = self.request.GET.get('filtre', 'toutes')
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['today'] = date.today()
        return ctx


class AudienceCreateView(LoginRequiredMixin, CreateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'dossiers/audience_form.html'
    success_url = reverse_lazy('audience_list')

    def get_initial(self):
        initial = super().get_initial()
        dossier_id = self.request.GET.get('dossier')
        if dossier_id:
            initial['dossier'] = dossier_id
        return initial


class AudienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'dossiers/audience_form.html'
    success_url = reverse_lazy('audience_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_update'] = True
        return ctx


class AudienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Audience
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('audience_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object_type'] = "l'audience"
        ctx['object_name'] = f"{self.object.tribunal} — {self.object.date_audience.strftime('%d/%m/%Y')}"
        ctx['cancel_url'] = reverse_lazy('audience_list')
        return ctx
