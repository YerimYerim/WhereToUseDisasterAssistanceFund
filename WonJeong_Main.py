from GetData import GetDataFromURL, rows

GetDataFromURL()

for i in rows:
    if rows[i] == '채움아이학원':
        print(rows[i])