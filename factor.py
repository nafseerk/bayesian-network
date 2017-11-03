from tabulate import tabulate

class Factor(object):


    def __init__(self):
        self.table = {}
        self.variables = []

    def loadTableFromFile(self, inputFile):
        f = open(inputFile, 'r') 
        lines = f.readlines()
        f.close()

        self.variables = lines[0].rstrip().split(' ')

        for line in lines[1:]:
            variablesAssignment = tuple(line.split(' ')[:-1])
            probabilityValue = float(line.split(' ')[-1])
            self.table[variablesAssignment] = probabilityValue

    def validate(self):
        '''
            Ensure the count of entries in correct 
        '''
        pass

    def getVariables(self):
        return self.variables

    def setVariables(self, variables):
        self.variables = variables

    def getAssignmentOfVariable(self, variable, variablesAssignment):
        variableIndex = self.variables.index(variable)
        return variablesAssignment[variableIndex]

    def addEntry(self, variablesAssignment, probabilityValue):
        self.table[variablesAssignment] = probabilityValue

    def print(self):
        '''
            print CPT in tabular form
        '''
        print(20*'=' + "CPT" + 20*'=')
        headers = self.variables + ['Probability']
        data = list(k + (v,) for k,v in self.table.items())
        print(tabulate(data, headers=headers))
        print(43*'=')


if __name__ == '__main__':
    CPT_FS = Factor()
    inputFile = '/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FH_given_FS_FM_NDG.txt'
    CPT_FS.loadTableFromFile(inputFile)
    CPT_FS.print()
