#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam a iniciar a validação dos dados e criação dos dados
# Move os arquivos para um diretório especificado pelo config.cfg
#########################################################################################################

import os
import sys
import magic
import datetime
import utils as csv
import fixfile as fix
import metadata as meta
import send_mail as email
import pandas_access as mdb

# Inicia o Validador
# get_in = Diretório onde os arquivos estão
def start(get_in):
    configuration = os.path.dirname(get_in + '/') + '/config.cfg'
    
    with open(configuration,'r') as configs:   
        for cfg in configs:
            read_files(get_in, cfg)
            if 'location:' in cfg or 'files:' in cfg:
                execute_steps(get_in, cfg)

# Verificar se os arquivos encontrados no diretório estão no cfg
# get_in = Diretório onde os arquivos estão
# cfg = Linha com os parametros usados no processo
def read_files(get_in, cfg):
    for r, _, files in os.walk(get_in, topdown=False):
        for f in files:
            if r == get_in and f in cfg:                
                execute_steps(get_in, cfg, f)


def execute_steps(get_in, cfg, filename = ''):
    positional = []
    columns_name = []
    sheets = []
    cfg = cfg.replace('\n', '')
    log = os.path.dirname(get_in + '/') + '/warns.log'
    with open(log,'a') as warn:  
        type = get_value(cfg, ':', 0)
        if type != 'location' and get_value(cfg, ';', get_parameter(type)) != '': 
            csv.date_format = get_value(cfg, ';', get_parameter(type))
            meta.write_logs(warn, 'INFO', 'Formato de data encontrado para o arquivo ' + filename,'date_format = ' + csv.date_format)               
        if type == 'text' or type == 'positional':
            type_txt(type, cfg, warn, filename, get_in, sheets, positional, columns_name)
        elif type == 'excel':
            type_excel(warn, filename, cfg, get_in, sheets, positional, columns_name)
        elif type == 'access':                
            meta.write_logs(warn, 'INFO', 'Configuração Access encontrada, arquivo ' + filename,'Config - ' + cfg)
            convert_type_to_csv(os.path.join(get_in, filename), sheets=sheets, positional=positional, columns_name=columns_name)
        elif type == 'location':   
            meta.write_logs(warn, 'INFO', 'Configuração de localização encontrada','Config - ' + cfg)
            move_files_csv(warn, get_in, cfg.split(';')[0].split(':')[1])
            meta.write_logs(warn, 'INFO', 'Enviando emails para usuários cadastrados','Config - ' + cfg)
            email.send_email(os.environ['EMAIL_SENDER'], cfg.split(';')[1], os.environ['EMAIL_PASSWORD'])
        else:
            type = ''

def get_value(cfg, delimiter, pos):
    return cfg.split(delimiter)[pos]            

def get_parameter(type):
    return 2 if type == 'text' or type == 'excel' else 1

def type_excel(warn, filename, cfg, get_in, sheets, positional, columns_name):
    meta.write_logs(warn, 'INFO', 'Configuração excel encontrada, arquivo ' + filename,'Config - ' + cfg)
    if cfg.split(';')[0].split(':')[2] != '':
        sheets = cfg.split(';')[0].split(':')[2].split(',')
    convert_type_to_csv(os.path.join(get_in, filename), sheets=sheets, positional=positional, columns_name=columns_name)

def type_txt(type, cfg, warn, filename, get_in, sheets, positional, columns_name):
    if (type == 'positional'):
        positional = cfg.split(';')[0].split(':')[2].split(',')
        columns_name = cfg.split(';')[0].split(':')[3].split(',')
        meta.write_logs(warn, 'INFO', 'Configuração posicional encontrada, arquivo ' + filename,'Config - ' + cfg)
    else: 
        meta.write_logs(warn, 'INFO', 'Configuração texto encontrada, arquivo ' + filename,'Config - ' + cfg)
        fix.search_breakline(os.path.join(get_in, filename))
        meta.write_logs(warn, 'INFO', 'Analisando linhas do arquivo ' + filename,'Analisando e corrigindo quebras de linhas e caracteres especiais.')
    convert_type_to_csv(os.path.join(get_in, filename), sheets=sheets, positional=positional, columns_name=columns_name)


def convert_type_to_csv(get_in, sheets = [], positional = [], columns_name = []):
    try:
        directory = os.path.dirname(get_in) + '/'
        m = magic.Magic()
        file_type = m.from_file(get_in)
        filename = os.path.splitext(os.path.basename(get_in))    
        get_out = filename[0]    
        log = directory + get_out + '_warns.log'
    except:
        with open(log,'a') as warn:   
            meta.write_logs(warn, 'ERROR', 'Leitura de dados','Arquivo não encontrado.')
    prepare_convert(log, file_type, directory, get_out, filename, get_in, positional, columns_name, sheets)

