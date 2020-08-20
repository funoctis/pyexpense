CREATE TABLE IF NOT EXISTS "users" (
	"userid"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"budget"	NUMERIC,
	PRIMARY KEY("userid" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "expenses" (
	"id"	INTEGER NOT NULL UNIQUE,
	"userid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"amount"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY(userid) REFERENCES USERS(userid)
);