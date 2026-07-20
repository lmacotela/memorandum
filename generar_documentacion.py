"""Genera el PDF de documentación del sistema de memorandums."""
from fpdf import FPDF
from datetime import date


AZUL_OSCURO  = (23,  55,  94)
AZUL_MEDIO   = (41,  98, 162)
AZUL_CLARO   = (219, 234, 254)
GRIS_TEXTO   = (60,  60,  60)
GRIS_CLARO   = (245, 245, 245)
VERDE        = (21, 128,  61)
NARANJA      = (180,  80,   0)
BLANCO       = (255, 255, 255)


class PDF(FPDF):

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*AZUL_OSCURO)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BLANCO)
        self.set_xy(10, 2)
        self.cell(0, 8, "Sistema de Generacion de Memorandums - Sapiens Consulting Peru", align="L")
        self.set_xy(0, 2)
        self.cell(200, 8, f"Pagina {self.page_no()}", align="R")
        self.ln(10)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_fill_color(*AZUL_CLARO)
        self.rect(0, self.get_y(), 210, 12, "F")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*AZUL_OSCURO)
        self.set_x(10)
        self.cell(0, 10, f"Documento generado el {date.today().strftime('%d/%m/%Y')}  |  Confidencial", align="L")

    # ── utilidades ──────────────────────────────────────────────────────

    def titulo_seccion(self, numero: str, texto: str):
        self.ln(6)
        self.set_fill_color(*AZUL_OSCURO)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 13)
        self.rect(10, self.get_y(), 190, 10, "F")
        self.set_x(13)
        self.cell(0, 10, f"  {numero}  {texto}", ln=True)
        self.set_text_color(*GRIS_TEXTO)
        self.ln(3)

    def subtitulo(self, texto: str):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*AZUL_MEDIO)
        self.set_x(10)
        self.cell(0, 7, texto, ln=True)
        self.set_text_color(*GRIS_TEXTO)

    def parrafo(self, texto: str, indent: int = 10):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*GRIS_TEXTO)
        self.set_x(indent)
        self.multi_cell(190 - (indent - 10), 6, texto)
        self.ln(1)

    def bullet(self, texto: str, nivel: int = 1):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*GRIS_TEXTO)
        indent = 14 + (nivel - 1) * 6
        simbolo = "  -  " if nivel > 1 else "  *  "
        self.set_x(indent)
        self.multi_cell(185 - indent, 6, f"{simbolo}{texto}")

    def caja_info(self, titulo: str, contenido: str, color=None):
        if color is None:
            color = AZUL_CLARO
        self.ln(3)
        y_ini = self.get_y()
        self.set_fill_color(*color)
        # Dibujamos la caja con un alto estimado primero
        self.set_x(10)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*AZUL_OSCURO)
        self.cell(190, 7, f"  {titulo}", ln=True, fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRIS_TEXTO)
        self.set_fill_color(250, 250, 250)
        self.set_x(10)
        self.multi_cell(190, 5.5, contenido, border=1, fill=True)
        self.ln(3)

    def caja_codigo(self, codigo: str):
        self.ln(2)
        self.set_fill_color(30, 30, 30)
        self.set_text_color(180, 255, 180)
        self.set_font("Courier", "", 8.5)
        self.set_x(10)
        self.multi_cell(190, 5, codigo, fill=True)
        self.set_text_color(*GRIS_TEXTO)
        self.ln(2)

    def caja_json(self, titulo: str, json_texto: str):
        self.ln(2)
        self.set_fill_color(*AZUL_OSCURO)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 9)
        self.set_x(10)
        self.cell(190, 6, f"  {titulo}", ln=True, fill=True)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(50, 50, 50)
        self.set_font("Courier", "", 8.5)
        self.set_x(10)
        self.multi_cell(190, 5, json_texto, border=1, fill=True)
        self.ln(3)

    def paso_flujo(self, numero: str, titulo: str, descripcion: str, url: str = ""):
        self.ln(2)
        self.set_fill_color(*AZUL_MEDIO)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 10)
        self.set_x(10)
        self.cell(12, 8, numero, align="C", fill=True)
        self.set_fill_color(*AZUL_CLARO)
        self.set_text_color(*AZUL_OSCURO)
        self.cell(178, 8, f"  {titulo}", fill=True, ln=True)
        if url:
            self.set_font("Courier", "", 8)
            self.set_text_color(*NARANJA)
            self.set_x(22)
            self.cell(178, 5, url, ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRIS_TEXTO)
        self.set_x(22)
        self.multi_cell(178, 5, descripcion)
        self.ln(1)

    def tabla_campos(self, encabezados: list, filas: list):
        self.ln(2)
        col_w = [50, 55, 85]
        self.set_fill_color(*AZUL_OSCURO)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 9)
        self.set_x(10)
        for i, h in enumerate(encabezados):
            self.cell(col_w[i], 7, f"  {h}", border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 9)
        fill = False
        for fila in filas:
            self.set_fill_color(*GRIS_CLARO if fill else BLANCO)
            self.set_text_color(*GRIS_TEXTO)
            self.set_x(10)
            for i, celda in enumerate(fila):
                self.cell(col_w[i], 6, f"  {celda}", border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(3)


# ════════════════════════════════════════════════════════════════════════════
def generar_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ── PORTADA ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*AZUL_OSCURO)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.set_y(60)
    pdf.set_text_color(*BLANCO)
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 12, "Sistema de Generacion", align="C", ln=True)
    pdf.cell(0, 12, "de Memorandums", align="C", ln=True)

    pdf.ln(6)
    pdf.set_fill_color(*AZUL_MEDIO)
    pdf.rect(30, pdf.get_y(), 150, 1, "F")
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(200, 220, 255)
    pdf.cell(0, 8, "Sapiens Consulting Peru", align="C", ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(170, 200, 240)
    pdf.cell(0, 7, "Guia de uso para el equipo de Recursos Humanos", align="C", ln=True)

    pdf.ln(50)
    pdf.set_fill_color(*AZUL_CLARO)
    pdf.rect(30, pdf.get_y(), 150, 40, "F")
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_text_color(*AZUL_OSCURO)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 7, "QUE ENCONTRARAS EN ESTE DOCUMENTO", align="C", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 80, 120)
    for item in [
        "Como funciona el sistema paso a paso",
        "Como generar documentos Word automaticamente",
        "Ejemplos de uso con capturas y datos reales",
        "Como publicar el sistema en un servidor",
    ]:
        pdf.cell(0, 6, f"       {item}", align="L", ln=True)

    pdf.ln(30)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 160, 210)
    pdf.cell(0, 6, f"Version 1.0  |  {date.today().strftime('%d de %B de %Y')}", align="C", ln=True)

    # ── PAG 2: QUE ES Y PARA QUE SIRVE ─────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("1", "Que es este sistema?")
    pdf.parrafo(
        "Este sistema es una herramienta que permite generar documentos Word de memorandums "
        "de forma automatica, sin necesidad de escribirlos manualmente uno por uno."
    )
    pdf.parrafo(
        "Funciona como un asistente inteligente: se conecta al sistema de empleados de Sapiens, "
        "obtiene la informacion de cada trabajador y la coloca automaticamente en la plantilla "
        "de memorandum que ya conoces."
    )

    pdf.titulo_seccion("2", "Como funciona? (Flujo de 3 pasos)")
    pdf.parrafo("El sistema realiza tres acciones de forma automatica cada vez que lo usas:")

    pdf.paso_flujo(
        "1", "Inicio de sesion automatico",
        "El sistema ingresa al portal de empleados de Sapiens usando las credenciales "
        "configuradas. Esto es transparente para el usuario, ocurre en segundos.",
        "URL: https://empleados.sapiensconsultingperu.com/apitest/api/Auth/Login"
    )
    pdf.paso_flujo(
        "2", "Obtencion de datos de empleados",
        "Con el acceso obtenido en el paso 1, consulta la informacion de los empleados "
        "en el rango de fechas que indiques: nombre, dias de permiso, documento, etc.",
        "URL: https://empleados.sapiensconsultingperu.com/apitest/api/TimesheetStatus/GetReporteMemorandumTimesheet"
    )
    pdf.paso_flujo(
        "3", "Generacion del documento Word",
        "Toma la plantilla de memorandum (.docx) y reemplaza automaticamente los campos "
        "como <NombreEmpleado>, <fecha>, <dias>, etc. con los datos reales de cada empleado. "
        "Si son varios empleados, genera un archivo por cada uno y los entrega en un .zip."
    )

    # ── PAG 3: COMO USARLO ───────────────────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("3", "Como usar el sistema")
    pdf.parrafo(
        "El sistema tiene una pantalla de pruebas integrada llamada Swagger UI. "
        "No necesitas saber programar para usarla."
    )

    pdf.subtitulo("Paso 1: Abrir el sistema en el navegador")
    pdf.parrafo("Escribe esta direccion en tu navegador (Chrome, Edge, Firefox):")
    pdf.caja_codigo("    http://localhost:8000/docs\n    (o la IP de tu servidor si ya fue publicado)")

    pdf.subtitulo("Paso 2: Usar el flujo automatizado")
    pdf.parrafo(
        "En la pantalla de Swagger veras varios botones. El mas importante es "
        "'POST /flujo-automatizado'. Haz clic en el, luego en 'Try it out' y "
        "llena los campos:"
    )

    pdf.tabla_campos(
        ["Campo", "Ejemplo", "Descripcion"],
        [
            ["from_date",      "2026-01-01",                      "Fecha de inicio del reporte"],
            ["to_date",        "2026-04-17",                      "Fecha de fin del reporte"],
            ["user_ids",       "029E5A4D-88BB-...",               "ID del empleado en el sistema"],
            ["titulo",         "Memorandum Vacaciones",           "Titulo que tendra el documento"],
            ["template_name",  "memorandum.docx",                 "Nombre de la plantilla a usar"],
        ]
    )

    pdf.subtitulo("Paso 3: Descargar el documento")
    pdf.parrafo(
        "Haz clic en 'Execute'. El sistema procesara la solicitud y en segundos "
        "aparecera un boton 'Download file'. Al hacer clic se descargara el archivo "
        ".docx ya listo con los datos del empleado."
    )

    pdf.caja_info(
        "CONSEJO",
        "Si solicitas varios empleados a la vez, el sistema descargara un archivo .zip\n"
        "que contendra un documento Word separado para cada empleado.",
        color=(220, 252, 231)
    )

    # ── PAG 4: EJEMPLO COMPLETO ──────────────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("4", "Ejemplo completo de uso")

    pdf.subtitulo("Lo que envias al sistema:")
    pdf.caja_json(
        "Solicitud (lo que escribes en el sistema)",
        '{\n'
        '  "from_date": "2026-01-01",\n'
        '  "to_date":   "2026-04-17",\n'
        '  "user_ids":  ["029E5A4D-88BB-470E-1507-08DB56A77B7F"],\n'
        '  "titulo":    "Memorandum de Permiso",\n'
        '  "template_name": "memorandum.docx"\n'
        '}'
    )

    pdf.subtitulo("Lo que hace el sistema internamente:")
    for paso in [
        ("1", "Inicia sesion en Sapiens con las credenciales configuradas"),
        ("2", "Busca al empleado con ID '029E5A4D...' entre enero y abril 2026"),
        ("3", "Obtiene sus datos: nombre, dias autorizados, numero de documento"),
        ("4", "Abre la plantilla memorandum.docx"),
        ("5", "Reemplaza los campos en el documento"),
        ("6", "Descarga el documento listo para firmar"),
    ]:
        pdf.set_x(14)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*AZUL_MEDIO)
        pdf.cell(8, 6, f"{paso[0]}.")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRIS_TEXTO)
        pdf.cell(0, 6, paso[1], ln=True)

    pdf.subtitulo("El documento generado contiene:")
    pdf.caja_json(
        "Antes (plantilla)                    ->    Despues (documento generado)",
        "PARA:      <NombreEmpleado>           ->    PARA:      Carlos Ramirez Torres\n"
        "ASUNTO:    <Asunto>                   ->    ASUNTO:    Permiso por vacaciones anuales\n"
        "FECHA:     <fecha>                    ->    FECHA:     15 de marzo de 2026\n"
        "DOCUMENTO: <Documento>                ->    DOCUMENTO: RH-2026-042\n\n"
        "...se le han autorizado <dias> dias   ->    ...se le han autorizado 15 dias..."
    )

    # ── PAG 5: GESTION DE PLANTILLAS ────────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("5", "Gestion de plantillas Word")

    pdf.subtitulo("Como agregar una nueva plantilla")
    pdf.parrafo(
        "Una plantilla es simplemente un documento Word (.docx) con marcadores especiales "
        "en los lugares donde quieres que el sistema coloque informacion automaticamente."
    )
    pdf.parrafo("Los marcadores disponibles son:")

    pdf.tabla_campos(
        ["Marcador en el Word", "Se reemplaza con", "Ejemplo del resultado"],
        [
            ["<NombreEmpleado>", "Nombre completo del trabajador",    "Ana Garcia Lopez"],
            ["<Asunto>",         "Motivo del memorandum",             "Permiso por enfermedad"],
            ["<fecha>",          "Fecha del documento",               "01 de julio de 2026"],
            ["<dias>",           "Numero de dias autorizados",        "5"],
            ["<Documento>",      "Numero de documento interno",       "RH-2026-015"],
        ]
    )

    pdf.parrafo(
        "Para crear una nueva plantilla: abre Word, escribe el memorandum normalmente "
        "y donde quieras que vaya el nombre del empleado escribe exactamente <NombreEmpleado> "
        "(con los simbolos < >, sin espacios). Guarda el archivo en la carpeta 'templates/'."
    )

    pdf.caja_info(
        "IMPORTANTE",
        "Los marcadores deben escribirse exactamente como aparecen en la tabla de arriba,\n"
        "incluyendo mayusculas y minusculas. Por ejemplo: <fecha> no es igual a <Fecha>.",
        color=(255, 237, 213)
    )

    pdf.subtitulo("Ver las plantillas disponibles")
    pdf.parrafo("Puedes ver que plantillas estan cargadas en el sistema visitando:")
    pdf.caja_codigo("    http://localhost:8000/plantillas")
    pdf.parrafo("El sistema respondera con la lista de archivos disponibles.")

    # ── PAG 6: DIAGNÓSTICO ───────────────────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("6", "Solucion de problemas frecuentes")

    problemas = [
        (
            "El sistema dice 'Credenciales incorrectas'",
            [
                "Verificar con el administrador de Sapiens que el usuario y contrasena sean correctos.",
                "Confirmar que la cuenta tenga permisos para consultar memorandums.",
                "Si la contrasena fue cambiada recientemente, actualizar el archivo .env del sistema.",
            ]
        ),
        (
            "Aparece 'Plantilla no encontrada'",
            [
                "Verificar que el archivo .docx este dentro de la carpeta 'templates/'.",
                "Confirmar que el nombre escrito en 'template_name' sea identico al nombre del archivo.",
                "Ejemplo correcto: 'memorandum.docx' (con minusculas y sin espacios extra).",
            ]
        ),
        (
            "El documento generado tiene campos sin reemplazar (sale <NombreEmpleado>)",
            [
                "El API de Sapiens no devolvio datos para ese campo.",
                "Usar el endpoint /flujo-debug para ver exactamente que datos devuelve el sistema.",
                "Notificar al equipo de TI para revisar el mapeo de campos.",
            ]
        ),
        (
            "El sistema no responde / no abre en el navegador",
            [
                "Verificar que el servidor este encendido y el servicio corriendo.",
                "En Linux ejecutar: sudo systemctl status memorandum",
                "Revisar que el puerto 8000 (o 80 con Nginx) no este bloqueado.",
            ]
        ),
    ]

    for problema, soluciones in problemas:
        pdf.subtitulo(f"Problema: {problema}")
        for s in soluciones:
            pdf.bullet(s)
        pdf.ln(1)

    pdf.titulo_seccion("7", "Endpoint de diagnostico")
    pdf.parrafo(
        "Existe un endpoint especial para verificar que todo funcione correctamente "
        "sin generar ningun documento. Util para diagnosticar problemas de credenciales "
        "o de conexion con Sapiens."
    )
    pdf.caja_codigo("    GET http://localhost:8000/flujo-debug")
    pdf.parrafo("Este endpoint muestra:")
    pdf.bullet("Si el login con Sapiens fue exitoso o no")
    pdf.bullet("Los primeros caracteres del token obtenido")
    pdf.bullet("Cuantos registros de empleados devolvio el sistema")
    pdf.bullet("El contenido del primer registro (para verificar los nombres de campos)")

    # ── PAG 7: PUBLICACION EN SERVIDOR ──────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("8", "Publicar el sistema en un servidor Linux")
    pdf.parrafo(
        "Una vez que el sistema funcione correctamente en tu computadora, "
        "puedes instalarlo en un servidor para que todo el equipo pueda usarlo "
        "desde el navegador sin necesidad de tener nada instalado."
    )

    pdf.subtitulo("Opcion A: Con Docker (recomendada)")
    pdf.parrafo(
        "Docker es una tecnologia que empaqueta todo el sistema en una caja sellada. "
        "Es la forma mas sencilla y segura de publicar el sistema."
    )
    pdf.caja_codigo(
        "# 1. Copiar los archivos al servidor\n"
        "scp -r memorandum/ usuario@IP-DEL-SERVIDOR:/opt/memorandum\n\n"
        "# 2. Conectarse al servidor y construir la imagen\n"
        "ssh usuario@IP-DEL-SERVIDOR\n"
        "cd /opt/memorandum\n"
        "docker build -t memorandum-api .\n\n"
        "# 3. Iniciar el sistema (se reinicia automaticamente si el servidor reinicia)\n"
        "docker run -d --restart=always --name memorandum -p 8000:8000 memorandum-api"
    )

    pdf.subtitulo("Opcion B: Con Systemd + Nginx (sin Docker)")
    pdf.caja_codigo(
        "# 1. Copiar archivos al servidor\n"
        "scp -r memorandum/ usuario@IP:/opt/memorandum\n\n"
        "# 2. Instalar dependencias en el servidor\n"
        "cd /opt/memorandum\n"
        "python3 -m venv venv\n"
        "venv/bin/pip install -r requirements.txt\n\n"
        "# 3. Registrar como servicio del sistema\n"
        "sudo cp memorandum.service /etc/systemd/system/\n"
        "sudo systemctl enable --now memorandum\n\n"
        "# 4. Configurar Nginx como puerta de entrada\n"
        "sudo cp nginx.conf /etc/nginx/sites-available/memorandum\n"
        "sudo ln -s /etc/nginx/sites-available/memorandum /etc/nginx/sites-enabled/\n"
        "sudo systemctl reload nginx\n\n"
        "# 5. Agregar HTTPS gratis (opcional pero recomendado)\n"
        "sudo certbot --nginx -d tu-dominio.com"
    )

    pdf.caja_info(
        "RESULTADO FINAL",
        "Una vez publicado, cualquier persona del equipo podra acceder al sistema\n"
        "escribiendo en su navegador: http://tu-dominio.com/docs\n"
        "No necesitan instalar nada en su computadora.",
        color=(220, 252, 231)
    )

    # ── PAG 8: RESUMEN ───────────────────────────────────────────────────
    pdf.add_page()

    pdf.titulo_seccion("9", "Resumen rapido")

    pdf.subtitulo("Endpoints disponibles")
    pdf.tabla_campos(
        ["Direccion",              "Que hace"],
        [
            ["/docs",                  "Pantalla visual para usar el sistema (Swagger UI)"],
            ["/flujo-automatizado",    "Genera documentos Word automaticamente desde Sapiens"],
            ["/generar-documento",     "Genera un documento Word con datos ingresados a mano"],
            ["/flujo-debug",           "Diagnostico: muestra si el login y datos funcionan"],
            ["/plantillas",            "Lista las plantillas .docx disponibles"],
            ["/health",                "Verifica que el sistema este encendido"],
        ]
    )

    pdf.ln(3)
    pdf.subtitulo("Archivos del proyecto")
    pdf.tabla_campos(
        ["Archivo / Carpeta",     "Para que sirve"],
        [
            ["main.py",            "Cerebro del sistema. Define todos los endpoints de la API"],
            ["sapiens_client.py",  "Maneja la conexion con el sistema de Sapiens (login + datos)"],
            ["word_service.py",    "Genera los documentos Word desde la plantilla"],
            [".env",               "Contiene usuario y contrasena de Sapiens (editar aqui)"],
            ["templates/",         "Carpeta donde van las plantillas Word (.docx)"],
            ["output/",            "Carpeta donde se guardan los documentos generados"],
        ]
    )

    pdf.ln(5)
    pdf.set_fill_color(*AZUL_OSCURO)
    pdf.rect(10, pdf.get_y(), 190, 28, "F")
    pdf.set_y(pdf.get_y() + 4)
    pdf.set_text_color(*BLANCO)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Para cambiar las credenciales de Sapiens:", align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(200, 220, 255)
    pdf.cell(0, 6, "Edita el archivo  .env  y actualiza SAPIENS_USERNAME y SAPIENS_PASSWORD", align="C", ln=True)
    pdf.cell(0, 6, "Luego reinicia el servicio para que los cambios tomen efecto.", align="C", ln=True)

    # guardar
    output = "Documentacion_Sistema_Memorandums.pdf"
    pdf.output(output)
    print(f"PDF generado: {output}")
    return output


if __name__ == "__main__":
    generar_documentacion()
