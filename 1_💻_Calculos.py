import json
import os
import requests
import subprocess
import openpyxl
import pythoncom
import docx2pdf 
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie  
from docxtpl import DocxTemplate, InlineImage
from streamlit_extras.stylable_container import stylable_container
from matplotlib import pyplot as plt
from funCapCargaAoki import resultAoki
from funCapCargaDC import resultDC
from resultadosAokiDq import resultAokiDq

st.set_page_config(
    page_title= 'Aplicación multipágina',
    page_icon= '⚙',
    layout='centered'
)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json() 

lottie_hello = load_lottieurl("https://lottie.host/5cc13fa3-b5c1-4568-879b-1e9372233ad8/8undRuQWaF.json")


if 'tipo_pilote' not in st.session_state:
    st.session_state['tipo_pilote'] = 'Excavada'
if 'D' not in st.session_state:
    st.session_state['D'] = 0.30
if 'carga_adm_esperada' not in st.session_state:
    st.session_state['carga_adm_esperada'] = 200
if 'lista_nspt' not in st.session_state:
    st.session_state['lista_nspt'] = [0, 1, 1, 3, 6, 10, 11, 16, 30, 50, 50, 50, 50, 50, 50]
if 'lista_tipo_suelo' not in st.session_state:
    st.session_state['lista_tipo_suelo'] = [23, 23, 23, 23, 32, 32, 32, 32, 32, 12, 12, 12, 12, 12, 12]
if 'sheet_name' not in st.session_state:
    st.session_state['sheet_name'] = ''
if 'input_option' not in st.session_state:
    st.session_state['input_option'] = 'Manual'

def check_format(df):
    if len(df.columns) >= 2 and df.applymap(lambda x: isinstance(x, (int, float))).all().all():
        return True
    return False

with st.sidebar:
    st.title('Datos:')
    st.session_state['tipo_pilote'] = st.selectbox('Tipo de pilote', ['Excavada', 'Raiz', 'HCM'], index=['Excavada', 'Raiz', 'HCM'].index(st.session_state['tipo_pilote']))
    st.session_state['D'] = st.number_input('Diámetro de pilote (m)', value=st.session_state['D'])
    st.session_state['carga_adm_esperada'] = st.number_input('Carga Admisible Esperada (kN)', value=st.session_state['carga_adm_esperada'])

    st.session_state['input_option'] = st.radio("Selecciona la forma de ingresar los datos NSPT:", ("Manual", "Subir archivo Excel"), index=("Manual", "Subir archivo Excel").index(st.session_state['input_option']))
    if st.session_state['input_option'] == "Manual":
        st.session_state['lista_nspt'] = st.text_input('Resistencia a penetración (NSPT)', ', '.join(map(str, st.session_state['lista_nspt'])))
        st.session_state['lista_tipo_suelo'] = st.text_input('Tipo de suelo (Ver pestaña - Código de suelo)', ', '.join(map(str, st.session_state['lista_tipo_suelo'])))
        st.session_state['lista_nspt'] = [int(x.strip()) for x in st.session_state['lista_nspt'].split(',')]
        st.session_state['lista_tipo_suelo'] = [int(x.strip()) for x in st.session_state['lista_tipo_suelo'].split(',')]
        data_valid = True
    else:
        uploaded_file = st.file_uploader("Sube el archivo Excel con los datos", type=["xlsx"])
        data_valid = False
        if uploaded_file:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            st.session_state['sheet_name'] = st.radio("Selecciona la hoja en el archivo Excel:", sheet_names)
            try:
                df = pd.read_excel(uploaded_file, sheet_name=st.session_state['sheet_name'], header=1)
                if check_format(df):
                    st.session_state['lista_tipo_suelo'] = df.iloc[:, 0].tolist()
                    st.session_state['lista_nspt'] = df.iloc[:, 1].tolist()
                    data_valid = True
                else:
                    st.warning("Verificar mensaje de error")
            except IndexError:
                st.warning("No se seleccionó una hoja válida en el archivo Excel.")
            except ValueError:
                st.warning("Error en la lectura del archivo Excel.")
        else:
            st.warning("Subir archivo")

