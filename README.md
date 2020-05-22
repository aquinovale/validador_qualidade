## Objetivo

O validador tem o objetivo de ajudar na analise inicial dos arquivos em texto plano, Microsoft Excel e Microsoft Access. O validador lê o arquivo original, verifica se o mesmo tem campos obrigatórios, corrige possíveis quebras de linhas, remove caracteres especiais, e espaços em branco. Também gera SHA256 do arquivo original e do arquivo final criado. 

O sistema identifica os cabeçalhos automaticamente, reconhece possiveis tipos e gera arquivos com informações do que foi identificado, também é criado um relatório em formato HTML em inglês e português com a qualidade dos dados encontrados.

No final do processo os dados são enviados para um diretório especificado, e envia email avisando aos responsáveis.


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

### nome_arquivo_warns.log
	O arquivo de *_warns.logs mostra as informações sobre o que foi encontrado no arquivo e as verificações feitas. Serve de auxilio para identificação do que está errado e os possíveis problemas no arquivo.


### nome_arquivo_warns_fields.log
	O arquivo *_fields.logs mostra as informações a respeito dos campos obrigatórios, se foram ou não encontrados. Serve para ajudar o usuário a identificar se o arquivo apresenta o mínimo necessário para ser ingerido.


### nome_arquivo_metadata.schema
	O arquivo .schema possui os campos e possíveis tipos identificados no arquivo. Serve para ajudar o usuário a preencher os dados necessários para cadastro do layout.

### warns.log
	O arquivo warns.log trás informações gerais sobre a execução de todos os arquivos validados. Serve para apoio do administrador.
 


