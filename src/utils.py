#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam na conversão para csv
# Cria o profiling de qualidade dos dados
# Traduz de English para Português
#########################################################################################################

import os
import pandas as pd
import fixfile as fix
import pandas_profiling
import metadata as meta   
import pandas_access as mdb

date_format = '%d/%m/%Y %H:%M:%S'

# Cria o profiling dos dados para qualidade
# get_in = Diretório de onde os dados estão
# df = DataFrame do dado lido
# run = Se é para rodar ou não o profiling
def create_profiling(get_in, df, run = False, json = False):
    if run:
        directory = os.path.dirname(get_in) + '/'
        filename = os.path.splitext(os.path.basename(get_in))    
        new_file = directory + filename[0] + '_en.html'
        profile = df.profile_report(title=filename[0],plot={'histogram': {'bayesian_blocks_bins': False,
                                                'bins': 10}})
        profile.set_variable("html.style.logo", meta.get_logo())
        #profile.set_variable("html.inline", False)
        profile.set_variable("html.style.theme", 'flatly')
        profile.to_file(output_file=new_file + '' if not json else '.json')
        #translate_language(new_file)

# Faz a tradução do html gerado de ingles para portugues
# get_in = Diretório de onde os dados estão
def translate_language(get_in):
    html = ''
    with open(get_in, 'r') as html_en:
        html = html_en.read()
        with open('traduzido-en', 'r') as en:
            traduzido_en = en.read().split('\n')
        with open('traduzido-br', 'r') as br:
            traduzido_br = br.read().split('\n')
        for i in range(0, len(traduzido_br)):
            html = html.replace(traduzido_en[i], traduzido_br[i])

    with open(get_in.replace('_en', '_br'), 'w') as html_br:
        html_br.write(html) 

# Faz a leitura dos arquivo de config para pegar os campos obrigatórios que precisam ser avaliados
# get_in = Diretório de onde os dados estão
def read_required_fields(get_in):
    configuration = os.path.dirname(get_in) + '/config.cfg'
    filename = os.path.splitext(os.path.basename(get_in))[0].replace('_temp', '')
    with open(configuration,'r') as configs:   
        for cfg in configs:
            cfg = cfg.replace('\n', '')
            if 'location:' not in cfg and cfg != '' and ('text:' in cfg or 'excel:' in cfg):
                if filename in cfg:
                    return cfg.split(';')[1].split(',')
    return []

# Faz a identificação do data type do dataframe
# get_in = Diretório de onde os dados estão 
# delimiter = Recebe o delimitador usado na leitura do arquivo
# columns = Lista com as colunas que serão analisada para o tipo datetime
def identify_datatypes(get_in, delimiter, columns = []):
    log = os.path.dirname(get_in) + '/' + os.path.splitext(os.path.basename(get_in))[0] + '_warns.log'
    with open(log,'a+') as warn:                                
        column = []
        for col in columns:
            col_name, col_dtype = col.split(':')[0:2]
            if 'datetime' in col_dtype:
                meta.write_logs(warn, 'INFO','Campo data encontrado ' + col_name, 'Campo datetime encontrado -' + col_name + ' ' + col_dtype)
                column.append(col_name)
        df = pd.read_csv(get_in , sep=delimiter, encoding='utf-8', infer_datetime_format = True, parse_dates = column).replace('\r?\n', ' ', regex=True).replace(delimiter, ' ', regex=True)
    meta.write_metadata(df.dtypes, os.path.dirname(get_in) + '/' + os.path.splitext(os.path.basename(get_in))[0].replace('_temp', '') + '_metadata.schema')    
    return df

# Converte o texto para csv
# get_in = Diretório de onde os dados estão 
# get_out = Diretório de onde os dados vão ser salvos
# delimiter = Recebe o delimitador usado na leitura do arquivo
# columns_name = Lista com nome das colunas que são usadas pelo posicional
def txt_to_csv(get_in, get_out, delimiter, columns_name = []):
    if columns_name == []:
        df = pd.read_csv(get_in, sep=delimiter, encoding='utf-8', infer_datetime_format = True, parse_dates = meta.get_head(get_in).split(delimiter)).replace('\r?\n', ' ', regex=True).replace(delimiter, ' ', regex=True)
        df = identify_datatypes(get_in, delimiter, meta.get_dtype(df.dtypes))        
        df.to_csv(get_out, encoding='utf-8', index = False, header = True, sep = ';', date_format = date_format)  
        fix.required_fields(get_out, read_required_fields(get_in))
        try:            
            create_profiling(get_out, df, True)
        except:
            log = os.path.dirname(get_in) + '/' + os.path.splitext(os.path.basename(get_in))[0] + '_warns.log'
            with open(log,'a+') as warn: 
                meta.write_logs(warn, 'ERROR','txt_to_csv - Montagem de profiling', 'Erro ao montar profiling.')
    else:        
        positional_to_csv(get_in, get_out, delimiter, columns_name)    

# Converte posicional para csv
# get_in = Diretório de onde os dados estão 
# get_out = Diretório de onde os dados vão ser salvos
# positional = Recebe as posições do arquivo posicional
# columns_name = Lista com nome das colunas que são usadas pelo posicional
def positional_to_csv(get_in, get_out, positional = [], columns_name = []):
    get_old = os.path.dirname(get_out) + '/' + os.path.splitext(os.path.basename(get_in))[0]    
    df = pd.read_fwf(get_in , widths = positional, names = columns_name, encoding ='utf-8')
    df.to_csv(get_old + '_temp.csv', encoding = 'utf-8', index = False, header = True, sep = ';', date_format = date_format)  
    txt_to_csv(get_old + '_temp.csv', get_out, ';')


# Converte access para csv
# get_in = Diretório de onde os dados estão 
# get_out = Diretório de onde os dados vão ser salvos
# table = nome da tabela a ser convertida 
def access_to_csv(get_in, get_out, table):
    df = mdb.read_table(get_in, table)
    df.columns = [ meta.clean_metadata(x.lower()) for x in df.columns]  
    df.to_csv(get_out + '_temp_' + table + '.csv', date_format=date_format, encoding='utf-8', index = False, header = True, sep = ';')
    txt_to_csv(get_out + '_temp_' + table + '.csv', get_out + '_' + table + '.csv', ';')

# Converte excel para csv
# get_in = Diretório de onde os dados estão 
# get_out = Diretório de onde os dados vão ser salvos
# sheet = Nome da aba a ser convertida
def excel_to_csv(get_in, get_out, sheet = ''):
    original = sheet
    if sheet != '':
        df = pd.read_excel(get_in, sheet_name=sheet).replace('\r?\n', ' ', regex = True).replace(';', ' ', regex = True)                
        sheet = '_temp_' + sheet + '.csv'
        original = '_' + original
    else:
        df = pd.read_excel(get_in).replace('\r?\n', ' ', regex = True).replace(';', ' ', regex = True)                
        sheet = '_temp.csv'
    df.columns = [ meta.clean_metadata(x.lower()) for x in df.columns]  
    df.to_csv(get_out + sheet, encoding='utf-8', date_format=date_format, index = False, header = True, sep = ';')
    txt_to_csv(get_out + sheet, get_out + original + '.csv', ';')
