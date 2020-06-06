#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam leitura do cabeçalho, criação de SHA256 e detecção de delimitadores
# Logo da empresa em formato base64
#########################################################################################################

import re
import string
import hashlib
import datetime
from unidecode import unidecode

BLOCKSIZE = 1024*1024

#Retorna o cabeçalho do arquivo removendo caracteres especiais
# get_in = Diretório de onde está o arquivo para ser ingerido
def get_head(get_in):  
    with open(get_in, 'r') as f:
        line = f.readline().replace('\r\n', '').replace('\n', '').lower()
        return clean_metadata(line)

def clean_metadata(line):
    try:
        delimiter = detect_delimiter(line) 
        regex = '\\' + delimiter + '[0-9]+'
        special_chars = re.escape(string.punctuation.replace('|', '').replace(';', '').replace('_', ''))
        line_clean = unidecode(re.sub('[' + special_chars + ']', '', line)).replace('\'','').replace(' ', '_').lower()
        return re.sub(regex, delimiter, line_clean)
    except:
        return line    

# Retorna a chave SHA256 do arquivo analisado.
# get_in = Diretório de onde está o arquivo para ser ingerido
def md5_hash(get_in):
    chave = hashlib.sha256()
    with open(get_in, 'rb') as f:
        while True:
            data = f.read(BLOCKSIZE)
            if not data: break
            chave.update(data)
    return chave.hexdigest()

# Detecta o delimitador usado na separação do arquivo
# line = Recebe a linha a ser verificada o delimitador
# positional = Recebe as posições caso seja um arquivo posicional
def detect_delimiter(line, positional = []):
    try:
        PATTERN = '([;|\t|\\|])'  # define os possiveis delimitadores
        return (re.search(PATTERN, line)).group() if positional == [] else positional
    except:
        #return positional
        return ''

# Identifica os tipos dos dados
# dtypes = Tipagem vinda do DataFrame
def get_dtype(dtypes):
    line = ''
    lines = []
    odd = False
    for dtype in dtypes.to_string().split():
        line = line + ':' + dtype if line != '' else dtype
        if odd:
            lines.append(line)        
            line = ''
        odd = not odd
    return lines

# Escreve as informações do metadata do dado
# dtypes = Tipagem vinda do DataFrame
# metadata = Local onde será gravado as informações sobre o metadado
def write_metadata(dtypes, metadata):
    with open(metadata,'w') as meta:                        
        for campo in get_dtype(dtypes):
            meta.write(campo + '\n')

# Escreve as informações do metadata do dado
# warn = Local onde será gravado as informações sobre o log
# tipo_erro = Tipo do erro
# erro = Exceção do erro
# msg = Msg de erro encontrado
def write_logs(warn, tipo_erro, erro, msg, debug = False):    
    delimiter = ':'
    if debug:
        warn.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' DEBUG' + delimiter + erro + delimiter + msg + '\n')
    else:
        warn.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + tipo_erro + delimiter + erro + delimiter + msg + '\n')


def get_logo():
    return 'data:image/png;base64,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'