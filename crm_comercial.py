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
    page = st.sidebar.radio("Ir a", ["CAT", "ORIGINACION DE CREDITO", "CAMPAÑA MOTOS", "CAMPAÑA SIN FRICCION"])
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
                    
    elif page == "CAMPAÑA MOTOS":
    # Cargar los datos desde SQL (QUITAMOS EL ORDER BY, ya que vamos a ordenar en Pandas)
        query_motos = "SELECT * FROM CRM_MOTOS_Final"
        data_motos = pd.read_sql(query_motos, engine)

        # Filtrar solo los clientes asignados al gestor autenticado
        data_motos = data_motos[data_motos["GestorVirtual"] == gestor_autenticado].copy()

        # Crear columna auxiliar: 1 si Gestion es NULL, 0 si no lo es
        data_motos["Gestion_NULL_Flag"] = data_motos["Gestion"].isna().astype(int)

        # Ordenar: primero los NULL en Gestión, luego por Número de Cliente
        data_motos = data_motos.sort_values(by=["Gestion_NULL_Flag", "NumeroCliente"], ascending=[False, True]).reset_index(drop=True)

        # Eliminar la columna auxiliar (opcional)
        data_motos.drop(columns=["Gestion_NULL_Flag"], inplace=True)


        # Filtrar filas donde ID_Cliente no sea NULL (en Pandas, NaN)
        data_motos = data_motos.dropna(subset=["ID_Cliente"])

        
        # Agregar columna Jerarquía si no existe
        if "NumeroCliente" not in data_motos.columns:
            data_motos["NumeroCliente"] = range(1, len(data_motos) + 1)


        if data_motos.empty:
            st.warning("No hay datos en la campaña de motos.")
        else:
            filtered_data = data_motos
            unique_clients = filtered_data.drop_duplicates(subset=["ID_Cliente"]).reset_index(drop=True)
            total_clients = len(unique_clients)

            # Sección de búsqueda
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
                    cliente_index = unique_clients[unique_clients["NumeroCliente"] == input_jerarquia].index
                    if len(cliente_index) > 0:
                        st.session_state["cliente_index_motos"] = cliente_index[0]
                    else:
                        st.warning(f"No se encontró un cliente con jerarquía {input_jerarquia}.")
                except ValueError:
                    st.error("Por favor, ingrese un número válido.")

            # Búsqueda por ID Cliente
            if input_id_cliente:
                cliente_index = unique_clients[unique_clients["ID_Cliente"] == input_id_cliente].index
                if len(cliente_index) > 0:
                    st.session_state["cliente_index_motos"] = cliente_index[0]
                else:
                    st.warning(f"No se encontró un cliente con ID {input_id_cliente}.")

            # Validar el índice del cliente actual
            if "cliente_index_motos" not in st.session_state:
                st.session_state["cliente_index_motos"] = 0
            cliente_index = st.session_state["cliente_index_motos"]
            cliente_index = max(0, min(cliente_index, total_clients - 1))
            st.session_state["cliente_index_motos"] = cliente_index

            # Botones de navegación
            cols_navigation = st.columns([1, 1])
            with cols_navigation[0]:
                if st.button("Anterior"):
                    st.session_state["cliente_index_motos"] = max(cliente_index - 1, 0)
            with cols_navigation[1]:
                if st.button("Siguiente"):
                    st.session_state["cliente_index_motos"] = min(cliente_index + 1, total_clients - 1)

            # Obtener cliente actual
            cliente_actual = unique_clients.iloc[st.session_state["cliente_index_motos"]]

            # Mostrar información del cliente actual
            st.subheader("Información del Cliente - Campaña Motos")
            cols = st.columns(2)
            with cols[0]:
                st.write(f"**Nombre:** {cliente_actual['Nom_Cte']}")
                st.write(f"**ID cliente:** {cliente_actual['ID_Cliente']}")
                st.write(f"**Sucursal:** {cliente_actual['Ultima_Sucursal']}")
                st.write(f"**Teléfono:** {cliente_actual['Telefono']}")
                st.write(f"**Jerarquia:** {cliente_actual['NumeroCliente']}")
                
            with cols[1]:
                st.write(f"**Modelo:** {cliente_actual['Modelo_Moto']}")
                st.write(f"**Costo Moto:** {cliente_actual['Costo_Moto']}")
                st.write(f"**Limite de crédito:** {cliente_actual['Limite_credito']}")
                st.write(f"**Credito disponible:** {cliente_actual['Credito_Disponible']}")
                st.write(f"**Enganche:** {cliente_actual['Enganche_Motos']}")
                st.markdown(
                    f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
                

            st.divider()

            # Gestión del Cliente
            st.subheader("Gestiones del Cliente")
            gestion_key = f"gestion_motos_{cliente_actual['ID_Cliente']}"
            comentario_key = f"comentario_motos_{cliente_actual['ID_Cliente']}"

            with st.form(key=f"gestion_form_motos"):
                gestion = st.selectbox(
                    "Gestión",
                    options=[None, "Interesado", "No interesado", "Recado", "Sin contacto"],
                    index=0 if st.session_state.get(gestion_key) is None else
                          ["Interesado", "No interesado", "Recado", "Sin contacto"].index(st.session_state[gestion_key]),
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
                        SET Gestion = :gestion, Comentario = :comentario, FECHA_GESTION = GETDATE()
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
                            "id_cliente": int(cliente_actual["ID_Cliente"]),  # Convertimos a int
                            "gestor": gestor,  # Asegúrate de pasar el nombre del gestor aquí
                            "gestion": gestion,
                            "comentario": comentario
                        })
                    st.success("Gestión guardada exitosamente.")
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {e}")



    elif page == "CAMPAÑA SIN FRICCION":
    # Cargar los datos desde SQL (QUITAMOS EL ORDER BY, ya que vamos a ordenar en Pandas)
        query_sinfriccion = "SELECT * FROM CRM_SINFRICCION_Final"
        data_sinfriccion = pd.read_sql(query_sinfriccion, engine)

        # Filtrar solo los clientes asignados al gestor autenticado
        data_sinfriccion = data_sinfriccion[data_sinfriccion["GestorVirtual"] == gestor_autenticado]

        # Verificar si el DataFrame está vacío antes de continuar
        if data_sinfriccion.empty:
            st.warning("No hay datos en la campaña de motos.")
        else:
            # Crear una columna auxiliar para dar prioridad a los NULL
            data_sinfriccion["Gestion_NULL_Flag"] = data_sinfriccion["Gestion"].isna().astype(int)

            # Ordenar primero por NULL (1 = NULL, 0 = No NULL), luego por NumeroCliente
            unique_clients = (
                data_sinfriccion
                .drop_duplicates(subset=["ID_Cliente"])
                .sort_values(by=["Gestion_NULL_Flag", "NumeroCliente"], ascending=[False, True])  # NULL primero
                .reset_index(drop=True)
            )

            # Eliminar la columna auxiliar después de ordenar
            unique_clients = unique_clients.drop(columns=["Gestion_NULL_Flag"])

            total_clients = len(unique_clients)



        
        # Agregar columna Jerarquía si no existe
        if "NumeroCliente" not in data_sinfriccion.columns:
            data_sinfriccion.insert(0, "NumeroCliente", range(1, len(data_sinfriccion) + 1))

        if data_sinfriccion.empty:
            st.warning("No hay datos en la campaña sin fricción.")
        else:
            filtered_data = data_sinfriccion
            unique_clients = filtered_data.drop_duplicates(subset=["ID_Cliente"]).reset_index(drop=True)
            total_clients = len(unique_clients)

            # Sección de búsqueda
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
                    cliente_index = unique_clients[unique_clients["NumeroCliente"] == input_jerarquia].index
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

            # Validar el índice del cliente actual
            if "cliente_index_sinfriccion" not in st.session_state:
                st.session_state["cliente_index_sinfriccion"] = 0
            cliente_index = st.session_state["cliente_index_sinfriccion"]
            cliente_index = max(0, min(cliente_index, total_clients - 1))
            st.session_state["cliente_index_sinfriccion"] = cliente_index

            # Botones de navegación
            cols_navigation = st.columns([1, 1])
            with cols_navigation[0]:
                if st.button("Anterior"):
                    st.session_state["cliente_index_sinfriccion"] = max(cliente_index - 1, 0)
            with cols_navigation[1]:
                if st.button("Siguiente"):
                    st.session_state["cliente_index_sinfriccion"] = min(cliente_index + 1, total_clients - 1)

            # Obtener cliente actual
            cliente_actual = unique_clients.iloc[st.session_state["cliente_index_sinfriccion"]]

            # Mostrar información del cliente actual
            st.subheader("Información del Cliente - Campaña Sin Fricción")
            cols = st.columns(2)
            with cols[0]:
                st.write(f"**Nombre:** {cliente_actual['Nom_Cte']}")
                st.write(f"**ID cliente:** {cliente_actual['ID_Cliente']}")
                st.write(f"**Sucursal:** {cliente_actual['Ultima_Sucursal']}")
                st.write(f"**Teléfono:** {cliente_actual['Telefono']}")
                
            with cols[1]:
                st.write(f"**Mensualidad:** {cliente_actual['Mensualidad_Actual']}")
                st.write(f"**Saldo Actual:** {cliente_actual['SaldoActual']}")
                st.write(f"**Limite de crédito:** {cliente_actual['Limite_credito']}")
                st.write(f"**Credito disponible:** {cliente_actual['Credito_Disponible']}")
                st.markdown(
                    f"<span class='highlight'>Gestionado: {'Sí' if pd.notna(cliente_actual['Gestion']) else 'No'}</span>",
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
                

            st.divider()

            # Gestión del Cliente
            st.subheader("Gestiones del Cliente")
            gestion_key = f"gestion_sinfriccion_{cliente_actual['ID_Cliente']}"
            comentario_key = f"comentario_sinfriccion_{cliente_actual['ID_Cliente']}"

            with st.form(key=f"gestion_form_sinfriccion"):
                gestion = st.selectbox(
                    "Gestión",
                    options=[None, "Interesado", "No interesado", "Recado", "Sin contacto"],
                    index=0 if st.session_state.get(gestion_key) is None else
                          ["Interesado", "No interesado", "Recado", "Sin contacto"].index(st.session_state[gestion_key]),
                )
                comentario = st.text_area("Comentarios", value=st.session_state.get(comentario_key, ""))
                submit_button = st.form_submit_button("Guardar Gestión")

            if submit_button:
                st.session_state[gestion_key] = gestion
                st.session_state[comentario_key] = comentario
                try:
                    gestor = st.session_state.get("gestor") 
                    query_update = text("""
                        UPDATE CRM_SINFRICCION_Final
                        SET Gestion = :gestion, Comentario = :comentario, FECHA_GESTION = GETDATE()
                        WHERE ID_Cliente = :id_cliente
                    """)
                    query_insert = text("""
                        INSERT INTO GESTIONES_SINFRICCION_COMERCIAL (ID_CLIENTE, CAMPAÑA, FECHA_GESTION, GESTOR, GESTION, COMENTARIO)
                        VALUES (:id_cliente, 'CAMPAÑA SIN FRICCION', GETDATE(), :gestor, :gestion, :comentario)
                    """)
                    with engine.begin() as conn:
                        conn.execute(query_update, {
                            "gestion": gestion,
                            "comentario": comentario,
                            "id_cliente": cliente_actual["ID_Cliente"],
                        })
                        conn.execute(query_insert, {
                            "id_cliente": int(cliente_actual["ID_Cliente"]),  # Convertimos a int
                            "gestor": gestor,  # Asegúrate de pasar el nombre del gestor aquí
                            "gestion": gestion,
                            "comentario": comentario
                        })
                    st.success("Gestión guardada exitosamente.")
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {e}")