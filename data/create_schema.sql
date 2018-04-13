CREATE TABLE OrderTable(OID INTEGER PRIMARY KEY, Status TEXT, CID INTEGER NOT NULL,
                FOREIGN KEY(CID) REFERENCES Cart(CID));

CREATE TABLE Item(IID INTEGER PRIMARY KEY, Price REAL, SID INTEGER NOT NULL, QUANTITY INTEGER, FOREIGN KEY(SID) REFERENCES Store(SID));

CREATE TABLE CartItem(ID INTEGER PRIMARY KEY, 
                CID INTEGER,
                IID INTEGER);

CREATE TABLE Cart(CID INTEGER PRIMARY KEY, 
                IID INTEGER, 
                Total REAL, 
                SID INTEGER, 
                UID INTEGER,
                FOREIGN KEY(IID) REFERENCES Item(IID),
                FOREIGN KEY(SID) REFERENCES Store(SID),
                FOREIGN KEY(UID) REFERENCES User(UID));

CREATE TABLE Store(SID INTEGER PRIMARY KEY, Threshold REAL, Address TEXT, Address2 TEXT, City Text, State Text, Zip INTEGER, OID INTEGER,
                FOREIGN KEY(OID) REFERENCES OrderTable(OID));

CREATE TABLE User(
   UID INTEGER PRIMARY KEY,
   UserLevel TEXT,
   Username TEXT UNIQUE,
   Password TEXT,
   Email TEXT,
   Address TEXT,
   City Text,
   State Text,
   Zip Text,
   FirstName TEXT,
   LastName TEXT,
   OID INTEGER);

CREATE TABLE PreMatch(PMID INTEGER PRIMARY KEY, UID1 INTEGER, UID2 INTEGER, Status INTEGER,
                FOREIGN KEY(UID1) REFERENCES User(UID),
                FOREIGN KEY(UID2) REFERENCES User(UID));

CREATE TABLE Report(RID INTEGER PRIMARY KEY, Author INTEGER, Subject INTEGER, Comment TEXT, TimeStamp DATETIME,
                FOREIGN KEY(Author) REFERENCES User(UID),
                FOREIGN KEY(Subject) REFERENCES User(UID));

CREATE TABLE Review(RVID INTEGER PRIMARY KEY, Author INTEGER, Subject INTEGER, Comment TEXT, Rating INTEGER,
                FOREIGN KEY(Author) REFERENCES User(UID),
                FOREIGN KEY(Subject) REFERENCES User(UID));

CREATE TABLE Invoice(IVID INTEGER PRIMARY KEY, OID INTEGER, Total REAL, UID INTEGER, ShippingUser INTEGER, SID INTEGER, Status TEXT, TimeStamp DATETIME,
                FOREIGN KEY(OID) REFERENCES OrderTable(OID),
                FOREIGN KEY(UID) REFERENCES User(UID)
                FOREIGN KEY(ShippingUser) REFERENCES User(UID),
                FOREIGN KEY(SID) REFERENCES Store(SID));

CREATE TABLE userOrder(
                user_id INTEGER,
                order_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES User(UID) ON DELETE CASCADE,
                FOREIGN KEY(order_id) REFERENCES OrderTable(OID) ON DELETE CASCADE
);
/*
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('ckhoury','','ckhoury@wisc.edu','44 Clay Street','Yonkers','NY','10701','Cam','Khoury');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('bschwab','','bschwab@wisc.edu','28 E. Chapel Lane','Nashua','NH','03060','Brad','Schwab');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('ppape','','ppape@wisc.edu','14 Griffin Street','New Britain','CT','06051','Phil','Pape');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('tlarson','','tlarson@wisc.edu','9714 Jackson Street','Rossville','GA','30741','Tyler','Larson');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('jgibbs','','jgibbs@wisc.edu','7959 East Annadale Lane','Taylors','SC','29687','Jackson','Gibbs');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('ttevich','','ttevich@wisc.edu','7593 Alderwood Lane','Middle River','MD','21220','Tyler','Tevich');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('esolis','','esolis@wisc.edu','891 College Court','Lynn','MA','01902','Eric','Solis');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('aschultz','','aschultz@wisc.edu','29 Locust Rd.','Ormond Beach','FL','32174','Adam','Schultz');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('kkrueger','','kkrueger@wisc.edu','53 Silver Spear Street','Endicott','NY','13760','Kyle','Krueger');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('mserebin','','mserebin@wisc.edu','57 Smith Store Street','Lake Mary','FL','32746','Molly','Serebin');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('ahoyer','','ahoyer@wisc.edu','860 Leatherwood Lane','Benton Harbor','MI','49022','Amanda','Hoyer');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('bsmith','','bsmith@wisc.edu','450 Sulphur Springs Dr.','Danvers','MA','01923','Ben','Smith');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('jlopez','','jlopez@wisc.edu','46 Fieldstone Drive','Santa Monica','CA','90403','Jason','Lopez');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('sjackson','','sjackson@wisc.edu','18 South Gonzales Ave.','Chicopee','MA','01020','Sam','Jackson');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('bkappel','','bkappel@wisc.edu','359 Henry Lane','New Philadelphia','OH','44663','Brandon','Kappel');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('dadams','','dadams@wisc.edu','374 Orange Street','Chaska','MN','553318','David','Adams');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('sjobs','','sjobs@wisc.edu','9780 Nicolls Rd.','Greenfield','IN','46140','Steve','Jobs');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('bgates','','bgates@wisc.edu','85 Anderson St.','Beverly','MA','01020','Bill','Gates');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('dturner','','dturner@wisc.edu','8 Trenton Ave','Sunnyside','NY','11104','Daniel','Turner');
INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES ('mjohnson','','mjohnson@wisc.edu','47 Foxrun Street','Henrico','VA','23228','Mark','Johnson');
*/
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('1', '128', '1', '1');
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('2', '256', '2', '1');
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('3', '512', '3', '2');
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('1', '768', '1', '2');
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('2', '1024', '2', '3');
INSERT INTO Cart(IID , Total , SID , UID ) VALUES ('3', '2048', '2', '3');

INSERT INTO Item(Price, SID, QUANTITY) VALUES ('200', '1', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('600', '1', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('800', '1', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('200', '2', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('400', '2', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('600', '2', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('200', '3', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('400', '3', '4');
INSERT INTO Item(Price, SID, QUANTITY) VALUES ('600', '3', '4');

INSERT INTO CartItem(CID, IID) VALUES ('1', '1');
INSERT INTO CartItem(CID, IID) VALUES ('1', '2');
INSERT INTO CartItem(CID, IID) VALUES ('1', '3');
INSERT INTO CartItem(CID, IID) VALUES ('1', '4');
INSERT INTO CartItem(CID, IID) VALUES ('1', '5');




