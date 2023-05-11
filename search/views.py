from django.shortcuts import redirect, render,get_object_or_404
from django.http import JsonResponse
from data.models import  *
from django.db.models import *
from search.filters import *
from search.utils import *
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.cache import cache_control

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recherche(request):
    search_term = request.GET.get('search')
    consultations = Consultation.objects.all()
    consultations = search(consultations,search_term)
    myFilter = DataFilter(request.GET, queryset=consultations)
    consultations  = myFilter.qs


    occupants = Occupant.objects.filter(consultation__in=consultations).distinct()

    latest_consultations = []
    for occupant in occupants:
        consultation = Consultation.objects.filter(occupant=occupant.id).latest('created_at')
        latest_consultations.append(consultation)


    logement = {}
    occupants = None # initialise la variable occupant
    if search_term:

     if not consultations.exists():
        occupants = Occupant.objects.filter(Q(Q(nom_oc__icontains=search_term) | Q(prenom_oc__icontains=search_term)))



        for occupant in occupants:
            contrats = Contrat.objects.filter(occupant=occupant.id)
            for contrat in contrats:
                logement[occupant.id] = Logement.objects.filter(contrat=contrat.id).first()


    context ={
        'service': 'Service Recouvrement',
        'title': "Recherche", 
        'myFilter': myFilter,
        'occupants': occupants,
        'logement': logement,
        'consultations':consultations,
        'latest_consultations':latest_consultations
        }

    return render(request, 'search/search.html', context=context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def occupant_detail(request, pk):
    if   Occupant.objects.filter(id=pk).exists():
        occupant = get_object_or_404(Occupant, pk = pk)
        contrats = Contrat.objects.filter(occupant=occupant)
        for contrat in contrats:
            logements= Logement.objects.filter(contrat=contrat)
        context = {
        'service': 'Service Recouvrement',
        'title': 'Dashbord',
        'subtitle': "Occupant Detail",
        'contrats': contrats,
        'logements': logements,
        'occupant': occupant,
        }
        return render(request, "service_recouvrement/occupant_detail.html", context=context)
    
    elif   not  Consultation.objects.filter(pk=pk).exists():
        return redirect('home')
    else : 
        consultation = get_object_or_404(Consultation, pk = pk)

        total_months = Consultation.objects.filter(occupant=consultation.occupant).aggregate(Sum('mois'))['mois__sum'] or 0
        montant_dette = consultation.calculer_dette()
        montant_dette=abs(montant_dette)
        mois_entiers = int((consultation.created_at - consultation.logement.contrat.date_strt_loyer).total_seconds() / 2628000) - total_months

        if mois_entiers <= 0 :
                                mois_entiers = 0
                                montant_dette = 0
        
        if montant_dette == 0:
            status = 'En règle'
        elif montant_dette > consultation.logement.contrat.total_of_month:
            status = 'En dette'
        else :
            status = 'En dette'

        archives = archive_consultations_mois(consultation.occupant.id)

        archivesyears,total_dettes = archive_consultations_annee(consultation.occupant.id)
        
    
    context = {
        'service': 'Service Recouvrement',
        'title': 'Dashbord',
        'subtitle': "Occupant Detail",
        'consultation': consultation,
        'archives': archives,
        'archivesyears': archivesyears,
        'montant_dette': montant_dette,
        'total_dettes': total_dettes,
        'mois_entiers': mois_entiers,
        'total_months': total_months,
        'status': status,
    }

    return render(request, "service_recouvrement/occupant_detail.html", context=context)



@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_cites(request):
    unite_id = request.GET.get('unite_id')
    cites = Cite.objects.filter(batiment__Cite__unite_id=unite_id).distinct()

    data = {
        'cites': list(cites.values('id', 'lib_Cite')),
    }

    return JsonResponse(data)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_batiments(request):
    Cite_id = request.GET.get('Cite_id')
    batiments = Batiment.objects.filter(Cite_id=Cite_id).distinct()
    data = {
         'batiments': list(batiments.values('id', 'lib_Batiment')),
    }
    return JsonResponse(data)