ANALYZE "sqlite_master";
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'1');
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'2');

-- Verifique se a tabela já existe antes de criá-la
CREATE TABLE IF NOT EXISTS tb_cadastro (
    ID_CADASTRO INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME CHAR,
    TELEFONE CHAR,
    EMAIL CHAR,
    TIPO CHAR,
    APARTAMENTO CHAR,
    BLOCO CHAR
);

-- Apaga todos os registros da tabela
DELETE FROM tb_cadastro;

-- Reseta a sequência de IDs para começar em 0
DELETE FROM sqlite_sequence WHERE name = 'tb_cadastro';
