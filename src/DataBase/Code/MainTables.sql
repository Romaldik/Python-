-- Таблиця TrainingProgram
CREATE TABLE TrainingProgram (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    duration INTERVAL NOT NULL
);

-- Таблиця Team
CREATE TABLE Team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(255) NOT NULL,
    training_program_id INT,
    period_of_sponsorship INTERVAL NOT NULL,
    FOREIGN KEY (training_program_id) REFERENCES TrainingProgram(id)
);

-- Таблиця Coach
CREATE TABLE Coach (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    Nickname VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES Team(id)
);

-- Таблиця Player
CREATE TABLE Player (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    Nickname VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    Role VARCHAR(255),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES Team(id)
);

-- Таблиця Sponsor
CREATE TABLE Sponsor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Таблиця Team_Sponsor (зв'язок між Team та Sponsor)
CREATE TABLE Team_Sponsor (
    team_id INT,
    sponsor_id INT,
    PRIMARY KEY (team_id, sponsor_id),
    FOREIGN KEY (team_id) REFERENCES Team(id),
    FOREIGN KEY (sponsor_id) REFERENCES Sponsor(id)
);

-- Таблиця Tournament
CREATE TABLE Tournament (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL,
    location VARCHAR(255) NOT NULL,
    prize_money DECIMAL(10, 2) NOT NULL
);

-- Таблиця Tournament_Team (зв'язок між Tournament та Team)
CREATE TABLE Tournament_Team (
    tournament_id INT,
    team_id INT,
    PRIMARY KEY (tournament_id, team_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id),
    FOREIGN KEY (team_id) REFERENCES Team(id)
);

-- Таблиця Tournament_Sponsor (зв'язок між Tournament та Sponsor)
CREATE TABLE Tournament_Sponsor (
    tournament_id INT,
    sponsor_id INT,
    PRIMARY KEY (tournament_id, sponsor_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id),
    FOREIGN KEY (sponsor_id) REFERENCES Sponsor(id)
);

-- Таблиця Staff
CREATE TABLE Staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    role VARCHAR(255) NOT NULL
);


-- Таблиця Team_Staff (зв'язок між Team та Staff)
CREATE TABLE Team_Staff (
    team_id INT,
    staff_id INT,
    PRIMARY KEY (team_id, staff_id),
    FOREIGN KEY (team_id) REFERENCES Team(id),
    FOREIGN KEY (staff_id) REFERENCES Staff(id)
);