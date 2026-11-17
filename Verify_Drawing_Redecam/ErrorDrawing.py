import os


# Catálogo de erros, a ordem aqui é a ordem em que aparecem na resposta
ERRORS = {
    'ER01': 'O nome arquivo não está separado corretamente.',
    'ER02': 'Bloco de Legenda está com código errado.',
    'ER03': 'Bloco de Legenda está com escala errado.',
    'ER04': 'Bloco de Revisão atual está com revisão de pares incorreta.',
    'ER05': 'A Revisão de Pares do Bloco de Revisão 0 deve ser igual ao Bloco de Título.',
    'ER06': 'LTScale está diferente da metade da Escala do Desenho.',
    'ER07': 'Camadas obsoletas presentes no desenho.',
    'ER08': 'Linhas de Chamada ou Cotas não estão na camada QUOTE.',
    'ER09': 'Lista de blocos duplicados identificados no desenho.',
    'ER10': 'Bloco de Revisão 0 está com a Data diferente da Data de Emissão no Bloco de Legenda.',
    'ER11': 'Bloco de Revisão atual está com a Data diferente da Data de Revisão no Bloco de Legenda.',
    'ER12': 'Bloco de Revisão atual não está preenchido.',
    'ER13': 'Bloco de Legenda/Revisão não está com a data informada.',
    'ER14': 'As camadas do desenho não estão configuradas corretamente.',
    'ER15': 'Peso no Bloco de Peça com vírgula.',
    'ER16': 'Bloco de Peça com peso não batendo a multiplicação.',
    'ER17': 'Bloco de Legenda deve estar aprovado em branco.',
    'ER18': 'Nota com Código de Identificação das peças diferente do Código do Desenho.',
    'ER19': 'Bloco de Peça com código incorreto.',
    # 'ER20': 'Nota com Peso Aproximado está diferente da Soma dos Blocos de Peça.',
    'ER21': 'Cota com linha fora do Por Camada.',
    'ER22': 'Cota com escala global incorreta.',
    'ER23': 'Fator de Escala ou Nome da cota incorreta.',
    'ER24': 'Bloco de Formato não está na origem (0,0,0).',
    'ER25': 'Cota com Passo x Quantidade divergente da Dimensão.',
    'ER26': 'Lista de Blocos na escala errada.',
    'ER27': 'Lista de Blocos na versão antiga.',
    'ER28': 'Marcas encontradas no desenho, mas ausente na Lista de Peças.',
    'ER29': 'Bloco de Legenda com descrição no TIT-2 ou TIT-4.',
    'ER30': 'Estilos de fonte de texto inválidos vindos do extraído.',
    'ER31': 'As configurações padrão do desenho estão incorretas. Layer atual deve ser "0" e o estilo de cota deve corresponder à escala do desenho.',
    'ER32': 'Notas do Peso das Peças com peso total divergente da multiplicação.',
    'ER33': 'Notas do Peso das Peças com quantidades divergentes.',
    'ER34': 'Soma dos pesos unitários das Notas do Peso das Peças divergente do peso da Lista de Materiais.',
    'ER35': 'Materiais das notas "SHEET MATERIAL" ou "PROFILES MATERIAL" divergentes da Lista de Materiais.',
    'ER36': 'O desenho contém referências a outro projeto.',
    'ER37': 'Bloco de Legenda com descrição incorreta no TIT-3 para o tipo de documento.',
    'ER38': 'Bloco comercial com código não prenchido ou incorreto.',
    'ER39': 'Bloco comercial preenchido incorretamente.',
    'ER40': 'Bloco de Indicação de Revisão divergente da revisão esperada.',
    'ER41': 'Nuvem de Revisão não está na camada NOTE.',
    'ER42': 'Nuvem de Revisão com comprimento do arco incorreto.',
    'ER43': 'Notas obsoletas presentes no desenho.',
    'ER44': 'Bloco de Legenda com descrições divergentes do projeto.',
    'ALI01': 'Quantidade de peças diverge do número de Marcas no desenho.',
}

# 'ERXX': 'XXXXXXXXX',


class ErrorDrawing:
    def __init__(self):
        self._details = {}

    # Marca o erro como encontrado, opcionalmente com um detalhe (camada, bloco, cota...)
    def add(self, code, detail=None):
        if code not in ERRORS:
            raise KeyError(f'Código de erro desconhecido: {code}')

        details = self._details.setdefault(code, [])

        if detail is not None:
            details.append(str(detail))

    def has(self, code):
        return code in self._details

    def get_errors(self):
        return [
            {
                'code': code,
                'level': 'alert' if code.startswith('ALI') else 'error',
                'message': message,
                'details': list(self._details[code]),
            }
            for code, message in ERRORS.items()
            if code in self._details
        ]

    # Compila as mensagens de erros numa única só string
    def split_message(self, message, limit):
        messages = []

        while len(message) > limit:
            split_index = message.rfind("\n", 0, limit)

            if split_index <= 0:
                split_index = limit
            else:
                split_index += 1

            messages.append(message[:split_index])
            message = message[split_index:]

        if message:
            messages.append(message)

        return messages

    # Formato antigo para o Discord, mantido enquanto o bot não lê o `errors`
    def get_error_messages(self):
        discord_limit = int(os.getenv("DISCORD_LIMIT_PATH_MESSAGE"))

        full_message = ""

        for error in self.get_errors():
            code = error['code']
            label = f"Alert {code[3:]}" if error['level'] == 'alert' else f"Error {code[2:]}"

            full_message += f":lady_beetle: {label}: {error['message']}\n"

            for detail in error['details']:
                full_message += f"\t\t\t{detail}\n"

        if not full_message:
            return []

        return self.split_message(full_message, discord_limit)
