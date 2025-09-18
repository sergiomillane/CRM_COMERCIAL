import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import plotly.express as px

# =============================================
# FUNCIÓN PARA NORMALIZAR NOMBRES
# =============================================
def normalizar_nombre(nombre):
    """Convierte a mayúsculas, elimina tildes y espacios extras"""
    if not isinstance(nombre, str):
        return ""
    nombre = nombre.upper().strip()
    traduccion = str.maketrans("ÁÉÍÓÚÑ", "AEIOUN")
    return nombre.translate(traduccion)


# =============================================
# CONFIGURACIÓN DE PERMISOS POR CAMPAÑA
# =============================================
PERMISOS_CAMPANAS = {
    "CAT": [
        "Ana Laura Rivera Inzunza", "Cinthia Guadalupe Checa Robles", 
        "Dafne Gabriela Miramontes Graciano", "Guadalupe Paola Beltran Ramos",
        "Jessica Maribel Vargas Villagrana", "Jesus Anahi Perez Gamez",
        "José Alfredo Alvarado Hernandez", "Jose Andres Borquez Blanco",
        "Jose Eduardo Lopez Portillo Bazua", "Jose Daniel Flores Herrera",
        "Julissa Iveth Gamez Ramirez", "Karely Elizabeth Olmeda Gutierrez",
        "Lizbeth Guadalupe Contreras Leal", "Melissa Angulo Rios",
        "Oscar Eduardo Sánchez Grande", "Reyna Berenice Salazar Cabrera",
        "EDGAR QUIÑONEZ", "SILVIA LOPEZ"
    ],
    "ORIGINACION DE CREDITO": [
        "Ana Laura Rivera Inzunza", "Cinthia Guadalupe Checa Robles",
        "Dafne Gabriela Miramontes Graciano", "Guadalupe Paola Beltran Ramos",
        "Jessica Maribel Vargas Villagrana", "Jesus Anahi Perez Gamez",
        "José Alfredo Alvarado Hernandez", "Jose Andres Borquez Blanco",
        "Jose Eduardo Lopez Portillo Bazua", "Jose Daniel Flores Herrera",
        "Julissa Iveth Gamez Ramirez", "Karely Elizabeth Olmeda Gutierrez",
        "Lizbeth Guadalupe Contreras Leal", "Melissa Angulo Rios",
        "Oscar Eduardo Sánchez Grande", "Reyna Berenice Salazar Cabrera",
        "EDGAR QUIÑONEZ", "SILVIA LOPEZ", "NANCY BURGOS", "Lorena Andrade Perez"
    ],
    "CAMPAÑA MOTOS": [
        "Bryan Junnyel Rios Castro", "NANCY BURGOS", "Lorena Andrade Perez", "Carmen Samano"
    ],
    "CAMPAÑA SIN FRICCION": [
        "Bryan Felix", "Maria Fernanda Zazueta Aguilar", "Daniela Boada"
    ],
    "CAMPAÑA SIN ENGANCHE": [
        "Bryan Junnyel Rios Castro", "NANCY BURGOS", "Lorena Andrade Perez", "Daniela Boada", "Carmen Samano"
    ],
    "CAMPAÑA REFINANCIAMIENTO": [
        "Bryan Junnyel Rios Castro", "NANCY BURGOS", "Lorena Andrade Perez", "Bryan Felix"
    ],
    "INDICADORES": [
        # Todos los usuarios pueden ver indicadores
        "Ana Laura Rivera Inzunza", "Cinthia Guadalupe Checa Robles", 
        "Dafne Gabriela Miramontes Graciano", "Guadalupe Paola Beltran Ramos",
        "Jessica Maribel Vargas Villagrana", "Jesus Anahi Perez Gamez",
        "José Alfredo Alvarado Hernandez", "Jose Andres Borquez Blanco",
        "Jose Eduardo Lopez Portillo Bazua", "Bryan Felix", "Jose Daniel Flores Herrera",
        "Julissa Iveth Gamez Ramirez", "Bryan Junnyel Rios Castro", "Maria Fernanda Zazueta Aguilar",
        "Karely Elizabeth Olmeda Gutierrez", "Lizbeth Guadalupe Contreras Leal",
        "Melissa Angulo Rios", "Oscar Eduardo Sánchez Grande", "Reyna Berenice Salazar Cabrera",
        "NANCY BURGOS", "Lorena Andrade Perez", "EDGAR QUIÑONEZ", "SILVIA LOPEZ", "Daniela Boada", "Carmen Samano"
    ]
}

# =============================================
# FUNCIÓN PARA VERIFICAR PERMISOS
# =============================================
def tiene_permiso(gestor, campana):
    """Verifica si un gestor tiene permiso para acceder a una campaña"""
    return gestor in PERMISOS_CAMPANAS.get(campana, [])

