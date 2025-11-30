# filiere/dto/response_filiere.py
from dataclasses import dataclass

@dataclass
class ResponseFiliereDto:
    idFiliere: int
    code: str
    libelle: str

    @staticmethod
    def from_model(model):
        return ResponseFiliereDto(
            idFiliere=model.idFiliere,
            code=model.code,
            libelle=model.libelle
        )
