import sqlite3

conect = sqlite3.connect("db.sqlite3")

def llenar_facultades(cursor):
    for i in range(4):
        name = f"facultad: {i+1}" 
        cursor.execute("INSERT INTO facultad_facultad (name) VALUES (?)", (name,))

def llenar_grupos(cursor):
    num_grupo = 101
    facultad = 1
    for a in range(6):
        print(facultad)
        num_grupo = 401
        for i in range(4):     
            name = f"grupo: {num_grupo}" 
            print(f"Nombre: {name}" )
            cursor.execute("INSERT INTO grupos_grupo (name, facultad_id) VALUES (?, ?)", (name, facultad))
            num_grupo += 1
        
        facultad +=1
        
        




cursor = conect.cursor()
#llenar_facultades(cursor)
llenar_grupos(cursor)
conect.commit()

