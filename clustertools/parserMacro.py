
import os
import colorama

class ParserMacro:
    def __init__(self):
        self.parserAllFiles = {}
        self.aliasToGate = {}
        self.aliasNumber = 0
        self.parserAlias = {}
        self.parserAttributes = {}
        self.macFiles = []
        self.fullMacroDir = ""

    def parseMacFiles(self, fullMacroDir, mainMacroFile):
        self.fullMacroDir = fullMacroDir
        self.macFiles = [os.path.join(self.fullMacroDir, mainMacroFile)]
        while len(self.macFiles) != 0:
            #Take first macro file in the list
            currentMacFiles = self.macFiles[0]

            # Structure containing all lines of the macro file
            self.parserAllFiles[currentMacFiles] = []
            with open(os.path.join(fullMacroDir, currentMacFiles)) as f:  # open file
                for line in f:
                    self.parserAllFiles[currentMacFiles] += [line]

            #Start to parse the macro file
            self.parseControlCommand(currentMacFiles)
            self.parseAttributes(currentMacFiles)

            #Take next file
            del self.macFiles[0]

    def parseControlCommand(self, file):
        #Parse macro file to get /control/ commands
        for index, line in enumerate(self.parserAllFiles[file]):
            if not line.startswith('#') and not line == '\n':
                line = line.strip()
                splitLine = line.split(" ")
                splitLine = [x for x in splitLine if x]
                if len(splitLine) > 0 and splitLine[0][:9] == '/control/':
                    self.checkControlCommand(splitLine, file, index)

    def checkControlCommand(self, splitLine, file, index):
        if len(splitLine) > 0 and splitLine[0] == '/control/alias':
            self.parseAlias(splitLine)
        elif len(splitLine) > 0 and splitLine[0] == '/control/strdoif':
            newSplitLine = self.parseCondition(splitLine)
            if len(newSplitLine) > 0:
                newLine = " ".join(newSplitLine)
                newLine += '\n'
                self.parserAllFiles[file][index] = newLine
                if newSplitLine[0][:9] == '/control/':
                    self.checkControlCommand(newSplitLine, file, index)
            else:
                self.parserAllFiles[file][index] = "\n"
        elif len(splitLine) > 0 and splitLine[0] == '/control/execute':
            self.getMacroFiles(splitLine)
        elif len(splitLine) > 0 and (splitLine[0] == '/control/add' or
                                     splitLine[0] == '/control/substract' or
                                     splitLine[0] == '/control/multiply' or
                                     splitLine[0] == '/control/divide'):
            value = self.parseOperation(splitLine)
            if value is not None:
                newLine = '/control/alias ' + splitLine[1] + " " + str(value) + '\n'
                self.parserAllFiles[file][index] = newLine
        elif len(splitLine) > 0 and splitLine[0] != '/control/verbose' and splitLine[0] != '/control/listAlias':
            print(colorama.Fore.YELLOW + "WARNING: "
                  "Ignored /control command: " + splitLine[0] + colorama.Style.RESET_ALL)

    def parseAlias(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/alias':
            splitLine[2] = self.decriptAlias(splitLine[2])
            splitLine[2] = " ".join(splitLine[2])
            self.parserAlias[splitLine[1]] = splitLine[2]

    def parseCondition(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/strdoif':
            #left condition
            splitLine[1] = self.decriptAlias(splitLine[1])
            splitLine[1] = " ".join(splitLine[1])
            #right condition
            splitLine[3] = self.decriptAlias(splitLine[3])
            splitLine[3] = " ".join(splitLine[3])
            if splitLine[2] == "==":
                if splitLine[1] == splitLine[3]:
                    return splitLine[4:]
            elif splitLine[2] == "!=":
                if splitLine[1] != splitLine[3]:
                    return splitLine[4:]
            else:
                print(colorama.Fore.YELLOW + "WARNING: Not possible to decrypt: " + " ".join(splitLine) + colorama.Style.RESET_ALL)
            return []

    def getMacroFiles(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/execute':
            splitLine[1] = self.decriptAlias(splitLine[1])
            splitLine[1] = " ".join(splitLine[1])
            self.macFiles.append(os.path.join(self.fullMacroDir, splitLine[1]))

    def parseOperation(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/add':
            return self.parseAdd(splitLine)
        elif len(splitLine) > 0 and splitLine[0] == '/control/subtract':
            return self.parseSubtract(splitLine)
        elif len(splitLine) > 0 and splitLine[0] == '/control/multiply':
            return self.parseMultiply(splitLine)
        elif len(splitLine) > 0 and splitLine[0] == '/control/divide':
            return self.parseDivide(splitLine)
        return None

    def parseAdd(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/add':
            splitLine[2] = self.decriptAlias(splitLine[2])
            splitLine[2] = " ".join(splitLine[2])
            splitLine[3] = self.decriptAlias(splitLine[3])
            splitLine[3] = " ".join(splitLine[3])
            value = str(float(splitLine[2]) + float(splitLine[3]))
            self.parserAlias[splitLine[1]] = value
            return value

    def parseSubtract(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/subtract':
            splitLine[2] = self.decriptAlias(splitLine[2])
            splitLine[2] = " ".join(splitLine[2])
            splitLine[3] = self.decriptAlias(splitLine[3])
            splitLine[3] = " ".join(splitLine[3])
            value = str(float(splitLine[2]) - float(splitLine[3]))
            self.parserAlias[splitLine[1]] = value
            return value

    def parseMultiply(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/multiply':
            splitLine[2] = self.decriptAlias(splitLine[2])
            splitLine[2] = " ".join(splitLine[2])
            splitLine[3] = self.decriptAlias(splitLine[3])
            splitLine[3] = " ".join(splitLine[3])
            value = str(float(splitLine[2]) * float(splitLine[3]))
            self.parserAlias[splitLine[1]] = value
            return value

    def parseDivide(self, splitLine):
        if len(splitLine) > 0 and splitLine[0] == '/control/divide':
            splitLine[2] = self.decriptAlias(splitLine[2])
            splitLine[2] = " ".join(splitLine[2])
            splitLine[3] = self.decriptAlias(splitLine[3])
            splitLine[3] = " ".join(splitLine[3])
            value = str(float(splitLine[2]) / float(splitLine[3]))
            self.parserAlias[splitLine[1]] = value
            return value

    def parseAttributes(self, file):
        for index, line in enumerate(self.parserAllFiles[file]):
            if not line.startswith('#') and not line == '\n':
                line = line.strip() #Remove trailing whitespace
                if line.startswith('/gate/application/setTimeStart'):
                    self.parserAttributes["setTimeStart"] = [file, index]
                elif line.startswith('/gate/application/setTimeSlice'):
                    self.parserAttributes["setTimeSlice"] = [file, index]
                elif line.startswith('/gate/application/setTimeStop'):
                    self.parserAttributes["setTimeStop"] = [file, index]
                elif line.startswith('/gate/application/setTotalNumberOfPrimaries'):
                    self.parserAttributes["setTotalNumberOfPrimaries"] = [file, index]

    def setAlias(self, alias, jobs):
        for a in alias:
            self.parserAlias[a[0]] = str(a[1])
            self.aliasToGate[a[0]] = jobs*[str(a[1])]
            self.aliasNumber += 1

    def setAttributes(self, attribute, valuesForAllJobs):
        line = self.parserAllFiles[self.parserAttributes[attribute][0]][self.parserAttributes[attribute][1]]
        line = line.strip() #Remove trailing whitespace
        splitLine = line.split(" ")
        splitLine = [x for x in splitLine if x]
        if not isinstance(valuesForAllJobs[0], list):
            splitLine[1] = '{' + attribute + '_' + str(self.aliasNumber) + '}'
            self.aliasToGate[attribute + '_' + str(self.aliasNumber)] = valuesForAllJobs
            self.aliasNumber += 1
        else:
            for index, value in enumerate(valuesForAllJobs[0]):
                splitLine[index + 1] = '{' + attribute + '_' + str(self.aliasNumber) + '}'
                self.aliasToGate[attribute + '_' + str(self.aliasNumber)] = valuesForAllJobs[:][index]
                self.aliasNumber += 1
        self.parserAllFiles[self.parserAttributes[attribute][0]][self.parserAttributes[attribute][1]] = " ".join(splitLine) + '\n'

    # Return the value of the attribute, not the command
    # Check if containing alias, in such a case, replace it by the alias value if it exist, else raise an error
    def getAttributes(self, attribute):
        line = self.parserAllFiles[self.parserAttributes[attribute][0]][self.parserAttributes[attribute][1]]
        splitLine = self.decriptAlias(line, attribute)
        return splitLine[1:]

    def getAlias(self, alias):
        if not alias in self.parserAlias:
            print(colorama.Fore.RED + "ERROR: alias " + alias + " is not found in macro files" + colorama.Style.RESET_ALL)
            exit(1)
        return self.parserAlias[alias] #Do not return the command and the name of the alias

    def decriptAlias(self, line, attribute=""):
        line = line.strip()
        line = line.split(" ")
        splitLine = []
        for x in line:
            startAliasIndex = x.find('{')
            endAliasIndex = x.find('}')
            if startAliasIndex != -1 and endAliasIndex != 1:
                if startAliasIndex < endAliasIndex:
                    if x[startAliasIndex+1:endAliasIndex] in self.parserAlias:
                        xAlias = x[:startAliasIndex] + self.getAlias(x[startAliasIndex+1:endAliasIndex]) + x[endAliasIndex+1:]
                        splitLine += [xAlias]
                    else:
                        print(colorama.Fore.RED + "ERROR: attribute \"" + x + "\" is an alias " + x[startAliasIndex+1:endAliasIndex] + colorama.Style.RESET_ALL)
                        print(colorama.Fore.RED + "And the alias was not found in macro files" + colorama.Style.RESET_ALL)
                        exit(1)
            elif x:
                splitLine += [x]
        return splitLine

    def writeMacFiles(self, outputDir):
        for file in self.parserAllFiles:
            writtingFile = file[len(self.fullMacroDir):]
            folder = os.path.dirname(os.path.join(outputDir, writtingFile))
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(outputDir, writtingFile), 'w') as f:
                for element in self.parserAllFiles[file]:
                    f.write(element)