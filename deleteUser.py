import requests
import sqlite3 as sql
import sys

def main():

    try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()
            # inserted = con.execute("SELECT * FROM User WHERE Username = (?)", (users[i][0],))
            # for row in inserted:
            #     if row[1] == users[i][0]:  print("Found " +  users[i][0])

            deleted = con.execute("DELETE FROM User WHERE UID = (?)", (sys.argv[1],))
            print("Deleted: " + str(deleted.rowcount) + " entries.")
            con.commit()

    except Exception as e:
         con.rollback()
         print(e)

    finally:
        con.close()

if __name__ == '__main__':
    main()
