class carrera:
    def __init__(self, nombre_carrera, id_carrera="", nota_corte="", duracion=""):
        self.__id_carrera = id_carrera
        self.__nombre_carrera = nombre_carrera
        self.__nota_corte = nota_corte
        self.__duracion = duracion
# Métodos getter y setter para nombre_carrera
    def get_nombre_carrera(self):
        return self.__nombre_carrera
    def set_nombre_carrera(self, nuevo_nombre):
        self.__nombre_carrera = nuevo_nombre
    def get_id_carrera(self):
        return self.__id_carrera
    def set_id_carrera(self, nuevo_id):
        self.__id_carrera = nuevo_id
    def get_nota_corte(self):
        return self.__nota_corte
    def set_nota_corte(self, nueva_nota):
        self.__nota_corte = nueva_nota
    def get_duracion(self):
        return self.__duracion
    def set_duracion(self, nueva_duracion):
        self.__duracion = nueva_duracion
    def getter(self):
        return self.__nombre_carrera
    def setter(self, nuevo_nombre):
        self.__nombre_carrera = nuevo_nombre 
    def getter_id(self):
        return self.__id_carrera
    def __str__(self):
        if  1 ==  len(str(self.__id_carrera)):
            return f"[{self.__id_carrera}]  -> {self.__nombre_carrera} - Nota de corte: {self.__nota_corte} - Duración: {self.__duracion} años"
        elif 2 == len(str(self.__id_carrera)):
            return f"[{self.__id_carrera}] -> {self.__nombre_carrera} - Nota de corte: {self.__nota_corte} - Duración: {self.__duracion} años"
#end of file carrera.py