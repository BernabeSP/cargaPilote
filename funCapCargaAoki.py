import math
import pandas as pd
from matplotlib import pyplot as plt
from pilotesParametros import paramAokiPil, factorCorrAoki
from funCapCargaDC import resultDC
import openpyxl

def searchPramAoki(tipoSuelo):

    df = paramAokiPil()
    df2 =  df.loc[df['Suelo'] == tipoSuelo]
    listaValK = df2['K (kPa)'].tolist()
    listValAlfa = df2['Alfa'].tolist()

    listaParamAoki = [listaValK[0], listValAlfa[0]]

    return listaParamAoki


def searchCorrAoki(tipoPilote):

    df = factorCorrAoki()
    df2 = df.loc[df['Tipo de pilote'] == tipoPilote]
    listaValF1 = df2['F1'].tolist()
    listaValF2 = df2['F2'].tolist()

    listaFactorCorr = [listaValF1[0], listaValF2[0]]
 
    return listaFactorCorr

def calc_rpAoki (tipoSuelo, tipoPilote, nspt):

    valorK = searchPramAoki(tipoSuelo)[0]
    valorF1 = searchCorrAoki(tipoPilote)[0]

    rp = valorK * nspt / valorF1 #rp en kPa

    return rp

def calc_rlAoki (tipoSuelo, tipoPilote, nspt):

    valorK = searchPramAoki(tipoSuelo)[0]
    valorAlfa = searchPramAoki(tipoSuelo)[1]
    valorF2 = searchCorrAoki(tipoPilote)[1]

    rl = valorK * nspt * valorAlfa / valorF2 #rl en kPa

    return rl

def propGeomPil(diametro):

    perimetroPil = (diametro * math.pi)
    areaPil = (pow(diametro, 2) * math.pi / 4)

    resultPropGeom = [diametro, perimetroPil, areaPil]

    return resultPropGeom

def valoresK(listaTipoSuelo):

    listaValoresK = []

    for ts in range(len(listaTipoSuelo)):
        listaValoresK.append(searchPramAoki(listaTipoSuelo[ts])[0])

    return listaValoresK

def valoresrp(listaTipoSuelo, tipoPilote, listaNspt):

    listaNspt.append(listaNspt[-1])
    listaValoresrp = []

    for i in range(len(listaTipoSuelo)):
        listaValoresrp.append(calc_rpAoki(listaTipoSuelo[i], tipoPilote, listaNspt[i + 1]))

    listaNspt.pop()


    return listaValoresrp

