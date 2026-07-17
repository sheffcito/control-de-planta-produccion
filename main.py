import os
import sqlite3
import flet as ft
import estilos as es

# VALOR DE LA META SEMANAL
META_SEMANAL = 5000  

# ==========================================
# 1. MOTOR DE BASE DE DATOS (SQLite)
# ==========================================
def obtener_ruta_db():
    directorio = os.environ.get("FLET_APP_DATA_DIR", "")
    if not directorio:
        directorio = os.getcwd()
    return os.path.join(directorio, "produccion_planta.db")

def inicializar_base_datos():
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sap TEXT,
            maquina TEXT,
            producto TEXT,
            unidades INTEGER
        )
    """)
    conexion.commit()
    conexion.close()

def guardar_en_db(sap, maquina, producto, unidades):
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO turnos (sap, maquina, producto, unidades)
        VALUES (?, ?, ?, ?)
    """, (sap, maquina, producto, unidades))
    conexion.commit()
    conexion.close()

def obtener_todos_los_datos():
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("SELECT sap, maquina, producto, unidades FROM turnos ORDER BY id DESC")
    filas = cursor.fetchall()
    conexion.close()
    return filas

def calcular_total_unidades():
    ruta = obtener_ruta_db()
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(unidades) FROM turnos")
    resultado = cursor.fetchone()[0]
    conexion.close()
    return resultado if resultado is not None else 0