def prepare_convert(log, file_type, directory, get_out, filename, get_in, positional, columns_name, sheets):
    with open(log,'a') as warn:                        
        meta.write_logs(warn, 'INFO', 'Analisando dados ','Iniciando o processo.')
        try:
            if (file_type == 'text/plain'):   
                txt_to_csv(directory, get_out, filename, get_in, warn, file_type, positional, columns_name)
            elif (file_type in ['application/zip', 'application/octet-stream', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']):
                xls_to_csv(directory, get_out, warn, file_type, sheets, get_in)
            elif (file_type == 'application/x-msaccess'):
                accdb_to_csv(directory, get_out, warn, file_type, get_in)
            else:
                meta.write_logs(warn, 'ERROR', 'file_type ' + file_type, 'Tipo não encontrado, verifique se é um arquivo válido')         
        except:
            meta.write_logs(warn, 'ERROR', 'Falha ao exporta arquivo ' + file_type,'erro de leitura do arquivo')

def accdb_to_csv(directory, get_out, warn, file_type, get_in):
    get_out = directory + get_out
    meta.write_logs(warn, 'INFO', 'Arquivo encontrado ' + file_type, 'Formato Micrsoft Access (mdb,accdb).')
    for table in mdb.list_tables(get_in):
        try:
            meta.write_logs(warn, 'INFO', 'Tabela ' + table, 'Tabela encontrado dentro do arquivo.')
            csv.access_to_csv(get_in, get_out, table)                    
            meta.write_logs(warn, 'INFO', 'Chave ùnica criada ' + get_out + '_' + table + '.csv','SHA256(' + meta.md5_hash(get_out + '_temp_' + table + '.csv') + ')')
        except:
            meta.write_logs(warn, 'ERROR','Falha ao exportar tabela ' + table, 'Erro de leitura na tabela')

def xls_to_csv(directory, get_out, warn, file_type, sheets, get_in):
    get_out = directory + get_out 
    meta.write_logs(warn, 'INFO', 'Arquivo encontrado ' + file_type,'Formato Micrsoft Excel (xls,xlsx).')            
    try:
        if sheets != []:
            for sheet in sheets:
                    meta.write_logs(warn, 'INFO', 'Sheet encontrado ' + sheet,'Criando arquivo csv')
                    csv.excel_to_csv(get_in, get_out, sheet)
                    meta.write_logs(warn, 'INFO', 'Chave ùnica criada ' + get_out + '_' + sheet + '.csv','SHA256(' + meta.md5_hash(get_out + '_' + sheet + '.csv') + ')')
        else:
            meta.write_logs(warn, 'INFO','Arquivo sem sheets', 'Fazendo leitura do excel.')
            csv.excel_to_csv(get_in, get_out)
            meta.write_logs(warn, 'INFO', 'Chave ùnica criada ' + get_out + '.csv','SHA256(' + meta.md5_hash(get_out + '.csv') + ')')
    except:
        meta.write_logs(warn, 'ERROR','Falha ao exportar sheet ' + sheet, 'Erro de leitura do excel.')

def txt_to_csv(directory, get_out, filename, get_in, warn, file_type, positional, columns_name):
    get_out = directory + get_out + '.csv'                
    if(filename[1] =='.csv'):
        os.rename(get_in, get_in.replace('csv', 'txt'))
        get_in = get_in.replace('csv', 'txt')
    meta.write_logs(warn, 'INFO', 'Arquivo encontrado' + file_type,'Formato texto plano (txt,csv,tsv).')
    if positional != []:
        meta.write_logs(warn, 'INFO', 'Arquivo posicional encontrado','Padrão ' + str(positional) + '.') 
    meta.write_logs(warn, 'INFO', 'Remoção caracteres especiais','Quebras de linha e delimitador em local incorreto.')                                
    csv.txt_to_csv(get_in, get_out, meta.detect_delimiter(meta.get_head(get_in), positional), columns_name)                
    meta.write_logs(warn, 'INFO','Chave criada ' + get_out, 'SHA256(' +meta. md5_hash(get_out) + ')')


def move_files_csv(warn, get_in, s3_location):
    s3_location = s3_location + '/'
    try:
        now = datetime.datetime.now()
        location_raw = s3_location.replace(' ', '')
        for tutorial in ['cadastro', 'faturamento', 'sinistro']:
            location_root = os.path.join(s3_location, tutorial).replace(' ', '')
            location = os.path.join(location_root, os.path.join(os.path.join('year=' + str(now.year)), 'month=' + str(now.month))).replace(' ', '')
            os.makedirs(location, exist_ok=True)
        verify_file_to_move(get_in, warn, location_raw)
        return location_raw + '/warns.log'
    except:
        meta.write_logs(warn, 'ERROR', 'Movimentação de arquivos','Erro ao mover arquivos.')
        return get_in + '/warns.log'

def verify_file_to_move(get_in, warn, location_raw):
    for r, _, files in os.walk(get_in, topdown=False):
        for f in files:
            if ('.csv' in f or '.schema' in f or '_warns' in f or '.original' in f) and r == get_in:
                if '_temp' in f: # or ('.txt' in f and '.original' not in f):
                    meta.write_logs(warn, 'WARN', 'Arquivo temporário removido', 'Arquivo removido ' + get_in + f + '.')
                    os.remove(get_in + f)                            
                else:
                    meta.write_logs(warn, 'INFO', 'Movimentação de arquivos', 'Arquivo movido de ' + get_in + f + ' para ' + location_raw + f + '.')
                    os.rename(get_in + f, location_raw + f)


def main():
    print('Iniciando processo de validação dos arquivos, saída no diretório' + sys.argv[1] )
    start(sys.argv[1])
    print('Processo finalizado nos arquivos do diretório ' + sys.argv[1])

if __name__ == "__main__":
    main()