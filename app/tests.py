from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from django.test import TestCase
from .models import Usuario, Peca, DemandaDePeca



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
    
    fixtures = ["fixtures.json"]

    def setUp(self): 
        self.anunciante = Usuario.objects.get(username='anunciante2')
        self.admin = Usuario.objects.get(username='admin')
        self.peca = Peca.objects.get(id=1)
        self.cliente = APIClient()
        self.cliente.credentials(HTTP_AUTHORIZATION='Token ' + str(self.anunciante.auth_token))   
  

    def test_se_anunciante_tem_acesso_apenas_as_proprias_demandas(self):
        request = self.cliente.get(reverse("demandas-list"))
        query = DemandaDePeca.objects.filter(anunciante=self.anunciante) # Somente para pegra o len()
        self.assertEquals(status.HTTP_200_OK, request.status_code)
        self.assertEquals(len(query), len(request.data))

 
    def test_se_anunciante_tem_acesso_a_propria_demanda_especifica(self):
        demanda = DemandaDePeca.objects.filter(anunciante=self.anunciante).first()
        response = self.cliente.get(reverse("demandas-detail", args=[demanda.id]))
       
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertTrue(demanda.endereco_de_entrega == response.data['endereco_de_entrega'])
        self.assertTrue(demanda.anunciante.id == response.data['anunciante'])

    def test_se_anunciante_nao_tem_acesso_a_outras_demandas(self):
        query = DemandaDePeca.objects.filter(anunciante=self.admin).first()
        demanda = DemandaDePeca.objects.filter(anunciante=self.anunciante).first()
        response = self.cliente.get(reverse("demandas-detail", args=[query.id]))          
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertNotEquals(query.anunciante.id, demanda.anunciante.id)

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
        demanda = DemandaDePeca.objects.filter(anunciante=self.anunciante).first()

        payload = {
            'endereco_de_entrega': 'Rua Mudança, 23, Itatiaia',
            'status_de_finalizacao': False,
        }
        response = self.cliente.patch(
            reverse('demandas-detail', args=[demanda.id]), payload 
        )
        
        demanda.refresh_from_db()
        
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['endereco_de_entrega'], payload['endereco_de_entrega'])
        self.assertEqual(response.data['status_de_finalizacao'], payload['status_de_finalizacao'])

    def test_apagar_demanda(self):
        demanda = DemandaDePeca.objects.filter(anunciante=self.anunciante).first()
        response = self.cliente.delete(
            reverse('demandas-detail', args=[demanda.id])
        )
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(DemandaDePeca.objects.filter(pk=demanda.pk))

class FinalizarDemanda(APITestCase):
    """ Testa finalização da demanda """
    
    fixtures = ['fixtures.json']
    
    def setUp(self): 
        self.anunciante = Usuario.objects.get(username='anunciante')
        self.admin = Usuario.objects.get(username='admin')
        self.cliente = APIClient()
        self.cliente.credentials(HTTP_AUTHORIZATION='Token ' + str(self.anunciante.auth_token))
    
    def test_finalizar_demanda(self):
        demanda = DemandaDePeca.objects.filter(status_de_finalizacao=True).first()
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
    
        


        


        
    

    



        
    