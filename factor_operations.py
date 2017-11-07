from factor import Factor

'''
Special handling done for restricting a variable a factor of one variable
E.g restricting f(A) to A=True would return
===f(A)===
False 0.4
'''
def restrict(factor, variable, value):
    restrictedFactor = Factor()

    #The variable to be restricted should be one of the factor variables
    if variable not in factor.getVariables():
        print(' Variable ' + variable + ' not present in the factor')
        
    #Set the variables of the resulting restricted factor
    newVariables = []    
    if len(factor.getVariables()) == 1:  #Special case when restricting a factor of one variable. E.g. restricting f(A) to A=True
        newVariables.append(variable)
    else:
        newVariables = [var for var in factor.getVariables() if var != variable]
    restrictedFactor.setVariables(newVariables)
    
    #Restrict the CPT entries
    for variablesAssignment, probabilityValue in factor.table.items():
        if factor.getAssignmentOfVariable(variable, variablesAssignment) == value:
            newvariablesAssignment = ()
            for i in range(len(variablesAssignment)):
                if len(factor.getVariables()) == 1 or factor.getVariables()[i] != variable:
                   newvariablesAssignment += (variablesAssignment[i],)
            restrictedFactor.addEntry(newvariablesAssignment, probabilityValue)

    return restrictedFactor



def assignmentsMatch(assignment1, indexes1, assignment2, indexes2):
    '''
        Helper function used in multiplication operation. Checks whether a factory table entry assignment1 and
        another factory table entry assignment2 matches (i.e have same True/False assingments) for their corresponding indices
    '''
    if len(indexes1) != len(indexes2):
        print('Error matching 2 entries')
        
    isMatch = True 
    for i in range(len(indexes1)):
        if assignment1[indexes1[i]] != assignment2[indexes2[i]]:
            isMatch = False
            break
    return isMatch
    

def multiply(factor1, factor2):
    productFactor = Factor()
    commonVariables = list(set(factor1.getVariables()) & set(factor2.getVariables()))

    #Cannot multiply if the factors have no common variables
    if len(commonVariables) == 0:
        print('Cannot multiply the 2 factors. No common variables')
        return None

    #Set the variables of the resulting product factor
    newVariables = [var for var in factor1.getVariables()]
    newVariables += [var for var in factor2.getVariables() if var not in commonVariables]
    productFactor.setVariables(newVariables)

    #Get indexes of the common variables in both tables
    indexes1 = [factor1.getVariables().index(var) for var in commonVariables]
    indexes2 = [factor2.getVariables().index(var) for var in commonVariables]

    #Multiply the CPT entries
    for variablesAssignment1, probabilityValue1 in factor1.table.items():
        for variablesAssignment2, probabilityValue2 in factor2.table.items():            
            if assignmentsMatch(variablesAssignment1, indexes1, variablesAssignment2, indexes2):
                newVariablesAssignment = variablesAssignment1
                for i in range(len(variablesAssignment2)):
                    if i not in indexes2:
                        newVariablesAssignment += (variablesAssignment2[i],)

                newProbabilityValue = probabilityValue1 * probabilityValue2
                productFactor.addEntry(newVariablesAssignment, newProbabilityValue)

    return productFactor
                
def sumout(factor, variable):
    resultFactor = Factor()

    #Cannot sum out a variable that is not in the factor table
    if variable not in factor.getVariables():
        print('Cannot Sum out a variable that is not present in the factor')

    #Index of the variable to be summed out
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
                        

def normalize(factor):
    '''
        Normalizes each probability value of the factor table by dividing it by the total sum        
    '''
    
    normalizedFactor = Factor()

    #Set the variables of the normalized factor
    newVariables = [var for var in factor.getVariables()]
    normalizedFactor.setVariables(newVariables)

    #Normalize the CPT entries
    probabilitySum = sum(factor.table.values())
    for variablesAssignment, probabilityValue in factor.table.items():
        normalizedFactor.addEntry(variablesAssignment, probabilityValue/probabilitySum)

    return normalizedFactor
    
