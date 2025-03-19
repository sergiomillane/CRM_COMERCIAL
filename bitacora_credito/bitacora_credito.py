import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime

# Configuración de la conexión a SQL Server
SERVER = "52.167.231.145:51433"
DATABASE = "CreditoyCobranza"
USERNAME = "credito"
PASSWORD = "Cr3d$.23xme"

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
        )
        return conn
    except Exception as e:
        st.error(f"Error en la conexión con la base de datos: {e}")
        return None

# ========== INTERFAZ STREAMLIT ==========
st.title("Departamento de crédito - Bitácora de actividades")

# ========== FORMULARIO ==========
with st.form("registro_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        fecha = st.date_input("Fecha", datetime.today())
        ticket = st.text_input("Ticket")
        sucursal = st.selectbox("Sucursal", list(range(1, 101)))
        cliente = st.text_input("Cliente")

    with col2:
        venta = st.selectbox("Venta", ["AUTORIZADA", "NO AUTORIZADA", "AUTORIZADA PARCIAL"])
        moto = st.selectbox("Moto", ["SI", "NO"])
        tipo_cliente = st.selectbox("Tipo de Cliente", ["RECOMPRA ACTIVO", "NUEVO", "RECOMPRA INACTIVO", "CAMPAÑA"])
        notas = st.selectbox("Notas", ["CON ENGANCHE", "SIN ENGANCHE", "OTRO"])

    with col3:
        lc_actual = st.number_input("LC Actual", min_value=0.0, format="%.2f")
        lc_final = st.number_input("LC Final", min_value=0.0, format="%.2f")
        enganche_requerido = st.number_input("Enganche Requerido", min_value=0.0, format="%.2f")
        observacion = st.text_area("Observación")

    especial = st.selectbox("Especial", [
        "Aut. Fernando Valdez", "Aut. Francisco Valdez", "Aut. Gabriel Valdez", "Aut. Enrique Valdez",
        "Aut. Pedro Moreno", "Aut. Luis Corrales", "Aut. Christian Ayala", "Aut. Edmar Cruz",
        "Aut. Benjamin Rivera", "Aut. Jose Medina", "Aut. Ramon Casillas", "Aut. Area de crédito"
    ])
    autorizo = st.selectbox("Lider de sucursal", list(range(1, 101)))
    articulo = st.text_input("Artículo")
    ejecutivo = st.selectbox("Ejecutivo", ["Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])
    cel_cte = st.text_input("Celular Cliente")
    consulta_buro = st.selectbox("Consulta Buró", ["SI", "NO"])

    # Botón para enviar el formulario
    submit_button = st.form_submit_button("Guardar Registro")

# ========== GUARDAR REGISTRO ==========
if submit_button:
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO Bitacora_Credito (
                    FECHA, TICKET, SUC, CLIENTE, VENTA, MOTO, 
                    TIPO_DE_CLIENTE, NOTAS, LC_ACTUAL, LC_FINAL, 
                    ENGANCHE_REQUERIDO, OBSERVACION, ESPECIAL, 
                    AUTORIZO, ARTICULO, EJECUTIVO, CEL_CTE, CONSULTA_BURO
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(
                query,
                fecha.strftime('%Y-%m-%d'), ticket, sucursal, cliente, venta, moto,
                tipo_cliente, notas, lc_actual, lc_final, enganche_requerido,
                observacion, especial, autorizo, articulo, ejecutivo, cel_cte, consulta_buro
            )
            conn.commit()
            st.success("Registro guardado exitosamente en la base de datos.")
        except Exception as e:
            st.error(f"Error al guardar el registro: {e}")
        finally:
            conn.close()

# ========== VISUALIZADOR EN TIEMPO REAL ==========
st.header("📊 Registros en tiempo real")

# Filtros
col1, col2 = st.columns(2)
with col1:
    filtro_fecha = st.date_input("Filtrar por fecha", datetime.today())
with col2:
    filtro_ejecutivo = st.selectbox("Filtrar por Ejecutivo", ["Todos"] + ["Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])

# Función para obtener registros desde SQL Server
def fetch_records():
    conn = get_connection()
    if conn:
        try:
            query = "SELECT * FROM Bitacora_Credito WHERE FECHA = ?"
            params = [filtro_fecha.strftime('%Y-%m-%d')]

            if filtro_ejecutivo != "Todos":
                query += " AND EJECUTIVO = ?"
                params.append(filtro_ejecutivo)

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

# Actualizar automáticamente cada 10 segundos
st.experimental_rerun()