st.markdown("<h1 style='text-align: center; color: white;'>Cálculo capacidad de carga de pilote</h1>", unsafe_allow_html=True)
st.markdown('---')

if not data_valid:
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        height=200,
        width=None,
        key=None
    )
    if not uploaded_file:
        st.write('#### Por favor, sube un archivo Excel para continuar.')
    else:
        st.write('#### El archivo Excel seleccionado no cumple con el formato requerido.')    
else:
    if len(st.session_state['lista_nspt']) != len(st.session_state['lista_tipo_suelo']):
        st.error("##### ❌ Las listas NSPT y Tipo de suelo deben tener el mismo número de elementos.")
    else:
        # Obtener los resultados Aoki-Velloso
        df_result = resultAoki( st.session_state['lista_tipo_suelo'], st.session_state['tipo_pilote'], st.session_state['lista_nspt'], st.session_state['D'])
        cotas = df_result['Cotas (m)']
        pa_final_aoki = df_result['Pa Final Aoki (kN)']

        # Obtener los resultados Decourt-Quaresma
        df_result_DQ = resultDC( st.session_state['lista_tipo_suelo'], st.session_state['tipo_pilote'], st.session_state['lista_nspt'], st.session_state['D'])
        pa_final_DQ = df_result_DQ['Pa Final DecQua (kN)']

        #Obtener los resultados finales
        df_result_Final = resultAokiDq( st.session_state['lista_tipo_suelo'], st.session_state['tipo_pilote'], st.session_state['lista_nspt'], st.session_state['D'])
        pa_final_AokiDq= df_result_Final['Menor valor entre métodos (kN)']

    ##TABLAS
        # Tabla Aoki - Velloso
        st.subheader("Capacidad de carga por Aoki - Velloso:")
        tablaResult = pd.DataFrame(df_result)

        edited_df = st.data_editor(
            tablaResult,
            column_config={
                "rp (kPa)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rp (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "rl (kPa)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rl (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rl acum.(kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rt (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Norma (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Excavada (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Final Aoki(kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                )
            },
            hide_index=True,
        )

        st.subheader("Capacidad de carga por Decourt-Quaresma:")
        tablaResult = pd.DataFrame(df_result_DQ)

        edited_df = st.data_editor(
            tablaResult,
            column_config={
                "α": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "β": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rp (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rl (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rl acum.(kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Rt (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Norma (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Excavada (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Met. DecQua (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Final DecQua (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                )
            },
            hide_index=True,
        )

        st.subheader("Resultados Notables:")
        tablaResult = pd.DataFrame(df_result_Final)

        edited_df = st.data_editor(
            tablaResult,
            column_config={
                "Pa Final Aoki (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Pa Final DecQua (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                ),
                "Menor valor entre métodos (kN)": st.column_config.NumberColumn(
                    format="%0.2f",
                )
            
            },
            hide_index=True,
        )
    ##GRÁFICAS
        # Configuracón de gráfica 
        st.subheader("Carga admisible final:")
        fig, ax = plt.subplots(figsize=(5, 7))
        ax.plot(pa_final_AokiDq, cotas, color='green', marker='o', markerfacecolor='cyan', linestyle='-', label='Menor Val. Aoki e DerQua')
        ax.axvline(st.session_state['carga_adm_esperada'], color='blue', lw=3, ls='--', label='Carga Adm esperada')
        ax.set_title('Carga Admisible Final (kN)')
        ax.set_xlabel('Carga Admisible (kN)')
        ax.set_ylabel('Cotas (m)')
        ax.legend()
        ax.grid(True)
        plt.savefig("./Graficos/carga_admisible.png")
        st.pyplot(fig)    

        # Configuracón de gráfica comparativa
        st.subheader("Comparación entre los dos métodos:")
        fig, ax = plt.subplots(figsize=(5, 7))
        ax.plot(pa_final_aoki, cotas, color='green', marker='o', markerfacecolor='cyan', linestyle='-', label='Aoki - Velloso')
        ax.plot(pa_final_DQ, cotas, color='red', marker='o', markerfacecolor='cyan', linestyle='-', label='Decourt-Quaresma')
        ax.axvline(st.session_state['carga_adm_esperada'], color='blue', lw=3, ls='--', label='Carga Adm esperada')
        ax.set_title('Carga Admisible Final (kN)')
        ax.set_xlabel('Carga Admisible (kN)')
        ax.set_ylabel('Cotas (m)')
        ax.legend()
        ax.grid(True)
        plt.savefig("./Graficos/comparacion_metodos.png")
        st.pyplot(fig)  

        st.markdown('---')
        
    ###MEMORIA DE CÁLCULO
        st.subheader("Generar Memoria de Cálculo")
        st.write('La memoria de cálculo se genera en formato .docx')
        nombreArchivo = st.text_input("Nombre del archivo:", "Memoria de calculo")
        rutaArchivo = st.text_input("Ruta del archivo:", "C:/Users/silvi/Desktop/Pilotes_Datos/Reportes")
        rutaCompleta = os.path.join(rutaArchivo, f"{nombreArchivo}.docx")
        archivoExcel = os.path.join(rutaArchivo, 'Resultados.xlsx')

        def memoriaTipo(listaTipoSuelo, tipoPilote, listaNspt, D, cargaAdmEsperada,nombreArchivo,rutaArchivo):
            doc = DocxTemplate('./Plantilla.docx')
            df_result = resultAoki(listaTipoSuelo, tipoPilote, listaNspt, D)
            table_data = df_result.to_dict(orient='records')
            df_result_DQ = resultDC(listaTipoSuelo, tipoPilote, listaNspt, D)
            table_data_DQ = df_result_DQ.to_dict(orient='records')
            df_result_AokiDq = resultAokiDq(listaTipoSuelo, tipoPilote, listaNspt, D)
            table_data_AokiDq = df_result_AokiDq.to_dict(orient='records')

            context = {
                'titulo': 'Cálculo capacidad de carga de pilote',
                'tipo_pilote': tipoPilote,
                'diametro_pilote': D,
                'carga_adm_esperada': cargaAdmEsperada,
                'lista_nspt': listaNspt,
                'table_data': table_data,
                'table_data_DQ': table_data_DQ,
                'table_data_AokiDq': table_data_AokiDq,
                'grafica_1': InlineImage(doc, './Graficos/carga_admisible.png'),
                'grafica_2': InlineImage(doc, './Graficos/comparacion_metodos.png'),
            }

            doc.render(context)
            ruta_completa = os.path.join(rutaArchivo, f"{nombreArchivo}.docx")
            doc.save(ruta_completa)
            return
        

        opcionSoftware = st.selectbox("Seleccione el software para convertir a PDF:", ("Microsoft Office", "LibreOffice"))


        if opcionSoftware == "LibreOffice":
            rutaLibreOffice = st.text_input("Ruta a LibreOffice:", r"C:\Program Files\LibreOffice\program\swriter.exe")
        
        def convertirDocxPdfLibreOffice(libreOfficePath, document_path, out_folder):
            if not os.path.exists(document_path):
                print(f"El archivo {document_path} no existe. Primero crea la memoria en Word.")
                return False
            
            comando = [libreOfficePath, "--headless", "--convert-to", "pdf", "--outdir", out_folder, document_path]
            codigoProceso = subprocess.call(comando)
            
            if codigoProceso == 0:
                print("Conversión a PDF completada!")
                return True
            else:
                print(f"Se ha presentado un error en el proceso de conversión: {codigoProceso}")
                return False
        
            
        def excelExportar(listaTipoSuelo, tipoPilote, listaNspt, diamPil, archivoExcel):
            with pd.ExcelWriter(archivoExcel, engine='openpyxl') as writer:
                resultAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil).to_excel(writer, sheet_name='Resultados Aoki - Velloso', index=False)
                resultDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil).to_excel(writer, sheet_name='Resultados Decourt-Quaresma', index=False)
                resultAokiDq(listaTipoSuelo, tipoPilote, listaNspt, diamPil).to_excel(writer, sheet_name='Resultados Notables', index=False)
                aplicarEstilos(writer.sheets['Resultados Aoki - Velloso'])
                aplicarEstilos(writer.sheets['Resultados Decourt-Quaresma'])
                aplicarEstilos(writer.sheets['Resultados Notables'])
                print(f"El archivo Excel se ha creado correctamente.")
            return

        def aplicarEstilos(worksheet):
            border = openpyxl.styles.Side(style="thin", color=openpyxl.styles.colors.Color(rgb="000000"))
            cell_border = openpyxl.styles.Border(left=border, right=border, top=border, bottom=border)
            header_row = worksheet[1]

            for row in worksheet.iter_rows():
                for cell in row:
                    cell.alignment = openpyxl.styles.Alignment(horizontal="left", vertical="center", wrap_text=True)
                    cell.border = cell_border
                    cell.font = openpyxl.styles.Font(name='Times New Roman')
                    
            for cell in header_row:
                cell.fill = openpyxl.styles.PatternFill(start_color="e8f2a1", fill_type="solid")
                cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center", wrap_text=True)
                
            return  


        ###ESTILOS BOTONES GENERACIÓN DE MEMORIA
        col1, col2 ,col3 = st.columns(3)

        with col1:
            with stylable_container(
                "word",
                css_styles="""
                button {
                    background-color: #333333;
                    color: white;
                }""",
            ):
                botonWord = st.button("📝Crear memoria", key="button1")

            
        with col2:
            with stylable_container(
                "pdf",
                css_styles="""
                button {
                    background-color: #333333;
                    color: cyan;
                }""",
            ):
                botonPdf = st.button("📑Convertir a Pdf", key="button2")

            

        with col3:
            with stylable_container(
                "excel",
                css_styles="""
                button {
                    background-color: #333333;
                    color: #FF00FF;
                }""",
            ):
                botonExcel = st.button("📉Exportar tablas", key="button3")    
        pythoncom.CoInitialize()

        def main():
            
            if botonWord:
                memoriaTipo( st.session_state['lista_tipo_suelo'], st.session_state['tipo_pilote'], st.session_state['lista_nspt'], st.session_state['D'], st.session_state['carga_adm_esperada'], nombreArchivo, rutaArchivo)
                st.success("Memoria de cálculo creada correctamente.")

            if botonPdf:
                if opcionSoftware == "Microsoft Office":
                    if os.path.exists(rutaCompleta):  
                        docx2pdf.convert(rutaCompleta)
                        st.success("¡Conversión a PDF completada para Microsoft Office!")
                    else:
                        st.error("Primero debe generar la memoria en Word antes de proceder a convertir a PDF.")
                elif opcionSoftware == "LibreOffice":
                    if convertirDocxPdfLibreOffice(rutaLibreOffice, rutaCompleta, rutaArchivo):
                        st.success("¡Conversión a PDF completada para LibreOffice!")
                    else:
                        st.error("Primero debe generar la memoria en Word antes de proceder a convertir a PDF.")

            if botonExcel:
                excelExportar( st.session_state['lista_tipo_suelo'], st.session_state['tipo_pilote'], st.session_state['lista_nspt'], st.session_state['D'], archivoExcel)
                st.success("El archivo Excel se ha creado correctamente!")

        if __name__ == "__main__":
            main()    

        st.write('**NOTAS:**')
        st.write("""
        - Para convertir a PDF, primero debe crear la memoria. El archivo generado se guardará en la ruta especificada.
        - Para convertir a PDF, puede utilizar una de las siguientes opciones:
            - **Microsoft Office**: No se requiere especificar ninguna ruta adicional.
            - **LibreOffice**: Debe especificar la ruta al ejecutable de LibreOffice.
        - Para exportar a Excel, el archivo generado se guardará en la ruta especificada.
        """)