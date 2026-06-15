import pandas as pd


def data_processing():

    df_raw = pd.read_excel("NPS.xlsx")
    #-- Standardization --
    new_columns = ['marca_temporal', 'institucion', 'operacion_reciente', 'antiguedad',
                   'productos_usados', 'canales_usados', 'canal_principal', 'ces',
                   'resolucion_primer_contacto', 'cal_rapidez', 'cal_transparencia',
                   'cal_facilidad_digital', 'cal_estabilidad_digital', 'cal_confianza',
                   'cal_atencion_humana', 'csat', 'nps', 'razon_nps', 'edad',
                   'estado', 'nivel_estudios', 'ocupacion']
    df_raw.columns = new_columns

    def clean_list(lst):
        return [x.strip() for x in lst if x and x.strip()]

    def multiselect_to_list(col_name, new_column=None):
        new_column = new_column or f"{col_name}_lista"
        df_raw[new_column] = (df_raw[col_name].fillna("").astype(str)
                                 .str.split(r"\s*[;,]\s*").apply(clean_list))

    multiselect_to_list('productos_usados')
    multiselect_to_list('canales_usados')
    multiselect_to_list('razon_nps')

    #-- Cleaning --
    df_raw.drop_duplicates(subset=["marca_temporal"], inplace=True)
    df_raw["marca_temporal"] = pd.to_datetime(df_raw["marca_temporal"])

    #Range validation
    df_raw = df_raw[df_raw["nps"].between(0, 10)]
    df_raw = df_raw[df_raw["ces"].between(1, 5)]
    df_raw = df_raw[df_raw["csat"].between(1, 5)]

    #Categorical columns — strip and lower for consistency
    cols_categoricas = ["institucion", "operacion_reciente", "antiguedad", "canal_principal",
                        "resolucion_primer_contacto", "estado", "nivel_estudios", "ocupacion",
                        "edad", "cal_rapidez", "cal_transparencia", "cal_facilidad_digital",
                        "cal_estabilidad_digital", "cal_confianza", "cal_atencion_humana"]
    df_raw[cols_categoricas] = df_raw[cols_categoricas].apply(
        lambda c: c.str.strip().str.lower().astype("category"))

    #NPS category
    df_raw["nps_categoria"] = pd.cut(df_raw["nps"], bins=[-1, 6, 8, 10],
                                     labels=["Detractor (0-6)", "Pasivo (7-8)", "Promotor (9-10)"])

    #Feature engineering
    df_raw["mes"]       = df_raw["marca_temporal"].dt.month
    df_raw["trimestre"] = df_raw["marca_temporal"].dt.quarter

    return df_raw