# filiere/services.py
# Traduction de FiliereServiceImpl Java -> Python

from filiere.repository import find_all, find_by_id, find_by_code, save, delete
from filiere.mappers import FiliereMapper
from filiere.dto.request_filiere import RequestFiliereDto
from filiere.dto.response_filiere import ResponseFiliereDto

class FiliereServiceImpl:
    def __init__(self, repository=None, mapper: FiliereMapper = None):
        # repository param is not required (we use repository module functions),
        # mais on garde l'argument pour la similarité avec Java et testabilité.
        self.mapper = mapper or FiliereMapper()

    def addFiliere(self, request_dto: dict) -> ResponseFiliereDto:
        """
        request_dto can be dict or RequestFiliereDto
        """
        # normalize to RequestFiliereDto
        if isinstance(request_dto, dict):
            dto = RequestFiliereDto(code=request_dto.get("code"), libelle=request_dto.get("libelle"))
        else:
            dto = request_dto

        # mapper -> entity
        filiere_entity = self.mapper.DTO_To_Entity(dto)
        # save
        saved = save(filiere_entity)
        return self.mapper.Entity_To_DTO(saved)

    def getAllFilieres(self):
        entities = find_all()
        return [self.mapper.Entity_To_DTO(e) for e in entities]

    def getFiliereById(self, id: int) -> ResponseFiliereDto:
        e = find_by_id(id)
        if not e:
            raise LookupError(f"Filiere id={id} introuvable")
        return self.mapper.Entity_To_DTO(e)

    def updateFiliere(self, request_dto: dict, id: int) -> ResponseFiliereDto:
        # allow dict or RequestFiliereDto
        if isinstance(request_dto, dict):
            dto = RequestFiliereDto(code=request_dto.get("code"), libelle=request_dto.get("libelle"))
        else:
            dto = request_dto

        # build entity from dto (partial)
        new_entity = self.mapper.DTO_To_Entity(dto)
        existing = find_by_id(id)
        if not existing:
            raise LookupError(f"Filiere id={id} introuvable")

        # copy non-null fields
        if new_entity.code is not None:
            # check uniqueness
            other = find_by_code(new_entity.code)
            if other and other.idFiliere != id:
                raise ValueError("Un enregistrement avec ce code existe déjà.")
            existing.code = new_entity.code

        if new_entity.libelle is not None:
            existing.libelle = new_entity.libelle

        updated = save(existing)
        return self.mapper.Entity_To_DTO(updated)

    def deleteFiliere(self, id: int):
        # in Java method returns ResponseFiliereDto but implementation returned null.
        # We'll delete and return None for parity.
        existing = find_by_id(id)
        if not existing:
            raise LookupError(f"Filiere id={id} introuvable")
        delete(existing)
        return None
