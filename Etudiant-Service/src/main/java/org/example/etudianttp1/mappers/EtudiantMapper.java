package org.example.etudianttp1.mappers;

import org.example.etudianttp1.dto.RequestEtudiantDto;
import org.example.etudianttp1.dto.ResponseEtudiantDto;
import org.example.etudianttp1.entities.Etudiant;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;

@Component
public class EtudiantMapper {
    public Etudiant DTO_To_Entity(RequestEtudiantDto requestEtudiantDto) {
        Etudiant E = new Etudiant();
        BeanUtils.copyProperties(requestEtudiantDto,E);
        return E;
    }
    public ResponseEtudiantDto Entity_To_DTO(Etudiant E){
        ResponseEtudiantDto responseEtudiantDto = new ResponseEtudiantDto();
        BeanUtils.copyProperties(E,responseEtudiantDto);
        return responseEtudiantDto;
    }
}