def valoresRp(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    areaPil = propGeomPil(diamPil)[2]
    rp = valoresrp(listaTipoSuelo, tipoPilote, listaNspt)

    listaValoresRp = []

    for i in range(len(listaTipoSuelo)):
        listaValoresRp.append(rp[i] * areaPil)

    return listaValoresRp

def valoresrl(listaTipoSuelo, tipoPilote, listaNspt):

    listaValoresDerl = []

    for i in range(len(listaTipoSuelo)):
        listaValoresDerl.append(calc_rlAoki(listaTipoSuelo[i], tipoPilote, listaNspt[i]))


    return listaValoresDerl

def valoresRl (listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    perimPilote = propGeomPil(diamPil)[1]
    rl = valoresrl(listaTipoSuelo, tipoPilote, listaNspt)

    listaValoresDeRl = []

    for i in range(len(listaTipoSuelo)):
        listaValoresDeRl.append(rl[i] * perimPilote)


    return listaValoresDeRl

def valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    listaValoresRl = valoresRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil)

    series = pd.Series(listaValoresRl)
    listaAcumuladaRl = series.cumsum()

    return listaAcumuladaRl

def resistenciaTotal(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    lateralAcumulado = valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    resitenciaPunta = valoresRp(listaTipoSuelo, tipoPilote, listaNspt, diamPil) 
    resistenciaTotalRpRl = []

    for i in range(len(lateralAcumulado)):
        resistenciaTotalRpRl.append(lateralAcumulado[i] + resitenciaPunta[i])


    return resistenciaTotalRpRl

def paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    resistTotal = resistenciaTotal(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    pa6122 = []

    for i in range(len(resistTotal)):
        pa6122.append(resistTotal[i] / 2)

    return pa6122



def paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    valoresRlacum = valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paEsc = []

    for i in range(len(valoresRlacum)):
        paEsc.append(valoresRlacum [i] * 1.25)

    return paEsc

def paFinalAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    pa6122 = paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paEsc = paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil)

    paFinal = []

    for i in range(len(pa6122)):
        paFinal.append(min([pa6122[i], paEsc[i]]))

    return paFinal

def cotasPunta(listaTipoSuelo):

    cotasProf = []

    for i in range(len(listaTipoSuelo)):
        cotasProf.append((i + 1) * (-1))

    return cotasProf

def resultAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    resultCompletoAoki = {
        'Cotas (m)' : cotasPunta(listaTipoSuelo),
        'K (kPa)' : valoresK(listaTipoSuelo),
        'rp (kPa)' : valoresrp(listaTipoSuelo, tipoPilote, listaNspt),
        'Rp (kN)' : valoresRp(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'rl (kPa)' : valoresrl(listaTipoSuelo, tipoPilote, listaNspt),
        'Rl (kN)' : valoresRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Rl acum.(kN)' : valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Rt (kN)' : resistenciaTotal(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Norma (kN)' : paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil), 
        'Pa Excavada (kN)' : paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Final Aoki (kN)' : paFinalAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil)       
    }

    for key in ['rp (kPa)', 'Rp (kN)','rl (kPa)', 'Rl (kN)', 'Rl acum.(kN)','Rt (kN)', 'Pa Norma (kN)', 'Pa Excavada (kN)', 'Pa Final Aoki (kN)']:
        resultCompletoAoki[key] = [round(val, 2) for val in resultCompletoAoki[key]]

    dfResult = pd.DataFrame(resultCompletoAoki)
   

    return dfResult

def graficaResultado(listaTipoSuelo, tipoPilote, listaNspt, diamPil, cargaAdmEsperada):

    resultadoFinal = resultAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    # Obtener los datos para generar el gráfico.
    cotas = resultadoFinal['Cotas (m)']
    paFinalAoki = resultadoFinal['Pa Final Aoki (kN)']

    # Generar la tabla y el gráfico en la misma fila, en columnas diferentes.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.5, 7), gridspec_kw={'width_ratios': [2, 1]})

    # Tabla
    ax1.axis('tight')
    ax1.axis('off')
    tabla = ax1.table(cellText=resultadoFinal.values, colLabels=resultadoFinal.columns, loc='center')
    tabla.auto_set_font_size(False)  # Desactivar el ajuste automático del tamaño de fuente
    tabla.set_fontsize(8)  # Establecer el tamaño de fuente
    tabla.scale(1.5, 1.5)  # Escalar la tabla para que sea más grande

    # Agregar título a la tabla
    ax1.text(0.5, 0.9, 'Capacidad de carga por Aoki - Velloso', fontsize=14, color='blue', fontweight='bold', ha='center', va='bottom', transform=ax1.transAxes)

    # Gráfico
    line_datos, = ax2.plot(paFinalAoki, cotas, color='green', marker='o', markerfacecolor='cyan', linestyle='-', label='Valor menor')
    ax2.set_title('Carga Admisible Final (kN)')
    ax2.set_xlabel('Carga Admisible (kN)')
    ax2.set_ylabel('Cotas (m)')
    line_v = ax2.axvline(cargaAdmEsperada, color='blue', lw=3, ls='--', label='Carga Adm esperada')
    ax2.legend(handles=[line_datos, line_v])
    ax2.grid(True)

    # Ajustar el tamaño de ventana a contenido (tabla y gráfica) 
    plt.tight_layout()
    #plt.show()

    return

def graficaAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil, cargaAdmEsperada):
    resultadoFinal = resultAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    cotas = resultadoFinal['Cotas (m)']
    paFinalAoki = resultadoFinal['Pa Final Aoki (kN)']

    # Generar la gráfica
    fig, ax = plt.subplots(figsize=(4, 8))
    ax.plot(paFinalAoki, cotas, color='green', marker='o', markerfacecolor='cyan', linestyle='-')
    ax.set_title('Carga Admisible Final (kN)')
    ax.set_xlabel('Carga Admisible (kN)')
    ax.set_ylabel('Cotas (m)')
    ax.axvline(cargaAdmEsperada, color='blue', lw=3, ls='--', label='Carga Adm esperada')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    #plt.show()

    return fig

def excelExportar(listaTipoSuelo, tipoPilote, listaNspt, diamPil, archivoExcel):
    with pd.ExcelWriter(archivoExcel, engine='openpyxl') as writer:
        resultAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil).to_excel(writer, sheet_name='Resultados Aoki - Velloso', index=False)
        resultDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil).to_excel(writer, sheet_name='Resultados Decourt-Quaresma', index=False)
        aplicarEstilos(writer.sheets['Resultados Aoki - Velloso'])
        aplicarEstilos(writer.sheets['Resultados Decourt-Quaresma'])
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
