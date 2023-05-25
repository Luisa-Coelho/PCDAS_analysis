import requests
import pandas as pd
import urllib.request
import re
import zipfile
import re
import numpy as np
import rispy
import itertools

# https://refdb.sourceforge.net/manual-0.9.6/sect1-ris-format.html


def extract_urls(json_file):
    diarios = []
    for item in json_file['gazettes']:
        with urllib.request.urlopen(item['txt_url']) as url:
            content = url.read().decode('utf-8')
            diarios.append(content)
    return diarios


def load_data(dir):
    extension = re.findall("\?(.*)", dir)
    if extension == 'xls' or 'xlsx':
        return pd.read_excel(dir)


def new_concat(df, new_column, *args):
    df[new_column] = ''
    for col in args:
        df[new_column] += df[col]
    return df


def join_bibdata_wos_format(*args):
    filepath = 'new_data/joined_bib.txt'
    
    control_kw = 0
    #ad_counter = 0
    #duplicates = 0
    control_ad = 0
    control_author = 0
    with open(filepath, 'w', encoding='utf-8') as bibliography_file:
        for file in args[0]:
            
            in_file = open(file, 'r', encoding="utf8")
            lines = in_file.readlines()
            
            for line_number, line in enumerate(lines):
                
                if control_ad > 0:
                    control_ad-=1
                    
                if control_kw > 0:
                    control_kw-=1
                    
                if control_author > 0:
                    control_author-=1
                    
                # type of reference
                if line.startswith('PT'):
                    next_line = re.sub("PT ", '', line)
                    bibliography_file.write(f'PT {next_line}')
                    begin_ref = line_number

                # type of reference
                if line.startswith('TY  -'):
                    next_line = re.sub("TY  - ", '', line)
                    next_line = ''.join(next_line)
                    begin_ref = line_number
                    if next_line == 'JOUR':
                        bibliography_file.write(f'PT J')
                    elif next_line == 'CONF':
                        bibliography_file.write(f'PT C')
                    elif next_line == 'SER':
                        bibliography_file.write(f'PT S')
                    elif next_line == 'BOOK':
                        bibliography_file.write(f'PT B')
                    else:
                        bibliography_file.write(f'PT {next_line}')
                        print("\n\nThere may be 1 TYPE missing...\n\n")
                # title
                if line.startswith('TI'):
                    next_line = re.sub("TI  - ", '', line)
                    next_line = re.sub("TI ", '', next_line)
                    bibliography_file.write(f'TI {next_line.upper()}')

                # year
                if line.startswith('PY'):
                    next_line = re.sub("PY  - ", '', line)
                    next_line = re.sub("PY ", '', next_line)
                    bibliography_file.write(f'PY {next_line}')

                # source of the publication
                if line.startswith('SO'):
                    next_line = re.sub("SO ", '', line)
                    bibliography_file.write(f'SO {next_line.upper()}')

                elif line.startswith('T2  -'):
                    next_line = re.sub("T2  - ", '', line)
                    bibliography_file.write(f'SO {next_line.upper()}')
                    
                else:
                    pass

                # authors
                if line.startswith('AU') and control_author == 0:
                    count = line_number
                    #control_author = 0
                    authors = []

                    for i in range(80):

                        try:
                            next_line = lines[count]
                            
                            if next_line.startswith('AU  - ') and control_author == 0:                             
                                next_line = re.sub("AU  - ", '', next_line)
                                bibliography_file.write(f'AU {next_line}')
                                control_author += 1
                                count += 1
                                authors.append(next_line)

                            elif next_line.startswith('AU ') and control_author == 0 and "AU  - " not in next_line:
                                next_line = re.sub("AU ", '', next_line)
                                bibliography_file.write(f'AU {next_line}')
                                control_author += 1
                                count += 1
                                #authors.append(next_line)
    
                            elif next_line.startswith("AU  - ") and control_author > 0:
                                next_line = re.sub("AU  - ", '', next_line)
                                bibliography_file.write(f'   {next_line}')
                                count += 1
                                control_author += 1
                                authors.append(next_line)
    
                            elif "   " in next_line:
                                next_line = re.sub("   ", '', next_line)
                                bibliography_file.write(f'   {next_line}')
                                #authors.append(next_line)
                                control_author += 1
                                count += 1
    
                            else:
                                #formatted_authors = '; '.join(authors)
                                break
    
                        except IndexError:
                            break

                #### DOI
                if line.startswith('DI '):
                    bibliography_file.write(line)
                    
                elif line.startswith('DO  - '):
                    next_line = re.sub("DO  - ", '', line)
                    bibliography_file.write(F'DI {next_line}')
                    
                else:
                    pass
                    
                # keywords
                if line.startswith('DE '):
                    count = line_number
                    for i in range(10):
                        next_line = lines[count]
                        if next_line.startswith('DE '):
                            bibliography_file.write(next_line)
                            count+=1
                        
                        elif next_line.startswith('   '):
                            bibliography_file.write(next_line)
                            count+=1
                            
                        else:
                            break
                    
                if line.startswith('ID '):
                    bibliography_file.write(line)

                if line.startswith('KW  - ') and control_kw == 0:
                    count = line_number
                    keywords = []
                    next_line = lines[count]
                    for i in range(30):
                        try:
                            if next_line.startswith('KW  - '):
                                next_line = lines[count]
                                next_line = re.sub("KW  - ", '', next_line)
                                keywords.append(next_line)
                                count += 1
                                control_kw += 1
                                
                            else:
                                final_list = []
                                for i in keywords:
                                    final_list.append(i.strip())
                                string = '; '.join(final_list)
                                break
                                                       
                        except IndexError:
                            break
                          
                    #str_list = [str(element) for element in list_keywords] 
                    #new_string = re.sub('\n', ';', string)
                    #print(new_string)
                    print(string)
                    bibliography_file.write('DE 'f'{string};')
                    #bibliography_file.write('\n')
                    #bibliography_file.write('DE ')
                    #output_str = "; ".join(list_keywords)
                    #bibliography_file.write(f'{output_str};')
                    #bibliography_file.write('\n')

                    #    bibliography_file.write()
                
                # abstract
                if line.startswith('AB'):
                    next_line = re.sub('AB  - ','', line)
                    next_line = re.sub('AB ', '', next_line)
                    bibliography_file.write(f'AB {next_line}')
                                       
                # Author affiliations
                if line.startswith('C1 '):
                    bibliography_file.write(line)
                    
                ##if line.startswith('AD  - ') and control_ad == 0:
                ##    count = line_number
                ##    next_line = lines[count]
                ##    affiliations = []
                ##    
                ##    while ('AD  - ') in next_line:
                ##        next_line = lines[count]
                ##        next_line = re.sub('AD  - ','', next_line)
                ##        affiliations.append(next_line)
                ##        ad_counter+=1
                ##        count+=1
                ##    
                ##    new_lines = ['a']
                ##    for i in range(ad_counter):    
                ##        #for author in authors:
                ##        if new_lines == ['a']:
                ##            new_line = (f'C1 [{formatted_authors}] {affiliations[i]}')
                ##            new_lines = new_lines.append(str(new_line))
                ##            bibliography_file.write(new_line)
