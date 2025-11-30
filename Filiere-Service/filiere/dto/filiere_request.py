# filiere/dto/request_filiere.py
from dataclasses import dataclass

@dataclass
class RequestFiliereDto:
    code: str
    libelle: str
