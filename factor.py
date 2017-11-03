from tabulate import tabulate

class Factor(object):

    counter = 0
    
    def __init__(self):
        self.table = {}
        self.variables = []
        Factor.counter += 1
        self.identifier = 'f' + str(Factor.counter)

    @staticmethod
    def resetCounter(self):
        counter = 0

    def loadTableFromFile(self, inputFile):
        f = open(inputFile, 'r') 
        lines = f.readlines()
        f.close()

        self.setVariables(lines[0].rstrip().split(' '))

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
        self.identifier +=  '(' + ','.join(self.variables) +')'

    def getAssignmentOfVariable(self, variable, variablesAssignment):
        variableIndex = self.variables.index(variable)
        return variablesAssignment[variableIndex]

    def addEntry(self, variablesAssignment, probabilityValue):
        if variablesAssignment:
            if variablesAssignment in self.table.keys():
                print('Error. Attempt to add duplicate entry in factor')
            else:
                self.table[variablesAssignment] = probabilityValue

    def getValueForAssignment(self, variablesAssignment):
        if variablesAssignment in self.table.keys():
            return self.table[variablesAssignment]
        else: return -1

    def print(self):
        '''
            print CPT in tabular form
        '''
        print(20*'=' + self.identifier + 20*'=')
        headers = self.variables + ['Probability']
        data = list(k + (v,) for k,v in self.table.items())
        print(tabulate(data, headers=headers))
        print(50*'=')


if __name__ == '__main__':
    CPT_FS = Factor()
    inputFile = '/Users/apple/Documents/git-repos/Q2/bayesian-network/Initial_CPTs/FH_given_FS_FM_NDG.txt'
    CPT_FS.loadTableFromFile(inputFile)
    CPT_FS.print()
