package com.internship.tool.repository;

import com.internship.tool.entity.ComplianceScore;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ComplianceScoreRepository extends JpaRepository<ComplianceScore, Long> {
}
