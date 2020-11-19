from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Triagem(models.Model):
    codigo = models.CharField(_('Código da triagem *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    febre = models.CharField(_('Tem febre? *'), max_length=50, null=True)
    dorcabeca = models.CharField(_('Tem dor de cabeça? *'), max_length=50, null=True)
    secrecaonasal = models.CharField(_('Tem secreção nasal ou espirros? *'), max_length=50, null=True)
    dorgarganta = models.CharField(_('Tem dor/irritação de garganta? *'), max_length=50, null=True)
    tosse = models.CharField(_('Tem tosse seca? *'), max_length=50, null=True)
    difrespiratoria = models.CharField(_('Tem dificuldade respiratória? *'), max_length=50, null=True)
    dorcorpo = models.CharField(_('Tem dores no corpo? *'), max_length=50, null=True)
    diarreia = models.CharField(_('Tem diarréia? *'), max_length=50, null=True)
    viagem = models.CharField(_('Viajou nos últimos 14 dias, para algum local com casos confirmados de COVID-19? *'), max_length=50, null=True)
    contato = models.CharField(_('Esteve em contato, nos últimos 14 dias, com um caso diagnosticado com COVID-19? *'), max_length=50, null=True)
    probabilidade = models.CharField(max_length=50, null=True)
    risco = models.CharField(max_length=50, null=True)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['codigo']
        verbose_name        =   ('triagem')
        verbose_name_plural =   ('triagens')
        unique_together     =   ['codigo'] #criando chave primária composta no BD

    def __str__(self):
        return "Curso: %s" % (self.codigo)

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

    def calcula_valor(self):
        total = 0
        valor_febre = self.febre
        valor_dorcabeca = self.dorcabeca
        valor_secrecaonasal = self.secrecaonasal
        valor_dorgarganta = self.dorgarganta
        valor_tosse = self.tosse
        valor_difrespiratoria = self.difrespiratoria
        valor_dorcorpo = self.dorcorpo
        valor_diarreia = self.diarreia
        valor_viagem = self.viagem
        valor_contato = self.contato

        if valor_febre.upper() == 'SIM':
            # peso = 5
            total += 5
        if valor_dorcabeca.upper() == 'SIM':
            # peso = 1
            total += 1
        if valor_secrecaonasal.upper() == 'SIM':
            # peso = 1
            total += 1
        if valor_dorgarganta.upper() == 'SIM':
            # peso = 1
            total += 1
        if valor_tosse.upper() == 'SIM':
            # peso = 3
            total += 3
        if valor_difrespiratoria.upper() == 'SIM':
            # peso = 10
            total += 10
        if valor_dorcorpo.upper() == 'SIM':
            # peso = 1
            total += 1
        if valor_diarreia.upper() == 'SIM':
            # peso = 1
            total += 1
        if valor_viagem.upper() == 'SIM':
            # peso = 3
            total += 3
        if valor_contato.upper() == 'SIM':
            # peso = 10
            total += 10
        if total <= 9:
            self.probabilidade = total
            self.risco = 'Risco Baixo'
        elif total <= 19:
            self.probabilidade = total
            self.risco = 'Risco Médio'
        else:
            self.probabilidade = total
            self.risco = 'Risco Alto'