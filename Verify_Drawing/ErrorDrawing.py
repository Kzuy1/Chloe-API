class ErrorDrawing: 
    def __init__(self):
        self.ed01 = {'description': ':lady_beetle: [Error ED01:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed01>) O nome arquivo não está separado corretamente.','boolean_value': False }
        self.ed02 = {'description': ':lady_beetle: [Error ED02:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed02>) Bloco de Legenda está com código errado.','boolean_value': False }
        self.ed03 = {'description': ':lady_beetle: [Error ED03:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed03>) Bloco de Legenda está com escala errado.','boolean_value': False }
        self.ed04 = {'description': ':lady_beetle: [Error ED04:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed04>) Bloco de Legenda está com DES., VERIF. ou APROV. errado.','boolean_value': False }
        # self.ed05 = {'description': ':lady_beetle: [Error ED05:](<https://docs.embrateceng.com.br/chloe/erros-de-desenho#error-ed05>) Bloco de Revisão está com escala errado.','boolean_value': False }
        self.ed06 = {'description': ':lady_beetle: [Error ED06:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed06>) LTScale está diferente da metade da Escala do Desenho.','boolean_value': False }
        self.ed07 = {'description': ':lady_beetle: [Error ED07:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed07>) Camadas obsoletas presentes no desenho:\n','boolean_value': False }
        self.ed08 = {'description': ':lady_beetle: [Error ED08:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed08>) Linha de Chamada não está na camada COTAS.','boolean_value': False }
        self.ed09 = {'description': ':lady_beetle: [Error ED09:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed09>) Deve ter apenas um Bloco de Legenda no mesmo desenho.','boolean_value': False }
        self.ed10 = {'description': ':lady_beetle: [Error ED10:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed10>) Bloco de Revisão 0 está com a Data diferente da Data de Emissão no Bloco de Legenda.','boolean_value': False }
        self.ed11 = {'description': ':lady_beetle: [Error ED11:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed11>) Bloco de Revisão atual está diferente da Data de Revisão no Bloco de Legenda.','boolean_value': False }
        self.ed12 = {'description': ':lady_beetle: [Error ED12:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed12>) Bloco de Revisão atual não preenchido.','boolean_value': False }
        self.ed13 = {'description': ':lady_beetle: [Error ED13:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed13>) Bloco de Legenda/Revisão não está com data de ','boolean_value': False }
        self.ed14 = {'description': ':lady_beetle: [Error ED14:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed14>) As camadas do desenho não estão configuradas corretamente.','boolean_value': False }
        self.ed15 = {'description': ':lady_beetle: [Error ED15:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed15>) Peso no Bloco de Peça com vírgula.','boolean_value': False }
        self.ed16 = {'description': ':lady_beetle: [Error ED16:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed16>) Bloco de Peça com peso não batendo a multiplicação.','boolean_value': False }
        self.ed17 = {'description': ':lady_beetle: [Error ED17:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed17>) Bloco de Peca com vírgula na descrição.','boolean_value': False }
        self.ed18 = {'description': ':lady_beetle: [Error ED18:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed18>) Nota com Código de Identificação das peças diferente do Código do Desenho.','boolean_value': False }
        self.ed19 = {'description': ':lady_beetle: [Error ED19:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed19>) Fator de Largura do atributo Marca no  Bloco de Peça diferente de 0,7.','boolean_value': False }
        self.ed20 = {'description': ':lady_beetle: [Error ED20:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed20>) Nota com Peso Aproximado está diferente da Soma dos Blocos de Peça, correto: ','boolean_value': False }
        self.ed21 = {'description': ':lady_beetle: [Error ED21:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed21>) Cota com linha fora do Por Camada:\n','boolean_value': False }
        self.ed22 = {'description': ':lady_beetle: [Error ED22:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed22>) Cota com escala global incorreta:\n','boolean_value': False }
        self.ed23 = {'description': ':lady_beetle: [Error ED23:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed23>) Fator de Escala ou Nome da cota incorreta:\n','boolean_value': False }
        self.edOB = {'description': ':lady_beetle: [Error EDOB:](<https://docs.satusequipamentos.com.br/docs/chloe/erros-de-desenho#error-ed0b>) Lista de Blocos na versão antiga:\n','boolean_value': False }
        self.edSC = {'description': ':lady_beetle: [Error EDSB:](<>) Lista de Blocos na escala errada:\n','boolean_value': False }

    # self.edXX = {'description': ':lady_beetle: [Error EDXX:](<>) XXXXXXXXX','boolean_value': False }
        
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