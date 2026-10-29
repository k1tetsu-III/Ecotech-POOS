def cargar_empleados(departamento_demo):
    datos = [("Ana Torres", "ana@ecotech.example")]

    for nombre, correo in datos:
        existente = EmpleadoDAO.buscar_por_correo(correo)
        if existente is not None:
            print(f"Ya existe: {correo}")
            continue
        empleado = Empleado(nombre, correo, departamento_demo)
        EmpleadoDAO.insertar(empleado)
        print(f"Creado: {correo}")