##
                ##        else:
                ##            new_line = (f'   [{formatted_authors}] {affiliations[i]}')
                ##            #new_lines.append(str(new_line))
                ##            bibliography_file.write(new_line)
                ##         
                    #for i in range(ad_counter):
                    #    bibliography_file.write(f"{new_lines[i]}")
                        
                ##if line.startswith('AD  - ') and control_ad == 1:
                ##    ad_counter-=1
                
                # end of reference
                if line.startswith('ER') and 'wos' in str(file):
                    bibliography_file.write(f"DB WEB OF SCIENCE\n")
                    bibliography_file.write('ER\n\n')
                if line.startswith('ER') and 'scopus' in str(file):
                    bibliography_file.write(f"\nDB SCOPUS\n")
                    bibliography_file.write('ER\n\n')
                if line.startswith('ER') and 'scielo' in str(file):
                    bibliography_file.write(f"DB SCIELO\n")
                    bibliography_file.write('ER\n\n')


                # if line == None or line.startswith('EF'):
                #    bibliography_file.write('EF\n')
                # você pode escrever manualmente o EF ou quando acabar de rodar a
                # lista

    return print('done')


def check_doc(excerto, text):
    if excerto in text:
        return 1

    else:
        return 0


def find_duplicates(file, bibliography_file, bibliography_content, begin_ref, line_number):
    try:
        with open('new_data/joined_bib.txt', 'r', encoding='utf-8') as bib:

            bibliography_content = bib.read()
            # Process the content as needed
            excerto = bibliography_content[begin_ref:line_number]
            if check_doc(excerto, bibliography_content) == 1:
                bibliography_content = bibliography_content.replace(
                    excerto, '')
                bibliography_file.write(bibliography_content)
                # identifying the duplicates
                with open("new_data/duplicates.txt", "w", encoding="utf8") as dup:
                    duplicates += 1
                    dup.write(f"Duplicate NÚMERO {duplicates}\n")
                    dup.write(f'FONTE: {file}\n')
                    dup.write(f'excerto \n')
                    dup.write('ER \n\n')

            else:
                bibliography_file.write('ER\n')
    except FileNotFoundError:
        print("File not found: " + 'new_data/joined_bib.txt')

    except IOError:
        print("Error reading the file: " + 'new_data/joined_bib.txt')


