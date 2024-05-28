import pandas as pd


def paramAokiPil ():
    coefKyAlfa = [[1, 1000, 0.014],
                  [12, 800, 0.02],
                  [123, 700, 0.024],
                  [13, 600, 0.03],
                  [132, 500, 0.028],
                  [2, 400, 0.03],
                  [21, 550, 0.022],
                  [213, 450, 0.03],
                  [23, 230, 0.034],
                  [231, 250, 0.03],
                  [3, 200, 0.06],
                  [31, 350, 0.024],
                  [312, 300, 0.028],
                  [32, 220, 0.04],
                  [321, 330, 0.03]]
    
    dfparamAoki = pd.DataFrame(coefKyAlfa, columns = ['Suelo', 'K (kPa)', 'Alfa'])
    
    return dfparamAoki

def factorCorrAoki ():

    corrAoki = [
        ['Excavada' , 3, 6],
        ['Raiz', 2, 4],
        ['HCM', 2, 4]
    ]

    dfCorreccionAoki = pd.DataFrame(corrAoki, columns = ['Tipo de pilote', 'F1', 'F2'])
   
    return dfCorreccionAoki

def parametroDCpilote():
    
    coef_C_DC = [
        [3, 120],
        [31, 120],
        [32, 120],
        [312, 120],
        [321, 120],
        [2, 200],
        [23, 200],
        [231, 200],
        [21, 250],
        [213, 250],
        [1, 400],
        [12, 400],
        [13, 400],
        [123, 400],
        [132, 400]
    ]

    dfParametroDC = pd.DataFrame(coef_C_DC, columns=['Suelo', 'C (kPa)'])
    
    return dfParametroDC

def factorAlphaDC():

    coefAlphaDC = [
            [1, 0.5, 0.3, 0.5],
            [12, 0.5, 0.3, 0.5],
            [123, 0.5, 0.3, 0.5],
            [13, 0.5, 0.3, 0.5],
            [132, 0.5, 0.3, 0.5],
            [2, 0.6, 0.3, 0.6],
            [21, 0.6, 0.3, 0.6],
            [213, 0.6, 0.3, 0.6],
            [23, 0.6, 0.3, 0.6],
            [231, 0.6, 0.3, 0.6],
            [3, 0.85, 0.3, 0.85],
            [31, 0.85, 0.3, 0.85],
            [312, 0.85, 0.3, 0.85],
            [32, 0.85, 0.3, 0.85],
            [321, 0.85, 0.3, 0.85]]
    dfFactorAlpha = pd.DataFrame(coefAlphaDC, columns=['Suelo', 'Excavada', 'HCM', 'Raiz'])
    
    return  dfFactorAlpha

def factorBetaDC():

    coefBetaDC = [
            [1, 0.5, 1, 1.5],
            [12, 0.5, 1, 1.5],
            [123, 0.5, 1, 1.5],
            [13, 0.5, 1, 1.5],
            [132, 0.5, 1, 1.5],
            [2, 0.65, 1, 1.5],
            [21, 0.65, 1, 1.5],
            [213, 0.65, 1, 1.5],
            [23, 0.65, 1, 1.5],
            [231, 0.65, 1, 1.5],
            [3, 0.8, 1, 1.5],
            [31, 0.8, 1, 1.5],
            [312, 0.8, 1, 1.5],
            [32, 0.8, 1, 1.5],
            [321, 0.8, 1, 1.5]]
        

    dfFactorBeta = pd.DataFrame(coefBetaDC, columns=['Suelo', 'Excavada', 'HCM', 'Raiz'])
    
    return  dfFactorBeta