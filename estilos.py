
import flet as ft

# ==========================================
# PALETA DE COLORES (Corregidos para Flet 0.85)
# ==========================================
COLOR_FONDO = ft.ThemeMode.DARK
COLOR_TITULO = ft.Colors.BLUE_400
COLOR_EXITO = ft.Colors.GREEN_400
COLOR_ERROR = ft.Colors.RED_400

# Colores corregidos sin guiones bajos conflictivos
COLOR_ALERTA_ALTA = ft.Colors.GREEN_ACCENT_400  # Vas sobre la meta
COLOR_ALERTA_BAJA = ft.Colors.ORANGE_ACCENT_400 # Vas bajo la meta

# ==========================================
# DIMENSIONES Y POSICIONAMIENTO
# ==========================================
ANCHO_COMPONENTES = 320  
ALTO_INPUTS = 55
MARGEN_SUPERIOR_TITULO = 40 

# ==========================================
# ESTILOS DE TEXTO
# ==========================================
TEXTO_TITULO = ft.TextStyle(
    size=24, 
    weight=ft.FontWeight.BOLD, 
    color=COLOR_TITULO,
    letter_spacing=1.2
)

TEXTO_SUBTITULO = ft.TextStyle(
    size=18,
    weight=ft.FontWeight.BOLD,
    color=ft.Colors.WHITE
)

TEXTO_ESTADO = ft.TextStyle(
    weight=ft.FontWeight.BOLD,
    size=14
)

# ==========================================
# ESTILOS DE BOTONES
# ==========================================
BOTON_PRINCIPAL = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=10),
    color={"": ft.Colors.WHITE},
    bgcolor={"": ft.Colors.BLUE_700}
)