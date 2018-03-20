CREATE TABLE OrderTable(OID INTEGER PRIMARY KEY, Status TEXT, CID INTEGER NOT NULL, 
                FOREIGN KEY(CID) REFERENCES Cart(CID));

CREATE TABLE Item(IID INTEGER PRIMARY KEY, Price REAL, SID INTEGER NOT NULL, QUANTITY INTEGER, FOREIGN KEY(SID) REFERENCES Store(SID));

CREATE TABLE Cart(CID INTEGER PRIMARY KEY, IID INTEGER, Total REAL, SID INTEGER, UID INTEGER, 
                FOREIGN KEY(IID) REFERENCES Item(IID),
                FOREIGN KEY(SID) REFERENCES Store(SID),
                FOREIGN KEY(UID) REFERENCES User(UID));
                
CREATE TABLE Store(SID INTEGER PRIMARY KEY, Threshold REAL, Address TEXT, Address2 TEXT, City Text, State Text, Zip INTEGER, OID INTEGER,
                FOREIGN KEY(OID) REFERENCES OrderTable(OID));
                
CREATE TABLE User(
   UID INTEGER PRIMARY KEY,
   Username TEXT,
   Password TEXT,
   Email TEXT,
   Address TEXT,
   Address2 TEXT,
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
					