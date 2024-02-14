class errorDrawing: 
    def __init__(self):
        self.ed01 = {'description': ':lady_beetle: [Error ED01:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207338757049815110) O nome arquivo não está separado corretamente.','booleanValue': False }
        self.ed02 = {'description': ':lady_beetle: [Error ED02:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207339702152200215) Bloco de Legenda está com código errado.','booleanValue': False }
        self.ed03 = {'description': ':lady_beetle: [Error ED03:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207342449450553445) Bloco de Lengenda está com SCALA errado.','booleanValue': False }
        self.ed04 = {'description': ':lady_beetle: [Error ED04:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207343645406003311) Bloco de Lengenda está com DRAW, CHECKED ou APPROVED errado.','booleanValue': False }
        self.ed05 = {'description': ':lady_beetle: [Error ED05:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207355422072377344) Bloco de Revisão está com escala errado.','booleanValue': False }
        self.ed06 = {'description': ':lady_beetle: [Error ED06:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207356045186301983) LTScale está errado.','booleanValue': False }
        self.ed07 = {'description': ':lady_beetle: [Error ED07:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207358295304708148) Layer CONTOUR EXI está presente no Desenho','booleanValue': False }
        self.edOB = {'description': ':lady_beetle: [Error EDOB:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207359201446207538) Lista de Blocos na versão antiga:\n','booleanValue': False }

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
                

