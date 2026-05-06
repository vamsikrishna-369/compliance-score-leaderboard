package com.internship.tool.service;

import com.internship.tool.entity.ComplianceScore;
import com.internship.tool.repository.ComplianceScoreRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ComplianceScoreService {

    @Autowired
    private ComplianceScoreRepository repository;

    // GET ALL
    public List<ComplianceScore> getAll() {
        return repository.findAll();
    }
}