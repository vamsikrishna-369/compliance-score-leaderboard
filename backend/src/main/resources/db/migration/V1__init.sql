CREATE TABLE compliance_record (
                                   id BIGINT PRIMARY KEY AUTO_INCREMENT,
                                   title VARCHAR(255) NOT NULL,
                                   description TEXT,
                                   score INT,
                                   status VARCHAR(50),
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_compliance_title ON compliance_record(title);
CREATE INDEX idx_compliance_status ON compliance_record(status);