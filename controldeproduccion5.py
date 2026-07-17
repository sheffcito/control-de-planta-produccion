import os
import json

# Nombre del archivo donde se guardarán los datos en el celular
ARCHIVO_DATOS = "produccion.txt"

# Estructura base por defecto
datos_produccion = {
    "pauta_mensual": {"Semana 1": 0, "Semana 2": 0, "Semana 3": 0, "Semana 4": 0},
    "produccion": {
        f"Semana {s}": {
            dia: []  # Lista de registros detallados por día
            for dia in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        } for s in range(1, 5)
    }
}

def guardar_datos():
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(datos_produccion, f, indent=4)

def cargar_datos():
    global datos_produccion
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            datos_produccion = json.load(f)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def leer_entero_seguro(mensaje_input):
    """MEJORADO: Si el usuario ingresa texto, muestra alerta y le permite reintentar el MISMO campo de inmediato."""
    while True:
        entrada = input(mensaje_input).strip()
        try:
            return int(entrada)
        except ValueError:
            print("\n⚠️  [ALERTA]: Ingresaste un valor no válido (debe ser un número entero).")
            print("👉 Por favor, vuelve a intentarlo.\n")

def obtener_ultima_caja_global():
    max_caja = 0
    for semana, dias in datos_produccion["produccion"].items():
        for dia, registros in dias.items():
            for r in registros:
                if "caja_final" in r and r["caja_final"] > max_caja:
                    max_caja = r["caja_final"]
    return max_caja

def configurar_pauta():
    limpiar_pantalla()
    print("=== CONFIGURAR PAUTA DEL MES ===")
    for semana in datos_produccion["pauta_mensual"].keys():
        meta = leer_entero_seguro(f"Ingrese meta para la {semana}: ")
        datos_produccion["pauta_mensual"][semana] = meta
    guardar_datos()
    print("\n✅ Pauta mensual guardada y respaldada.")
    input("\nPresione Enter para volver...")

def registrar_dia():
    limpiar_pantalla()
    print("=== REGISTRAR PRODUCCIÓN DIARIA ===")
    print("1. Semana 1 | 2. Semana 2 | 3. Semana 3 | 4. Semana 4")
    opc_sem = input("Seleccione Semana (1-4): ")
    semana_sel = f"Semana {opc_sem}"
    
    if semana_sel not in datos_produccion["produccion"]:
        print("❌ Semana no válida.")
        input("\nPresione Enter para volver...")
        return

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    print("\nSeleccione el Día:")
    for i, d in enumerate(dias, 1):
        print(f"{i}. {d}")
    
    try:
        opc_dia = int(input("Opción (1-7): ")) - 1
        dia_sel = dias[opc_dia]
    except (ValueError, IndexError):
        print("❌ Día no válido.")
        input("\nPresione Enter para volver...")
        return

    limpiar_pantalla()
    print(f"=== INGRESANDO: {semana_sel} -> {dia_sel} ===")
    
    sap = input("Número de SAP / Orden: ").strip()
    maquina = input("Tipo de Máquina / Línea: ").strip()
    producto = input("Nombre del Producto: ").strip()
    serie = input("Número de Serie: ").strip()
    
    # Si te equivocas aquí, te pedirá el mismo dato otra vez sin avanzar
    meta_lote = leer_entero_seguro("¿Cuál era la meta de unidades para este lote/turno?: ")
    u_hoy = leer_entero_seguro("¿Cuántas unidades reales se produjeron?: ")
    
    if meta_lote > 0:
        eficiencia = (u_hoy / meta_lote) * 100
    else:
        eficiencia = 100.0
        
    p_hoy = leer_entero_seguro("¿Cuántos palets completos se armaron?: ")
    cajas_por_palet = leer_entero_seguro("¿Cuántas cajas lleva cada palet?: ")
    
    # Registro de Tiempo Muerto
    print("\n--------------------------------------")
    print("⏱️ ¿Hubo detenciones o tiempos muertos en este lote?")
    tiene_parada = input("¿Sí o No? (s/n): ").strip().lower()
    
    minutos_muertos = 0
    motivo_parada = "N/A"
    
    if tiene_parada in ['s', 'si', 'sí']:
        minutos_muertos = leer_entero_seguro("¿Cuántos minutos en TOTAL estuvo parada la línea?: ")
        motivo_parada = input("Motivo de la detención (ej. Falla Mecánica / Limpieza): ").strip()
        if not motivo_parada:
            motivo_parada = "No especificado"

    # Lógica de Cajas Automáticas
    total_cajas_lote = p_hoy * cajas_por_palet
    ultima_caja_sistema = obtener_ultima_caja_global()
    caja_inicial = ultima_caja_sistema + 1
    caja_final = ultima_caja_sistema + total_cajas_lote
    
    # Guardamos todo el paquete estructurado
    nuevo_registro = {
        "sap": sap if sap else "N/A",
        "maquina": maquina if maquina else "N/A",
        "producto": producto if producto else "N/A",
        "serie": serie if serie else "N/A",
        "meta_lote": meta_lote,
        "unidades": u_hoy,
        "eficiencia": round(eficiencia, 1),
        "palets": p_hoy,
        "cajas_por_palet": cajas_por_palet,
        "total_cajas_lote": total_cajas_lote,
        "caja_inicial": caja_inicial if p_hoy > 0 else 0,
        "caja_final": caja_final if p_hoy > 0 else 0,
        "minutos_muertos": minutes_muertos if 'minutes_muertos' in locals() else minutos_muertos,
        "motivo_parada": motivo_parada
    }
    
    datos_produccion["produccion"][semana_sel][dia_sel].append(nuevo_registro)
    
    guardar_datos()
    print(f"\n✅ ¡Registro completado y guardado con éxito!")
    input("\nPresione Enter para volver...")

