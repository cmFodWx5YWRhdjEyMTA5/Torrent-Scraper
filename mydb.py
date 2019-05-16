import sqlite3, json, os, time

def insert_data(details):
    try:
        conn = sqlite3.connect('torrent.sqlite3')
        c = conn.cursor()
        if details['seeds'] == '-':
            return
        if 'seeds' not in details and 'added_date' not in details:
            name = details['name']
            size = details['size']
            hash = details['hash']
            c.execute('Insert into data(Name, Size, Hash) values (?,?,?)', [name, size,hash])
            conn.commit()
        elif 'seeds' not in details:
            name = details['name']
            size = details['size']
            hash = details['hash']
            date = details['added_date']
            c.execute('Insert into data(Name, Size, Hash, Date) values (?,?,?,?)', [name, size,hash, date])
            conn.commit()
        elif 'added_date' not in details:
            name = details['name']
            size = details['size']
            hash = details['hash']
            seeds = details['seeds']
            c.execute('Insert into data(Name, Size, Seeds, Hash) values (?,?,?,?)', [name, size, seeds, hash])
            conn.commit()
        else:
            name = details['name']
            size = details['size']
            hash = details['hash']
            date = details['added_date']
            seeds = details['seeds']
            c.execute('Insert into data(Name, Size, Seeds, Hash, Date) values (?,?,?,?,?)', [name, size, seeds, hash, date])
            conn.commit()
    except sqlite3.IntegrityError:
        print("Same Hash is occure")


def readFile(dirname):
    dir_count = os.listdir('cache/database/' + dirname.lower() +"/")
    number_files = len(dir_count)
    print("Total Files :", number_files)
    count = 0
    file_count = 0
    while True:
        count+=1
        path = "cache/database/" +dirname.lower()+'/' + dirname.lower() +'torrent_' + str(count) +'_.json'
        if os.path.exists(path):
            file_count +=1
            print("Reading FIle:",path)
            with open(path) as file:
                read = file.read()
                data_list = json.loads(read)
                for  data in data_list:
                    print("Inserting data into database of file:",file_count)
                    time.sleep(1)
                    insert = insert_data(data)
            if file_count == number_files:
                break


a = readFile('thepiratebay')
# Commands for create table in database
# CREATE TABLE data (Name TEXT, Size TEXT, Seeds INT, Hash TEXT UNIQUE, Date Text);
#
