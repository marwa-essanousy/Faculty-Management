package org.example.etudianttp1.dto;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RequestEtudiantDto {
    private String nom;
    private String prenom;
    private String cne;
    private Integer idFiliere;
}