# =============================================
# FUNCIÓN GENÉRICA PARA CAMPAÑAS
# =============================================
def mostrar_campana(nombre_campana, tabla_sql, campos_cliente, campos_adicionales, 
                   opciones_gestion, tabla_gestiones, nombre_tabla_gestion):
    """
    Función genérica para mostrar cualquier campaña
    """
    
    # Verificar permisos
    if not tiene_permiso(gestor_autenticado, nombre_campana):
        st.warning("Ups! No tienes acceso a esta pestaña :(")
        return
    
    # Determinar campo ID según la campaña
    if "REFINANCIAMIENTO" in nombre_campana:
        campo_id = "SapIdCliente"
        campo_gestor = "GestorVirtual"
    else:
        campo_id = "ID_Cliente"
        campo_gestor = "GestorVirtual"
    
    # 1) Cargar datos
    query = f"SELECT * FROM {tabla_sql} where gestion <> 'Numero equivocado'"
    data = pd.read_sql(query, engine)
    
    # 2) Filtrar por gestor y eliminar IDs inválidos
    data = data[data[campo_gestor] == gestor_autenticado].copy()
    data = data.dropna(subset=[campo_id])
    
    # 3) Asegurar FECHA_GESTION como datetime
    data["FECHA_GESTION"] = pd.to_datetime(data["FECHA_GESTION"], errors="coerce")
    
    # 4) Lógica de jerarquía fija
    if "NumeroCliente" in data.columns and not data["NumeroCliente"].isna().all():
        data = data.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
        data["jerarquia"] = data.index + 1
    else:
        data["orden_auxiliar"] = data["FECHA_GESTION"].fillna(pd.Timestamp.min)
        data = data.sort_values(by=["orden_auxiliar"], ascending=True).reset_index(drop=True)
        data["jerarquia"] = data.index + 1
        data.drop(columns=["orden_auxiliar"], inplace=True)
    
    if data.empty:
        st.warning(f"No hay datos en {nombre_campana}.")
        return
    
    # 5) Preparar lista única de clientes
    unique_clients = data.drop_duplicates(subset=[campo_id]).reset_index(drop=True)
    total_clients = len(unique_clients)
    
    # 6) UI de búsqueda por jerarquía o ID
    st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
    cols = st.columns([1, 1])
    with cols[0]:
        input_jerarquia = st.text_input("Borre el numero antes de usar el botón de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
    with cols[1]:
        input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

    # Lógica de búsqueda
    session_key = f"cliente_index_{nombre_campana.lower().replace(' ', '_')}"
    
    if input_jerarquia:
        try:
            input_jerarquia = int(input_jerarquia)
            idx = unique_clients[unique_clients["jerarquia"] == input_jerarquia].index
            if idx.size:
                st.session_state[session_key] = idx[0]
            else:
                st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
        except ValueError:
            st.error("Por favor, ingrese un número válido.")

    if input_id_cliente:
        try:
            input_id_cliente = int(input_id_cliente) if input_id_cliente.isdigit() else input_id_cliente
            idx = unique_clients[unique_clients[campo_id] == input_id_cliente].index
            if idx.size:
                st.session_state[session_key] = idx[0]
            else:
                st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
        except ValueError:
            st.error("Por favor, ingrese un ID válido.")
    
    # 7) Inicializar y acotar índice
    if session_key not in st.session_state:
        st.session_state[session_key] = 0
    cliente_index = st.session_state[session_key]
    cliente_index = max(0, min(cliente_index, total_clients - 1))
    st.session_state[session_key] = cliente_index
    
    # 8) Botones de navegación
    nav_cols = st.columns([1, 1])
    with nav_cols[0]:
        if st.button("Anterior"):
            st.session_state[session_key] = max(cliente_index - 1, 0)
    with nav_cols[1]:
        if st.button("Siguiente"):
            st.session_state[session_key] = min(cliente_index + 1, total_clients - 1)

    cliente_actual = unique_clients.iloc[st.session_state[session_key]]
    
    # 9) Mostrar cliente actual
    st.subheader(f"Información del Cliente - {nombre_campana}")
    cols = st.columns(2)
    
    with cols[0]:
        # Mostrar campos básicos del cliente
        for i, campo in enumerate(campos_cliente):
            if i >= len(campos_cliente)//2:
                break
            valor = cliente_actual.get(campo, "N/A")
            if campo == "jerarquia":
                st.write(f"**Jerarquia:** {valor}")
            else:
                nombre_campo = campo.replace('_', ' ').replace('SapId', 'ID').title()
                st.write(f"**{nombre_campo}:** {valor}")
    
    with cols[1]:
        # Mostrar campos adicionales y resto de campos básicos
        campos_restantes = campos_cliente[len(campos_cliente)//2:] + campos_adicionales
        for campo in campos_restantes:
            valor = cliente_actual.get(campo, "N/A")
            
            # Formatear porcentajes si es campo de enganche
            if "enganche" in campo.lower() and campo != "Enganche":
                if pd.notna(valor) and valor != 0:
                    valor = f"{float(valor) * 100:.0f}%"
                else:
                    valor = "0%"
            
            nombre_campo = campo.replace('_', ' ').replace('SapId', 'ID').title()
            st.write(f"**{nombre_campo}:** {valor}")
        
        # Fecha última gestión
        raw_fecha = cliente_actual.get("FECHA_GESTION", None)
        fecha_dt = pd.to_datetime(raw_fecha, errors="coerce")
        fecha_str = fecha_dt.strftime("%Y/%m/%d") if pd.notna(fecha_dt) else "N/A"
        st.write(f"**Fecha de Última Gestión:** {fecha_str}")
        st.markdown(f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual.get('Gestion')) else 'No'}</span>", unsafe_allow_html=True)

    st.divider()
    
    # 10) Formulario de gestión
    st.subheader("Gestiones del Cliente")
    gestion_key = f"gestion_{nombre_campana}_{cliente_actual[campo_id]}"
    comentario_key = f"comentario_{nombre_campana}_{cliente_actual[campo_id]}"

    with st.form(key=f"gestion_form_{nombre_campana}"):
        gestion = st.selectbox(
            "Gestión",
            options=[None] + opciones_gestion,
            index=0 if st.session_state.get(gestion_key) is None else
                opciones_gestion.index(st.session_state[gestion_key]) + 1,
        )
        comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
        submit_button = st.form_submit_button("Guardar Gestión")

    if submit_button:
        st.session_state[gestion_key] = gestion
        st.session_state[comentario_key] = comentario
        try:
            gestor = st.session_state.get("gestor")
            
            # Actualizar tabla principal
            query_update = text(f"""
                UPDATE {tabla_sql}
                SET Gestion = :gestion, 
                    Comentario = :comentario
                WHERE {campo_id} = :id_cliente
            """)
            
            # Insertar en tabla de gestiones
            query_insert = text(f"""
                INSERT INTO {tabla_gestiones} (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                VALUES (:id_cliente, :campana, GETDATE(), :gestor, :gestion, :comentario)
            """)
            
            with engine.begin() as conn:
                conn.execute(query_update, {
                    "gestion": gestion,
                    "comentario": comentario,
                    "id_cliente": cliente_actual[campo_id],
                })
                conn.execute(query_insert, {
                    "id_cliente": str(cliente_actual[campo_id]),
                    "campana": nombre_tabla_gestion,
                    "gestor": gestor,
                    "gestion": gestion,
                    "comentario": comentario
                })
            
            st.success("Gestión guardada exitosamente.")
            
        except Exception as e:
            st.error(f"Error al guardar los cambios: {e}")

# Estilos personalizados
st.markdown(
    """
    <style>
    .main {
        background-color: linear-gradient(120deg, #8E44AD, #3498DB);
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4c4c4c, #6b6b6b);
        font-family: 'Arial', sans-serif;
        color: white;
        padding: 10px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3, .sidebar .sidebar-content h4 {
        color: #ffffff;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .dataframe-container {
        max-width: 90%;
        margin: auto;
    }
    .compact-input input {
        font-size: 12px !important;
        height: 30px !important;
    }
    .highlight {
        background-color: #d4edda;
        color: #155724;
        padding: 5px;
        border-radius: 5px;
    }
    .header-container {
        background-color: #2c3e50;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .header-container h1 {
        color: white;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Encabezado de bienvenida
st.markdown(
    """
    <div class="header-container">
        <h1>CRM COMERCIAL</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Diccionario de usuarios con nombres formateados
usuarios = {
    "ana_laura": {"gestor": "Ana Laura Rivera Inzunza", "password": "UqgPls", "admin": False},
    "cinthia_guadalupe": {"gestor": "Cinthia Guadalupe Checa Robles", "password": "MXjpK4", "admin": False},
    "dafne_gabriela": {"gestor": "Dafne Gabriela Miramontes Graciano", "password": "z3S3ng", "admin": False},
    "guadalupe_paola": {"gestor": "Guadalupe Paola Beltran Ramos", "password":"uPAOLA", "admin": False},
    "jessica_maribel": {"gestor": "Jessica Maribel Vargas Villagrana", "password": "FcUf4T", "admin": False},
    "jesus_anahi": {"gestor": "Jesus Anahi Perez Gamez", "password": "HmicPl", "admin": False},
    "jose_alfredo": {"gestor": "José Alfredo Alvarado Hernandez", "password": "u8FhwV", "admin": False},
    "jose_andres": {"gestor": "Jose Andres Borquez Blanco", "password": "Ams3lC", "admin": False},
    "jose_eduardo": {"gestor": "Jose Eduardo Lopez Portillo Bazua", "password": "ZJ1Q35", "admin": False},
    "bryan_felix": {"gestor": "Bryan Felix", "password": "ZJ1Q35", "admin": False},
    "jose_daniel": {"gestor": "Jose Daniel Flores Herrera", "password": "ZJ1QRZ", "admin": False},
    "julissa_iveth": {"gestor": "Julissa Iveth Gamez Ramirez", "password": "OnHnp4", "admin": False},
    "junnyel_rios": {"gestor":"Bryan Junnyel Rios Castro", "password": "HhR43m", "admin":False},
    "fer_zazueta": {"gestor":"Maria Fernanda Zazueta Aguilar", "password": "bR33y", "admin":False},
    "karely_elizabeth": {"gestor": "Karely Elizabeth Olmeda Gutierrez", "password": "MhDEsm", "admin": False},
    "lizbeth_guadalupe": {"gestor": "Lizbeth Guadalupe Contreras Leal", "password": "32QVMR", "admin": False},
    "melissa_angulo": {"gestor": "Melissa Angulo Rios", "password": "Ok7Wsm", "admin": False},
    "oscar_eduardo": {"gestor": "Oscar Eduardo Sánchez Grande", "password": "FtQ7ZK", "admin": False},
    "reyna_berenice": {"gestor": "Reyna Berenice Salazar Cabrera", "password": "w7sZwz", "admin": False},
    "nancy_burgos": {"gestor": "NANCY BURGOS", "password": "w7sZwz", "admin": False},
    "lorena_andrade": {"gestor": "Lorena Andrade Perez", "password": "w7sZwz", "admin": False},
    "edgar_adolfo": {"gestor": "EDGAR QUIÑONEZ", "password": "eSLa6h", "admin": False},
    "marlene_lopez": {"gestor": "SILVIA LOPEZ", "password": "Marlene_vb$", "admin": False},
    "liliana_cortes": {"gestor": "Liliana Cortes", "password": "admin_vb3$", "admin": True},
    "carlos_quinonez": {"gestor": "Carlos Quiñonez", "password": "admin$", "admin": True},
    "roberto_boada": {"gestor": "Roberto Boada", "password": "admin_vb3$", "admin": True},
    "fernando_valdez": {"gestor": "Fernando Valdez", "password": "admin_vb3$", "admin": True},
    "juan_alberto": {"gestor": "Juan", "password": "admin_vb3$", "admin": True},
    "sergio_millan": {"gestor": "Sergio Millan", "password": "admin_vb3$", "admin": True},
    "rafael_plata": {"gestor": "Rafael Plata", "password": "admin_vb3$", "admin": True}, 
    "administrador": {"gestor": "Administrador", "password": "admin_vb3$", "admin": True},
    "daniela_boada": {"gestor": "Daniela Boada", "password": "Ok7Wsm", "admin": False},
    "carmen_samano": {"gestor": "Carmen Samano", "password": "Ok7Wsm", "admin": False},
}

# Función de inicio de sesión
def login():
    st.title("Iniciar Sesión")
    codigo_acceso = st.text_input("Código de Acceso")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if codigo_acceso in usuarios and usuarios[codigo_acceso]["password"] == password:
            gestor = usuarios[codigo_acceso]["gestor"]
            admin = usuarios[codigo_acceso]["admin"]
            st.success(f"Bienvenido {gestor}")
            st.session_state["authenticated"] = True
            st.session_state["gestor"] = gestor
            st.session_state["admin"] = admin
        else:
            st.error("Código de acceso o contraseña incorrectos")

# Botón para cerrar sesión
def cerrar_sesion():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # Borrar todas las variables de la sesión
    st.experimental_rerun()


# Verificar si el usuario está autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    # Configurar la conexión a SQL Server
    database_url = "mssql+pymssql://credito:Cr3d$.23xme@52.167.231.145:51433/CreditoYCobranza"
    engine = create_engine(database_url)

    gestor_autenticado = st.session_state["gestor"].strip()
    is_admin = st.session_state["admin"]

    gestor_normalizado = normalizar_nombre(gestor_autenticado)


    if is_admin:
        query = "SELECT * FROM CRM_COMERCIAL ORDER BY Jerarquia ASC"
    else:
        # Normalizar nombre (quitar acentos y mayúsculas)
        def normalizar_nombre(nombre):
            traduccion = str.maketrans("ÁÉÍÓÚÑ", "AEIOUN")
            return nombre.upper().translate(traduccion)

        # Tomar los dos primeros componentes del nombre (nombre + primer apellido)
        gestor_sql = " ".join(normalizar_nombre(gestor_autenticado).split()[:2])

        query = f"""
            SELECT * FROM CRM_COMERCIAL
            WHERE UPPER(Gestor) LIKE '%{gestor_sql}%'
            ORDER BY Jerarquia ASC
        """

    data = pd.read_sql(query, engine)


    # Sidebar para navegación y botón de cerrar sesión
    st.sidebar.title(f"Gestor: {gestor_autenticado}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Ir a", [
        "CAT", 
        "ORIGINACION DE CREDITO", 
        "CAMPAÑA MOTOS", 
        "CAMPAÑA SIN FRICCION",
        "CAMPAÑA SIN ENGANCHE",
        "CAMPAÑA REFINANCIAMIENTO",
        "INDICADORES"
    ])
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        cerrar_sesion()

    # Página de Información de Cliente
    if page == "CAT":
        # Verificar permisos
        if not tiene_permiso(gestor_autenticado, "CAT"):
            st.warning("Ups! No tienes acceso a esta pestaña:(")
        else:
            data_cat = data[
                (data["Canal"] == "CAT") &
                (data["Gestor"].apply(lambda x: normalizar_nombre(str(x))) == gestor_normalizado)
            ]

            if data_cat.empty:
                st.warning("No hay clientes asignados en esta campaña.")
            else:
                filtered_data = data_cat
                unique_clients = filtered_data.drop_duplicates(subset=["ID_CLIENTE"]).sort_values(by="Jerarquia").reset_index(drop=True)
                total_clients = len(unique_clients)

                # Sección de búsqueda
                st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
                cols = st.columns([1, 1])
                with cols[0]:
                    input_jerarquia = st.text_input("Borre el numero antes de usar el boton de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
                with cols[1]:
                    input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

                # Búsqueda por Jerarquía
                if input_jerarquia:
                    try:
                        input_jerarquia = int(input_jerarquia)
                        cliente_index = unique_clients[unique_clients["Jerarquia"] == input_jerarquia].index
                        if len(cliente_index) > 0:
                            st.session_state["cliente_index"] = cliente_index[0]
                        else:
                            st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                    except ValueError:
                        st.error("Por favor, ingrese un número válido.")

                # Búsqueda por ID Cliente
                if input_id_cliente:
                    try:
                        cliente_index = unique_clients[unique_clients["ID_CLIENTE"] == input_id_cliente].index
                        if len(cliente_index) > 0:
                            st.session_state["cliente_index"] = cliente_index[0]
                        else:
                            st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
                    except ValueError:
                        st.error("Por favor, ingrese un ID válido.")

                # Validar el índice del cliente actual
                if "cliente_index" not in st.session_state:
                    st.session_state["cliente_index"] = 0
                cliente_index = st.session_state["cliente_index"]
                cliente_index = max(0, min(cliente_index, total_clients - 1))
                st.session_state["cliente_index"] = cliente_index

                # Botones de navegación
                cols_navigation = st.columns([1, 1])
                with cols_navigation[0]:
                    if st.button("Anterior"):
                        st.session_state["cliente_index"] = max(cliente_index - 1, 0)
                with cols_navigation[1]:
                    if st.button("Siguiente"):
                        st.session_state["cliente_index"] = min(cliente_index + 1, total_clients - 1)

                # Obtener cliente actual
                cliente_actual = unique_clients.iloc[st.session_state["cliente_index"]]
                facturas_cliente = filtered_data[filtered_data["ID_CLIENTE"] == cliente_actual["ID_CLIENTE"]]

                # CSS personalizado
                st.markdown("""
                    <style>
                    .ajuste_interlineado {
                        font-size: 18px;
                        line-height: 2.2;
                        margin: 0;
                        padding: 0;
                    }
                    .script-container {
                        background-color: #f9f9f9;
                        border: 2px solid #6495ed;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 20px;
                        font-size: 16px;
                        font-weight: bold;
                        color: #333;
                    }
                    .script-title {
                        font-weight: bold;
                        color: #000080;
                        margin-bottom: 5px;
                        font-size: 18px;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                # Mostrar el script con título
                if "Script" in cliente_actual:
                    st.markdown(f"""
                        <div class="script-container">
                            <div class="script-title">Script:</div>
                            {cliente_actual['Script']}
                        </div>
                    """, unsafe_allow_html=True)
            
                # Mostrar información del cliente actual
                st.markdown('<div class="ajuste_interlineado">', unsafe_allow_html=True)
                st.subheader("Información del Cliente")
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Nombre Solicitante:** {cliente_actual['Solicitante']}")
                    st.write(f"**ID cliente:** {cliente_actual['ID_CLIENTE']}")
                    st.write(f"**Folio:** {cliente_actual['Folio']}")
                    st.write(f"**Limite de credito:** {cliente_actual['Limite_de_credito']}")
                    st.write(f"**Fecha de aprobacion:** {cliente_actual['Fecha_Aprobacion']}")
                    st.write(f"**Ultima Gestion:** {cliente_actual['FECHA_GESTION']}")
                with cols[1]:
                    st.write(f"**Telefono Celular:** {cliente_actual['Tel_Celular']}")
                    st.write(f"**Sucursal:** {cliente_actual['Sucursal']}")
                    st.write(f"**Gestion:** {cliente_actual['Gestion']}")
                    st.write(f"**Comentario:** {cliente_actual['Comentario']}")
                    st.write(f"**Categoria:** {cliente_actual['Segmento']}")
                    st.write(f"**Segmento originación:** {cliente_actual.get('SegmentoOriginacion', 'N/A')}")
                    st.write(f"**Jerarquia:** {cliente_actual['Jerarquia']}")
                    st.markdown(
                        f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>",
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

                st.divider()

                # Gestión del Cliente
                st.subheader("Gestiones del Cliente")
                gestion_key = f"gestion_{cliente_actual['ID_CLIENTE']}"
                comentario_key = f"comentario_{cliente_actual['ID_CLIENTE']}"

                with st.form(key=f"gestion_form"):
                    gestion = st.selectbox(
                        "Gestión",
                        options=[None, "Contacto_Efectivo", "Contacto_NoEfectivo", "Sin_Contacto", "Sin_Cobertura"],
                        index=0 if st.session_state.get(gestion_key) is None else
                              ["Contacto_Efectivo", "Contacto_NoEfectivo", "Sin_Contacto", "Sin_Cobertura"].index(st.session_state[gestion_key]),
                    )
                    comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                    submit_button = st.form_submit_button("Guardar Cambios")

                if submit_button:
                    st.session_state[gestion_key] = gestion
                    st.session_state[comentario_key] = comentario
                    try:
                        query_update = text("""
                            UPDATE CRM_COMERCIAL
                            SET Gestion = :gestion, Comentario = :comentario, FECHA_GESTION = GETDATE()
                            WHERE ID_CLIENTE = :id_cliente
                        """)
                        query_insert = text("""
                            INSERT INTO Gestiones_CRM_Comercial (ID_CLIENTE,GESTION, COMENTARIO, FECHA_GESTION, GESTOR)
                            VALUES (:id_cliente, :gestion, :comentario, GETDATE(), :gestor)
                        """)
                        with engine.begin() as conn:
                            conn.execute(query_update, {
                                "gestion": gestion,
                                "comentario": comentario,
                                "id_cliente": cliente_actual["ID_Cliente"],
                            })
                            conn.execute(query_insert, {
                                "id_cliente": int(cliente_actual["ID_Cliente"]),
                                "gestor": gestor,
                                "gestion": gestion,
                                "comentario": comentario
                            })
                            
                        st.success("Gestión guardada exitosamente.")
                        
                    except Exception as e:
                        st.error(f"Error al guardar los cambios: {e}")
# Página de Originación de Crédito
    elif page == "ORIGINACION DE CREDITO":
        # Verificar permisos
        if not tiene_permiso(gestor_autenticado, "ORIGINACION DE CREDITO"):
            st.warning("Ups! No tienes acceso a esta pestaña:(")
        else:
            data_cat = data[
                (data["Canal"].isin(["Originacion", "CAT"]))&
                (data["Gestor"].apply(lambda x: normalizar_nombre(str(x))) == gestor_normalizado)
            ]

            if data_cat.empty:
                st.warning("No hay clientes asignados en esta campaña.")
            else:
                filtered_data = data_cat
                # Crear columna auxiliar para ordenamiento prioritario: Express primero (0), luego otros (1)
                filtered_data_unique = filtered_data.drop_duplicates(subset=["ID_CLIENTE"])
                filtered_data_unique['_sort_priority'] = filtered_data_unique['SegmentoOriginacion'].apply(lambda x: 0 if x == 'Express' else 1)
                unique_clients = filtered_data_unique.sort_values(by=['_sort_priority', 'Jerarquia']).drop('_sort_priority', axis=1).reset_index(drop=True)
                total_clients = len(unique_clients)

                # Sección de búsqueda
                st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
                cols = st.columns([1, 1])
                with cols[0]:
                    input_jerarquia = st.text_input("Borre el numero antes de usar el boton de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
                with cols[1]:
                    input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

                # Búsqueda por Jerarquía
                if input_jerarquia:
                    try:
                        input_jerarquia = int(input_jerarquia)
                        cliente_index = unique_clients[unique_clients["Jerarquia"] == input_jerarquia].index
                        if len(cliente_index) > 0:
                            st.session_state["cliente_index"] = cliente_index[0]
                        else:
                            st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                    except ValueError:
                        st.error("Por favor, ingrese un número válido.")

                # Búsqueda por ID Cliente
                if input_id_cliente:
                    try:
                        cliente_index = unique_clients[unique_clients["ID_CLIENTE"] == input_id_cliente].index
                        if len(cliente_index) > 0:
                            st.session_state["cliente_index"] = cliente_index[0]
                        else:
                            st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
                    except ValueError:
                        st.error("Por favor, ingrese un ID válido.")

                # Validar el índice del cliente actual
                if "cliente_index" not in st.session_state:
                    st.session_state["cliente_index"] = 0
                cliente_index = st.session_state["cliente_index"]
                cliente_index = max(0, min(cliente_index, total_clients - 1))
                st.session_state["cliente_index"] = cliente_index

                # Botones de navegación
                cols_navigation = st.columns([1, 1])
                with cols_navigation[0]:
                    if st.button("Anterior"):
                        st.session_state["cliente_index"] = max(cliente_index - 1, 0)
                with cols_navigation[1]:
                    if st.button("Siguiente"):
                        st.session_state["cliente_index"] = min(cliente_index + 1, total_clients - 1)

                # Obtener cliente actual
                cliente_actual = unique_clients.iloc[st.session_state["cliente_index"]]

                # CSS personalizado
                st.markdown("""
                    <style>
                    .ajuste_interlineado {
                        font-size: 18px;
                        line-height: 2.2;
                        margin: 0;
                        padding: 0;
                    }
                    .script-container {
                        background-color: #f9f9f9;
                        border: 2px solid #6495ed;
                        border-radius: 8px;
                        padding: 15px;
                        margin-bottom: 20px;
                        font-size: 16px;
                        font-weight: bold;
                        color: #333;
                    }
                    .script-title {
                        font-weight: bold;
                        color: #000080;
                        margin-bottom: 5px;
                        font-size: 18px;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                # Mostrar el script con título
                if "Script" in cliente_actual:
                    st.markdown(f"""
                        <div class="script-container">
                            <div class="script-title">Script:</div>
                            {cliente_actual['Script']}
                        </div>
                    """, unsafe_allow_html=True)
            
                # Mostrar información del cliente actual
                st.markdown('<div class="ajuste_interlineado">', unsafe_allow_html=True)
                st.subheader("Información del Cliente")
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Nombre Solicitante:** {cliente_actual['Solicitante']}")
                    st.write(f"**ID cliente:** {cliente_actual['ID_CLIENTE']}")
                    st.write(f"**Folio:** {cliente_actual['Folio']}")
                    st.write(f"**Limite de credito:** {cliente_actual['Limite_de_credito']}")
                    st.write(f"**Fecha de aprobacion:** {cliente_actual['Fecha_Aprobacion']}")
                    st.write(f"**Ultima Gestion:** {cliente_actual['FECHA_GESTION']}")
                with cols[1]:
                    st.write(f"**Telefono Celular:** {cliente_actual['Tel_Celular']}")
                    st.write(f"**Sucursal:** {cliente_actual['Sucursal']}")
                    st.write(f"**Gestion:** {cliente_actual['Gestion']}")
                    st.write(f"**Comentario:** {cliente_actual['Comentario']}")
                    st.write(f"**Categoria:** {cliente_actual['Segmento']}")
                    st.write(f"**Segmento originación:** {cliente_actual.get('SegmentoOriginacion', 'N/A')}")
                    st.write(f"**Jerarquia:** {cliente_actual['Jerarquia']}")
                    st.markdown(
                        f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>",
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

                st.divider()

                # Gestión del Cliente
                st.subheader("Gestiones del Cliente")
                gestion_key = f"gestion_{cliente_actual['ID_CLIENTE']}"
                comentario_key = f"comentario_{cliente_actual['ID_CLIENTE']}"

                with st.form(key=f"gestion_form"):
                    gestion = st.selectbox(
                        "Gestión",
                        options=[None, "Contacto_Efectivo", "Contacto_NoEfectivo", "Sin_Contacto", "Sin_Cobertura"],
                        index=0 if st.session_state.get(gestion_key) is None else
                              ["Contacto_Efectivo", "Contacto_NoEfectivo", "Sin_Contacto", "Sin_Cobertura"].index(st.session_state[gestion_key]),
                    )
                    comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                    submit_button = st.form_submit_button("Guardar Cambios")

                if submit_button:
                    st.session_state[gestion_key] = gestion
                    st.session_state[comentario_key] = comentario
                    try:
                        query_update = text("""
                            UPDATE CRM_COMERCIAL
                            SET Gestion = :gestion, Comentario = :comentario, FECHA_GESTION = GETDATE()
                            WHERE ID_CLIENTE = :id_cliente
                        """)
                        query_insert = text("""
                            INSERT INTO Gestiones_CRM_Comercial (ID_CLIENTE,GESTION, COMENTARIO, FECHA_GESTION, GESTOR)
                            VALUES (:id_cliente, :gestion, :comentario, GETDATE(), :gestor)
                        """)
                        with engine.begin() as conn:
                            conn.execute(query_update, {
                                "gestion": gestion,
                                "comentario": comentario,
                                "id_cliente": cliente_actual["ID_CLIENTE"],
                            })
                            conn.execute(query_insert, {
                                "id_cliente": cliente_actual["ID_CLIENTE"],
                                "gestion": gestion,
                                "comentario": comentario,
                                "gestor": st.session_state["gestor"],
                            })
                        st.success("Gestión guardada exitosamente.")
                    except Exception as e:
                        st.error(f"Error al guardar los cambios: {e}")

    # CAMPAÑA MOTOS
    elif page == "CAMPAÑA MOTOS":
        # Verificar permisos
        if not tiene_permiso(gestor_autenticado, "CAMPAÑA MOTOS"):
            st.warning("Ups! No tienes acceso a esta pestaña :(")
        else:
            # 1) Cargar datos
            query_motos = "SELECT * FROM CRM_MOTOS_Final where gestion <> 'Numero equivocado'"
            data_motos = pd.read_sql(query_motos, engine)
            
            # 2) Filtrar por gestor y eliminar IDs inválidos
            data_motos = data_motos[data_motos["GestorVirtual"] == gestor_autenticado].copy()
            data_motos = data_motos.dropna(subset=["ID_Cliente"])
            
            # 3) Asegurar FECHA_GESTION como datetime
            data_motos["FECHA_GESTION"] = pd.to_datetime(data_motos["FECHA_GESTION"], errors="coerce")
            
            # 4) Lógica de jerarquía fija
            if "NumeroCliente" in data_motos.columns and not data_motos["NumeroCliente"].isna().all():
                data_motos = data_motos.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
                data_motos["jerarquia"] = data_motos.index + 1
            else:
                data_motos["orden_auxiliar"] = data_motos["FECHA_GESTION"].fillna(pd.Timestamp.min)
                data_motos = (
                    data_motos
                    .sort_values(by=["orden_auxiliar"], ascending=True)
                    .reset_index(drop=True)
                )
                data_motos["jerarquia"] = data_motos.index + 1
                data_motos.drop(columns=["orden_auxiliar"], inplace=True)
            
            if data_motos.empty:
                st.warning("No hay datos en la campaña de motos.")
            else:
                # 5) Preparar lista única de clientes
                unique_clients = data_motos.drop_duplicates(subset=["ID_Cliente"]).reset_index(drop=True)
                total_clients = len(unique_clients)
                
                # 6) UI de búsqueda por jerarquía o ID
                st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
                cols = st.columns([1, 1])
                with cols[0]:
                    input_jerarquia = st.text_input("Borre el numero antes de usar el botón de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
                with cols[1]:
                    input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

                if input_jerarquia:
                    try:
                        input_jerarquia = int(input_jerarquia)
                        idx = unique_clients[unique_clients["jerarquia"] == input_jerarquia].index
                        if idx.size:
                            st.session_state["cliente_index_motos"] = idx[0]
                        else:
                            st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                    except ValueError:
                        st.error("Por favor, ingrese un número válido.")

                if input_id_cliente:
                    idx = unique_clients[unique_clients["ID_Cliente"] == input_id_cliente].index
                    if idx.size:
                        st.session_state["cliente_index_motos"] = idx[0]
                    else:
                        st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
                
                # 7) Inicializar y acotar índice
                if "cliente_index_motos" not in st.session_state:
                    st.session_state["cliente_index_motos"] = 0
                cliente_index = st.session_state["cliente_index_motos"]
                cliente_index = max(0, min(cliente_index, total_clients - 1))
                st.session_state["cliente_index_motos"] = cliente_index
                
                # 8) Botones de navegación
                nav_cols = st.columns([1, 1])
                with nav_cols[0]:
                    if st.button("Anterior"):
                        st.session_state["cliente_index_motos"] = max(cliente_index - 1, 0)
                with nav_cols[1]:
                    if st.button("Siguiente"):
                        st.session_state["cliente_index_motos"] = min(cliente_index + 1, total_clients - 1)

                cliente_actual = unique_clients.iloc[st.session_state["cliente_index_motos"]]
                
                # 9) Mostrar cliente actual
                st.subheader("Información del Cliente - Campaña Motos")
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Nombre:** {cliente_actual['Nom_Cte']}")
                    st.write(f"**ID cliente:** {cliente_actual['ID_Cliente']}")
                    st.write(f"**Sucursal:** {cliente_actual['Ultima_Sucursal']}")
                    st.write(f"**Teléfono:** {cliente_actual['Telefono']}")
                    st.write(f"**Jerarquia:** {cliente_actual['jerarquia']}")

                with cols[1]:
                    st.write(f"**Modelo:** {cliente_actual['Modelo_Moto']}")
                    st.write(f"**Costo Moto:** {cliente_actual['Costo_Moto']}")
                    st.write(f"**Limite de crédito:** {cliente_actual['Limite_credito']}")
                    st.write(f"**Credito disponible:** {cliente_actual['Credito_Disponible']}")
                    
                    # Formatear enganche como porcentaje
                    enganche_valor = cliente_actual.get('Enganche_Motos', 0)
                    if pd.notna(enganche_valor) and enganche_valor != 0:
                        enganche_porcentaje = f"{float(enganche_valor) * 100:.0f}%"
                    else:
                        enganche_porcentaje = "0%"
                    st.write(f"**Enganche:** {enganche_porcentaje}")
                    
                    # Fecha última gestión
                    raw_fecha = cliente_actual.get("FECHA_GESTION", None)
                    fecha_dt = pd.to_datetime(raw_fecha, errors="coerce")
                    fecha_str = fecha_dt.strftime("%Y/%m/%d") if pd.notna(fecha_dt) else "N/A"
                    st.write(f"**Fecha de Última Gestión:** {fecha_str}")
                    st.markdown(f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>", unsafe_allow_html=True)
                st.divider()
                
                # 10) Formulario de gestión
                st.subheader("Gestiones del Cliente")
                gestion_key = f"gestion_motos_{cliente_actual['ID_Cliente']}"
                comentario_key = f"comentario_motos_{cliente_actual['ID_Cliente']}"

                with st.form(key=f"gestion_form_motos"):
                    gestion = st.selectbox(
                        "Gestión",
                        options=[None, "Interesado", "Llamar Después", "Recado", "Sin contacto", "No interesado", "Numero equivocado"],
                        index=0 if st.session_state.get(gestion_key) is None else
                            ["Interesado", "Llamar Después", "Recado", "Sin contacto", "No interesado", "Numero equivocado"].index(
                                st.session_state[gestion_key]
                            ),
                    )
                    comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                    submit_button = st.form_submit_button("Guardar Gestión")

                if submit_button:
                    st.session_state[gestion_key] = gestion
                    st.session_state[comentario_key] = comentario
                    try:
                        gestor = st.session_state.get("gestor")
                        
                        query_update = text("""
                            UPDATE CRM_MOTOS_Final
                            SET Gestion = :gestion, 
                                Comentario = :comentario
                            WHERE ID_Cliente = :id_cliente
                        """)
                        
                        query_insert = text("""
                            INSERT INTO GESTIONES_CAMPAÑAS_COMERCIAL (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                            VALUES (:id_cliente, 'CAMPAÑA MOTOS', GETDATE(), :gestor, :gestion, :comentario)
                        """)
                        
                        with engine.begin() as conn:
                            conn.execute(query_update, {
                                "gestion": gestion,
                                "comentario": comentario,
                                "id_cliente": cliente_actual["ID_Cliente"],
                            })
                            conn.execute(query_insert, {
                                "id_cliente": int(cliente_actual["ID_Cliente"]),
                                "gestor": gestor,
                                "gestion": gestion,
                                "comentario": comentario
                            })
                        
                        st.success("Gestión guardada exitosamente.")
                        
                    except Exception as e:
                        st.error(f"Error al guardar los cambios: {e}")
    elif page == "CAMPAÑA SIN FRICCION":
        # 1) Cargar los datos desde SQL
        query_sinfriccion = "SELECT * FROM CRM_SINFRICCION_Final where gestion <> 'Numero equivocado'"
        data_sinfriccion = pd.read_sql(query_sinfriccion, engine)

        # 2) Filtrar solo los clientes asignados al gestor autenticado
        data_sinfriccion = data_sinfriccion[
            data_sinfriccion["GestorVirtual"] == gestor_autenticado
        ].copy()

        # 3) Eliminar los clientes sin ID válido
        data_sinfriccion = data_sinfriccion.dropna(subset=["ID_Cliente"])

        # 4) Asegurarnos de que FECHA_GESTION sea datetime
        data_sinfriccion["FECHA_GESTION"] = pd.to_datetime(
            data_sinfriccion["FECHA_GESTION"], errors="coerce"
        )

        # 5) LÓGICA DE JERARQUÍA FIJA - usar NumeroCliente de la BD
        # La columna de jerarquía en BD se llama "NumeroCliente"
        # La columna de jerarquía en BD se llama "NumeroCliente"
        if "NumeroCliente" in data_sinfriccion.columns and not data_sinfriccion["NumeroCliente"].isna().all():
            # Ordenar por NumeroCliente pero reindexar la jerarquía desde 1
            data_sinfriccion = data_sinfriccion.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
            data_sinfriccion["jerarquia"] = data_sinfriccion.index + 1  # ← SIEMPRE desde 1
        else:
            # Crear jerarquía solo si no existe en BD
            data_sinfriccion["orden_auxiliar"] = data_sinfriccion["FECHA_GESTION"].fillna(pd.Timestamp.min)
            data_sinfriccion = (
                data_sinfriccion
                .sort_values(by=["orden_auxiliar"], ascending=True)
                .reset_index(drop=True)
            )
            data_sinfriccion["jerarquia"] = data_sinfriccion.index + 1
            data_sinfriccion.drop(columns=["orden_auxiliar"], inplace=True)

        if data_sinfriccion.empty:
            st.warning("No hay datos en la campaña sin fricción.")
        else:
            # 6) Preparar lista única de clientes (manteniendo jerarquía original)
            unique_clients = data_sinfriccion.drop_duplicates(subset=["ID_Cliente"]).reset_index(drop=True)
            total_clients = len(unique_clients)

            # 7) UI de búsqueda por jerarquía o ID
            st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
            cols = st.columns([1, 1])
            with cols[0]:
                input_jerarquia = st.text_input("Borre el numero antes de usar el botón de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
            with cols[1]:
                input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

            # Búsqueda por Jerarquía
            if input_jerarquia:
                try:
                    input_jerarquia = int(input_jerarquia)
                    cliente_index = unique_clients[unique_clients["jerarquia"] == input_jerarquia].index
                    if len(cliente_index) > 0:
                        st.session_state["cliente_index_sinfriccion"] = cliente_index[0]
                    else:
                        st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                except ValueError:
                    st.error("Por favor, ingrese un número válido.")

            # Búsqueda por ID Cliente
            if input_id_cliente:
                cliente_index = unique_clients[unique_clients["ID_Cliente"] == input_id_cliente].index
                if len(cliente_index) > 0:
                    st.session_state["cliente_index_sinfriccion"] = cliente_index[0]
                else:
                    st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")

            # 8) Validar el índice del cliente actual
            if "cliente_index_sinfriccion" not in st.session_state:
                st.session_state["cliente_index_sinfriccion"] = 0
            cliente_index = st.session_state["cliente_index_sinfriccion"]
            cliente_index = max(0, min(cliente_index, total_clients - 1))
            st.session_state["cliente_index_sinfriccion"] = cliente_index

            # 9) Botones de navegación
            cols_navigation = st.columns([1, 1])
            with cols_navigation[0]:
                if st.button("Anterior"):
                    st.session_state["cliente_index_sinfriccion"] = max(cliente_index - 1, 0)
            with cols_navigation[1]:
                if st.button("Siguiente"):
                    st.session_state["cliente_index_sinfriccion"] = min(cliente_index + 1, total_clients - 1)

            # 10) Obtener cliente actual
            cliente_actual = unique_clients.iloc[st.session_state["cliente_index_sinfriccion"]]

            # 11) Mostrar información del cliente actual
            st.subheader("Información del Cliente - Campaña Sin Fricción")
            cols = st.columns(2)
            with cols[0]:
                st.write(f"**Nombre:** {cliente_actual['Nom_Cte']}")
                st.write(f"**ID cliente:** {cliente_actual['ID_Cliente']}")
                st.write(f"**Sucursal:** {cliente_actual['Ultima_Sucursal']}")
                st.write(f"**Teléfono:** {cliente_actual['Telefono']}")
                st.write(f"**Jerarquia:** {cliente_actual['jerarquia']}")
                
            with cols[1]:
                st.write(f"**Mensualidad:** {cliente_actual['Mensualidad_Actual']}")
                st.write(f"**Saldo Actual:** {cliente_actual['SaldoActual']}")
                st.write(f"**Limite de crédito:** {cliente_actual['Limite_credito']}")
                st.write(f"**Credito disponible:** {cliente_actual['Credito_Disponible']}")
                
                # Formatear enganches como porcentajes
                enganche_no_motos = cliente_actual.get('Enganche_No_Motos', 0)
                enganche_motos = cliente_actual.get('Enganche_Motos', 0)
                
                if pd.notna(enganche_no_motos) and enganche_no_motos != 0:
                    enganche_no_motos_pct = f"{float(enganche_no_motos) * 100:.0f}%"
                else:
                    enganche_no_motos_pct = "0%"
                    
                if pd.notna(enganche_motos) and enganche_motos != 0:
                    enganche_motos_pct = f"{float(enganche_motos) * 100:.0f}%"
                else:
                    enganche_motos_pct = "0%"
                    
                st.write(f"**Enganche No Motos:** {enganche_no_motos_pct}")
                st.write(f"**Enganche Motos:** {enganche_motos_pct}")
                
                # Fecha última gestión
                raw_fecha = cliente_actual.get("FECHA_GESTION", None)
                fecha_dt = pd.to_datetime(raw_fecha, errors="coerce")
                fecha_str = fecha_dt.strftime("%Y/%m/%d") if pd.notna(fecha_dt) else "N/A"
                st.write(f"**Fecha última gestión:** {fecha_str}")

                st.markdown(
                    f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>",
                    unsafe_allow_html=True,
                )

            st.divider()

            # 12) Formulario de gestión
            st.subheader("Gestiones del Cliente")
            gestion_key = f"gestion_sinfriccion_{cliente_actual['ID_Cliente']}"
            comentario_key = f"comentario_sinfriccion_{cliente_actual['ID_Cliente']}"

            with st.form(key=f"gestion_form_sinfriccion"):
                gestion = st.selectbox(
                    "Gestión",
                    options=[None, "Interesado", "No interesado", "Recado", "Sin contacto", "Numero equivocado"],
                    index=0 if st.session_state.get(gestion_key) is None else
                        ["Interesado", "No interesado", "Recado", "Sin contacto", "Numero equivocado"].index(st.session_state[gestion_key]),
                )
                comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                submit_button = st.form_submit_button("Guardar Gestión")

            if submit_button:
                st.session_state[gestion_key] = gestion
                st.session_state[comentario_key] = comentario
                try:
                    gestor = st.session_state.get("gestor") 
                    
                    # IMPORTANTE: NO actualizar FECHA_GESTION en CRM_SINFRICCION_Final
                    # Solo actualizar Gestion y Comentario
                    # La fecha se actualizará mañana con el SP nocturno
                    query_update = text("""
                        UPDATE CRM_SINFRICCION_Final
                        SET Gestion = :gestion, 
                            Comentario = :comentario 
                        WHERE ID_Cliente = :id_cliente
                    """)

                    # Solo guardar el histórico con fecha actual
                    query_insert = text("""
                        INSERT INTO GESTIONES_CAMPAÑA_SINFRICCION (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                        VALUES (:id_cliente, 'CAMPAÑA SIN FRICCION', GETDATE(), :gestor, :gestion, :comentario)
                    """)

                    with engine.begin() as conn:
                        conn.execute(query_update, {
                            "gestion": gestion,
                            "comentario": comentario,
                            "id_cliente": cliente_actual["ID_Cliente"],
                        })
                        conn.execute(query_insert, {
                            "id_cliente": int(cliente_actual["ID_Cliente"]),
                            "gestor": gestor,
                            "gestion": gestion,
                            "comentario": comentario
                        })
                        
                    st.success("Gestión guardada exitosamente.")
                    
                    # NO usar st.rerun() para mantener jerarquía fija durante el día
                    # La jerarquía solo cambiará mañana con el SP nocturno
                    
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {e}")
    # CAMPAÑA SIN ENGANCHE
    # CAMPAÑA SIN ENGANCHE - CÓDIGO CORREGIDO
    elif page == "CAMPAÑA SIN ENGANCHE":
        # Verificar permisos
        if not tiene_permiso(gestor_autenticado, "CAMPAÑA SIN ENGANCHE"):
            st.warning("Ups! No tienes acceso a esta pestaña :(")
        else:
            # 1) Cargar datos
            query_sin_enganche = "SELECT * FROM CampañaSinEnganche WHERE gestion IS NULL OR gestion <> 'Numero equivocado'"
            data_sin_enganche = pd.read_sql(query_sin_enganche, engine)
            
            # 2) Filtrar por gestor y eliminar IDs inválidos
            data_sin_enganche = data_sin_enganche[data_sin_enganche["GestorVirtual"] == gestor_autenticado].copy()
            data_sin_enganche = data_sin_enganche.dropna(subset=["ID_CLIENTE"])  # CORREGIDO: Cambié ID_Cliente por ID_CLIENTE
            
            # 3) Asegurar FECHA_GESTION como datetime
            data_sin_enganche["FECHA_GESTION"] = pd.to_datetime(data_sin_enganche["FECHA_GESTION"], errors="coerce")
            
            # 4) Lógica de jerarquía fija - usar NumeroCliente
            if "NumeroCliente" in data_sin_enganche.columns and not data_sin_enganche["NumeroCliente"].isna().all():
                data_sin_enganche = data_sin_enganche.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
                data_sin_enganche["jerarquia"] = data_sin_enganche.index + 1
            else:
                data_sin_enganche["orden_auxiliar"] = data_sin_enganche["FECHA_GESTION"].fillna(pd.Timestamp.min)
                data_sin_enganche = (
                    data_sin_enganche
                    .sort_values(by=["orden_auxiliar"], ascending=True)
                    .reset_index(drop=True)
                )
                data_sin_enganche["jerarquia"] = data_sin_enganche.index + 1
                data_sin_enganche.drop(columns=["orden_auxiliar"], inplace=True)
            
            if data_sin_enganche.empty:
                st.warning("No hay datos en la campaña sin enganche.")
            else:
                # 5) Preparar lista única de clientes
                unique_clients = data_sin_enganche.drop_duplicates(subset=["ID_CLIENTE"]).reset_index(drop=True)  # CORREGIDO
                total_clients = len(unique_clients)
                
                # 6) UI de búsqueda por jerarquía o ID
                st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
                cols = st.columns([1, 1])
                with cols[0]:
                    input_jerarquia = st.text_input("Borre el numero antes de usar el botón de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
                with cols[1]:
                    input_id_cliente = st.text_input("ID Cliente", "", help="Ingrese el ID del cliente y presione Enter")

                if input_jerarquia:
                    try:
                        input_jerarquia = int(input_jerarquia)
                        idx = unique_clients[unique_clients["jerarquia"] == input_jerarquia].index
                        if idx.size:
                            st.session_state["cliente_index_sin_enganche"] = idx[0]
                        else:
                            st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                    except ValueError:
                        st.error("Por favor, ingrese un número válido.")

                if input_id_cliente:
                    try:
                        input_id_cliente = int(input_id_cliente) if input_id_cliente.isdigit() else input_id_cliente
                        idx = unique_clients[unique_clients["ID_CLIENTE"] == input_id_cliente].index  # CORREGIDO
                        if idx.size:
                            st.session_state["cliente_index_sin_enganche"] = idx[0]
                        else:
                            st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
                    except ValueError:
                        st.error("Por favor, ingrese un ID válido.")
                
                # 7) Inicializar y acotar índice
                if "cliente_index_sin_enganche" not in st.session_state:
                    st.session_state["cliente_index_sin_enganche"] = 0
                cliente_index = st.session_state["cliente_index_sin_enganche"]
                cliente_index = max(0, min(cliente_index, total_clients - 1))
                st.session_state["cliente_index_sin_enganche"] = cliente_index
                
                # 8) Botones de navegación
                nav_cols = st.columns([1, 1])
                with nav_cols[0]:
                    if st.button("Anterior"):
                        st.session_state["cliente_index_sin_enganche"] = max(cliente_index - 1, 0)
                with nav_cols[1]:
                    if st.button("Siguiente"):
                        st.session_state["cliente_index_sin_enganche"] = min(cliente_index + 1, total_clients - 1)

                cliente_actual = unique_clients.iloc[st.session_state["cliente_index_sin_enganche"]]
                
                # 9) Mostrar cliente actual
                st.subheader("Información del Cliente - Campaña Sin Enganche")
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Nombre:** {cliente_actual.get('NombreCliente', 'N/A')}")  # NUEVO: Mostrar nombre
                    st.write(f"**ID Cliente:** {cliente_actual['ID_CLIENTE']}")
                    st.write(f"**Primer Teléfono:** {cliente_actual.get('PrimerTelefono', 'N/A')}")
                    st.write(f"**Segundo Teléfono:** {cliente_actual.get('SegundoTelefono', 'N/A')}")
                    st.write(f"**Jerarquia:** {cliente_actual['jerarquia']}")

                with cols[1]:
                    st.write(f"**CC Actual:** {cliente_actual.get('CC_Actual', 'N/A')}")
                    st.write(f"**LC Actual:** {cliente_actual.get('LC_Actual', 'N/A')}")
                    st.write(f"**LC Disponible:** {cliente_actual.get('LC_Disponible', 'N/A')}")
                    st.write(f"**Score Ponderado:** {cliente_actual.get('ScorePonderado', 'N/A')}")
                    st.write(f"**Facturas Liquidadas:** {cliente_actual.get('Facturas_Liquidadas', 'N/A')}")
                    st.write(f"**Facturas Activas:** {cliente_actual.get('Facturas_Activas', 'N/A')}")
                    
                    # Formatear enganche como porcentaje
                    enganche_valor = cliente_actual.get('Enganche', 0)
                    if pd.notna(enganche_valor) and enganche_valor != 0:
                        enganche_porcentaje = f"{float(enganche_valor) * 100:.0f}%"
                    else:
                        enganche_porcentaje = "0%"
                    st.write(f"**Enganche:** {enganche_porcentaje}")
                    
                    # Fecha última gestión
                    raw_fecha = cliente_actual.get("FECHA_GESTION", None)
                    fecha_dt = pd.to_datetime(raw_fecha, errors="coerce")
                    fecha_str = fecha_dt.strftime("%Y/%m/%d") if pd.notna(fecha_dt) else "N/A"
                    st.write(f"**Fecha de Última Gestión:** {fecha_str}")
                    st.markdown(f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual.get('Gestion')) else 'No'}</span>", unsafe_allow_html=True)
                
                st.divider()
                
                # 10) Formulario de gestión
                st.subheader("Gestiones del Cliente")
                gestion_key = f"gestion_sin_enganche_{cliente_actual['ID_CLIENTE']}"  # CORREGIDO
                comentario_key = f"comentario_sin_enganche_{cliente_actual['ID_CLIENTE']}"  # CORREGIDO

                with st.form(key=f"gestion_form_sin_enganche"):
                    gestion = st.selectbox(
                        "Gestión",
                        options=[None, "Interesado", "No interesado", "Llamar Después", "Recado", "Sin contacto", "Numero equivocado"],
                        index=0 if st.session_state.get(gestion_key) is None else
                            ["Interesado", "No interesado", "Llamar Después", "Recado", "Sin contacto", "Numero equivocado"].index(
                                st.session_state[gestion_key]
                            ) + 1,
                    )
                    comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                    submit_button = st.form_submit_button("Guardar Gestión")

                if submit_button:
                                st.session_state[gestion_key] = gestion
                                st.session_state[comentario_key] = comentario
                                try:
                                    gestor = st.session_state.get("gestor")
                                    
                                    # CONVERSIÓN EXPLÍCITA A TIPOS PYTHON NATIVOS
                                    id_cliente_valor = cliente_actual["ID_CLIENTE"]
                                    
                                    # Convertir numpy.int64 a int de Python
                                    if hasattr(id_cliente_valor, 'item'):
                                        id_cliente_python = id_cliente_valor.item()  # Convierte numpy.int64 a int
                                    else:
                                        id_cliente_python = int(id_cliente_valor)  # Conversión regular
                                    
                                    query_update = text("""
                                        UPDATE CampañaSinEnganche
                                        SET Gestion = :gestion, 
                                            Comentario = :comentario
                                        WHERE ID_CLIENTE = :id_cliente
                                    """)
                                    
                                    query_insert = text("""
                                        INSERT INTO GESTIONES_CAMPAÑA_SIN_ENGANCHE (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                                        VALUES (:id_cliente, 'CAMPAÑA SIN ENGANCHE', GETDATE(), :gestor, :gestion, :comentario)
                                    """)
                                    
                                    with engine.begin() as conn:
                                        conn.execute(query_update, {
                                            "gestion": gestion,
                                            "comentario": comentario,
                                            "id_cliente": id_cliente_python,  # Usar el valor convertido
                                        })
                                        conn.execute(query_insert, {
                                            "id_cliente": str(id_cliente_python),  # Convertir a string también
                                            "gestor": gestor,
                                            "gestion": gestion,
                                            "comentario": comentario
                                        })
                                    
                                    st.success("Gestión guardada exitosamente.")
                                    
                                except Exception as e:
                                    st.error(f"Error al guardar los cambios: {e}")

    # CAMPAÑA REFINANCIAMIENTO
    # CAMPAÑA REFINANCIAMIENTO
    elif page == "CAMPAÑA REFINANCIAMIENTO":
        # Verificar permisos
        if not tiene_permiso(gestor_autenticado, "CAMPAÑA REFINANCIAMIENTO"):
            st.warning("Ups! No tienes acceso a esta pestaña :(")
        else:
            # 1) Cargar datos
            query_refinanciamiento = "SELECT * FROM Tabla_Campaña_Refinanciamiento WHERE gestion IS NULL OR gestion <> 'Numero equivocado'"
            data_refinanciamiento = pd.read_sql(query_refinanciamiento, engine)
            
            # 2) Filtrar por gestor y eliminar IDs inválidos
            data_refinanciamiento = data_refinanciamiento[data_refinanciamiento["GestorVirtual"] == gestor_autenticado].copy()
            data_refinanciamiento = data_refinanciamiento.dropna(subset=["SapIdCliente"])
            
            # 3) Asegurar FECHA_GESTION como datetime
            data_refinanciamiento["FECHA_GESTION"] = pd.to_datetime(data_refinanciamiento["FECHA_GESTION"], errors="coerce")
            
            # 4) Lógica de jerarquía fija - usar NumeroCliente
            if "NumeroCliente" in data_refinanciamiento.columns and not data_refinanciamiento["NumeroCliente"].isna().all():
                data_refinanciamiento = data_refinanciamiento.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
                data_refinanciamiento["jerarquia"] = data_refinanciamiento.index + 1
            else:
                data_refinanciamiento["orden_auxiliar"] = data_refinanciamiento["FECHA_GESTION"].fillna(pd.Timestamp.min)
                data_refinanciamiento = (
                    data_refinanciamiento
                    .sort_values(by=["orden_auxiliar"], ascending=True)
                    .reset_index(drop=True)
                )
                data_refinanciamiento["jerarquia"] = data_refinanciamiento.index + 1
                data_refinanciamiento.drop(columns=["orden_auxiliar"], inplace=True)
            
            if data_refinanciamiento.empty:
                st.warning("No hay datos en la campaña de refinanciamiento.")
            else:
                # 5) Preparar lista única de clientes
                unique_clients = data_refinanciamiento.drop_duplicates(subset=["SapIdCliente"]).reset_index(drop=True)
                total_clients = len(unique_clients)
                
                # 6) UI de búsqueda por jerarquía o ID
                st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda por Jerarquia</div>", unsafe_allow_html=True)
                cols = st.columns([1, 1])
                with cols[0]:
                    input_jerarquia = st.text_input("Borre el numero antes de usar el botón de siguiente", "", help="Ingrese la jerarquía del cliente y presione Enter")
                with cols[1]:
                    input_id_cliente = st.text_input("SapIdCliente", "", help="Ingrese el ID del cliente y presione Enter")

                if input_jerarquia:
                    try:
                        input_jerarquia = int(input_jerarquia)
                        idx = unique_clients[unique_clients["jerarquia"] == input_jerarquia].index
                        if idx.size:
                            st.session_state["cliente_index_refinanciamiento"] = idx[0]
                        else:
                            st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                    except ValueError:
                        st.error("Por favor, ingrese un número válido.")

                if input_id_cliente:
                    try:
                        input_id_cliente = int(input_id_cliente) if input_id_cliente.isdigit() else input_id_cliente
                        idx = unique_clients[unique_clients["SapIdCliente"] == input_id_cliente].index
                        if idx.size:
                            st.session_state["cliente_index_refinanciamiento"] = idx[0]
                        else:
                            st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")
                    except ValueError:
                        st.error("Por favor, ingrese un ID válido.")
                
                # 7) Inicializar y acotar índice
                if "cliente_index_refinanciamiento" not in st.session_state:
                    st.session_state["cliente_index_refinanciamiento"] = 0
                cliente_index = st.session_state["cliente_index_refinanciamiento"]
                cliente_index = max(0, min(cliente_index, total_clients - 1))
                st.session_state["cliente_index_refinanciamiento"] = cliente_index
                
                # 8) Botones de navegación
                nav_cols = st.columns([1, 1])
                with nav_cols[0]:
                    if st.button("Anterior"):
                        st.session_state["cliente_index_refinanciamiento"] = max(cliente_index - 1, 0)
                with nav_cols[1]:
                    if st.button("Siguiente"):
                        st.session_state["cliente_index_refinanciamiento"] = min(cliente_index + 1, total_clients - 1)

                cliente_actual = unique_clients.iloc[st.session_state["cliente_index_refinanciamiento"]]
                
                # 9) Mostrar cliente actual
                st.subheader("Información del Cliente - Campaña Refinanciamiento")
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Nombre:** {cliente_actual.get('Nom_Cte', 'N/A')}")
                    st.write(f"**SapIdCliente:** {cliente_actual['SapIdCliente']}")
                    st.write(f"**Primer Teléfono:** {cliente_actual.get('PrimerTelefono', 'N/A')}")
                    st.write(f"**Segundo Teléfono:** {cliente_actual.get('SegundoTelefono', 'N/A')}")
                    st.write(f"**Jerarquia:** {cliente_actual['jerarquia']}")

                with cols[1]:
                    st.write(f"**Segmento:** {cliente_actual.get('Segmento', 'N/A')}")
                    st.write(f"**LC Actual:** {cliente_actual.get('LC_Actual', 'N/A')}")
                    st.write(f"**LC Disponible:** {cliente_actual.get('LC_Disponible', 'N/A')}")
                    st.write(f"**LiquideCon:** {cliente_actual.get('LiquideCon', 'N/A')}")
                    st.write(f"**Saldo Actual:** {cliente_actual.get('SaldoActual', 'N/A')}")
                    st.write(f"**Pagado:** {cliente_actual.get('Pagado', 'N/A')}")
                    st.write(f"**Total Factura:** {cliente_actual.get('TotalFactura', 'N/A')}")
                    
                    # Formatear porcentaje pagado
                    porcentaje_valor = cliente_actual.get('Porcentaje_Pagado', 0)
                    if pd.notna(porcentaje_valor) and porcentaje_valor != 0:
                        porcentaje_str = f"{float(porcentaje_valor) * 100:.1f}%"
                    else:
                        porcentaje_str = "0%"
                    st.write(f"**Porcentaje Pagado:** {porcentaje_str}")
                    
                    st.write(f"**AP VAP FACTURA:** {cliente_actual.get('AP_VAP_FACTURA', 'N/A')}")
                    st.write(f"**Plazo:** {cliente_actual.get('Plazo', 'N/A')}")
                    st.write(f"**Folio:** {cliente_actual.get('Folio', 'N/A')}")
                    
                    # Fecha última gestión
                    raw_fecha = cliente_actual.get("FECHA_GESTION", None)
                    fecha_dt = pd.to_datetime(raw_fecha, errors="coerce")
                    fecha_str = fecha_dt.strftime("%Y/%m/%d") if pd.notna(fecha_dt) else "N/A"
                    st.write(f"**Fecha de Última Gestión:** {fecha_str}")
                    st.markdown(f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual.get('Gestion')) else 'No'}</span>", unsafe_allow_html=True)
                
                st.divider()
                
                # 10) Formulario de gestión
                st.subheader("Gestiones del Cliente")
                gestion_key = f"gestion_refinanciamiento_{cliente_actual['SapIdCliente']}"
                comentario_key = f"comentario_refinanciamiento_{cliente_actual['SapIdCliente']}"

                with st.form(key=f"gestion_form_refinanciamiento"):
                    gestion = st.selectbox(
                        "Gestión",
                        options=[None, "Interesado", "No interesado", "Llamar Después", "Recado", "Sin contacto", "Numero equivocado"],
                        index=0 if st.session_state.get(gestion_key) is None else
                            ["Interesado", "No interesado", "Llamar Después", "Recado", "Sin contacto", "Numero equivocado"].index(
                                st.session_state[gestion_key]
                            ) + 1,
                    )
                    comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                    submit_button = st.form_submit_button("Guardar Gestión")

                if submit_button:
                    st.session_state[gestion_key] = gestion
                    st.session_state[comentario_key] = comentario
                    try:
                        gestor = st.session_state.get("gestor")
                        
                        query_update = text("""
                            UPDATE Tabla_Campaña_Refinanciamiento
                            SET Gestion = :gestion, 
                                Comentario = :comentario
                            WHERE SapIdCliente = :id_cliente
                        """)
                        
                        query_insert = text("""
                            INSERT INTO GESTIONES_CAMPAÑA_REFINANCIAMIENTO (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                            VALUES (:id_cliente, 'CAMPAÑA REFINANCIAMIENTO', GETDATE(), :gestor, :gestion, :comentario)
                        """)
                        
                        with engine.begin() as conn:
                            conn.execute(query_update, {
                                "gestion": gestion,
                                "comentario": comentario,
                                "id_cliente": cliente_actual["SapIdCliente"],
                            })
                            conn.execute(query_insert, {
                                "id_cliente": str(cliente_actual["SapIdCliente"]),
                                "gestor": gestor,
                                "gestion": gestion,
                                "comentario": comentario
                            })
                        
                        st.success("Gestión guardada exitosamente.")
                        
                    except Exception as e:
                        st.error(f"Error al guardar los cambios: {e}")

    elif page == "INDICADORES":
        # Verificar permisos para indicadores
        if not tiene_permiso(gestor_autenticado, "INDICADORES"):
            st.warning("Ups! No tienes acceso a esta pestaña :(")
        else:
            # Definir la función de conexión correctamente
            def get_connection():
                try:
                    engine = create_engine("mssql+pymssql://credito:Cr3d$.23xme@52.167.231.145:51433/CreditoYCobranza")
                    connection = engine.connect()
                    return connection
                except Exception as e:
                    st.error(f"Error al conectar a la base de datos: {e}")
                    return None

            # Conexión a la base de datos
            conn = get_connection()
            if conn:
                try:
                    # Consulta para obtener las gestiones de "SIN FRICCION"
                    query_sinfriccion = text("""
                        SELECT
                            [GESTOR],
                            COUNT(*) AS [NumeroDeGestiones]
                        FROM
                            [CreditoyCobranza].[dbo].[GESTIONES_CAMPAÑA_SINFRICCION]
                        WHERE
                            CONVERT(DATE, [FECHA_GESTION]) = CONVERT(DATE, GETDATE())  -- Filtra solo el día de hoy
                        GROUP BY
                            [GESTOR]
                        ORDER BY
                            NumeroDeGestiones DESC;
                    """)
                    gestiones_sinfriccion = pd.read_sql(query_sinfriccion, conn)

                    # Consulta para obtener las gestiones por tipo en la campaña "SIN FRICCION"
                    query_gestiones_sinfriccion_tipo = text("""
                        SELECT
                            [GESTOR],
                            [GESTION],
                            COUNT(*) AS [NumeroDeGestiones]
                        FROM
                            [CreditoyCobranza].[dbo].[GESTIONES_CAMPAÑA_SINFRICCION]
                        WHERE
                            CONVERT(DATE, [FECHA_GESTION]) = CONVERT(DATE, GETDATE())  -- Filtra solo el día de hoy
                        GROUP BY
                            [GESTOR], [GESTION]
                        ORDER BY
                            [GESTOR], NumeroDeGestiones DESC;
                    """)
                    gestiones_sinfriccion_tipo = pd.read_sql(query_gestiones_sinfriccion_tipo, conn)

                    # Consulta para obtener las gestiones de "CAMPAÑAS_COMERCIAL"
                    query_comercial = text("""
                        SELECT
                            [GESTOR],
                            COUNT(*) AS [NumeroDeGestiones]
                        FROM
                            [CreditoyCobranza].[dbo].[GESTIONES_CAMPAÑAS_COMERCIAL]
                        WHERE
                            CONVERT(DATE, [FECHA_GESTION]) = CONVERT(DATE, GETDATE())  -- Filtra solo el día de hoy
                        GROUP BY
                            [GESTOR]
                        ORDER BY
                            NumeroDeGestiones DESC;
                    """)
                    gestiones_comercial = pd.read_sql(query_comercial, conn)

                    # Consulta para obtener las gestiones por tipo en la campaña "CAMPAÑAS_COMERCIAL"
                    query_gestiones_comercial_tipo = text("""
                        SELECT
                            [GESTOR],
                            [GESTION],
                            COUNT(*) AS [NumeroDeGestiones]
                        FROM
                            [CreditoyCobranza].[dbo].[GESTIONES_CAMPAÑAS_COMERCIAL]
                        WHERE
                            CONVERT(DATE, [FECHA_GESTION]) = CONVERT(DATE, GETDATE())  -- Filtra solo el día de hoy
                        GROUP BY
                            [GESTOR], [GESTION]
                        ORDER BY
                            [GESTOR], NumeroDeGestiones DESC;
                    """)
                    gestiones_comercial_tipo = pd.read_sql(query_gestiones_comercial_tipo, conn)

                    # Cerrar la conexión
                    conn.close()

                except Exception as e:
                    st.error(f"Error al obtener los datos de gestiones: {e}")
                    gestiones_sinfriccion = pd.DataFrame()
                    gestiones_comercial = pd.DataFrame()
                    gestiones_sinfriccion_tipo = pd.DataFrame()
                    gestiones_comercial_tipo = pd.DataFrame()

                # Mostrar los resultados de la campaña "SIN FRICCION"
                if not gestiones_sinfriccion.empty:
                    st.subheader("Campaña Sin Fricción")

                    # Crear un selectbox para elegir el gestor de la campaña "SIN FRICCION"
                    gestores_sinfriccion = gestiones_sinfriccion['GESTOR'].unique()
                    gestor_sinfriccion_seleccionado = st.selectbox('Selecciona un Gestor - Sin Fricción', gestores_sinfriccion)

                    # Filtrar las gestiones por el gestor seleccionado de "SIN FRICCION"
                    gestiones_sinfriccion_filtradas = gestiones_sinfriccion_tipo[gestiones_sinfriccion_tipo['GESTOR'] == gestor_sinfriccion_seleccionado]

                    # Mostrar tabla general de gestiones
                    st.subheader("Gestiones por Ejecutivo")
                    st.dataframe(gestiones_sinfriccion, use_container_width=True)

                    # Mostrar gráfico de distribución por tipo de gestión
                    st.subheader(f"Distribución de gestiones por tipo para el Gestor: {gestor_sinfriccion_seleccionado}")
                    fig_sinfriccion = px.bar(
                        gestiones_sinfriccion_filtradas,
                        x='GESTION',
                        y='NumeroDeGestiones',
                        color='GESTION',
                        labels={"GESTION": "Tipo de Gestión", "NumeroDeGestiones": "Número de Gestiones"},
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    st.plotly_chart(fig_sinfriccion)

                else:
                    st.warning("No se encontraron gestiones para la campaña SIN FRICCION el día de hoy.")

                # Mostrar los resultados de la campaña "CAMPAÑAS COMERCIAL"
                if not gestiones_comercial.empty:
                    st.subheader("Campaña Comercial")

                    # Crear un selectbox para elegir el gestor de la campaña "CAMPAÑAS_COMERCIAL"
                    gestores_comercial = gestiones_comercial['GESTOR'].unique()
                    gestor_comercial_seleccionado = st.selectbox('Selecciona un Gestor - Comercial', gestores_comercial)

                    # Filtrar las gestiones por el gestor seleccionado de "CAMPAÑAS_COMERCIAL"
                    gestiones_comercial_filtradas = gestiones_comercial_tipo[gestiones_comercial_tipo['GESTOR'] == gestor_comercial_seleccionado]

                    # Mostrar tabla general de gestiones
                    st.subheader("Gestiones por Ejecutivo")
                    st.dataframe(gestiones_comercial, use_container_width=True)

                    # Mostrar gráfico de distribución por tipo de gestión
                    st.subheader(f"Distribución de gestiones por tipo para el Gestor: {gestor_comercial_seleccionado}")
                    fig_comercial = px.bar(
                        gestiones_comercial_filtradas,
                        x='GESTION',
                        y='NumeroDeGestiones',
                        color='GESTION',
                        labels={"GESTION": "Tipo de Gestión", "NumeroDeGestiones": "Número de Gestiones"},
                        color_discrete_sequence=px.colors.qualitative.Set1
                    )
                    st.plotly_chart(fig_comercial)

                    # 🔽 VISUALIZACIONES DE EJEMPLO — DEMO SOLO PARA VISUALIZACIÓN
                    st.subheader("📈 Clientes Contactados sin Compra ")

                    # Gráfico de pastel de ejemplo
                    data_pie = pd.DataFrame({
                        "Respuesta": ["Sí compra", "No compra"],
                        "Porcentaje": [11, 89]
                    })

                    fig_pie = px.pie(
                        data_pie,
                        names="Respuesta",
                        values="Porcentaje",
                        title="Clientes contactados sin compra",
                        color_discrete_sequence=px.colors.qualitative.Set1
                    )
                    st.plotly_chart(fig_pie)

                    # Tabla de clientes de ejemplo
                    data_clientes = pd.DataFrame({
                        "Cliente": [
                            "Laura Méndez", "Carlos Torres", "Ana Ruiz",
                            "Eduardo Vargas", "Sofía Camacho", "Mario Delgado"
                        ],
                        "Teléfono": [
                            "6441234567", "6442345678", "6443456789",
                            "6444567890", "6445678901", "6446789012"
                        ],
                        "Límite de Crédito": [
                            "$30,000", "$45,000", "$38,000", "$50,000", "$65,000", "$33,500"
                        ],
                        "CC": [
                            "Distinguido", "Esencial", "Nuevo",
                            "Distinguido", "Nuevo", "Esencial"
                        ],
                        "Gestor": [
                            "Robert Boada", "Maria Fernanda", "Bryan", "David Samano", "Nancy", "Bryan"
                        ],
                        "Fecha":[
                            "10-04-2025","10-04-2025","10-04-2025","10-04-2025","10-04-2025","10-04-2025"
                        ]
                    })

                    st.subheader("🧾 Clientes Contactados ")
                    st.dataframe(data_clientes, use_container_width=True)

                else:
                    st.warning("No se encontraron gestiones para la campaña Comercial el día de hoy.")


