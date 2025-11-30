package org.example.etudianttp1.web;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;
import org.example.etudianttp1.dto.RequestEtudiantDto;
import org.example.etudianttp1.dto.ResponseEtudiantDto;
import org.example.etudianttp1.entities.Etudiant;
import org.example.etudianttp1.service.EtudiantServiceImpl;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
@OpenAPIDefinition(
        info = @Info(
                title = "API de gestion des Étudiants",
                version = "1.0",
                description = "Cette API permet de gérer les étudiants et leurs filières"
        ),
        servers = @Server(url = "http://localhost:8081")
)
@RestController
@RequestMapping("/v1/etudiants")
public class EtudiantRestController {
    private EtudiantServiceImpl etudiantService;

    public EtudiantRestController(EtudiantServiceImpl etudiantService) {
        this.etudiantService = etudiantService;
    }
    @Operation(
            summary = "Créer un nouvel étudiant",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Étudiant ajouté avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = Etudiant.class))),
                    @ApiResponse(responseCode = "400", description = "Requête invalide")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ADMIN')")
    @PostMapping
    public ResponseEntity<ResponseEtudiantDto> add (@RequestBody RequestEtudiantDto requestEtudiantDto)
    {
        ResponseEtudiantDto responseEtudiantDto =  etudiantService.addEtudiant(requestEtudiantDto);
        return ResponseEntity.ok(responseEtudiantDto);
    }

    @Operation(
            summary = "Récupérer la liste de tous les étudiants",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Liste récupérée avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = Etudiant.class))),
                    @ApiResponse(responseCode = "500", description = "Erreur serveur")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_USER')")
    @GetMapping
    public ResponseEntity <List<ResponseEtudiantDto>> getall(){
        List<ResponseEtudiantDto> etudiantDtos = etudiantService.getAllEtudiants();
        return ResponseEntity.ok(etudiantDtos);
    }

    @Operation(
            summary = "Récupérer un étudiant par ID",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Étudiant trouvé",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = ResponseEtudiantDto.class))),
                    @ApiResponse(responseCode = "404", description = "Étudiant introuvable")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_USER')")
    @GetMapping("/{id}")
    public ResponseEntity <ResponseEtudiantDto> get(@PathVariable int id){
        ResponseEtudiantDto responseEtudiantDto = etudiantService.getEtudiantById(id);
        return ResponseEntity.ok(responseEtudiantDto);
    }

    @Operation(
            summary = "Mettre à jour un étudiant",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Étudiant mis à jour avec succès"),
                    @ApiResponse(responseCode = "404", description = "Étudiant introuvable")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ADMIN')")
    @PutMapping("/{id}")
    public ResponseEntity<ResponseEtudiantDto> update(@PathVariable int id, @RequestBody RequestEtudiantDto dto) {
        ResponseEtudiantDto response = etudiantService.updateEtudiant(dto, id);
        return ResponseEntity.ok(response);
    }

    @Operation(
            summary = "Supprimer un étudiant",
            responses = {
                    @ApiResponse(responseCode = "204", description = "Étudiant supprimé avec succès"),
                    @ApiResponse(responseCode = "404", description = "Étudiant introuvable")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ADMIN')")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        etudiantService.deleteEtudiant(id);
        return ResponseEntity.noContent().build();
    }
}
