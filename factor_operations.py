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


if __name__ == '__main__':
    CPT1 = Factor()
    inputFile = '/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FH_given_FS_FM_NDG.txt'
    CPT1.loadTableFromFile(inputFile)
    CPT1.print()

    restrictedCPT = restrict(CPT1, 'NDG', 'True')

    restrictedCPT.print()
    
