BEGIN TRANSACTION;
ANALYZE "sqlite_master";
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'2');
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'1');
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'2');
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'1');
INSERT INTO "sqlite_stat1" VALUES('tb_cadastro',NULL,'2');
CREATE TABLE tb_cadastro (
    ID_CADASTRO INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME CHAR,
    TELEFONE CHAR,
    EMAIL CHAR,
    TIPO CHAR,
    APARTAMENTO CHAR,
    BLOCO CHAR
);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('tb_cadastro',2);
COMMIT;
