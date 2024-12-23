import streamlit as st
import amortizacion
import pandas as pd
from io import BytesIO


st.title("Tabla de Amortización")

st.sidebar.header("Parámetros")
cost = st.sidebar.number_input("Costo del vehículo:", value = 0.0)
down = st.sidebar.number_input("Enganche:", value = 0.0)
interest = st.sidebar.number_input("Tasa de Interés Anual:", value = 0.0)
years = st.sidebar.number_input("Años a financiar:", value = 5)

is_first_year_free = st.sidebar.selectbox("¿Primer año de seguro gratis?", ["Si", "No"])
is_life_insurance = st.sidebar.selectbox("Seguro de Vida", ["Si", "No"])

if is_life_insurance == "Si" and is_first_year_free == "Si":
    life_insurance_1 = st.sidebar.number_input("Costo de seguro de vida primer:", value = 0.0)
    life_insurance_2 = st.sidebar.number_input("Costo de seguro de vida segundo:", value = 0.0)

elif is_life_insurance == "Si" and is_first_year_free == "No":
    life_insurance = st.sidebar.number_input("Costo de seguro de vida:", value = 0.0)

else:
    is_life_insurance = False

insurance = st.sidebar.number_input("Costo de seguro:", value = 0.0)

accesories = st.sidebar.number_input("Accesorios:", value = 0.0)
extras = st.sidebar.number_input("Extras:", value = 0.0)

def generate_table(is_first_year_free):
    df = pd.DataFrame()
    if is_first_year_free == "Si":
        table = amortizacion.first_year_free_amort_table(
            cost,
            down,
            interest,
            years,
            insurance,
            accesories,
            extras,
            is_life_insurance = is_life_insurance,
            life_insurance_1 = life_insurance_1,
            life_insurance_2 = life_insurance_2
        )
        df = pd.DataFrame(table)

    else:
        table = amortizacion.amort_table(
            cost,
            down,
            interest,
            years,
            insurance,
            accesories,
            extras,
            is_life_insurance = is_life_insurance,
            life_insurance = life_insurance
        )
        df = pd.DataFrame(table)
    
    return df


def download_table():
    df = generate_table(is_first_year_free)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index = False, sheet_name = "Amortización")
    processed_data = output.getvalue()
    return processed_data

if st.button("Generar"):
    df = generate_table(is_first_year_free)
    st.dataframe(df)

if st.button("Descargar Tabla"):
    excel_data = download_table()
    st.download_button(
        label = "Save Excel File",
        data = excel_data,
        file_name = "Tabla_Amortizacion.xlsx",
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
