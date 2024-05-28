from pilotesParametros import parametroDCpilote, factorAlphaDC, factorBetaDC
import math
import pandas as pd

def search_c_Decourt(tipoSuelo):

    cGeral = pd.DataFrame(parametroDCpilote())
    locCoefC = cGeral.loc[cGeral['Suelo'] == tipoSuelo]
    listaC = locCoefC['C (kPa)'].tolist()
    coef_c_Decourt = listaC[0]

    return coef_c_Decourt

def searchParamDc(tipoSuelo):

    df = parametroDCpilote()
    df2 = df.loc[df['Suelo'] == tipoSuelo]
    lista_C = df2['C (kPa)'].tolist()

    lista_param_DC = [lista_C[0]]

    return lista_param_DC

def searchCorrAlphaDc(tipoSuelo, tipoPilote):

    df = factorAlphaDC()
    df2 = df.loc[df['Suelo'] == tipoSuelo]
    
    lista_val_alpha = df2[tipoPilote].tolist()
    
    return lista_val_alpha

def searchCorrBetaDc(tipoSuelo, tipoPilote):

    df = factorBetaDC()
    df2 = df.loc[df['Suelo'] == tipoSuelo]

    lista_valor_beta = df2[tipoPilote].tolist()

    return lista_valor_beta

def valoresC(listaTipoSuelo):

    listaValC = []
    for tipoSuelo in listaTipoSuelo:
        listaValC.append(searchParamDc(tipoSuelo)[0])

    return listaValC

def valoresAlpha(listaTipoSuelo, tipoPilote):

    listaValAlpha = []
    for tipoSuelo in listaTipoSuelo:
        listaValAlpha.append(searchCorrAlphaDc(tipoSuelo,tipoPilote)[0])

    return listaValAlpha

def valoresBeta(listaTipoSuelo, tipoPilote):

    listaValBeta = []
    for tipoSuelo in listaTipoSuelo:
        listaValBeta.append(searchCorrBetaDc(tipoSuelo,tipoPilote)[0])

    return listaValBeta


def propGeomPil(diametro):

    perimetroPil = (diametro * math.pi)
    areaPil = (pow(diametro, 2) * math.pi / 4)

    resultPropGeom = [diametro, perimetroPil, areaPil]

    return resultPropGeom

def calc_rpDq(listaTipoSuelo, listaNspt):
    extended_nspt = listaNspt + [listaNspt[-1], listaNspt[-1]]

    coefC = []
    npDecourt = []

    for i in range(len(listaTipoSuelo)):
        coefC.append(search_c_Decourt(listaTipoSuelo[i]))
        npDecourt.append((extended_nspt[i] + extended_nspt[i + 1] + extended_nspt[i + 2]) / 3)

    lista_rp = []

    for i in range(len(listaNspt)):
        lista_rp.append(coefC[i] * npDecourt[i])

    return lista_rp


def valoresRp(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    alpha = searchCorrAlphaDc(listaTipoSuelo[0], tipoPilote)[0]
    areaPilote = propGeomPil(diamPil)[2]
    listaRp = []
    valores_rp = calc_rpDq(listaTipoSuelo, listaNspt)
    
    for i in range(len(listaTipoSuelo)):
        listaRp.append(valores_rp[i] * alpha * areaPilote)
       
    return listaRp


def calc_rl(nspt):

    rl = 10 * ((nspt / 3) + 1)

    return rl

def valores_rl(listaNspt):

    listaValrl = []
    for i in range(len(listaNspt)):
        listaValrl.append(calc_rl(listaNspt[i]))
    
    return listaValrl


def valoresRl(listaTipoSuelo,tipoPilote,listaNspt,diamPil):

    perimEstaca = propGeomPil(diamPil)[1]
    rl = valores_rl(listaNspt)
    beta = searchCorrBetaDc(listaTipoSuelo[0], tipoPilote)[0]

    listaValoresRl = []
    for i in range(len(listaTipoSuelo)):
        listaValoresRl.append(beta * rl[i] * perimEstaca)


    return listaValoresRl

def valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    listaValoresRl = valoresRl(listaTipoSuelo,tipoPilote,listaNspt,diamPil)

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

def paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil):

    valoresRlacum = valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paEsc = []

    for i in range(len(valoresRlacum)):
        paEsc.append(valoresRlacum [i] * 1.25)

    return paEsc

def paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    resistTotal = resistenciaTotal(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    pa6122 = []

    for i in range(len(resistTotal)):
        pa6122.append(resistTotal[i] / 2)

    return pa6122

def paMetDq(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    valores_Rl = valoresAcumRl(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    valores_Rp = valoresRp(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paDequar = []

    for i in range(len(valores_Rl)):
        suma_valores = valores_Rl[i] / 1.3 + valores_Rp[i] / 4
        paDequar.append(suma_valores)
        
    return paDequar


def paFinalDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    pa6122 = paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paEsc = paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paDQ = paMetDq(listaTipoSuelo, tipoPilote, listaNspt, diamPil)

    paFinal = []

    for i in range(len(pa6122)):
        paFinal.append(min([pa6122[i], paEsc[i], paDQ[i]]))

    return paFinal

def cotasPunta(listaTipoSuelo):

    cotasProf = []

    for i in range(len(listaTipoSuelo)):
        cotasProf.append((i + 1) * (-1))

    return cotasProf

def resultDC(listaTipoSuelo,tipoPilote,listaNspt,diamPil):

    resultCompletoDQ = {
        'Cotas (m)' : cotasPunta(listaTipoSuelo),
        'C (kPa)' : valoresC(listaTipoSuelo),
        'α' : valoresAlpha(listaTipoSuelo,tipoPilote),
        'β' : valoresBeta(listaTipoSuelo,tipoPilote),
        'Rp (kN)' : valoresRp(listaTipoSuelo, tipoPilote,listaNspt, diamPil),
        'Rl (kN)' : valoresRl(listaTipoSuelo, tipoPilote,listaNspt, diamPil),
        'Rl acum.(kN)' : valoresAcumRl(listaTipoSuelo, tipoPilote,listaNspt, diamPil),
        'Rt (kN)' : resistenciaTotal(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Norma (kN)' : paNbr6122(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Excavada (kN)' : paExcavadas(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Met. DecQua (kN)' : paMetDq(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Pa Final DecQua (kN)' : paFinalDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        
    }
    for key in ['α', 'β', 'Rp (kN)', 'Rl (kN)','Rl acum.(kN)','Rt (kN)', 'Pa Norma (kN)', 'Pa Excavada (kN)', 'Pa Met. DecQua (kN)' ,'Pa Final DecQua (kN)']:
        resultCompletoDQ[key] = [round(val, 2) for val in resultCompletoDQ[key]]

    
    dfResultDQ = pd.DataFrame(resultCompletoDQ)
    return  dfResultDQ

