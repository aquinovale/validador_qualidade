#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam na correção e validação dos arquivos
#########################################################################################################

import os
import metadata as meta


# Busca se o arquivo possui os campos obrigatórios para aceitar o arquivo como válido.
# Recebe como argumentos
# get_in = Diretório de onde fica os arquivos necessários 
# fields_required = Lista de nome de campos que são obrigatórios
def required_fields(get_in, fields_required = []): 
    log = os.path.dirname(get_in) + '/' + os.path.splitext(os.path.basename(get_in))[0].replace('_temp', '') + '_warns_fields.log'
    with open(log,'a+') as warn: 
        result = False
        try:
            if fields_required != [] and fields_required != ['']:
                heads = meta.get_head(get_in)
                meta.write_logs(warn, 'INFO', 'Campos obrigatórios' ,'Campos obrigatórios definidos - ' + ','.join(fields_required))
                for field in fields_required:
                    if meta.clean_metadata(';' + field) in heads:
                        meta.write_logs(warn, 'INFO', 'Campo obrigatório encontrado' ,'Campo obrigatório - ' + field)
                        result = True
                    else:    
                        meta.write_logs(warn, 'ERROR', 'Campo obrigatório não encontrado' ,'Campo obrigatório - ' + field)
                        result = False
                meta.write_logs(warn, 'INFO', 'Campos obrigatórios' ,'Busca por campos obrigatórios finalizado.')                    
        except:                
            meta.write_logs(warn, 'ERROR', 'Campos obrigatórios' ,'Falha ao identificar campos obrigatórios.')                                
    return result            

# Abre o arquivo e faz a busca por problemas na linha
# Recebe como argumentos
# get_in = Diretório de onde fica os arquivos necessários 
def search_breakline(get_in):
    directory = os.path.dirname(get_in) + '/'
    filename = os.path.splitext(os.path.basename(get_in))    
    log = directory + filename[0] + '_warns.log'
    with open(log,'a+') as warn:                        
        headline = meta.get_head(get_in)
        meta.write_logs(warn, 'INFO', 'Fazendo validação final no arquivo', 'Iniciando a analise do arquivo - ' + os.path.basename(get_in))
        os.rename(get_in, get_in + '.original')
        meta.write_logs(warn, 'INFO', 'Renomeando arquivo original', 'Renomeando arquivo para ' + os.path.basename(get_in) + '.original')
        meta.write_logs(warn, 'INFO','Chave criada para arquivo original ' + os.path.basename(get_in) + '.original','SHA256(' + meta.md5_hash(get_in + '.original') + ').')
        analyze_and_fix_line(get_in, warn, headline)
        meta.write_logs(warn, 'INFO', 'Fazendo validação final no arquivo', 'Processo finalizado.')

# Renomeia o arquivo original para .original
# Cria um arquivo novo com as correções da linha, se houver
# Recebe como argumentos
# get_in = Diretório de onde fica os arquivos necessários 
# warn = Variável de criação de Logs
# headline = Cabeçalho do arquivo, com os campos.
def analyze_and_fix_line(get_in, warn, headline):
    with open(get_in  + '.original', 'rt') as file:
        with open(get_in, 'w') as fix_file:
            lastline = ''
            i = 1
            for line in file:
                if i == 1:
                    fix_file.write(headline + '\n')
                else:
                    if (analize_line(warn, i, line, headline)):
                        lastline = fix_line(warn, i, line, lastline, headline)
                        if not (analize_line(warn, i, lastline, headline, log = False)):
                            meta.write_logs(warn, 'INFO', 'Correção das linhas', 'Tentativa de correção das linhas, descritas acima.')
                            fix_file.write(lastline.replace('"', '').strip() + '\n')  
                            lastline = ''
                    else:
                        fix_file.write(line.replace('"', '').strip() + '\n')
                i += 1


# Analiza a linha para ver se possui a quantidade esperada de campos
# Recebe como argumentos
# get_in = Diretório de onde fica os arquivos necessários 
# warn = Variável de criação de Logs
# headline = Cabeçalho do arquivo, com os campos
# log = Que ativa o log se for ativado
def analize_line(warn, i, line, headline, log = True):
    linecount = len(line.split(';'))
    headcount = len(headline.split(';'))
    if(linecount == headcount): 
        return False
    else:
        if log:
            meta.write_logs(warn, 'WARN', 'Diferença de colunas encontrado na linha - ' + str(i), 'Cabeçalho com ' + str(headcount) + ' colunas, encontrado ' + str(linecount) + '.')
        return True

# Corrigi a linha que tiver menos campos do que esperado
# Recebe como argumentos
# warn = Variável de criação de Logs
# i = Posição da linha no arquivo
# headline = Cabeçalho do arquivo, com os campos
def fix_line(warn, i, line, lastline, headline):
    if line != lastline :
        linecount = len(line.split(';')) + len(lastline.split(';')) -1 if lastline != '' else len(line.split(';'))
        headcount = len(headline.split(';'))
        if (linecount != headcount):
            if (linecount > headcount):
                meta.write_logs(warn, 'ERROR', 'Impossível corrigir a linha - ' + str(i), 'Esperado ' + str(headcount) + ' colunas, encontrado ' + str(linecount) + '. Linha será removida.')
                return ''
            else:
                return (lastline + line).replace('\n', '')
        else:
            return (lastline + line).replace('\n', '')
    return line