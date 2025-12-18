import os
import sqlite3

def procesar_datos_usuario_complejo(usuarios_lista, modo_admin):
    # Esta función hace DE TODO: Valida, guarda, ejecuta comandos y calcula
    # Es el típico código "Spaghetti" difícil de mantener y vulnerable.
    
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    
    for usuario in usuarios_lista:
        if usuario['activo']:
            if modo_admin:
                print("Procesando admin...")
                #  PELIGRO: Inyección SQL
                # NLOC suma, Complejidad suma (if dentro de for)
                query = "SELECT * FROM users WHERE name = '" + usuario['nombre'] + "'"
                cur.execute(query)
                datos = cur.fetchone()
                
                if datos:
                    if usuario['rol'] == 'superadmin':
                        #  PELIGRO: Inyección de Comandos
                        # Más anidación = Más complejidad
                        cmd = "echo Procesando " + usuario['nombre']
                        os.system(cmd) 
                    else:
                        print("Admin normal")
                else:
                    print("Usuario no encontrado en DB")
            
            else:
                # Lógica para usuarios normales
                if usuario['tipo'] == 'invitado':
                    pass
                elif usuario['tipo'] == 'registrado':
                    #  PELIGRO: Eval inseguro
                    calculo = usuario.get('formula', '1+1')
                    try:
                        res = eval(calculo)
                        print(f"Resultado: {res}")
                    except:
                        print("Error en calculo")
        else:
            print("Usuario inactivo")
            
    con.close()
    return True