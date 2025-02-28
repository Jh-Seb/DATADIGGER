import shared_state

def generar_reporte():
    # Accedemos a la variable x actualizada
    titulo_actual = shared_state.titulo
    parrafos_actuales = shared_state.parrafos
    print("Titulo", titulo_actual)
    print(parrafos_actuales)
    # Aquí iría el resto del código para generar el reporte

if __name__ == '__main__':
    generar_reporte()
