import re
import os
import pandas as pd
from PyPDF2 import PdfReader

def clean_text(text):
    
    stop_words = [
        r"PEFIN - CONSULTA DE PENDÊNCIAS FINANCEIRAS POR PARTICIPANTE",
        r"https://sitenet.serasa.com.br/novosisconvem/SisconvemPrincipal",
        r"02.275.901/0001-11",
        r"SERASA",
        r"Versão.+",
        r"\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}",
        r"\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2}",
        r"\d{2}\/\d{2}\/\d{4}\d{2}:\d{2}",
        r"\d{2}\/\d{2}\/\d{4}\d{2}:\d{2}:\d{2}",
        r"\d{2}\/\d{2}\/\d{4}  \d{2}:\d{2}:\d{2}",
        r"\d of .+\d:\d{2}",
        r"\d{2} of \d{2}",
        r"\d of \d{2}",
        r"Período.+\d"
    ]
    
    
    
    for word in stop_words:
        text = re.sub(word, "", text)
    
    # remove all \n inside cnpj or cpf
    text = re.sub(r"\d{3}-(\n)\d{2}", lambda x: x.group().replace("\n", ""), text)

    # remove all \n inside value
    text = re.sub(r"R\$(\n)", "R$ ", text)
    
    return text

def get_text_info(text):
    """
    This function only works based on the premise that the text is well structured, where each data is in the correct order.
    Hopefully, the text is structured. For now...
    """
    
    # regex to: value, cnpj, data_lanc, data_venc, code
    value_pattern = r"(R\$ .+,\d\d)"
    cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}"
    cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    data_pattern = r"\d{2}\/\d{2}\/\d{4}"
    code_pattern = r"\d+\d"
    
    df = pd.DataFrame(columns=["CODIGO", "DATAINCLU", "CNPJ", "VALOR"], index=[0])
    
    # temporary dict to control if the data was found in the line
    find_data = {
        "value": False,
        "cnpj": False,
        "cpf": False,
        "data": False,
        "code": False
    }
    
    lines = text.split("\n")
    
    for line in lines:
        
        # verify if line has value, cnpj, cpf, data and code.
        # if line has value, cnpj, cpf, data and code, save 
        # in temporary variables to insert into dataframe
        
        value_result = re.search(value_pattern, line)
        if value_result:
            find_data['value'] = True
            temp_value = value_result.group(0)
            temp_value = (temp_value.replace("R$ ", ""))
            line = re.sub(value_pattern, "", line)
            
        cnpj_result = re.search(cnpj_pattern, line)
        if cnpj_result:
            find_data['cnpj'] = True
            temp_cnpj = cnpj_result.group(0)
            line = re.sub(cnpj_pattern, "", line)
        
        cpf_result= re.search(cpf_pattern, line)
        if cpf_result:
            find_data['cpf'] = True
            temp_cpf = cpf_result.group(0)
            line = re.sub(cpf_pattern, "", line)
        
        data_result = re.findall(data_pattern, line)
        if data_result:
            find_data['data'] = True
            temp_data = data_result
            line = re.sub(data_pattern, "", line)

        code_result = re.search(code_pattern, line)
        if code_result:
            find_data['code'] = True
            temp_code = code_result.group(0)
            temp_code = temp_code[-9:]
            line = re.sub(code_pattern, "", line)

            
        # if all data is found, insert into dataframe
        if (find_data['value'] and (find_data['cnpj'] or find_data['cpf']) and find_data['data'] and find_data['code']):
            
            temp = {
                "CODIGO": temp_code,
                "DATAINCLU": temp_data,
                "CNPJ": temp_cnpj if find_data['cnpj'] else temp_cpf,
                "VALOR": temp_value
            }
            
            df = pd.concat([df, pd.DataFrame(temp, index=[0])])
                
            find_data = {
                "value": False,
                "cnpj": False,
                "cpf": False,
                "data": False,
                "code": False
            }

    #remove empty rows
    df.dropna(inplace=True)
    
    return df

def create_csv(filename, path):
    # Open PDF file and clean the text
    
    # technical artifice to find the file path
    reader = PdfReader(os.path.join(path.replace("csv", "upload"), filename.replace("csv", "pdf")))
    file_text = ""
    for page in reader.pages:
        file_text += page.extract_text()
    
    clean_file_text = clean_text(file_text)
    
    df = get_text_info(clean_file_text)
    
    # save dataframe to csv
    df.to_csv(os.path.join(path, filename), index=False, sep=';')
    
    
def deprecated_create_csv(final_list, filename, path):
    csv = open(os.path.join(path, filename), 'w')
    csv.write('CODIGO;DATALANC;DATAVENC;CNPJ;VALOR\n')
    for line in final_list:
        csv.write(f'{line[4]};')
        csv.write(f'{line[0]};')
        csv.write(f'{line[1]};')
        csv.write(f'{line[2]};')
        csv.write(f'{line[3]}\n')
    csv.close()