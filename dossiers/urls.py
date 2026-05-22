"""
URL patterns for the dossiers app.
"""

from django.urls import path
from . import views

urlpatterns = [

    # ------------------------------------------------------------------
    # Dossiers
    # ------------------------------------------------------------------
    path('dossiers/', views.DossierListView.as_view(), name='dossier_list'),
    path('dossiers/nouveau/', views.DossierCreateView.as_view(), name='dossier_create'),
    path('dossiers/<int:pk>/', views.DossierDetailView.as_view(), name='dossier_detail'),
    path('dossiers/<int:pk>/modifier/', views.DossierUpdateView.as_view(), name='dossier_update'),
    path('dossiers/<int:pk>/supprimer/', views.DossierDeleteView.as_view(), name='dossier_delete'),

    # ------------------------------------------------------------------
    # Documents
    # ------------------------------------------------------------------
    path('dossiers/<int:pk>/documents/importer/', views.importer_document, name='importer_document'),
    path('documents/<int:pk>/supprimer/', views.supprimer_document, name='supprimer_document'),

    # ------------------------------------------------------------------
    # Interventions
    # ------------------------------------------------------------------
    path('dossiers/<int:pk>/interventions/ajouter/', views.ajouter_intervention, name='ajouter_intervention'),
    path('interventions/<int:pk>/supprimer/', views.supprimer_intervention, name='supprimer_intervention'),

    # ------------------------------------------------------------------
    # Clients
    # ------------------------------------------------------------------
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/nouveau/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/modifier/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/supprimer/', views.ClientDeleteView.as_view(), name='client_delete'),

    # ------------------------------------------------------------------
    # Audiences
    # ------------------------------------------------------------------
    path('audiences/', views.AudienceListView.as_view(), name='audience_list'),
    path('audiences/nouvelle/', views.AudienceCreateView.as_view(), name='audience_create'),
    path('audiences/<int:pk>/modifier/', views.AudienceUpdateView.as_view(), name='audience_update'),
    path('audiences/<int:pk>/supprimer/', views.AudienceDeleteView.as_view(), name='audience_delete'),
]
