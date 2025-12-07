DROP DATABASE IF EXISTS nu_connect;
CREATE DATABASE IF NOT EXISTS nu_connect;
USE nu_connect;

-- Location table
DROP TABLE IF EXISTS location;
CREATE TABLE IF NOT EXISTS location (
   location_id INT PRIMARY KEY AUTO_INCREMENT,
   city VARCHAR(100) NOT NULL,
   state VARCHAR(100),
   country VARCHAR(100) NOT NULL
);

-- Major table
DROP TABLE IF EXISTS major;
CREATE TABLE IF NOT EXISTS major (
   major_id INT PRIMARY KEY AUTO_INCREMENT,
   major_name VARCHAR(100) NOT NULL UNIQUE,
   department VARCHAR(100)
);

-- Company table
DROP TABLE IF EXISTS company;
CREATE TABLE IF NOT EXISTS company (
   company_id INT PRIMARY KEY AUTO_INCREMENT,
   company_name VARCHAR(150) NOT NULL,
   industry VARCHAR(100)
);

-- Admin table
DROP TABLE IF EXISTS admin;
CREATE TABLE IF NOT EXISTS admin (
   admin_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   role VARCHAR(50)
);

-- Analyst table
DROP TABLE IF EXISTS analyst;
CREATE TABLE IF NOT EXISTS analyst (
   analyst_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   department VARCHAR(100)
);

-- Student table
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student (
   student_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   major_id INT,
   location_id INT,
   graduation_year INT,
   profile_summary TEXT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (major_id) REFERENCES major(major_id) ON DELETE SET NULL,
   FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE SET NULL
);

-- Alumni table
DROP TABLE IF EXISTS alumni;
CREATE TABLE IF NOT EXISTS alumni (
   alumni_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   graduation_year INT,
   current_role VARCHAR(100),
   company_id INT,
   field VARCHAR(100),
   bio TEXT,
   location_id INT,
   availability_status VARCHAR(20) DEFAULT 'available',
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (company_id) REFERENCES company(company_id) ON DELETE SET NULL,
   FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE SET NULL
);

-- Connection table
DROP TABLE IF EXISTS connection;
CREATE TABLE IF NOT EXISTS connection (
   connection_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   alumni_id INT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   date_connected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE,
   UNIQUE KEY unique_connection (student_id, alumni_id)
);

