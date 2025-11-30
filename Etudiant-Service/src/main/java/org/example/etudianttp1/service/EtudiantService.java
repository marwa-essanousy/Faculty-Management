package org.example.etudianttp1.service;

import org.example.etudianttp1.dto.RequestEtudiantDto;
import org.example.etudianttp1.dto.ResponseEtudiantDto;
import org.example.etudianttp1.entities.Etudiant;

import java.util.List;

public interface EtudiantService {
    public ResponseEtudiantDto addEtudiant(RequestEtudiantDto dto);
    List <ResponseEtudiantDto> getAllEtudiants();
    public ResponseEtudiantDto getEtudiantById(int id);
    ResponseEtudiantDto updateEtudiant(RequestEtudiantDto requestEtudiantDto, int id);

    public ResponseEtudiantDto deleteEtudiant(int id);

}
