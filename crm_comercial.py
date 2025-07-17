import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import plotly.express as px

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
    query = "SELECT * FROM CRM_COMERCIAL ORDER BY Jerarquia ASC" if is_admin else f"SELECT * FROM CRM_COMERCIAL WHERE Gestor = '{gestor_autenticado}' ORDER BY Jerarquia ASC "
    data = pd.read_sql(query, engine)

    # Sidebar para navegación y botón de cerrar sesión
    st.sidebar.title(f"Gestor: {gestor_autenticado}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Ir a", ["CAT", "ORIGINACION DE CREDITO", "CAMPAÑA MOTOS", "CAMPAÑA SIN FRICCION","IRRECUPERABLES","INDICADORES"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        cerrar_sesion()

    # Página de Información de Cliente
    if page == "CAT":
        data_cat = data[data["Canal"]=="CAT"]
        if data_cat.empty:
            st.warning("Ups! No tienes acceso a esta pestaña:(")
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
                
        # Página de Información de Cliente
    elif page == "ORIGINACION DE CREDITO":
        data_cat = data[data["Canal"]=="Originacion"]
        if data_cat.empty:
            st.warning("Ups! No tienes acceso a esta pestaña:(")
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


##---------------------------------------------------CAMPAÑA MOTOS----------------------------------------------------------

    elif page == "CAMPAÑA MOTOS":
        # 1) Cargar datos
        query_motos = "SELECT * FROM CRM_MOTOS_Final where gestion <> 'Numero equivocado'"
        data_motos = pd.read_sql(query_motos, engine)
        
        # 2) Filtrar por gestor y eliminar IDs inválidos
        data_motos = data_motos[data_motos["GestorVirtual"] == gestor_autenticado].copy()
        data_motos = data_motos.dropna(subset=["ID_Cliente"])
        
        # 3) Asegurar FECHA_GESTION como datetime
        data_motos["FECHA_GESTION"] = pd.to_datetime(data_motos["FECHA_GESTION"], errors="coerce")
        
        # 4) ORDENAMIENTO FIJO - Solo se ejecuta una vez al día por el SP nocturno
        # La jerarquía ya debe venir calculada desde la base de datos
        # Si no existe columna jerarquia en BD, calcularla aquí pero mantenerla fija
        
        # La columna de jerarquía en BD se llama "NumeroCliente"
        if "NumeroCliente" in data_motos.columns and not data_motos["NumeroCliente"].isna().all():
            # Si ya existe jerarquía en BD, mantenerla tal como está
            data_motos = data_motos.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
            data_motos["jerarquia"] = data_motos["NumeroCliente"]
        else:
            # Crear jerarquía solo si no existe en BD
            # Ordenar: primero sin gestión (fecha null), luego por fecha ascendente  
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
            # 5) Preparar lista única de clientes (manteniendo jerarquía original)
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
                    
                    # IMPORTANTE: NO actualizar FECHA_GESTION en CRM_MOTOS_Final
                    # Solo actualizar Gestion y Comentario
                    # La fecha se actualizará mañana con el SP nocturno
                    query_update = text("""
                        UPDATE CRM_MOTOS_Final
                        SET Gestion = :gestion, 
                            Comentario = :comentario
                        WHERE ID_Cliente = :id_cliente
                    """)
                    
                    # Solo guardar el histórico con fecha actual
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
                    
                    # NO usar st.rerun() para mantener jerarquía fija durante el día
                    # La jerarquía solo cambiará mañana con el SP nocturno
                    
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {e}")



##--------------------------------------------------------------sin friccion------------------------------------------------------
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
        if "NumeroCliente" in data_sinfriccion.columns and not data_sinfriccion["NumeroCliente"].isna().all():
            # Si ya existe jerarquía en BD, mantenerla tal como está
            data_sinfriccion = data_sinfriccion.sort_values(by=["NumeroCliente"], ascending=True).reset_index(drop=True)
            data_sinfriccion["jerarquia"] = data_sinfriccion["NumeroCliente"]
        else:
            # Crear jerarquía solo si no existe en BD
            # Ordenar: primero sin gestión (fecha null), luego por fecha ascendente  
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

   #------------------------------------ INDICADORES -----------------------------------------------#   

    elif page == "INDICADORES":
        st.header("📊 Indicadores de gestiones")

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


