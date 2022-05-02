CREATE TABLE IF NOT EXISTS refugiados (
	id_refugiados serial,
	passagem_fronteira varchar(40),
	via varchar(30),
	data date,
	direcao_polonia varchar (40),
	cidadania varchar(2),
	checkin integer,
	checkout integer,
	CONSTRAINT refugiados_pk PRIMARY KEY (id_refugiados)
);
