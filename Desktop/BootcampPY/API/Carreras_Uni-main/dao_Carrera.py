import mysql.connector

def connect_db(user,passwd):
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user= user,
            password= passwd,
            database="carreras")
        return cnx
    except mysql.connector.Error as err:
        return err

def user_query(cur,query):
    try:
        cur.execute(query)
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def añadir_carrera(cur,nombre_carrera,nota_corte,duracion):
    try:
        cur.execute("INSERT INTO carrera (Nombre_Carrera,Nota_de_corte,Duracion) VALUES (%s,%s,%s)", (nombre_carrera,nota_corte,duracion,))
    except mysql.connector.Error as err:
        print("Error al insertar la carrera (añadir_carrera):", err)
        
def añadir_carrera_id(cur,id_carrera,nombre_carrera,notadeCorte,duracion):
    try:
        cur.execute("INSERT INTO carrera (id_Carrera,Nombre_Carrera,Nota_de_corte,Duracion) VALUES (%s,%s,%s,%s) ", (id_carrera,nombre_carrera,notadeCorte,duracion,))
    except mysql.connector.Error as err:
        print("Error al insertar la carrera (añadir_carrera_id): ", err)
        
def modificar_carrera(cursor,id_carrera,nombre_carrera,notadeCorte,duracion):
    try:
        borrar_carrera(cursor,id_carrera)
    except:
        pass
    try:
        añadir_carrera_id(cursor,id_carrera,nombre_carrera,notadeCorte,duracion)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print("Error al modificar la carrera en (modificar_carrera) :", err) 
         
def ver_carreras(cur):
    try:
        cur.execute("SELECT * FROM carrera")
        return cur.fetchall()
    except mysql.connector.Error as err:
        print("Error al ver las carreras :", err)
        
def borrar_carrera(cursor,id_carrera):
    try:         
        cursor.execute("SELECT Nombre_Carrera FROM carrera WHERE id_Carrera = %s", (id_carrera,))
        resultados = cursor.fetchall()
        cursor.execute("DELETE from carrera WHERE id_Carrera = %s", (id_carrera,))
        return resultados
    except mysql.connector.Error as err:
        print("Error al borrar la carrera: ",err)  