from django.contrib import admin
from .models import Client, Dossier, Intervention, Audience, Document


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'telephone', 'date_ajout')
    search_fields = ('nom', 'prenom', 'telephone')


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'client', 'type_affaire', 'statut')
    list_filter = ('statut', 'type_affaire')
    search_fields = ('titre', 'client__nom', 'client__prenom')


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_intervention')


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'tribunal', 'date_audience')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_creation')
