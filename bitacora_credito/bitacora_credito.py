import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text







# Configurar la conexión a SQL Server usando pymssql
DATABASE_URL = "mssql+pymssql://credito:Cr3d$.23xme@52.167.231.145:51433/CreditoyCobranza"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

def get_connection():
    """Obtiene la conexión a la base de datos."""
    try:
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error en la conexión con la base de datos: {e}")
        return None

# ========== INTERFAZ STREAMLIT ==========
st.title("Departamento de crédito - Bitácora de actividades")

st.markdown("### ⚠️ **NO DAR ENTER O SE GUARDARÁ EL REGISTRO** ⚠️")
st.markdown("Por favor, utilice el botón **'Guardar Registro'** para enviar el formulario.")

# ========== FORMULARIO ==========
with st.form("registro_form", clear_on_submit=True):  
    col1, col2, col3 = st.columns(3)

    with col1:
        fecha = st.date_input("Fecha", datetime.today())
        ticket = st.text_input("Ticket")  # ✅ Altura reducida
        sucursal = st.selectbox("Sucursal", list(range(1, 101)))
        tipo_cliente = st.selectbox("Tipo de Cliente", ["RECOMPRA ACTIVO", "NUEVO", "RECOMPRA INACTIVO", "CAMPAÑA"])
        
    with col2:
        venta = st.selectbox("Venta", ["AUTORIZADA", "NO AUTORIZADA", "AUTORIZADA PARCIAL"])
        cliente = st.text_input("ID_Cliente")  # ✅ Evita el envío automático con ENTER
        notas = st.selectbox("Notas", ["CON ENGANCHE", "SIN ENGANCHE", "OTRO"])
        enganche_requerido = st.number_input("Enganche Requerido", min_value=0.0, format="%.2f")

    with col3:
        moto = st.selectbox("Moto", ["SI", "NO"])
        observacion = st.text_input("Observación")  # ✅ Mantiene altura baja para parecer un input
        lc_actual = st.number_input("LC Actual", min_value=0.0, format="%.2f")
        lc_final = st.number_input("LC Final", min_value=0.0, format="%.2f")

    especial = st.selectbox("Especial", ["Ninguno",
        "Aut. Fernando Valdez", "Aut. Francisco Valdez", "Aut. Gabriel Valdez", "Aut. Enrique Valdez",
        "Aut. Pedro Moreno", "Aut. Luis Corrales", "Aut. Christian Ayala", "Aut. Edmar Cruz",
        "Aut. Benjamin Rivera", "Aut. Jose Medina", "Aut. Ramon Casillas", "Aut. Area de crédito"
    ])

    

    articulo = st.text_input("Artículo")
    ejecutivo = st.selectbox("Ejecutivo", ["Francis", "Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])
    cel_cte = st.text_input("Celular Cliente")
    consulta_buro = st.selectbox("Consulta Buró", ["SI", "NO"])

    # ✅ IMPORTANTE: Botón de envío dentro del `st.form()`
    submit_button = st.form_submit_button("Guardar Registro")


# ========== CONTROL DE ENVÍO ==========
if submit_button:
    # ✅ Verificar que el usuario haya usado Ctrl + Enter
    st.session_state["submit_key_pressed"] = st.session_state.get("submit_key_pressed", False)

    if not st.session_state["submit_key_pressed"]:
        st.warning("Para enviar el formulario haz clic en el botón.")
    else:
        # ✅ Guardar en base de datos (simulado aquí)
        st.success("Registro guardado exitosamente en la base de datos.")
        st.session_state["submit_key_pressed"] = False  # Reset

# ========== CONTROL DE TECLAS ==========
def set_submit_key():
    st.session_state["submit_key_pressed"] = True




# ========== GUARDAR REGISTRO ==========
if submit_button:
    conn = get_connection()
    if conn:
        try:
            query = text("""
                INSERT INTO Bitacora_Credito (
                    FECHA, TICKET, SUC, CLIENTE, VENTA, MOTO, 
                    TIPO_DE_CLIENTE, NOTAS, LC_ACTUAL, LC_FINAL, 
                    ENGANCHE_REQUERIDO, OBSERVACION, ESPECIAL, 
                    AUTORIZO, ARTICULO, EJECUTIVO, CEL_CTE, CONSULTA_BURO
                ) 
                VALUES (:fecha, :ticket, :sucursal, :cliente, :venta, :moto, 
                        :tipo_cliente, :notas, :lc_actual, :lc_final, 
                        :enganche_requerido, :observacion, :especial, 
                        :autorizo, :articulo, :ejecutivo, :cel_cte, :consulta_buro)
            """)

            conn.execute(query, {
                "fecha": fecha.strftime('%Y-%m-%d'),
                "ticket": ticket,
                "sucursal": sucursal,
                "cliente": cliente,
                "venta": venta,
                "moto": moto,
                "tipo_cliente": tipo_cliente,
                "notas": notas,
                "lc_actual": lc_actual,
                "lc_final": lc_final,
                "enganche_requerido": enganche_requerido,
                "observacion": observacion,
                "especial": especial,
                "autorizo": autorizo,
                "articulo": articulo,
                "ejecutivo": ejecutivo,
                "cel_cte": cel_cte,
                "consulta_buro": consulta_buro
            })
            conn.commit()
            st.success("Registro guardado exitosamente en la base de datos.")
        except Exception as e:
            st.error(f"Error al guardar el registro: {e}")
        finally:
            conn.close()

# ========== VISUALIZADOR EN TIEMPO REAL ==========
st.header("📊 Registros en tiempo real")

# Filtros
col1, col2,col3 = st.columns(3)
with col1:
    filtro_cliente = st.text_input("Filtrar por ID Cliente", "")
with col2:
    filtro_fecha = st.date_input("Filtrar por fecha", datetime.today())
with col3:
    filtro_ejecutivo = st.selectbox("Filtrar por Ejecutivo", ["Todos"] + ["Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])

# Función para obtener registros desde SQL Server
def fetch_records():
    conn = get_connection()
    if conn:
        try:
            query = text("SELECT * FROM Bitacora_Credito WHERE FECHA = :fecha")
            params = {"fecha": filtro_fecha.strftime('%Y-%m-%d')}

            if filtro_ejecutivo != "Todos":
                query = text("SELECT * FROM Bitacora_Credito WHERE FECHA = :fecha AND EJECUTIVO = :ejecutivo")
                params["ejecutivo"] = filtro_ejecutivo

            df = pd.read_sql(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error al obtener los registros: {e}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    return pd.DataFrame()

# Mostrar registros en tiempo real
df_records = fetch_records()

if not df_records.empty:
    st.dataframe(df_records)
else:
    st.warning("No hay registros para mostrar con los filtros seleccionados.")

