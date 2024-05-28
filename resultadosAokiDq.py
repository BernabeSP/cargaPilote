import pandas as pd
from funCapCargaAoki import cotasPunta,paFinalAoki
from funCapCargaDC import paFinalDC


def paFinalAokiDq (listaTipoSuelo, tipoPilote, listaNspt, diamPil):
    paAoki = paFinalAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    paDq = paFinalDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil)

    paFinal = []

    for i in range(len(paAoki)):
        paFinal.append(min([paAoki[i], paDq[i]]))

    return paFinal

 
def resultAokiDq(listaTipoSuelo,tipoPilote,listaNspt,diamPil):

    resultCompletoAokiDq = {
        'Cotas (m)' : cotasPunta(listaTipoSuelo),
        'Pa Final Aoki (kN)' : paFinalAoki(listaTipoSuelo, tipoPilote, listaNspt, diamPil),  
        'Pa Final DecQua (kN)' : paFinalDC(listaTipoSuelo, tipoPilote, listaNspt, diamPil),
        'Menor valor entre métodos (kN)': paFinalAokiDq(listaTipoSuelo, tipoPilote, listaNspt, diamPil)
    }
    for key in ['Pa Final Aoki (kN)','Pa Final DecQua (kN)','Menor valor entre métodos (kN)']:
        resultCompletoAokiDq[key] = [round(val, 2) for val in resultCompletoAokiDq[key]]

    
    dfResultAokiDq = pd.DataFrame(resultCompletoAokiDq)
    return  dfResultAokiDq

