package com.internship.tool.controller;

import com.internship.tool.entity.ComplianceScore;
import com.internship.tool.service.ComplianceScoreService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/compliance")
@CrossOrigin(origins = "*")
public class ComplianceScoreController {

    @Autowired
    private ComplianceScoreService service;

    // GET ALL API
    @GetMapping("/all")
    public List<ComplianceScore> getAll() {
        return service.getAll();
    }
}