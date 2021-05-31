from rest_framework.viewsets import ModelViewSet
from .models import DemandaDePeca
from .serializers import DemandaSerializer


class DemandaViewSet(ModelViewSet):
    serializer_class = DemandaSerializer
    queryset = DemandaDePeca.objects.all()

    def get_queryset(self): # Filtra se o usuário é Administrador ou Anunciante
        user = self.request.user
        if user.is_administrador or user.is_superuser:
            return DemandaDePeca.objects.all()
        return DemandaDePeca.objects.filter(anunciante=user)
     
    def perform_create(self, serializer): # Adiciona o usuário como Anunciante
        anunciante = None
        if self.request and hasattr(self.request, "user"):
            anunciante = self.request.user
        serializer.save(anunciante=anunciante)
