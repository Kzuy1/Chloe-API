class ErrorDrawing: 
    def __init__(self):
        self.ed01 = {'description': ':lady_beetle: [Error ED01:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207338757049815110) O nome arquivo não está separado corretamente.','boolean_value': False }
        self.ed02 = {'description': ':lady_beetle: [Error ED02:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207339702152200215) Bloco de Legenda está com código errado.','boolean_value': False }
        self.ed03 = {'description': ':lady_beetle: [Error ED03:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207342449450553445) Bloco de Legenda está com SCALA errado.','boolean_value': False }
        self.ed04 = {'description': ':lady_beetle: [Error ED04:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207343645406003311) Bloco de Legenda está com DRAW, CHECKED ou APPROVED errado.','boolean_value': False }
        # self.ed05 = {'description': ':lady_beetle: [Error ED05:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207355422072377344) Bloco de Revisão está com escala errado.','boolean_value': False }
        self.ed06 = {'description': ':lady_beetle: [Error ED06:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207356045186301983) LTScale está errado.','boolean_value': False }
        self.ed07 = {'description': ':lady_beetle: [Error ED07:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207358295304708148) Layer CONTOUR EXI está presente no Desenho.','boolean_value': False }
        self.ed08 = {'description': ':lady_beetle: [Error ED08:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217544751272693860) Linha de Chamada não está na camada QUOTE.','boolean_value': False }
        self.ed09 = {'description': ':lady_beetle: [Error ED09:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217546052631003216) Deve ter apenas um Bloco de Legenda no mesmo desenho.','boolean_value': False }
        self.ed10 = {'description': ':lady_beetle: [Error ED10:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217547272284274749) Bloco de Revisão 0 está com a Data diferente da Data de Emissão no Bloco de Legenda.','boolean_value': False }
        self.ed11 = {'description': ':lady_beetle: [Error ED11:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217552948385550427) Bloco de Revisão atual está diferente da Data de Revisão no Bloco de Legenda.','boolean_value': False }
        self.ed12 = {'description': ':lady_beetle: [Error ED12:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217555347217186969) Blocos de Revisões não preenchido.','boolean_value': False }
        self.ed13 = {'description': ':lady_beetle: [Error ED13:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217557431421501521) Bloco de Legenda não está com data de ','boolean_value': False }
        self.ed14 = {'description': ':lady_beetle: [Error ED14:](https://discord.com/channels/1122685290205679748/1207328035108298804/1218257763537391696) As camadas do desenho não estão configuradas corretamente.','boolean_value': False }
        self.edSC = {'description': ':lady_beetle: [Error EDSB:](https://discord.com/channels/1122685290205679748/1207328035108298804/1217558592119378030) Lista de Blocos na escala errada:\n','boolean_value': False }
        self.edOB = {'description': ':lady_beetle: [Error EDOB:](https://discord.com/channels/1122685290205679748/1207328035108298804/1207359201446207538) Lista de Blocos na versão antiga:\n','boolean_value': False }

    # self.edXX = {'description': ':lady_beetle: [Error EDXX:]() XXXXXXXXX','boolean_value': False }
        
    # Compila as mensagens de erros numa única só string
    def get_error_messages(self):
        string_error = []
        string_message = ''

        for error in self.__dict__.items():
            if error[1]['boolean_value']:
                message_error = error[1]['description']
                if len(message_error) > 3999:
                    string_error.append(string_message)
                    string_message = message_error
                else:
                    string_message += message_error + "\n"
        string_error.append(string_message)

        return string_error