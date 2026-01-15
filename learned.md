# Initial Connection setup. 

##### you can use the code below to create and insert data into the file directly from the terminal : 
cat > requirements.txt << EOF 
fastapi 
uvicorn
pymongo
EOF -this will insert all of these dependencies into the requirements.txt file.

and to append (above one is to create or overwrite the file completely):
cat >> requirements.txt << EOF>>

### Pooling connections in the Database: 
this is basically done to store the connection object and reuse it instead of creating a new connection object for every request to the database. 

this refers to maintaining a pool(collection) of reusable connections to the database instead of opening and closing a new connection for every request.

connections are expensive(handshakes, authentication, resource allocation).

when your app needs to query it borrows a connection from the pool,
    uses it, and returns it to the pool for future use.