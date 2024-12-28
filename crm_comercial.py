import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

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
    "jose_daniel": {"gestor": "Jose Daniel Flores Herrera", "password": "ZJ1QRZ", "admin": False},
    "julissa_iveth": {"gestor": "Julissa Iveth Gamez Ramirez", "password": "OnHnp4", "admin": False},
    "karely_elizabeth": {"gestor": "Karely Elizabeth Olmeda Gutierrez", "password": "MhDEsm", "admin": False},
    "lizbeth_guadalupe": {"gestor": "Lizbeth Guadalupe Contreras Leal", "password": "32QVMR", "admin": False},
    "melissa_angulo": {"gestor": "Melissa Angulo Rios", "password": "Ok7Wsm", "admin": False},
    "oscar_eduardo": {"gestor": "Oscar Eduardo Sánchez Grande", "password": "FtQ7ZK", "admin": False},
    "reyna_berenice": {"gestor": "Reyna Berenice Salazar Cabrera", "password": "w7sZwz", "admin": False},
    "saul_armando": {"gestor": "Saul Armando Lara Parra", "password": "eSLa6h", "admin": False},
    "allison_priscila": {"gestor": "Allison Priscila Perez Garay", "password": "ASPa4h", "admin": False},
    "liliana_cortes": {"gestor": "Liliana Cortes", "password": "admin_vb3$", "admin": True},
    "carlos_quinonez": {"gestor": "Carlos Quiñonez", "password": "admin_vb3$", "admin": True},
    "roberto_boada": {"gestor": "Roberto Boada", "password": "admin_vb3$", "admin": True},
    "fernando_valdez": {"gestor": "Fernando Valdez", "password": "admin_vb3$", "admin": True},
    "juan_alberto": {"gestor": "Juan", "password": "admin_vb3$", "admin": True},
    "sergio_millan": {"gestor": "Sergio Millan", "password": "admin_vb3$", "admin": True}, 
    "administrador": {"gestor": "Administrador", "password": "admin_vb3$", "admin": True},
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
    query = "SELECT * FROM CRM_COMERCIAL ORDER BY Jerarquia ASC" if is_admin else f"SELECT * FROM CRM_COMERCIAL ORDER BY Jerarquia ASC "
    data = pd.read_sql(query, engine)

    # Sidebar para navegación y botón de cerrar sesión
    st.sidebar.title(f"Gestor: {gestor_autenticado}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Ir a", ["Información para gestión", "Base de clientes"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        cerrar_sesion()

    # Página de Información de Cliente
    if page == "Información para gestión":
        filtered_data = data
        unique_clients = filtered_data.drop_duplicates(subset=["ID_CLIENTE"]).reset_index(drop=True)
        total_clients = len(unique_clients)
        # Sección de búsqueda
        st.markdown("<div style='font-size:16px; font-weight:bold;'>Busqueda ordenada de Jerarquia</div>", unsafe_allow_html=True)
        cols = st.columns([1, 1])
        with cols[0]:
            input_jerarquia = st.text_input("Número", "", help="Ingrese la jerarquía del cliente y presione Enter")
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

        # Obtener cliente actual
        cliente_actual = unique_clients.iloc[cliente_index]
        facturas_cliente = filtered_data[filtered_data["ID_CLIENTE"] == cliente_actual["ID_CLIENTE"]]
        
        # Agregamos un CSS personalizado para reducir el espacio solo en la clase 'compact-section'
        # Nota: con line-height es que hago más pequeño el interlineado
        st.markdown("""
            <style>
            .ajuste_interlineado {
                font-size: 18px;
                line-height: 2.2; /* Ajusta el interlineado aquí */
                margin: 0;
                padding: 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # CSS personalizado para mejorar el diseño del script
        st.markdown("""
            <style>
            .ajuste_interlineado {
                font-size: 18px;
                line-height: 2.2;
                margin: 0;
                padding: 0;
            }
            .script-container {
                background-color: #f9f9f9;  /* Color de fondo claro */
                border: 2px solid #6495ed;  /* Borde azul */
                border-radius: 8px;         /* Bordes redondeados */
                padding: 15px;             /* Espaciado interno */
                margin-bottom: 20px;       /* Espaciado con otros elementos */
                font-size: 16px;
                font-weight: bold;
                color: #333;               /* Color del texto */
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
        
        # Sección 1: Información General del Cliente
        st.markdown('<div class="ajuste_interlineado">', unsafe_allow_html=True)
        st.subheader("Información del Cliente")
        cols = st.columns(2)
        with cols[0]:
            st.write(f"**Nombre Solicitante:** {cliente_actual['Solicitante']}")
            st.write(f"**ID cliente:** {cliente_actual['ID_CLIENTE']}")
            st.write(f"**Folio:** {cliente_actual['Folio']}")
            st.write(f"**Clasificación:** {cliente_actual['Clasificacion']}")
            st.write(f"**Limite de credito:** {cliente_actual['Limite_de_credito']}")
            st.write(f"**Fecha de aprobacion:** {cliente_actual['Fecha_Aprobacion']}")
            st.write(f"**Ultima Gestion:** {cliente_actual['FECHA_GESTION']}")
        with cols[1]:
            st.write(f"**Telefono Celular:** {cliente_actual['Tel_Celular']}")
            st.write(f"**Sucursal:** {cliente_actual['Sucursal']}")
            st.write(f"**Gestion:** {cliente_actual['Gestion']}")
            st.write(f"**Comentario:** {cliente_actual['Comentario']}")
            st.write(f"**Categoria:** {cliente_actual['Segmento']}")
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
                options=[None,"Contacto_Efectivo", "Contacto_NoEfectivo", "Sin_Contacto", "Sin_Cobertura"],
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
                    INSERT INTO Gestiones_CRM_Comercial (ID_CLIENTE,GESTION, COMENTARIO, FECHA_GESTION)
                    VALUES (:id_cliente, :gestion, :comentario, GETDATE())
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
                    })
                st.success("Gestión guardada exitosamente.")
            except Exception as e:
                st.error(f"Error al guardar los cambios: {e}")
