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

# ========== VISUALIZADOR EN TIEMPO REAL ==========
st.header("📊 Registros en tiempo real")

# Filtros
col1, col2, col3 = st.columns(3)
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
            query = text("SELECT Registro AS '#Registro', * FROM Bitacora_Credito WHERE FECHA = :fecha ORDER BY Registro ASC")
            params = {"fecha": filtro_fecha.strftime('%Y-%m-%d')}

            if filtro_ejecutivo != "Todos":
                query = text("SELECT Registro AS '#Registro', * FROM Bitacora_Credito WHERE FECHA = :fecha AND EJECUTIVO = :ejecutivo ORDER BY Registro ASC")
                params["ejecutivo"] = filtro_ejecutivo

            df = pd.read_sql(query, conn, params=params)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error al obtener los registros: {e}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    return pd.DataFrame()

# Obtener los registros para visualización
df_records = fetch_records()

# Mostrar registros en tiempo real
if not df_records.empty:
    st.dataframe(df_records)
else:
    st.warning("No hay registros para mostrar con los filtros seleccionados.")

# ========== ELIMINACIÓN DE REGISTROS ==========
st.subheader("❌ Eliminar un registro")

# Obtener la lista de registros disponibles para eliminar
if not df_records.empty:
    registros_disponibles = df_records["#Registro"].tolist()
    registro_seleccionado = st.selectbox("Seleccione el número de registro a eliminar:", registros_disponibles)

    if st.button("Eliminar Registro"):
        conn = get_connection()
        if conn:
            try:
                delete_query = text("DELETE FROM Bitacora_Credito WHERE Registro = :registro")
                conn.execute(delete_query, {"registro": registro_seleccionado})
                conn.commit()
                st.success(f"Registro #{registro_seleccionado} eliminado exitosamente.")
            except Exception as e:
                st.error(f"Error al eliminar el registro: {e}")
            finally:
                conn.close()

 