from django.db import models
from data.models import Consultation

class Dette (models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.SET)
    montant_dette = models.FloatField(default=0)
    
    def save(self, *args, **kwargs):
        self.montant_dette = self.consultation.calculer_dette()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.consultation.occupant.nom_oc
    class Meta:
        db_table = 'data_dette'