-- Banco
CREATE DATABASE IF NOT EXISTS Projeto;
USE Projeto;

-- 1. Espécies
CREATE TABLE especies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_comum VARCHAR(100),
    nome_cientifico VARCHAR(150),
    classificacao VARCHAR(50),
    origem VARCHAR(100)
);

-- 2. Habitats
CREATE TABLE habitats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    tipo VARCHAR(50),
    temperatura_media DECIMAL(5,2),
    umidade_media DECIMAL(5,2)
);

-- 3. Tratadores
CREATE TABLE tratadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    especialidade VARCHAR(100),
    telefone VARCHAR(20)
);

-- 4. Animais
CREATE TABLE animais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    sexo VARCHAR(10),
    idade INT,
    especie_id INT,
    habitat_id INT,
    tratador_id INT,
    FOREIGN KEY (especie_id) REFERENCES especies(id),
    FOREIGN KEY (habitat_id) REFERENCES habitats(id),
    FOREIGN KEY (tratador_id) REFERENCES tratadores(id)
);

-- 5. Alimentações
CREATE TABLE alimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT,
    tipo_racao VARCHAR(100),
    quantidade_kg DECIMAL(5,2),
    horario TIME,
    FOREIGN KEY (animal_id) REFERENCES animais(id)
);

-- 6. Visitas Veterinárias
CREATE TABLE visitas_veterinarias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT,
    data_visita DATE,
    observacoes TEXT,
    FOREIGN KEY (animal_id) REFERENCES animais(id)
);

-- Espécies
INSERT INTO especies (nome_comum, nome_cientifico, classificacao, origem) VALUES
('Leão', 'Panthera leo', 'Mamífero', 'África'),
('Arara Azul', 'Anodorhynchus hyacinthinus', 'Ave', 'América do Sul'),
('Tigre de Bengala', 'Panthera tigris tigris', 'Mamífero', 'Índia'),
('Elefante Africano', 'Loxodonta africana', 'Mamífero', 'África'),
('Pinguim-de-Adélia', 'Pygoscelis adeliae', 'Ave', 'Antártica'),
('Jiboia', 'Boa constrictor', 'Réptil', 'América do Sul'),
('Jacaré-do-Pantanal', 'Caiman yacare', 'Réptil', 'Brasil'),
('Urso Polar', 'Ursus maritimus', 'Mamífero', 'Ártico'),
('Canguru Vermelho', 'Macropus rufus', 'Mamífero', 'Austrália');

-- Habitats
INSERT INTO habitats (nome, tipo, temperatura_media, umidade_media) VALUES
('Savana Artificial', 'Terrestre', 30.0, 40.0),
('Aviário Tropical', 'Aéreo', 27.5, 60.0),
('Floresta Tropical', 'Terrestre', 28.0, 80.0),
('Pantanal Artificial', 'Terrestre', 26.0, 70.0),
('Região Glacial', 'Terrestre', -5.0, 60.0),
('Savana Australiana', 'Terrestre', 35.0, 20.0),
('Terrário Reptiliano', 'Terrestre', 30.0, 50.0),
('Aviário Polar', 'Aéreo', 0.0, 40.0),
('Planície Seca', 'Terrestre', 32.0, 25.0);

-- Tratadores
INSERT INTO tratadores (nome, especialidade, telefone) VALUES
('Carlos Silva', 'Mamíferos', '11999990001'),
('Ana Souza', 'Aves Tropicais', '11999990002'),
('Bruno Oliveira', 'Mamíferos de grande porte', '11999990003'),
('Fernanda Lima', 'Répteis e Anfíbios', '11999990004'),
('Thiago Rocha', 'Aves de clima frio', '11999990005'),
('Juliana Torres', 'Animais australianos', '11999990006'),
('Gabriel Martins', 'Felinos selvagens', '11999990007'),
('Rafael Costa', 'Animais do Pantanal', '11999990008');

-- Animais
INSERT INTO animais (nome, sexo, idade, especie_id, habitat_id, tratador_id) VALUES
('Simba', 'Macho', 5, 1, 1, 1),
('Azulão', 'Fêmea', 3, 2, 2, 2),
('Shere Khan', 'Macho', 7, 3, 1, 7),     
('Dumbo', 'Macho', 12, 4, 5, 3),         
('Pingo', 'Fêmea', 2, 5, 8, 5),          
('Sinuosa', 'Fêmea', 4, 6, 7, 4),        
('Pantaneiro', 'Macho', 8, 7, 4, 8),     
('Ártico', 'Macho', 5, 8, 5, 3),         
('Skippy', 'Macho', 6, 9, 6, 6);

-- Alimentações
INSERT INTO alimentacoes (animal_id, tipo_racao, quantidade_kg, horario) VALUES
(1, 'Carne fresca', 5.00, '12:00:00'),
(2, 'Sementes e frutas', 0.50, '09:00:00');

-- Visitas veterinárias
INSERT INTO visitas_veterinarias (animal_id, data_visita, observacoes) VALUES
(1, '2025-06-10', 'Animal saudável. Nenhuma anomalia detectada.'),
(2, '2025-06-11', 'Leve resfriado, receitado suplemento vitamínico.');

select * from animais