def ver_reporte():
    limpiar_pantalla()
    total_pauta = sum(datos_produccion["pauta_mensual"].values())
    total_real_mes = 0
    total_palets_mes = 0
    total_cajas_mes = 0
    total_minutos_muertos_mes = 0
    
    print("=======================================================================")
    print("          REPORTE GENERAL DE PRODUCCIÓN Y TIEMPOS MUERTOS             ")
    print("=======================================================================")
    
    for sem, dias in datos_produccion["produccion"].items():
        pauta_sem = datos_produccion["pauta_mensual"][sem]
        
        real_sem = 0
        palets_sem = 0
        for lista_registros in dias.values():
            real_sem += sum(r["unidades"] for r in lista_registros)
            palets_sem += sum(r["palets"] for r in lista_registros)
            
        total_real_mes += real_sem
        total_palets_mes += palets_sem
        
        print(f"\n🔹 {sem} (Meta Semanal: {pauta_sem} u. | Total Real: {real_sem} u.)")
        print(f"   ↳ Palets totales en la semana: {palets_sem}")
        
        hubo_produccion = False
        for dia, registros in dias.items():
            if registros:
                print(f"     📍 {dia}:")
                for r in registros:
                    if r["eficiencia"] < 80.0:
                        alerta = f"🔴 CRÍTICO ({r['eficiencia']}% de meta)"
                    elif r["eficiencia"] < 100.0:
                        alerta = f"🟡 BAJO TARGET ({r['eficiencia']}% de meta)"
                    else:
                        alerta = f"🟢 EFICIENTE ({r['eficiencia']}% de meta)"
                        
                    print(f"       [SAP: {r['sap']}] | [Máq: {r['maquina']}] | [Prod: {r['producto']}]")
                    print(f"       ↳ Rendimiento: {alerta} | Meta: {r['meta_lote']} u. -> Real: {r['unidades']} u.")
                    print(f"       ↳ Serie: {r['serie']} | {r['palets']} palets")
                    
                    if r['palets'] > 0:
                        print(f"       ↳ Empaque: {r['total_cajas_lote']} cajas | Rango: #{r['caja_inicial']} al #{r['caja_final']}")
                        total_cajas_mes += r['total_cajas_lote']
                        
                    if r['minutos_muertos'] > 0:
                        print(f"       ⚠️  Tiempo Muerto: {r['minutos_muertos']} min. | Motivo: {r['motivo_parada']}")
                        total_minutos_muertos_mes += r['minutos_muertos']
                        
                    print("       " + "-"*50)
                hubo_produccion = True
                
        if not hubo_produccion:
            print("     (Sin producción registrada esta semana)")
            
    print("\n=======================================================================")
    print("                            RESUMEN DEL MES                            ")
    print("=======================================================================")
    print(f"Meta Total del Mes:         {total_pauta} u.")
    print(f"Producción Acumulada:       {total_real_mes} u.")
    print(f"Palets Totales del Mes:     {total_palets_mes} p.")
    print(f"Cajas Totales del Mes:      {total_cajas_mes} cajas.")
    print(f"Tiempo Muerto Total Mes:    {total_minutos_muertos_mes} minutos ({round(total_minutos_mes/60, 1) if 'total_minutos_mes' in locals() else round(total_minutos_muertos_mes/60, 1)} hrs).")
    
    diferencia = total_real_mes - total_pauta
    if diferencia >= 0:
        print(f"Balance: 🎉 ¡Vas SOBRE la pauta por +{diferencia} unidades!")
    else:
        print(f"Balance: ⚠️ ¡Vas BAJO la pauta por {diferencia} unidades!")
    print("=======================================================================")
    input("\nPresione Enter para volver al menú...")

# Inicio del programa
cargar_datos()

while True:
    limpiar_pantalla()
    print("📱 CONTROL DE PLANTA PRO v7.5 (Reintento Activo) 📱")
    print("1. Configurar Pautas Semanales")
    print("2. Registrar Turno (Eficiencia, Cajas y Tiempo Muerto)")
    print("3. Ver Reporte General e Historial")
    print("4. Salir")
    
    opcion = input("\nSeleccione una opción (1-4): ")
    
    if opcion == "1":
        configurar_pauta()
    elif opcion == "2":
        registrar_dia()
    elif opcion == "3":
        ver_reporte()
    elif opcion == "4":
        print("\n¡Datos guardados! Saliendo del sistema...")
        break
    else:
        print("\n❌ Opción inválida.")
        input("\nPresione Enter para continuar...")