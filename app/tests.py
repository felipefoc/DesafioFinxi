from django.db.models import query
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from django.test import TestCase
import unittest
from .models import Usuario, Peca, DemandaDePeca
from .serializers import UsuarioSerializer, PecaSerializer, DemandaSerializer
import pytest


# Create your tests here.
class testTipoUsuario(TestCase):
    """ Testa se o usuário está sendo criado com o tipo correto """

    def setUp(self):
        Usuario.objects.create(
            username='Administrador',
            password='password',
            administrador=True,
            email='administrador@test.com'
        )
        Usuario.objects.create(
            username='Anunciante',
            password='password',
            email='administrador@test.com'
        )
    def test_usuario_administrador(self):
        admin = Usuario.objects.get(username='Administrador')
        self.assertTrue(admin.administrador)
    
    def test_usuario_anunciante(self):
        anunciante = Usuario.objects.get(username='Anunciante')
        self.assertFalse(anunciante.administrador)
        self.assertTrue(anunciante.anunciante)

class ModelViewSetTest(APITestCase):
    """ Testa o CRUD """
    
    fixtures = ['fixtures.json']
    anunciante = Usuario.objects.get(username='anunciante')
    admin = Usuario.objects.get(username='admin')
    peca = Peca.objects.get(id=2)
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION='Token ' + str(anunciante.auth_token))


    def test_se_anunciante_tem_acesso_apenas_a_propria_demanda(self):
        response = self.cliente.get(reverse("demandas-list"))
        query = DemandaDePeca.objects.filter(anunciante=self.anunciante.id)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(query), len(response.data))

 
    def test_se_anunciante_tem_acesso_a_propria_demanda_especifica(self):
        response = self.cliente.get(reverse("demandas-detail", args=[1]))
        query = DemandaDePeca.objects.filter(anunciante=self.anunciante.id).first()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(query.endereco_de_entrega == response.data['endereco_de_entrega'])
        self.assertTrue(query.anunciante.id == response.data['anunciante'])

    def test_se_anunciante_nao_tem_acesso_a_outras_demandas(self):
        response = self.cliente.get(reverse("demandas-detail", args=[4]))
        query = DemandaDePeca.objects.filter(anunciante=self.admin).first()
        second_query = DemandaDePeca.objects.filter(anunciante=self.anunciante).first()
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertNotEquals(query.anunciante.id, second_query.anunciante.id)

    def test_criacao_de_demanda(self):
        payload = {
            'descricao': self.peca.pk,
            'endereco_de_entrega': 'Rua test, 22, Jardim Botanico',
            'informacoes_de_contato': '(21)96692-9828',
            'status_de_finalizacao': True,
            'anunciante': self.anunciante.pk
        }
        response = self.cliente.post(reverse("demandas-list"), payload)
        query = DemandaDePeca.objects.filter(anunciante=self.anunciante).last()
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(query.endereco_de_entrega, payload['endereco_de_entrega'])

    def test_update_de_demanda(self):
        demanda = {
            'descricao': self.peca,
            'endereco_de_entrega': 'Rua test, 22, Jardim Botanico',
            'informacoes_de_contato': '(21)96692-9828',
            'status_de_finalizacao': True,
            'anunciante': self.anunciante
        }
        objeto = DemandaDePeca.objects.create(**demanda)
        payload = {
            'endereco_de_entrega': 'Rua Mudança, 23, Itatiaia',
            'status_de_finalizacao': False,
        }
        response = self.cliente.patch(reverse('demandas-detail', args=[objeto.id]), payload)

        objeto.refresh_from_db()

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertNotEquals(demanda['endereco_de_entrega'], response.data['endereco_de_entrega'])
        self.assertEqual(response.data['endereco_de_entrega'], payload['endereco_de_entrega'])
        self.assertNotEquals(demanda['status_de_finalizacao'], payload['status_de_finalizacao'])
        self.assertEqual(response.data['status_de_finalizacao'], payload['status_de_finalizacao'])

    def test_apagar_demanda(self):
        demanda = DemandaDePeca.objects.get(id=2)
        response = self.cliente.delete(
            reverse('demandas-detail', args=[2])
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(DemandaDePeca.objects.filter(pk=demanda.pk))

class FinalizarDemanda(APITestCase):
    """ Testa finalização da demanda """
    
    fixtures = ['fixtures.json']
    anunciante = Usuario.objects.get(username='anunciante')
    admin = Usuario.objects.get(username='admin')
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION='Token ' + str(anunciante.auth_token))
    
    def test_finalizar_demanda(self):
        demanda = DemandaDePeca.objects.filter(status_de_finalizacao = True).first()
        response = self.cliente.put(
            reverse('finalizar', args=[demanda.pk])
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(demanda.status_de_finalizacao, False)
        
    def test_finalizar_demanda_de_terceiros(self):
        demanda = DemandaDePeca.objects.filter(anunciante=self.admin).first()
        response = self.cliente.put(
            reverse('finalizar', args=[demanda.pk])
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertTrue(demanda.status_de_finalizacao, True)
        


        


        
    

    



        
    