import dao_Carrera as dao
import carrera as c
import os
import requests as req
import mysql.connector
carreras=[]
start_program = False
# Código para activar la negrita
NEGRITA = '\033[1m'
# Código para restablecer el formato (desactiva la negrita)
RESET = '\033[0m'
# gestor_carreras.py
conexion = None
def connect_db():
    user = input("input user name: ")
    passwd = input("input your password: ") 
    cnx = dao.connect_db(user, passwd)
    return cnx
conexion = connect_db()
if isinstance(conexion, mysql.connector.Error):
    print(f"--- Error: {conexion.msg}")            # Mensaje de error
else:
    print("---Conexión establecida---")
    start_program = True
    cursor = conexion.cursor()

def pausa():
    input("\nPresiona cualquier tecla para continuar...")

def mostrar_menu():
    print("\n--- MENÚ GESTOR DE CARRERAS ---")
    print("1. Añadir carrera")
    print("2. Actualizar carrera")
    print("3. Ver carreras")
    print("4. Borrar carrera")
    print("5. Salir")

def añadir_carrera(cursor):
    nombre = input("Introduce el nombre de la carrera: ")
    duracion = input("Introduce la duración de la carrera (en años): ") 
    try:
        nota_corte = float(input("Introduce la nota de corte de la carrera: "))
    except ValueError:
        print("la nota de corte debe ser un número.")
        try:
            nota_corte = float(input("Introduce la nota de corte de la carrera: "))
        except ValueError:
            print("la nota de corte debe ser un número.")
            return
    if nota_corte < 0 or nota_corte > 14:
        print("la nota de corte debe estar entre 0 y 14.")
    else:
        nueva_carrera = c.carrera(nombre,"",nota_corte,duracion)
        dao.añadir_carrera(cursor, nueva_carrera.getter(),nueva_carrera.get_nota_corte(),nueva_carrera.get_duracion())
        conexion.commit()
        print(f"\nla carrera {NEGRITA}{nombre}{RESET} se ha añadido.\n")
    pausa()

def actualizar_carrera(cursor):
    id_carrera = input("Introduce el ID de la carrera a actualizar: ")
    nombre_carrera = input("Introduce el nuevo nombre de la carrera: ")
    notaDeCorte = input("Introduce la nueva nota de corte de la carrera: ")
    duracion = input("Introduce la nueva duración de la carrera (en años): ")
    modificar_carrera = c.carrera(nombre_carrera,id_carrera,notaDeCorte,duracion)
    resultados = dao.modificar_carrera(cursor,modificar_carrera.getter_id(),modificar_carrera.getter(),modificar_carrera.get_nota_corte(),modificar_carrera.get_duracion())
    conexion.commit()
    if id_carrera in [str(i.getter_id()) for i in carreras]:  
        for i in resultados:
            print(f"\nLa carrera {NEGRITA}{i[0]}{RESET} se ha modificado a {NEGRITA}{nombre_carrera}{RESET}.\n")
    else:
        print("\nCarrera no encontrada.\n")
    pausa()

def ver_carreras(cursor):
    del carreras[:]
    resultados = dao.ver_carreras(cursor)
    if not resultados:
        print("No hay carreras registradas.")
    else:
        print("\n--- LISTA DE CARRERAS ---")
        for (id_Carrera,Nombre_Carrera,nota_corte,duracion) in resultados:
            carreras.append(c.carrera(Nombre_Carrera,id_Carrera,duracion,nota_corte))

def borrar_carrera(cursor):
    id_carrera = input("Introduce el ID de la carrera a borrar: ")
    borrar_carrera = c.carrera("",id_carrera)
    resultados = dao.borrar_carrera(cursor,borrar_carrera.getter_id())
    conexion.commit()
    if not resultados:
        print("\nCarrera no encontrada.\n")
    else:
        for i in resultados:
            print(f"\nLa carrera {NEGRITA}{i[0]}{RESET} se ha borrado.\n")
    pausa()
    
#query personalizada 
def user_query(cursor):
    query = input("Introduce la consulta SQL: ")
    resultados=dao.user_query(cursor,query)
    if not resultados:
        print("No hay resultados.")
    else:
        for row in resultados:
            print(row)
    pausa()
# Programa principal
while start_program:
    os.system('cls' if os.name == 'nt' else 'clear')
    mostrar_menu()
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        añadir_carrera(cursor)
    elif opcion == "2":
        actualizar_carrera(cursor)
    elif opcion == "3":
        listar_carreras = req.get("http://127.0.0.1:5000//ver/carreras")
        for i in carreras:
            print(i)    
        input("press any key to continue.....")
    elif opcion == "4":
        borrar_carrera(cursor)
    elif opcion == "5":
        cursor.close()
        conexion.close()
        print("\nSaliendo del programa...\n")
        start_program = False
    elif opcion == "0":
        user_query(cursor)
    else:
        print("Opción no válida.")
