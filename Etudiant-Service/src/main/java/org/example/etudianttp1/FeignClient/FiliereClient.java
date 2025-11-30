package org.example.etudianttp1.FeignClient;


import org.example.etudianttp1.dto.FiliereDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "FILIERE-SERVICE") // nom identique à APP_NAME en Flask
public interface FiliereClient {
    @GetMapping("/filieres/{id}")
    FiliereDto getFiliereById(@PathVariable("id") Integer id);
}