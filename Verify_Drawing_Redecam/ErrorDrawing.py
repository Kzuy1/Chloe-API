class ErrorDrawing: 
    def __init__(self):
        self.er01 = {'description': ':lady_beetle: Error 01: O nome arquivo não está separado corretamente.','boolean_value': False }
        self.er02 = {'description': ':lady_beetle: Error 02: Bloco de Legenda está com código errado.','boolean_value': False }
        self.er03 = {'description': ':lady_beetle: Error 03: Bloco de Legenda está com escala errado.','boolean_value': False }
        self.er04 = {'description': ':lady_beetle: Error 04: Bloco de Revisão atual está com revisão de pares incorreta.','boolean_value': False }
        self.er05 = {'description': ':lady_beetle: Error 05: A Revisão de Pares do Bloco de Revisão 0 deve ser igual ao Bloco de Título.','boolean_value': False }
        self.er06 = {'description': ':lady_beetle: Error 06: LTScale está diferente da metade da Escala do Desenho.','boolean_value': False }
        self.er07 = {'description': ':lady_beetle: Error 07: Camadas obsoletas presentes no desenho:\n','boolean_value': False }
        self.er08 = {'description': ':lady_beetle: Error 08: Linha de Chamada não está na camada QUOTE.','boolean_value': False }
        self.er09 = {'description': ':lady_beetle: Error 09: Lista de blocos duplicados identificados no desenho:','boolean_value': False }
        self.er10 = {'description': ':lady_beetle: Error 10: Bloco de Revisão 0 está com a Data diferente da Data de Emissão no Bloco de Legenda.','boolean_value': False }
        self.er11 = {'description': ':lady_beetle: Error 11: Bloco de Revisão atual está com a Data diferente da Data de Revisão no Bloco de Legenda.','boolean_value': False }
        self.er12 = {'description': ':lady_beetle: Error 12: Bloco de Revisão atual não está preenchido.','boolean_value': False }
        self.er13 = {'description': ':lady_beetle: Error 13: Bloco de Legenda/Revisão não está com data de ','boolean_value': False }
        self.er14 = {'description': ':lady_beetle: Error 14: As camadas do desenho não estão configuradas corretamente.','boolean_value': False }
        self.er15 = {'description': ':lady_beetle: Error 15: Peso no Bloco de Peça com vírgula.','boolean_value': False }
        self.er16 = {'description': ':lady_beetle: Error 16: Bloco de Peça com peso não batendo a multiplicação.','boolean_value': False }
        self.er17 = {'description': ':lady_beetle: Error 17: Bloco de Legenda deve estar aprovado em branco.','boolean_value': False }
        self.er18 = {'description': ':lady_beetle: Error 18: Nota com Código de Identificação das peças diferente do Código do Desenho.','boolean_value': False }
        self.er19 = {'description': ':lady_beetle: Error 19: Bloco de Peça com código incorreto.','boolean_value': False }
        # self.er20 = {'description': ':lady_beetle: Error 20: Nota com Peso Aproximado está diferente da Soma dos Blocos de Peça, correto: ','boolean_value': False }
        self.er21 = {'description': ':lady_beetle: Error 21: Cota com linha fora do Por Camada:\n','boolean_value': False }
        self.er22 = {'description': ':lady_beetle: Error 22: Cota com escala global incorreta:\n','boolean_value': False }
        self.er23 = {'description': ':lady_beetle: Error 23: Fator de Escala ou Nome da cota incorreta:\n','boolean_value': False }
        self.er24 = {'description': ':lady_beetle: Error 24: Bloco de Formato não está na origem (0,0,0).','boolean_value': False }
        self.er25 = {'description': ':lady_beetle: Error 25: Cota com Passo x Quantidade divergente da Dimensão.','boolean_value': False }
        self.er26 = {'description': ':lady_beetle: Error 26: Lista de Blocos na escala errada:\n','boolean_value': False }
        self.er27 = {'description': ':lady_beetle: Error 27: Lista de Blocos na versão antiga:\n','boolean_value': False }
        self.er28 = {'description': ':lady_beetle: Error 28: Marcas encontradas no desenho, mas ausente na Lista de Peças:\n','boolean_value': False }
        self.er29 = {'description': ':lady_beetle: Error 29: Bloco de Legenda com descrição no TIT-2 ou TIT-4.','boolean_value': False }
        self.er30 = {'description': ':lady_beetle: Error 30: Estilos de fonte de texto inválidos vindos do extraído.','boolean_value': False }
        self.er31 = {'description': ':lady_beetle: Error 31: As configurações padrão do desenho estão incorretas. Layer atual deve ser "0" e o estilo de cota deve corresponder à escala do desenho.','boolean_value': False }
        self.er32 = {'description': ':lady_beetle: Error 32: Notas do Peso das Peças com peso total divergente da multiplicação','boolean_value': False }
        self.er33 = {'description': ':lady_beetle: Error 33: Notas do Peso das Peças com quantidades divergentes.','boolean_value': False }
        self.er34 = {'description': ':lady_beetle: Error 34: Soma dos pesos unitários das Notas do Peso das Peças divergente do peso da Lista de Materiais.','boolean_value': False }
        self.er35 = {'description': ':lady_beetle: Error 35: Materiais das notas "SHEET MATERIAL" ou "PROFILES MATERIAL" divergentes da Lista de Materiais.','boolean_value': False }
        self.al01 = {'description': ':lady_beetle: Alert 01: Quantidade de peças diverge do número de Marcas no desenho:\n','boolean_value': False }

    # self.erXX = {'description': ':lady_beetle: Error XX: XXXXXXXXX','boolean_value': False }
        
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
                    
        if string_message:  # Adiciona a última mensagem apenas se não estiver vazia
            string_error.append(string_message)

        return string_error if string_error else []