# ==========================================
# 2. INTERFAZ GRÁFICA (Flet)
# ==========================================
def main(page: ft.Page):
    page.title = "Control de Producción v5.0"
    page.window_width = 390
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = es.COLOR_FONDO
    
    inicializar_base_datos()

    # ------------------------------------------
    # PESTAÑA 1: REGISTRO
    # ------------------------------------------
    titulo_p1 = ft.Text("REGISTRO DE PLANTA", style=es.TEXTO_TITULO)
    
    input_sap = ft.TextField(
        label="Número de SAP / Orden", 
        icon=ft.Icons.RECEIPT,
        hint_text="Ej: SAP-100234",
        width=es.ANCHO_COMPONENTES,
        height=es.ALTO_INPUTS
    )
    
    input_maquina = ft.Dropdown(
        label="Seleccionar Máquina / Línea",
        options=[
            ft.DropdownOption("Excavadora Línea A"),
            ft.DropdownOption("Planta de Mezclado"),
            ft.DropdownOption("Prensa Hidráulica 01"),
            ft.DropdownOption("Línea de Envasado Gral"),
        ],
        width=es.ANCHO_COMPONENTES,
        height=es.ALTO_INPUTS
    )
    
    input_producto = ft.Dropdown(
        label="Seleccionar Producto / Material",
        options=[
            ft.DropdownOption("Árido Clasificado"),
            ft.DropdownOption("Mezcla Estándar Tipo A"),
            ft.DropdownOption("Materia Prima Premium"),
            ft.DropdownOption("Producto Terminado Pack"),
        ],
        width=es.ANCHO_COMPONENTES,
        height=es.ALTO_INPUTS
    )
    
    input_unidades = ft.TextField(
        label="Unidades Producidas", 
        icon=ft.Icons.NUMBERS, 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=es.ANCHO_COMPONENTES,
        height=es.ALTO_INPUTS
    )
    
    texto_estado = ft.Text("", style=es.TEXTO_ESTADO)

    def boton_guardar_click(e):
        if not input_maquina.value or not input_producto.value or not input_sap.value or not input_unidades.value:
            texto_estado.value = "⚠️ Error: Por favor completa todos los campos."
            texto_estado.color = es.COLOR_ERROR
            page.update()
            return

        try:
            unidades = int(input_unidades.value)
        except ValueError:
            texto_estado.value = "⚠️ Error: Las unidades deben ser un número entero."
            texto_estado.color = es.COLOR_ERROR
            page.update()
            return

        guardar_en_db(input_sap.value, input_maquina.value, input_producto.value, unidades)

        input_sap.value = ""
        input_maquina.value = None
        input_producto.value = None
        input_unidades.value = ""
        texto_estado.value = "✅ ¡Datos guardados con éxito!"
        texto_estado.color = es.COLOR_EXITO
        
        actualizar_pantalla_datos()
        actualizar_pantalla_metas()
        page.update()

    btn_guardar = ft.Button(
        content=ft.Text("Guardar en Planta", weight=ft.FontWeight.BOLD),
        icon=ft.Icons.SAVE,
        on_click=boton_guardar_click,
        style=es.BOTON_PRINCIPAL,
        width=es.ANCHO_COMPONENTES,
        height=50
    )

    vista_registro = ft.Column(
        controls=[
            ft.Divider(height=es.MARGEN_SUPERIOR_TITULO, color=ft.Colors.TRANSPARENT),
            titulo_p1,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            input_sap,
            input_maquina,
            input_producto,
            input_unidades,
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            btn_guardar,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            texto_estado
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18
    )

    # ------------------------------------------
    # PESTAÑA 2: DATOS GUARDADOS
    # ------------------------------------------
    titulo_p2 = ft.Text("DATOS GUARDADOS", style=es.TEXTO_TITULO)
    
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("SAP")),
            ft.DataColumn(ft.Text("Máquina")),
            ft.DataColumn(ft.Text("Cant.")),
        ],
        rows=[]
    )
    
    contenedor_tabla = ft.ListView(
        controls=[tabla_datos],
        expand=True,
        spacing=10,
        height=500
    )

    def actualizar_pantalla_datos():
        registros = obtener_todos_los_datos()
        tabla_datos.rows.clear()
        for r in registros:
            tabla_datos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r[0]))),
                        ft.DataCell(ft.Text(str(r[1]).split()[0])), 
                        ft.DataCell(ft.Text(str(r[3]))),
                    ]
                )
            )

    vista_datos = ft.Column(
        controls=[
            ft.Divider(height=es.MARGEN_SUPERIOR_TITULO, color=ft.Colors.TRANSPARENT),
            titulo_p2,
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            contenedor_tabla
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=False
    )

    # ------------------------------------------
    # PESTAÑA 3: METAS Y ESTADÍSTICAS
    # ------------------------------------------
    titulo_p3 = ft.Text("METAS SEMANALES", style=es.TEXTO_TITULO)
    
    txt_total_actual = ft.Text("0", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    txt_meta_fija = ft.Text(f"Meta de la semana: {META_SEMANAL} unidades", size=16, color=ft.Colors.GREY_400)
    
    txt_mensaje_rendimiento = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    
    tarjeta_alerta = ft.Container(
        content=txt_mensaje_rendimiento,
        padding=15,
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        width=es.ANCHO_COMPONENTES
    )

    def actualizar_pantalla_metas():
        total = calcular_total_unidades()
        txt_total_actual.value = f"{total:,}".replace(",", ".")
        
        if total >= META_SEMANAL:
            txt_mensaje_rendimiento.value = "🚀 ¡Excelente! Vas por encima de la meta semanal."
            tarjeta_alerta.bgcolor = es.COLOR_ALERTA_ALTA
            txt_mensaje_rendimiento.color = ft.Colors.BLACK
        else:
            faltante = META_SEMANAL - total
            txt_mensaje_rendimiento.value = f"📉 Vas por debajo del promedio.\nFaltan {faltante:,} un. para la meta.".replace(",", ".")
            tarjeta_alerta.bgcolor = es.COLOR_ALERTA_BAJA
            txt_mensaje_rendimiento.color = ft.Colors.BLACK

    vista_metas = ft.Column(
        controls=[
            ft.Divider(height=es.MARGEN_SUPERIOR_TITULO, color=ft.Colors.TRANSPARENT),
            titulo_p3,
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Text("PRODUCCIÓN TOTAL ACUMULADA", size=14, weight=ft.FontWeight.W_500),
            txt_total_actual,
            txt_meta_fija,
            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
            tarjeta_alerta
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=False
    )

    # ------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------
    def navegar(e):
        vista_registro.visible = False
        vista_datos.visible = False
        vista_metas.visible = False
        
        if e.control.selected_index == 0:
            vista_registro.visible = True
        elif e.control.selected_index == 1:
            actualizar_pantalla_datos()
            vista_datos.visible = True
        elif e.control.selected_index == 2:
            actualizar_pantalla_metas()
            vista_metas.visible = True
            
        page.update()

    # CORREGIDO: Cambiado NavigationDestination por NavigationBarDestination
    barra_navegacion = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EDIT_NOTE, label="Registro"),
            ft.NavigationBarDestination(icon=ft.Icons.STORAGE, label="Datos Guardados"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Metas"),
        ],
        selected_index=0,
        on_change=navegar
    )

    page.navigation_bar = barra_navegacion
    page.add(vista_registro, vista_datos, vista_metas)

if __name__ == "__main__":
    ft.run(main)