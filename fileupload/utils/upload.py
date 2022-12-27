import os
import re

def clean_page(page_obj, qtd_pages):
    text = page_obj.extractText()
    text = text.replace('\n', ' ')

    for i in range(1, qtd_pages + 1):
        text = text.replace(f' {i} of {qtd_pages} ', ' ')
    
    for i in range(1, qtd_pages + 1):
        text = text.replace(f'{i} of {qtd_pages} ', ' ')
    
    for i in range(1, qtd_pages + 1):
        text = text.replace(f'{i} of {qtd_pages}', ' ')
    
    url = 'https://sitenet.serasa.com.br/novosisconvem/SisconvemPrincipal'
    text = text.replace(f'{url}', ' ')
    
    regex = '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] [0-9][0-9]:[0-9][0-9]'
    text = re.sub(regex, ' ', text)
    
    regex2 = '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] à [0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
    text = re.sub(regex2, ' ', text)

    text = text.replace('Versão:', ' ')
    text = text.replace('2.22.1.1', ' ')
    text = text.replace('LOGOUT', ' ')
    text = text.replace('PEFIN', ' ')
    text = text.replace(' - ', ' ')
    text = text.replace('CONSULTA', ' ')
    text = text.replace('PENDÊNCIAS', ' ')
    text = text.replace('FINANCEIRAS', ' ')
    text = text.replace('PARTICIPANTE', ' ')
    text = text.replace('CONFIDENCIAL', ' ')
    text = text.replace('PARA:', ' ')
    text = text.replace('02.275.901/0001-11', ' ')
    text = text.replace('CDA', ' ')
    text = text.replace('Período :', ' ')
    text = text.replace('DEVEDOR', ' ')
    text = text.replace('DATA', ' ')
    text = text.replace('RECEB.', ' ')
    text = text.replace('ANOTAÇÃO', ' ')
    text = text.replace('DOC.', ' ')
    text = text.replace('VALOR', ' ')
    text = text.replace('NATUREZA', ' ')
    text = text.replace('PRINCIPAL', ' ')
    text = text.replace('DP', ' ')
    text = text.replace('-DUPLICATA', ' ')
    text = text.replace('Nr.', ' ')
    text = text.replace('Contrato:', ' ')
    text = text.replace('Status:', ' ')
    text = text.replace('INDISP.', ' ')
    text = text.replace('CARTA', ' ')
    text = text.replace('ENVIADA', ' ')
    text = text.replace('R$', ' ')
    text = text.replace('SERASA', ' ')
    text = text.replace('SISCONVEM', ' ')
    text = text.replace('DISPONIVEL', ' ')
    text = text.replace('Qtde', ' ')
    text = text.replace('Anotações', ' ')
    text = text.replace(':', ' ')
    text = text.replace('de', ' ')
    text = text.replace('POR', ' ')
    text = text.replace('DE', ' ')

    text = text.replace('      ', ' ')
    text = text.replace('     ', ' ')
    text = text.replace('    ', ' ')
    text = text.replace('   ', ' ')
    text = text.replace('  ', ' ')
    return text


def transcript_and_clean_pages(pdf_reader):
    all_lines = ''
    qtd_pages = pdf_reader.numPages
    for page_num in range(qtd_pages):
        page_obj = pdf_reader.getPage(page_num)
        all_lines += clean_page(page_obj, qtd_pages)

    all_lines = all_lines.replace('  ', ' ')

    return all_lines


def list_of_lines(word_by_word):
    word_by_word.pop(0)

    for i in range(2):
        word_by_word.pop(-1)

    lines = [word_by_word[x:x+5] for x in range(0, len(word_by_word), 5)]

    return lines


def create_csv(final_list, filename, path):
    csv = open(os.path.join(path, filename), 'w')
    csv.write('CODIGO;DATALANC;DATAVENC;CNPJ;VALOR\n')
    for line in final_list:
        csv.write(f'{line[4]};')
        csv.write(f'{line[0]};')
        csv.write(f'{line[1]};')
        csv.write(f'{line[2]};')
        csv.write(f'{line[3]}\n')
    csv.close()