from django.db import models  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connections

class wilaya(models.Model):
   lib_wilaya = models.CharField(max_length=120)
   date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

   def __str__(self):
            return self.lib_wilaya

class Unite(models.Model):
        lib_unit = models.CharField(max_length=120)
        wilaya = models.ForeignKey(wilaya, on_delete=models.SET)
        date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

        def __str__(self):
            return self.lib_unit

class Cite(models.Model):
              lib_Cite = models.CharField(max_length=120)
              unite = models.ForeignKey(Unite, on_delete=models.SET)
              nb_logts = models.PositiveIntegerField()
              date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

              def __str__(self):
                 return self.lib_Cite

class Batiment (models.Model):
           lib_Batiment = models.CharField(max_length=120)
           Cite = models.ForeignKey(Unite, on_delete=models.SET)
           nb_logts = models.PositiveIntegerField()
           nb_etage = models.PositiveIntegerField()
           date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

           def __str__(self):
                 return self.lib_Batiment

class Occupant (models.Model):
       oc_id  = models.PositiveIntegerField()
       nom_oc = models.CharField(max_length=120)
       prenom_oc = models.CharField(max_length=120)
       prenom_oc = models.CharField(max_length=120)
       date_naiss = models.DateTimeField(null=True)
       lieu_naiss=models.CharField(max_length=120)

       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
                 return self.nom_oc

class Contrat(models.Model):
    occupant = models.ForeignKey(Occupant, on_delete=models.SET)
    date_cnt = models.DateTimeField(null=True)
    date_strt_loyer = models.DateTimeField(null=True)
    loyer = models.FloatField()
    charge = models.CharField(max_length=120)
    mnt_tva = models.FloatField()
    
   
    
    total_of_month = models.FloatField(default=0)
  #siglaler add to changer total 
    def __str__(self):
                 return self.occupant.nom_oc

 
@receiver(post_save, sender=Contrat)
def update_total_of_month(sender, instance, **kwargs):
       A = instance.loyer * (instance.mnt_tva/100)
       B = A * 1
       C = instance.loyer * 1
       D = B + C
       charges = float(instance.charge) * 1  # convert charge to float
       total = D + charges












       sender.objects.filter(id=instance.id).update(total_of_month=total)

class Logement (models.Model):
        batiment = models.ForeignKey(Batiment, on_delete=models.SET)
        contrat = models.ForeignKey(Contrat, on_delete=models.SET)
        surface=  models.FloatField( default='m2')
        prix_logement=  models.FloatField()
        type_logement=  models.CharField(max_length=120)

        created_at = models.DateTimeField(auto_now_add=True)
        def __str__(self):
                 return self.contrat.occupant.nom_oc

class Consultation (models.Model):
                logement = models.ForeignKey(Logement, on_delete=models.SET)
                occupant = models.ForeignKey(Occupant, on_delete=models.SET)

                mois=models.PositiveIntegerField()
                created_at = models.DateTimeField(auto_now_add=True)
                total =models.FloatField()

                def __str__(self):
                    return self.occupant.nom_oc
                
class Service_contentieux (models.Model):
     occupant = models.ForeignKey(Occupant, on_delete=models.SET)
     def __str__(self):
                 return self.occupant.nom_oc
     
@receiver(post_save, sender=Consultation)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        # Code to execute when a new instance of MyModel is saved
        print("A new instance of MyModel was created!")
        var1 = 5000
        instances = []

        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT data_occupant.nom_oc AS occupant_name, (((EXTRACT(YEAR FROM age(NOW(), date_strt_loyer)) * 12 + EXTRACT(MONTH FROM age(NOW(), date_strt_loyer)))::DECIMAL(10, 2) -   sum(data_consultation.mois))  * data_contrat.total_of_month ) AS monthly_rent FROM data_contrat JOIN data_consultation ON data_contrat.occupant_id = data_consultation.occupant_id JOIN data_occupant ON data_contrat.occupant_id = data_occupant.id GROUP BY data_contrat.date_strt_loyer, data_occupant.nom_oc,data_contrat.total_of_month ;'
                          
                   
                          )
            if cursor.rowcount > 0:
                print("Query executed successfully.")
                rows = cursor.fetchall()
                for row in rows:
                    col1_value = row[1]
                    my_int = int(col1_value)

                    if my_int < 0:
                        print("3ayche ghaya")
                    elif row[1] >= var1:
                        print("non", row[0])
                        occupant = Occupant.objects.get(nom_oc=row[0])
                        instance = Service_contentieux(occupant=occupant)
                        if not Service_contentieux.objects.filter(occupant=occupant).exists():
                           instances.append(instance)
                        else :
                                                   print("No instances created.")


                if instances:
                    Service_contentieux.objects.bulk_create(instances)
                else:
                    print("No instances created.")

            else:
                print("Query failed.")
