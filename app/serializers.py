from rest_framework import serializers
from .models import DemandaDePeca, Peca, Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

    
class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = "__all__"


class DemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandaDePeca
        fields = "__all__"
        read_only_fields = ['id', 'anunciante']
              
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['descricao'] = PecaSerializer(instance.descricao).data
        return rep
    

