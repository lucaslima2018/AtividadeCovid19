from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Triagem(models.Model):
    codigo = models.CharField(_('Código da triagem *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    data = models.DateField(_('Data da reunião *'), max_length=11, help_text='dd/mm/aaaa')
    hora = models.CharField(_('Hora da reunião *'), max_length=5, help_text='hh:mm')
    local = models.CharField(_('Local da reunião *'), max_length=50)
    pauta = models.TextField(_('Pauta da reunião'), max_length=200)
    texto = models.TextField(_('Texto da reunião'), null=True, blank=True, max_length=10000)
    validada = models.BooleanField(_('Ata validada? '), default=False, null=True, blank=True)
    febre = models.CharField(_('Tem febre? *'), max_length=50)
    dorcabeca = models.CharField(_('Tem dor de cabeça? *'), max_length=50)
    secrecaonasal = models.CharField(_('Tem secreção nasal ou espirros? *'), max_length=50)
    dorgarganta = models.CharField(_('Tem dor/irritação de garganta? *'), max_length=50)
    tosse = models.CharField(_('Tem tosse seca? *'), max_length=50)
    difrespiratoria = models.CharField(_('Tem dificuldade respiratória? *'), max_length=50)
    dorcorpo = models.CharField(_('Tem dores no corpo? *'), max_length=50)
    diarreia = models.CharField(_('Tem diarréia? *'), max_length=50)
    viagem = models.CharField(_('Viajou nos últimos 14 dias, para algum local com casos confirmados de COVID-19? *'), max_length=50)
    contato = models.CharField(_('Esteve em contato, nos últimos 14 dias, com um caso diagnosticado com COVID-19? *'), max_length=50)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['codigo','-data','-hora']
        verbose_name        =   ('triagem')
        verbose_name_plural =   ('triagens')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "%s: %s. Curso: %s" % (self.codigo, self.data, self.hora)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Triagem, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('triagem_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('triagem_delete', args=[str(self.id)])