def transf_txt_to_ris(lines):
    filepath = 'new_data/converted_scielo.ris'
    with open(filepath, 'w') as bibliography_file:

        title = 'TI'
        language = 'LA'
        address = 'C1'
        area = 'EC'
        identificador = 'DI'
        ano = 'PY'
        end_r = 'ER'
        end_f = 'EF'
        keywords = 'DE'

        count = 0
        list_scielo = []

        for line_number, linha in enumerate(lines):

            if linha.startswith('PT'):
                f1 = re.findall(r"(?![PT ])(\w+)", str(linha))
                if 'J' in f1:
                    bibliography_file.write(f'TY  - JOUR\n')
                else:
                    bibliography_file.write(f'TY  - ABST\n')

            elif linha.startswith('AU'):
                count = line_number
                for i in range(10):
                    try:
                        next_line = lines[count]
                    except IndexError:
                        break

                    if "AU" in next_line:
                        next_line = re.sub("AU ", '', next_line)
                        bibliography_file.write(f'AU  - {next_line}')
                        count += 1

                    elif "   " in next_line:
                        next_line = re.sub("   ", '', next_line)
                        bibliography_file.write(f'AU  - {next_line}')
                        count += 1

                    elif "TI" in next_line:
                        break

                    else:
                        pass

            elif linha.startswith(title):
                f1 = re.findall(r"(?![TI ])(\w+)", str(linha))
                f1 = ' '.join(f1)
                bibliography_file.write(f'TI  - {f1}\n')

            elif linha.startswith(identificador):
                f1 = re.findall(r"(?![DI ]).+", str(linha))
                # dicionario = {"DO": "-".join(f1)}
                f1 = ''.join(f1)
                bibliography_file.write(f'DO  - {f1}\n')

            elif linha.startswith(address):
                f1 = re.search(r"(?![C1 ]).+", str(linha))
                # list_address.append(f1.group())

            elif linha.startswith(language):
                f1 = re.findall(r"(?![LA ])(\w+)", str(linha))
                list_scielo.append(f'LA  - {f1}\n')
                # dicionario = {"LA": "-".join(f1)}
                f1 = ''.join(f1)
                bibliography_file.write(f'LA  - {f1}\n')

            elif linha.startswith(ano):
                f1 = re.findall(r"(?![PY ])(\w+)", str(linha))
                # list_year.append(f1.group())
                # dicionario = {"PY": "-".join(f1)}
                f1 = ''.join(f1)
                bibliography_file.write(f'PY  - {f1}\n')

            elif linha.startswith('SO'):
                f1 = re.findall(r"(?![SO ])(\w+)", str(linha))
                kw = ' '.join(f1)
                bibliography_file.write(f'JF  - {kw}\n')
            #    list_type.append(f1.group())

            elif linha.startswith(keywords):

                for kw in linha.split(';'):
                    if 'DE ' in kw:
                        kw = re.sub('DE ', "", kw)
                        bibliography_file.write(f'KW  - {kw}\n')
                    else:
                        kw = kw.strip()
                        bibliography_file.write(f'KW  - {kw}\n')

            elif linha.startswith('AB'):
                f1 = re.findall(r"(?![AB ]).+", str(linha))
                f1 = ' '.join(f1)
                bibliography_file.write(f'AB  - {f1}\n')

            elif linha.startswith(end_r):
                list_scielo.append('ER -\n\n')
                dicionario = {"ER": "-".join('\n')}
                bibliography_file.write('ER  -\n\n')

            elif linha.startswith(end_f):
                list_scielo.append('\nEF')
                break

            else:
                pass

            line_number += 1

    return list_scielo
