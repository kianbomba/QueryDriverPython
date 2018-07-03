# Python MYSQL-CONNECTION WRAPPER

This is just a small wrapper of mysql-connector that help to perform magic on the database
easily

Hope you like it :D 

### usage
```python

from Core.Connection import Connection

#
#
#
#
#
#
cnx = Connection("/path/to/db.config.json", True)

sql = "SELECT * FROM `HelloWorld`"
result = cnx.fetchall(sql)

for row in result:
    for field_name in row:
        print(row[field_name])


```


#### author Kianbomba
THIS IS GITHOOK TEST
