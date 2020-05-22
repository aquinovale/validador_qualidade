## Objetivo

O validador tem o objetivo de ajudar na analise inicial dos arquivos em texto plano, Microsoft Excel e Microsoft Access. O validador lê o arquivo original, verifica se o mesmo tem campos obrigatórios, corrige possíveis quebras de linhas, remove caracteres especiais, e espaços em branco. Também gera SHA256 do arquivo original e do arquivo final criado. 

O sistema identifica os cabeçalhos automaticamente, reconhece possiveis tipos e gera arquivos com informações do que foi identificado, também é criado um relatório em formato HTML em inglês e português com a qualidade dos dados encontrados.

No final do processo os dados são enviados para um diretório especificado, e envia email avisando aos responsáveis.


## Rodar o validador

Basta chamar o start.py diretorio/


Ex: python3.7 start.py /home/vinicius/git/validador-qualidade/


## Arquivo config.cfg

O arquivo config.cfg armazena as configurações do que é esperado para ser consumido pelo validador. Ele foi desenvolvido para ser flexível para ler vários arquivos de layouts diferentes de uma maneira simples, porém nada impede de ser usado por grupo de arquivos.

### Exemplo arquivo config.cfg

	text:latin1.txt;FirstNadme,Country;%d/%m/%Y %H:%M:%S
	positional:posicional.txt:14,13,3:data,nome,valor;%d/%m/%Y
	excel:excel.xlsx:tabela_a,tabela_b;;%d/%m/%Y %H:%M:%S
	access:access.accdb,access2.mdb;
	location:/home/vinicius/git/validador-qualidade/output;aquino.vale@gmail.com,vvale@funcionalcorp.com.br

Formatação:

- text:nome_arquivo[,];[campo_obrigatorio[,]];[date_format]
- positional:nome_arquivo[,]:posicao_campo[,]:nome_campo[,];[date_format]
- excel:nome_arquivo[,]:[nome_aba[,]];[nome_campo[,]];[date_format]
- access:nome_arquivo[,];[date_format]

	- nome_arquivo = É obrigatório e deve conter pelo menos um arquivo.
	- campos_obrigatorios = Pode ficar em branco, e caso tenha campos definidos, estes, serão pesquisados no arquivo. Lembrando que será avaliado a existência do campo, e não se o campo possui dados. 
	- posicao_campo = Posição que definem os campos no arquivo
	- nome_campo = Campos que devem receber um nome, conforme a posicao_campo
	- date_format = Formato escolhido para converter os tipos de data encontrados. Pode ficar em branco.

## Arquivos gerados pelo validador

nome_arquivo_warns.log
	O arquivo de *_warns.logs mostra as informações sobre o que foi encontrado no arquivo e as verificações feitas. Serve de auxilio para identificação do que está errado e os possíveis problemas no arquivo.


nome_arquivo_warns_fields.log
	O arquivo *_fields.logs mostra as informações a respeito dos campos obrigatórios, se foram ou não encontrados. Serve para ajudar o usuário a identificar se o arquivo apresenta o mínimo necessário para ser ingerido.


nome_arquivo_metadata.schema
	O arquivo .schema possui os campos e possíveis tipos identificados no arquivo. Serve para ajudar o usuário a preencher os dados necessários para cadastro do layout.

warns.log
	O arquivo warns.log trás informações gerais sobre a execução de todos os arquivos validados. Serve para apoio do administrador.
 



## 

================================================
  NLOC    CCN   token  PARAM  length  location  
------------------------------------------------
       3      1     35      1       3 get_head@15-17@./metadata.py
       8      3     50      1       8 md5_hash@21-28@./metadata.py
       6      3     41      2       6 detect_delimiter@33-38@./metadata.py
      11      4     59      1      11 get_dtype@42-52@./metadata.py
       4      2     33      2       4 write_metadata@57-60@./metadata.py
       3      1     45      4       3 write_logs@67-69@./metadata.py
       2      1      6      0       2 get_logo@72-73@./metadata.py
      16      5    162      2      16 required_fields@14-29@./fixfile.py
      12      1    170      1      12 search_breakline@34-45@./fixfile.py
      15      4    137      3      15 analyze_and_fix_line@53-67@./fixfile.py
       9      3     84      5       9 analize_line@76-84@./fixfile.py
      13      5    145      5      13 fix_line@91-103@./fixfile.py
      12      2    122      3      12 create_profiling@22-33@./utils.py
      12      2    121      1      13 translate_language@37-49@./utils.py
      10      7    112      1      10 read_required_fields@53-62@./utils.py
      12      3    205      3      12 identify_datatypes@68-79@./utils.py
       9      2    150      4       9 txt_to_csv@86-94@./utils.py
       7      2    131      4       7 positional_to_csv@101-107@./utils.py
       4      1     71      3       4 access_to_csv@114-117@./utils.py
      11      2    142      3      11 excel_to_csv@123-133@./utils.py
       7      4     55      1       7 start@18-24@./start.py
       5      5     47      2       5 read_files@29-33@./start.py
      23      8    261      3      23 execute_steps@36-58@./start.py
       2      1     19      3       2 get_value@60-61@./start.py
       2      3     17      1       2 get_parameter@63-64@./start.py
       5      2    103      7       5 type_excel@66-70@./start.py
      10      2    162      8      10 type_txt@72-81@./start.py
      12      2    123      4      12 convert_type_to_csv@84-95@./start.py
      14      5    148      9      14 prepare_convert@97-110@./start.py
      10      3    119      5      10 accdb_to_csv@112-121@./start.py
      15      4    171      6      15 xls_to_csv@123-137@./start.py
      11      3    159      8      11 txt_to_csv@139-149@./start.py
      14      3    154      3      14 move_files_csv@152-165@./start.py
      10      9    124      3      10 verify_file_to_move@167-176@./start.py
       4      1     35      0       4 main@179-182@./start.py
4 file analyzed.
==============================================================
NLOC    Avg.NLOC  AvgCCN  Avg.token  function_cnt    file
--------------------------------------------------------------
     41       5.3     2.1       38.4         7     ./metadata.py
     67      13.0     3.6      139.6         5     ./fixfile.py
     84       9.6     2.6      131.8         8     ./utils.py
    154       9.6     3.7      113.1        15     ./start.py



