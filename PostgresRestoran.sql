CREATE TABLE Restorani(
id_restoran INTEGER PRIMARY KEY NOT NULL,
naziv_restorana VARCHAR(50) NOT NULL,
adresa VARCHAR(70) NOT NULL);

/*DROP TABLE Restorani*/
INSERT INTO Restorani (id_restoran, naziv_restorana, adresa)
VALUES
	(101, 'Walter', 'Strahinjica Bana 57'),
	(102,'Hanan Food Shawarma','Dositejeva 1a'),
	(103,'Wok Republic','Francuska 5'),
	(104,'Oklagija Takovska','Takovska 33'),
	(105,'Tortilla Casa Centar','Cika Ljubina 6');

SELECT * FROM Restorani
	

CREATE TABLE Jelovnici(
id_jela INTEGER NOT NULL,
jelo VARCHAR(40) NOT NULL,
cena FLOAT NOT NULL,
id_restoran INTEGER NOT NULL,
PRIMARY KEY(id_jela),
FOREIGN KEY(id_restoran) REFERENCES Restorani(id_restoran));
/*DROP TABLE Jelovnici*/


INSERT INTO Jelovnici(id_jela, jelo, cena,id_restoran)
VALUES
	(10117,'Sarajevski cevap 10 komada',650.00,101),
	(10116,'Sarajevski cevap 5 komada',360.00,101),
  	(10201,'Falafel sendvic mali',470.00,102),
  	(10203,'Falafel obrok',950.00,102),
	(10353,'Pad See Ew Noodles',740.00,103),
	(10354,'Chopped Beef Rice',750.00,103),
	(10412,'Sarma od zelja',300.00,104),
	(10413,'Juneci gulas',330.00,104),
	(10589,'Taquitos',330.00,105),
	(10590,'Mini Chimichangas',410.00,105);

SELECT * FROM Jelovnici

CREATE TABLE Porudzbina(
br_porudzbine INTEGER NOT NULL,
ime_prezime VARCHAR(30),
adresa VARCHAR(50),
datum_porudzbine DATE NOT NULL,
id_jela INTEGER NOT NULL,
id_restoran INTEGER NOT NULL,
PRIMARY KEY(br_porudzbine),
FOREIGN KEY (id_jela) REFERENCES Jelovnici(id_jela),
FOREIGN KEY (id_restoran) REFERENCES Restorani(id_restoran));

/*DROP TABLE Porudzbina*/

INSERT INTO Porudzbina(br_porudzbine,ime_prezime,adresa,datum_porudzbine,id_jela,id_restoran)
VALUES
	(1,'Anja Milovanovic','Venizelosova 6','23-04-2023',10117,101),
	(2,'Petar Petrovic','Cara Dusana 79','04-05-2023',10201,102),
	(3,'Marko Markovic','Takovska 14','13-04-2023',10590,105),
	(4,'Ivana Ivanovic','Dzordza Vasingtona 15','16-04-2023',10117,101),
	(5,'Nikola Nikolic','Venizelosova 48','15-05-2023',10354,103),
	(6,'Stefan Stefanovic','Knjeginje Ljubice 18','22-04-2023',10201,102),
	(7,'Marija Marjanovic','Dositejeva 7','23-04-2023',10589,105),
	(8,'Tijana Tijanic','Gundulicev Venac 28','28-04-2023',10117,101),
	(9,'Uros Urosevic','Dunavska 35','06-05-2023',10412,104),
	(10,'Jovan Jovanovic','Cara Dusana 17','07-05-2023',10412,104);

SELECT * FROM Porudzbina