-- Session table
DROP TABLE IF EXISTS session;
CREATE TABLE IF NOT EXISTS session (
   session_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   alumni_id INT NOT NULL,
   session_date DATE NOT NULL,
   session_time TIME,
   topic VARCHAR(200),
   notes TEXT,
   status VARCHAR(20) DEFAULT 'scheduled',
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Application table
DROP TABLE IF EXISTS application;
CREATE TABLE IF NOT EXISTS application (
   application_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   admin_id INT,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

-- Report table
DROP TABLE IF EXISTS report;
CREATE TABLE IF NOT EXISTS report (
   report_id INT PRIMARY KEY AUTO_INCREMENT,
   reporter_id INT NOT NULL,
   reporter_type VARCHAR(20) NOT NULL,
   reported_user_id INT NOT NULL,
   reported_user_type VARCHAR(20) NOT NULL,
   reason TEXT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   admin_id INT,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

-- Community Guideline table
DROP TABLE IF EXISTS community_guideline;
CREATE TABLE IF NOT EXISTS community_guideline (
   guideline_id INT PRIMARY KEY AUTO_INCREMENT,
   guideline_text TEXT NOT NULL,
   created_by_admin_id INT NOT NULL,
   date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (created_by_admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE
);

-- Announcement table
DROP TABLE IF EXISTS announcement;
CREATE TABLE IF NOT EXISTS announcement (
   announcement_id INT PRIMARY KEY AUTO_INCREMENT,
   admin_id INT NOT NULL,
   title VARCHAR(200) NOT NULL,
   message TEXT NOT NULL,
   target_audience VARCHAR(20) DEFAULT 'all',
   date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE
);

-- Availability Schedule table
DROP TABLE IF EXISTS availability_schedule;
CREATE TABLE IF NOT EXISTS availability_schedule (
   schedule_id INT PRIMARY KEY AUTO_INCREMENT,
   alumni_id INT NOT NULL,
   day_of_week VARCHAR(20) NOT NULL,
   start_time TIME NOT NULL,
   end_time TIME NOT NULL,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Job Posting table
DROP TABLE IF EXISTS job_posting;
CREATE TABLE IF NOT EXISTS job_posting (
   posting_id INT PRIMARY KEY AUTO_INCREMENT,
   alumni_id INT NOT NULL,
   title VA
   
   RCHAR(200) NOT NULL,
   description TEXT,
   preferred_major VARCHAR(100),
   preferred_year INT,
   date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   status VARCHAR(20) DEFAULT 'active',
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_student_email ON student(email);
CREATE INDEX idx_alumni_email ON alumni(email);
CREATE INDEX idx_alumni_field ON alumni(field);
CREATE INDEX idx_connection_status ON connection(status);
CREATE INDEX idx_session_date ON session(session_date);
CREATE INDEX idx_session_status ON session(status);
CREATE INDEX idx_application_status ON application(status);
CREATE INDEX idx_report_status ON report(status);

-- Sample data for location
insert into location (city, state, country) values ('Irvine', 'California', 'United States');
insert into location (city, state, country) values ('Seattle', 'Washington', 'United States');
insert into location (city, state, country) values ('Washington', 'District of Columbia', 'United States');
insert into location (city, state, country) values ('Pensacola', 'Florida', 'United States');
insert into location (city, state, country) values ('Homestead', 'Florida', 'United States');
insert into location (city, state, country) values ('Houston', 'Texas', 'United States');
insert into location (city, state, country) values ('Washington', 'District of Columbia', 'United States');
insert into location (city, state, country) values ('Oakland', 'California', 'United States');
insert into location (city, state, country) values ('Las Cruces', 'New Mexico', 'United States');
insert into location (city, state, country) values ('San Francisco', 'California', 'United States');
insert into location (city, state, country) values ('Frederick', 'Maryland', 'United States');
insert into location (city, state, country) values ('Racine', 'Wisconsin', 'United States');
insert into location (city, state, country) values ('New Orleans', 'Louisiana', 'United States');
insert into location (city, state, country) values ('Asheville', 'North Carolina', 'United States');
insert into location (city, state, country) values ('Baltimore', 'Maryland', 'United States');
insert into location (city, state, country) values ('Vancouver', 'Washington', 'United States');
insert into location (city, state, country) values ('Berkeley', 'California', 'United States');
insert into location (city, state, country) values ('Lancaster', 'California', 'United States');
insert into location (city, state, country) values ('Colorado Springs', 'Colorado', 'United States');
insert into location (city, state, country) values ('Tucson', 'Arizona', 'United States');
insert into location (city, state, country) values ('Norman', 'Oklahoma', 'United States');
insert into location (city, state, country) values ('Tulsa', 'Oklahoma', 'United States');
insert into location (city, state, country) values ('Huntington', 'West Virginia', 'United States');
insert into location (city, state, country) values ('Evansville', 'Indiana', 'United States');
insert into location (city, state, country) values ('Laredo', 'Texas', 'United States');
insert into location (city, state, country) values ('Buffalo', 'New York', 'United States');
insert into location (city, state, country) values ('Des Moines', 'Iowa', 'United States');
insert into location (city, state, country) values ('Norfolk', 'Virginia', 'United States');
insert into location (city, state, country) values ('Lansing', 'Michigan', 'United States');
insert into location (city, state, country) values ('Falls Church', 'Virginia', 'United States');

-- Sample data for major
insert into major (major_name, department) values ('Computer Science', 'School of Engineering');
insert into major (major_name, department) values ('Data Science', 'School of Engineering');
insert into major (major_name, department) values ('Software Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Information Systems', 'School of Information');
insert into major (major_name, department) values ('Business Administration', 'School of Business');
insert into major (major_name, department) values ('Accounting', 'School of Business');
insert into major (major_name, department) values ('Finance', 'School of Business');
insert into major (major_name, department) values ('Marketing', 'School of Business');
insert into major (major_name, department) values ('Economics', 'School of Social Science');
insert into major (major_name, department) values ('Management', 'School of Social Science');
insert into major (major_name, department) values ('Psychology', 'School of Social Science');
insert into major (major_name, department) values ('Sociology', 'School of Humanities');
insert into major (major_name, department) values ('Political Science', 'School of Physical Science');
insert into major (major_name, department) values ('History', 'School of Biological Science');
insert into major (major_name, department) values ('Mathematics', 'School of Physical Science');
insert into major (major_name, department) values ('Statistics', 'School of Social Science');
insert into major (major_name, department) values ('Biology', 'School of Humanities');
insert into major (major_name, department) values ('Chemistry', 'School of Physical Sciences');
insert into major (major_name, department) values ('Physics', 'School of Biological Sciences');
insert into major (major_name, department) values ('Mechanical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Electrical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Civil Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Industrial Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Biomedical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Communication Studies', 'School of Communication');
insert into major (major_name, department) values ('Journalism', 'School of Communication');
insert into major (major_name, department) values ('Public Health', 'School of Public Health');
insert into major (major_name, department) values ('Education', 'School of Education');
insert into major (major_name, department) values ('Environmental Science', 'School of Social Studies');
insert into major (major_name, department) values ('Design & Media Arts', 'School of Arts');

