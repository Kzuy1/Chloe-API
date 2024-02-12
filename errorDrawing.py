class errorDrawing: 
    def __init__(self):
        self.ed01 = {'description': ':lady_beetle: [Error ED01:]() O arquivo não está separado corretamente.','booleanValue': False }
        self.ed02 = {'description': ':lady_beetle: [Error ED02:]() Bloco de Lengenda está com código errado.','booleanValue': False }
        self.ed03 = {'description': ':lady_beetle: [Error ED03:]() Bloco de Lengenda está com SCALA errado.','booleanValue': False }
        self.ed04 = {'description': ':lady_beetle: [Error ED04:]() Bloco de Lengenda está com DRAW errado.','booleanValue': False }
        self.ed05 = {'description': ':lady_beetle: [Error ED05:]() Bloco de Revisão está com SCALA errado.','booleanValue': False }
        self.ed06 = {'description': ':lady_beetle: [Error ED06:]() LTScale está errado.','booleanValue': False }
        self.edLA = {'description': ':lady_beetle: [Error EDLA:]() Lista de Layers errada:\n','booleanValue': False }
        self.edOB = {'description': ':lady_beetle: [Error EDOB:]() Lista de Blocos na versão antiga:\n','booleanValue': False }

    # Compila as mensagens de erros numa única só string
    def getErrorMessages(self):
        stringError = []
        stringMessage = ''

        for error in self.__dict__.items():
            if error[1]['booleanValue']:
                messageError = error[1]['description']
                if len(messageError) > 3999:
                    stringError.append(stringMessage)
                    stringMessage = messageError
                else:
                    stringMessage += messageError
        stringError.append(stringMessage)

        return stringError
                

