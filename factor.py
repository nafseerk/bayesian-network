from tabulate import tabulate

class Factor(object):
    '''
    class for representing a factor. Contains the following fields:
        1. variables - list of variable names. Each name is a string
        2. table - a dictionary to store the CPT, where the key is a tuple of
           variable assignmennts(True/False values for all the variable in the factor)
           and value is the probabilty.
           The value or assignment of an individual variable is a string either 'True' or 'False'.
           So for a factor of varialbes A, B, C one of the table keys will be ('True', 'False', 'True')
        3. identifier - which is a unique name for the CPT of the form: f<a number>(variable names). Eg. f3(A,B,C)
    '''

    counter = 0
    
    def __init__(self):
        self.table = {}
        self.variables = []
        Factor.counter += 1
        self.identifier = 'f' + str(Factor.counter)

    @staticmethod
    def resetCounter():
        Factor.counter = 0

    @staticmethod
    def getCounter():
        return Factor.counter 

    @staticmethod
    def setCounter(count):
        Factor.counter = count

    def loadTableFromFile(self, inputFile):
        '''
            Used for loading CPT values from a file. This can be used for loading
            the initial CPTs of the Beayesian Network
        '''
        f = open(inputFile, 'r') 
        lines = f.readlines()
        f.close()

        self.setVariables(lines[0].rstrip().split(' '))

        for line in lines[1:]:
            variablesAssignment = tuple(line.split(' ')[:-1])
            probabilityValue = float(line.split(' ')[-1])
            self.table[variablesAssignment] = probabilityValue

    def getVariables(self):
        return self.variables

    def setVariables(self, variables):
        '''
            Used for setting variables for a factor 
        '''
        self.variables = variables
        self.identifier +=  '(' + ','.join(self.variables) +')'

    def getAssignmentOfVariable(self, variable, variablesAssignment):
        '''
            Given a factor table entry "variablesAssignment"
            return the value assigned to that variable
        '''
        variableIndex = self.variables.index(variable)
        return variablesAssignment[variableIndex]

    def addEntry(self, variablesAssignment, probabilityValue):
        '''
            Add new entries in the factor table
        '''
        if variablesAssignment:
            if variablesAssignment in self.table.keys():
                print('Error. Attempt to add duplicate entry in factor')
            else:
                self.table[variablesAssignment] = probabilityValue

    def getValueForAssignment(self, variablesAssignment):
        '''
            Returns the probability value of a factor table entry
        '''
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
