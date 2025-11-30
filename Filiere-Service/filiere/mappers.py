# filiere/mappers.py
# Equivalent de FiliereMapper (MapStruct) en Java

from filiere.models import Filiere
from filiere.dto.request_filiere import RequestFiliereDto
from filiere.dto.response_filiere import ResponseFiliereDto

class FiliereMapper:

    @staticmethod
    def DTO_To_Entity(dto: RequestFiliereDto) -> Filiere:
        """
        Convertit RequestFiliereDto -> Filiere (SQLAlchemy model)
        Si dto fields sont None, elles restent None (le service gère l'update).
        """
        # on ne commit pas ici, on retourne l'instance
        return Filiere(code=dto.code, libelle=dto.libelle)

    @staticmethod
    def Entity_To_DTO(entity: Filiere) -> ResponseFiliereDto:
        """
        Convertit Filiere (model) -> ResponseFiliereDto
        """
        return ResponseFiliereDto.from_model(entity)
