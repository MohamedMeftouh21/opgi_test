import django_filters as filters
from django.core.validators import MinValueValidator
from data.models import *





class DataFilter(filters.FilterSet):
    min_loyer = filters.NumberFilter(field_name='dette__montant_dette', lookup_expr='gte',label="Montant de dette Min",validators=[MinValueValidator(0)],min_value=0)
    max_loyer = filters.NumberFilter(field_name='dette__montant_dette', lookup_expr='lte',label="Montant de dette Max",validators=[MinValueValidator(0)],min_value=0)
    unite = filters.ModelChoiceFilter(queryset=Unite.objects.all(),field_name='logement__batiment__Cite__unite__lib_unit', lookup_expr='icontains',label="Unité")
    cite = filters.ModelChoiceFilter(queryset=Cite.objects.none(),field_name='logement__batiment__Cite__lib_Cite', lookup_expr='icontains',label="Cité")
    batiment = filters.ModelChoiceFilter(queryset=Batiment.objects.none(),field_name='logement__batiment__lib_Batiment', lookup_expr='icontains',label="Batiment")

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['cite'].queryset = Cite.objects.none()
        self.filters['batiment'].queryset = Batiment.objects.none()

        if 'unite' in self.data:
            try:
                unite_id = int(self.data.get('unite'))
                self.filters['cite'].queryset = Cite.objects.filter(batiment__Cite__unite_id=unite_id ).distinct()
            except (ValueError, TypeError):
                pass

        if 'cite' in self.data:
            try:
                cite_id = int(self.data.get('cite'))
                self.filters['batiment'].queryset = Batiment.objects.filter(Cite_id=cite_id).distinct()
            except (ValueError, TypeError):
                pass
    
    class Meta:
        
        model = Consultation
        fields = ['min_loyer', 'max_loyer', 'unite', 'cite', 'batiment']
