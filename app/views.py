from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.http import Http404
from .models import DemandaDePeca, Usuario
from .serializers import DemandaSerializer


class DemandaViewSet(ModelViewSet):
    serializer_class = DemandaSerializer
    queryset = None

    def get_queryset(self): # Filtra se o usuário é Administrador ou Anunciante
        usuario = self.request.user
        if usuario.administrador or usuario.is_superuser:
            return DemandaDePeca.objects.all()
        return DemandaDePeca.objects.filter(anunciante=usuario)
     
    def perform_create(self, serializer): # Adiciona o usuário como Anunciante
        anunciante = None
        if self.request and hasattr(self.request, "user"):
            anunciante = self.request.user
        serializer.save(anunciante=anunciante)

class FinalizarDemandaAPIView(UpdateAPIView):
    queryset = None
    serializer_class = DemandaSerializer
    lookup_field = 'pk'
    
    def get_queryset(self): # Filtra se o usuário é Administrador ou Anunciante
        usuario = self.request.user
        if usuario.administrador or usuario.is_superuser:
            return DemandaDePeca.objects.all()
        return DemandaDePeca.objects.filter(anunciante=usuario)
    
    def update(self, request, *args, **kwargs): # Atualiza status_de_finalizacao
        instance = self.get_object()
        instance.status_de_finalizacao = False
        instance.save()
        
        serializer = self.get_serializer(instance)
        if serializer.is_valid:
            return Response(serializer.data)
        
        
        
        


            

    