def inference(factorList, queryVariable, orderedListOfHiddenVariables, evidenceList):
    '''
        Assumptions
        1. evidenceList is a list of tuples (variable, assignment)
        2. queryVariable is a single variable
        
    '''

    print('The intial factors are:')
    for factor in factorList:
        factor.print()
    
    #Perform restriction
    for variable, value in evidenceList:
        for i in range(len(factorList)):
            if variable in factorList[i].getVariables():
                print('\nRestricting ' + variable + ' to ' +  value +' in the below factor')
                factorList[i].print()
                restrictedFactor = restrict(factorList[i], variable, value)                                       
                restrictedFactor.print()
                factorList[i] = restrictedFactor

    '''
      This is a post-restriction step. After restricting, eliminate the
      factors with one variable that have been restricted. For e.g. if a factor f(A) has been restricted (say A=True)
      the result would be a factor of the form:
      ===f(A)===
      False 0.4

      Such factors are eliminated
    '''
    filteredFactorList = []
    for factor in factorList:
        if not (len(factor.getVariables()) == 1 and factor.getVariables()[0] in [var for var, value in evidenceList]):
            filteredFactorList.append(factor)
    factorList = filteredFactorList
    
    #Performing sum out
    for variable in orderedListOfHiddenVariables:
        print('\nSumming out variable %s...' % variable)
        factorsWithThisVariable = [factor for factor in factorList if variable in factor.getVariables()]
        print('Factors to multiply = ', end=' ')
        print(len(factorsWithThisVariable))
        while len(factorsWithThisVariable) != 1:
            productFactor = multiply(factorsWithThisVariable.pop(), factorsWithThisVariable.pop())
            factorsWithThisVariable.append(productFactor)

        print('Product factor after multiplying all factors with variable %s' % variable)
        factorsWithThisVariable[0].print()

        print('Result factor after summing out variable %s' % variable)
        resultFactor = sumout(factorsWithThisVariable[0], variable)
        resultFactor.print()
        factorList = [factor for factor in factorList if variable not in factor.getVariables()]
        factorList.append(resultFactor)

    '''
        Final step - when the final factor list are all factors of the query variable
        If there are more than one of such factors, then multiply them to get a single factor
    '''
    print('\nFinal factors remaining:')
    for factor in factorList:
        factor.print()

    #Final processing
    while len(factorList) != 1:
        f1 = factorList.pop()
        f2 = factorList.pop()
        if f1 == None:
            factorList.append(f2)
            break
        elif f2 == None:
            factorList.append(f1)
            break
        productFactor = multiply(f1, f2)
        factorList.append(productFactor)

    #Normalize the final factor
    if len(factorList) != 1:
        print('Something wrong..Final factor list should have a single factor')
        return None
    else:
        normalizedFactor = normalize(factorList[0])
        print('\nFinal Factor after normalizing')
        normalizedFactor.print()
        return normalizedFactor

                                
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
    print('Multiplying the factors...')
    productFactor.print()
    print('\n\n')

    #Test Sumout operation
    print('Testing Sumout operation')
    CPT2.print()

    print('Summing out A...')
    resultFactor = sumout(CPT2, 'A')
    resultFactor.print()
    print('\n\n')

    #Test Normalize operation
    print('Testing Normalize operation')
    resultFactor.print()

    print('Normalizing the factor...')
    normalizedFactor = normalize(resultFactor)
    normalizedFactor.print()
    print('\n\n')

    Factor.resetCounter()
    CPT_FB_given_FS = Factor()
    CPT_FB_given_FS.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FB_given_FS.txt')
    CPT_FH_given_FS_FM_NDG = Factor()
    CPT_FH_given_FS_FM_NDG.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FH_given_FS_FM_NDG.txt')
    CPT_FM = Factor()
    CPT_FM.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FM.txt')
    CPT_FS = Factor()
    CPT_FS.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FS.txt')
    CPT_NA = Factor()
    CPT_NA.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/NA.txt')
    CPT_NDG_given_NA_FM = Factor()
    CPT_NDG_given_NA_FM.loadTableFromFile('/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/NDG_given_NA_FM.txt')

    #Q. 3b Ans = 0.0730702
    initialFactorCount = Factor.getCounter()
    factorList = [CPT_FH_given_FS_FM_NDG, CPT_FS, CPT_FM, CPT_NDG_given_NA_FM, CPT_NA]
    queryVariables = ['FH']
    orderedListOfHiddenVariables = ['NA', 'FS', 'FM', 'NDG']
    evidenceList = []
    print('Inferring Q. 3b....')
    resultFactor = inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
    print('Answer is %.3f' % resultFactor.getValueForAssignment(('True',)))
    print('\n\n')

    #Q.3c Ans = 0.0859415
    Factor.setCounter(initialFactorCount)
    factorList = [CPT_FH_given_FS_FM_NDG, CPT_NDG_given_NA_FM, CPT_FS, CPT_FM, CPT_NA]
    queryVariables = ['FS']
    orderedListOfHiddenVariables = ['NA', 'NDG']
    evidenceList = [('FM', 'True'), ('FH', 'True')]
    print('Inferring Q. 3c....')
    resultFactor = inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
    print('Answer is %.3f' % resultFactor.getValueForAssignment(('True',)))
    print('\n\n')

    #Q.3d Ans = 0.360667
    Factor.setCounter(initialFactorCount)
    factorList = [CPT_FH_given_FS_FM_NDG, CPT_NDG_given_NA_FM, CPT_FB_given_FS, CPT_FS, CPT_FM, CPT_NA]
    queryVariables = ['FS']
    orderedListOfHiddenVariables = ['NA', 'NDG']
    evidenceList = [('FM', 'True'), ('FH', 'True'), ('FB', 'True')]
    print('Inferring Q. 3d....')
    resultFactor = inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
    print('Answer is %.3f' % resultFactor.getValueForAssignment(('True',)))
    print('\n\n')

    #Q. 3e Ans = 0.33844
    Factor.setCounter(initialFactorCount)
    factorList = [CPT_FH_given_FS_FM_NDG, CPT_NDG_given_NA_FM, CPT_FB_given_FS, CPT_FS, CPT_FM, CPT_NA]
    queryVariables = ['FS']
    orderedListOfHiddenVariables = ['NDG']
    evidenceList = [('FM', 'True'), ('FH', 'True'), ('FB', 'True'), ('NA', 'True')]
    print('Inferring Q. 3e....')
    resultFactor = inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
    print('Answer is %.3f' % resultFactor.getValueForAssignment(('True',)))
    print('\n\n')
    
