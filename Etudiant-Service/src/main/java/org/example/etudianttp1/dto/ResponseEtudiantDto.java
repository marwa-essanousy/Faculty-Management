package org.example.etudianttp1.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ResponseEtudiantDto {
    private Integer idEtudiant;
    private String nom;
    private String prenom;
    private String cne;
    private Integer idFiliere;
    private FiliereDto filiere;
}
