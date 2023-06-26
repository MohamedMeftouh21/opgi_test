from django.db import models
from data.models import * 
from django.db import models
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from django.db.models import Sum
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from data.models import Consultation, Unite
import calendar
from datetime import datetime, date, timedelta

# Create your models here.
class MontantMensuel(models.Model):
    unite = models.ForeignKey(Unite, on_delete=models.SET,db_column='unite_id')
    mois = models.PositiveIntegerField(db_column='mois')
    annee = models.PositiveIntegerField(db_column='annee')
    total = models.FloatField(db_column='total')
    total_of_month = models.FloatField(db_column='total_of_month')
    def __str__(self):
        return f"MontantMensuel {self.unite.lib_unit} - {self.mois}/{self.annee}"
    class Meta:
        db_table = 'recouvrement_montantmensuel'
        managed = False    
        unique_together = ('unite','annee', 'mois')


class Notification_chef_service(models.Model):
    unite = models.ForeignKey(Unite, on_delete=models.SET,db_column='unite_id')

    created_at = models.DateTimeField(auto_now_add=True,db_column='created_at')
    read = models.BooleanField(default=False,db_column='read')

  
        
    def __str__(self):
        return f"MontantMensuel {self.unite.lib_unit} "
    class Meta:
        db_table = 'recouvrement_notification_chef_service'
        managed = False 
    
@receiver(post_save, sender=Consultation)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        # Calculer le total des consultations pour chaque mois et chaque unité
        consultations_totals = Consultation.objects.values('unite', 'created_at__month').annotate(total=Sum('total'))

        # Boucler sur les résultats pour créer les instances MontantMensuel correspondantes
        for c in consultations_totals:
            # Vérifier si l'unité correspondante a un MontantMensuel pour le mois en question
            try:
                montant_mensuel = MontantMensuel.objects.get(unite=c['unite'], mois=c['created_at__month'])
            except MontantMensuel.DoesNotExist:
                # Si le MontantMensuel n'existe pas, créer une nouvelle instance avec le total de consultations correspondant
                MontantMensuel.objects.create(unite=c['unite'], mois=c['created_at__month'], total_of_month=c['total'])
            else:
                # Sinon, mettre à jour le total du MontantMensuel avec le total de consultations correspondant
                montant_mensuel.total_of_month = c['total']
                montant_mensuel.save()
                 

    
@receiver(post_save, sender=Consultation)
def check_consultations_totals(sender, instance, created, **kwargs):
    if created:
        # Get the current date
            current_date = date.today()
            
# Get the last day of the current month
            last_day_of_month = datetime(current_date.year, current_date.month, 1) + timedelta(days=32) - timedelta(days=1)

# Convert the current date to a datetime object
            current_datetime = datetime.combine(current_date, datetime.min.time())

        # Vérifier si la date actuelle est dans les 10 derniers jours du mois
        #if (last_day_of_month - current_datetime).days < 10:

            # Obtenir la liste des unités dans la base de données
            units = MontantMensuel.objects.values_list('unite', flat=True).distinct()
            # Boucler sur chaque unité
            for unit in units:
                # Obtenir le total des consultations pour cette unité pour le mois actuel
                consultations_total_for_unit = Consultation.objects.filter(unite=unit, created_at__month=current_date.month).aggregate(total=Sum('total'))['total'] or 0
                montant_mensuel = MontantMensuel.objects.get(unite=unit, mois=current_date.month)  # Récupérer l'objet MontantMensuel correspondant
                total_fixe = montant_mensuel.total  # Accéder à l'attribut total_fixe de l'objet MontantMensuel
                unite = Unite.objects.get(id=unit)
                lib_unit = unite.lib_unit  # Accéder à l'attribut total_fixe de l'objet MontantMensuel
                instances = []

                  # Récupérer l'objet MontantMensuel correspondant

                # Vérifier si le total des consultations pour chaque unité est inférieur à 60% du total_fixe
                if consultations_total_for_unit < (total_fixe): #* 0.6):
                    # Si le total des consultations pour une unité est inférieur à 60% du total_fixe, créer une instance de Signal avec les détails appropriés
                    if not Notification_chef_service.objects.filter(unite=unite,read =False).exists()  :

                        instances.append(Notification_chef_service(unite=unite))
                        if instances:
                              Notification_chef_service.objects.bulk_create(instances)
                        else:
                            print("No instances created.")
                    else:
                        print("Signal min:",lib_unit)
                      
                else:
                    # Sinon, supprimer toute instance existante de Signal pour cette unité
                    print("Signal max:",lib_unit)
       # else:
            # La date actuelle n'est pas dans les 10 derniers jours du mois
         #   print("Current date is not within the last 10 days of the month")


