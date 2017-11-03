from factor import Factor

def restrict(factor, variable, value):
    restrictedFactor = Factor()

    if variable not in factor.getVariables():
        print(' Variable ' + variable + ' not present in the factor')

    #Set the variables of the restricted factor
    newVariables = [var for var in factor.getVariables() if var != variable]
    restrictedFactor.setVariables(newVariables)
    
    #Restrict the CPT entries
    for variablesAssignment, probabilityValue in factor.table.items():
        if factor.getAssignmentOfVariable(variable, variablesAssignment) == value:
            newvariablesAssignment = ()
            for i in range(len(variablesAssignment)):
                if factor.getVariables()[i] != variable:
                   newvariablesAssignment =  newvariablesAssignment + (variablesAssignment[i],)
            restrictedFactor.addEntry(newvariablesAssignment, probabilityValue)

    return restrictedFactor


def multiply(factor1, factor2):
    productFactor = Factor()
    commonVariables = list(set(factor1.getVariables()) & set(factor2.getVariables()))
    targetVariable = None
    
    if len(commonVariables) == 0:
        print('Cannot multiply the 2 factors. No common variables')
    elif len(commonVariables) == 1:
        targetVariable = commonVariables[0]
    else:
        #decide what to do when more than 1 common variable among the two factos
        pass

    if not targetVariable:
        print('Cannot multiply the 2 factors')
    
    tvIdxFactor1 = factor1.getVariables().index(targetVariable)
    tvIdxFactor2 = factor2.getVariables().index(targetVariable)

    #Set the variables of the product factor
    newVariables = [var for var in factor1.getVariables()]
    newVariables += [var for var in factor2.getVariables() if var != targetVariable]
    productFactor.setVariables(newVariables)

    #Multiply the CPT entries
    for variablesAssignment1, probabilityValue1 in factor1.table.items():
        for variablesAssignment2, probabilityValue2 in factor2.table.items():
            if variablesAssignment1[tvIdxFactor1] == variablesAssignment2[tvIdxFactor2]:
                newVariablesAssignment = variablesAssignment1
                for i in range(len(variablesAssignment2)):
                    if i != tvIdxFactor2:
                        newVariablesAssignment += (variablesAssignment2[i],)

                newProbabilityValue = probabilityValue1 * probabilityValue2
                productFactor.addEntry(newVariablesAssignment, newProbabilityValue)

    return productFactor
                
def sumout(factor, variable):
    resultFactor = Factor()

    if variable not in factor.getVariables():
        print('Cannot Sum out a variable that is not present in the factor')

    tvIdx = factor.getVariables().index(variable)

    #Set the variables of the result factor
    newVariables = [var for var in factor.getVariables() if var != variable]
    resultFactor.setVariables(newVariables)

    #Sum out the variable from CPT entries
    for variablesAssignment, probabilityValue in factor.table.items():
        for otherVariablesAssignment, otherProbabilityValue in factor.table.items():
            allOtherAssignmentsSame = True
            for i in range(len(variablesAssignment)):
                if i != tvIdx and variablesAssignment[i] != otherVariablesAssignment[i]:
                    allOtherAssignmentsSame = False
                    break
            if allOtherAssignmentsSame and variablesAssignment[tvIdx] != otherVariablesAssignment[tvIdx]:
                newVariablesAssignment = ()
                for i in range(len(variablesAssignment)):
                    if i != tvIdx:
                        newVariablesAssignment += (variablesAssignment[i],)                    
                newProbabilityValue = probabilityValue + otherProbabilityValue
                if resultFactor.getValueForAssignment(newVariablesAssignment) == -1:
                    resultFactor.addEntry(newVariablesAssignment, newProbabilityValue)

    return resultFactor
                        
            
    

if __name__ == '__main__':
    #Test Restrict operation
    print('Testing Restrict operation')
    CPT1 = Factor()
    inputFile = '/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FH_given_FS_FM_NDG.txt'
    CPT1.loadTableFromFile(inputFile)
    CPT1.print()

    restrictedFactor = restrict(CPT1, 'NDG', 'True')
    print('Restricting NDG to True...')
    print('Resticted Factor')
    restrictedFactor.print()
    print('\n\n')

    #Test Product operation
    print('Testing Product operation')
    CPT2 = Factor()
    CPT2.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/test-data/B_given_A.txt')
    CPT2.print()

    CPT3 = Factor()
    CPT3.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/test-data/C_given_B.txt')
    CPT3.print()

    productFactor = multiply(CPT2, CPT3)
    print('The product factor is...')
    productFactor.print()
    print('\n\n')

    #Test Sumout operation
    print('Testing Sumout operation')
    CPT2.print()

    print('Summing out A...')
    resultFactor = sumout(CPT2, 'A')
    resultFactor.print()
    print('\n\n')
    
