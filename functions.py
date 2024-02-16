import requests
import pandas as pd
import urllib.request
import re
import zipfile
import re
import numpy as np
import rispy
import itertools
import pathlib

PATH = pathlib.Path('.')

# https://refdb.sourceforge.net/manual-0.9.6/sect1-ris-format.html

def to_number(lst):
    new_lst = []
    for item in lst:
        item = int(item)
        new_lst.append(item)
    return new_lst

def calculate_mean(lst):
    total = sum(lst)
    count = len(lst)
    mean = total / count
    return mean

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


def join_bibdata_wos_format(path_choice, *args):
       
    if path_choice == 1:
        filepath = f'new_data/joined_{path_choice}.txt'
        
    elif path_choice == 2:
        filepath = f'new_data/joined_{path_choice}.txt'
    
    else:
        filepath = f'new_data/joined_{path_choice}.txt'
    
    control_kw = 0
    control_ad = 0
    control_author = 0
    control_cr = 0
    my_pt = []
    my_au = []
    my_ti = []
    my_so = []
    my_de = []
    my_ab = []
    my_c1 = []
    my_py = []
    my_di = []    
    my_cr = []
    my_tc = []
    my_nr = []
    n_authors = []
    nr = []
    tc = []
    years = []
    types = {'J': 0, 'C': 0, 'S': 0, 'B': 0, 'O': 0}
    
    with open(filepath, 'w', encoding='utf-8') as bibliography_file:
        title_df = []
        authors_df = []
        year_df = []
        ab_df = []
        doi_df = []
        db_df = []
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
                    
                if control_cr > 0:
                    control_cr-=1
                    
                # type of reference
                if line.startswith('PT'):
                    next_line = re.sub("PT ", '', line)
                    if next_line == 'J':
                        types['J'] +=1
                    if next_line == 'C':
                        types['C'] +=1
                    if next_line == 'B':
                        types['B'] +=1
                    if next_line == 'S':
                        types['S'] +=1
                    else:
                        types['O'] +=1
                    next_line = f'PT {next_line}'
                    my_pt.append(next_line)
                    begin_ref = line_number

                # type of reference
                if line.startswith('TY  -'):
                    next_line = re.sub("TY  - ", '', line)
                    next_line = ''.join(next_line)
                    begin_ref = line_number
                    if next_line == 'JOUR':
                        next_line = "PT J"
                        my_pt.append(next_line)
                        types['J'] +=1
                    elif next_line == 'CONF':
                        next_line = "PT C"
                        my_pt.append(next_line)
                        types['C'] +=1
                    elif next_line == 'SER':
                        next_line = "PT S"
                        my_pt.append(next_line)
                        types['S'] +=1
                    elif next_line == 'BOOK':
                        next_line = "PT B"
                        my_pt.append(next_line)
                        types['B'] +=1
                    else:
                        my_pt.append(f'PT OUTRO {next_line}')
                        types['O'] +=1
                        #bibliography_file.write(f'PT {next_line}')
                        #print("\n\nThere may be 1 TYPE missing...\n\n")
                # title
                if line.startswith('TI'):
                       for i in range(3):
                           next_line = lines[count]
                           
                           if next_line.startswith('TI'):
                               next_line = re.sub("TI  - ", '', next_line)
                               next_line = re.sub("TI ", '', next_line)
                               str_title = next_line
                               
                           elif next_line.startswith('   '):
                               next_line = re.sub("    ", ' ', next_line.upper())
                               next_line = str_title + next_line
                               my_ti.append(next_line) ##TALVEZ SEJA DIFERENTE TAMBEM, PRESENCA DE TITULOS QUEBRADOS
                            
                           else:
                               pass
                # year
                if line.startswith('PY'):
                    next_line = re.sub("PY  - ", '', line)
                    next_line = re.sub("PY ", '', next_line)
                    years.append(next_line)
                    next_line = f"PY {next_line}"
                    my_py.append(next_line)
                    
                else:
                    pass

                # source of the publication
                if line.startswith('SO'):
                    next_line = re.sub("SO ", '', line)
                    next_line = f"SO {next_line.upper()}"
                    my_so.append(next_line)

                elif line.startswith('T2  -'):
                    next_line = re.sub("T2  - ", '', line)
                    next_line = f"SO {next_line.upper()}"
                    my_so.append(next_line)
                    
                else:
                    pass

                # authors
                if line.startswith('AU') and control_author == 0:
                    count = line_number
                    authors = []

                    for i in range(80):

                        try:
                            next_line = lines[count]
                            
                            if next_line.startswith('AU  - ') and control_author == 0:                             
                                next_line = re.sub("AU  - ", '', next_line)
                                next_line = f"AU {next_line}"
                                my_au.append(next_line)
                                control_author += 1
                                count += 1
                                authors.append(next_line)

                            elif next_line.startswith('AU ') and control_author == 0 and "AU  - " not in next_line:
                                next_line = re.sub("AU ", '', next_line)
                                next_line = f"AU {next_line}"
                                my_au.append(next_line)
                                control_author += 1
                                count += 1
                                authors.append(next_line)
    
                            elif next_line.startswith("AU  - ") and control_author > 0:
                                next_line = re.sub("AU  - ", '', next_line)
                                next_line = f"   {next_line}"
                                my_au.append(next_line)
                                count += 1
                                control_author += 1
                                authors.append(next_line)
    
                            elif "   " in next_line:
                                next_line = re.sub("   ", '', next_line)
                                next_line = f"   {next_line}"
                                my_au.append(next_line)                                                                     
                                authors.append(next_line)
                                control_author += 1
                                count += 1
    
                            else:
                                #formatted_authors = '; '.join(authors)
                                n_authors.append(control_author)
                                line_number = count
                                break
    
                        except IndexError:
                            break

                #### DOI
                if line.startswith('DI '):
                    my_di.append(line)
                    
                elif line.startswith('DO  - '):
                    next_line = re.sub("DO  - ", '', line)
                    next_line = f"DI {next_line}"
                    my_di.append(next_line)
                    
                else:
                    pass
                    
                # keywords
                if line.startswith('DE '):
                    count = line_number
                    for i in range(10):
                        next_line = lines[count]
                        if next_line.startswith('DE '):
                            my_de.append(next_line)
                            count+=1
                        
                        elif next_line.startswith('   '):
                            my_de.append(next_line)
                            count+=1
                            
                        else:
                            line_number = count
                            break
                    
               # if line.startswith('ID '):
               #     my_de.append(line) # TA FALTANDO TIRAR O RE.SUB NAO?

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
                                my_de.append(next_line)
                                count += 1
                                control_kw += 1
                                
                            else:
                                final_list = []
                                for i in keywords:
                                    final_list.append(i.strip())
                                string = '; '.join(final_list)
                                line_number = count
                                break
                                                       
                        except IndexError:
                            break
                          
                    #str_list = [str(element) for element in list_keywords] 
                    #new_string = re.sub('\n', ';', string)
                    line_number = count
                    next_line = f'DE {string};'
                    #my_de.append(next_line)
                
                # Number of references
                if line.startswith('NR '):
                    my_nr.append(line)
                    nr.append(re.sub('NR ', '', line))
                
                # total citations
                if line.startswith('TC '):
                    my_tc.append(line)
                    tc.append(re.sub('TC ', '', line))
                    
                if line.startswith('N1  - Cited By :'):
                    next_line = re.sub('N1  - Cited By :', '', line)
                    my_tc.append(f'TC {next_line}')
                    tc.append(next_line)
                    
                # abstract
                if line.startswith('AB'):
                    next_line = re.sub('AB  - ','', line)
                    next_line = re.sub('AB ', '', next_line)
                    next_line = f'AB {next_line}'
                    my_ab.append(next_line)
                
                # Cited References    
                if line.startswith('CR '):
                    count = line_number

                    for i in range(150):

                        try:
                            next_line = lines[count]
                            
                            if next_line.startswith('CR ') and control_cr == 0:                             
                                
                                my_cr.append(next_line)
                                control_cr += 1
                                count += 1
 
                            elif "   " in next_line:
                                next_line = re.sub("   ", '', next_line)
                                next_line = f"   {next_line}"
                                my_cr.append(next_line)                                                                     
                                control_cr += 1
                                count += 1
    
                            else:
                                line_number = count
                                break
    
                        except IndexError:
                            break
                
                if line.startswith("N1  - References: "):
                    count = line_number
                    
                    for i in range(100):
                        try:
                            next_line = lines[count]
                            
                            if next_line.startswith("N1  - References: ") and control_cr == 0:
                                next_line = re.sub("N1  - References: ", "", next_line)
                                my_cr.append(next_line)
                                control_cr+=1
                                count+=1
                                
                            elif "UR  -" not in next_line and "N1  - References: " not in next_line and control_cr > 0:
                                my_cr.append(next_line)
                                control_cr+=1
                                count+=1
                            
                            else:
                                break
                        
                        except IndexError:
                            break
                    
                # Author affiliations
                #if line.startswith('C1 '):
                #    my_c1.append(line) ## DIFERENTES VERSÕES... TALVEZ
                #C1 [Grossi, José Antônio Saraiva] Universidade Federal de Viçosa, Brazil.
   #                [Martino, Daniela Correia] Universidade Federal de Viçosa, Brazil.
                #C1 [Huu-Thanh Duong; Bao-Quoc Ho] Univ Sci, Fac Informat Technol, VNU HCM, Ho Chi Minh City, Vietnam.
                    
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
                    # PT
                    for item in my_pt:
                        bibliography_file.write(str(item))
                    # AU
                    for item in my_au:
                        bibliography_file.write(str(item))
                    
                    ## TI
                    for item in my_ti:
                        bibliography_file.write(str(item))
                    
                    # SO
                    for item in my_so:
                        bibliography_file.write(str(item))
                    
                    # DE
                    for item in my_de:
                        bibliography_file.write(str(item))
                    
                    # AB
                    for item in my_ab:
                        bibliography_file.write(str(item))
                    
                    # C1 
                    #for item in my_c1:
                    #   bibliography_file.write(str(item))
                    #   
                    # CR 
                    for item in my_cr:
                       bibliography_file.write(str(item))
                    
                    # NR 
                    for item in my_nr:
                       bibliography_file.write(str(item))
                       
                    # TC
                    for item in my_tc:
                       bibliography_file.write(str(item))
                       
                    #PY
                    for item in my_py:
                       bibliography_file.write(str(item))
                    
                    # DI
                    for item in my_di:
                       bibliography_file.write(str(item))
                    
                    title_df.append(my_ti)
                    authors_df.append(my_au)                    
                    year_df.append(my_py)
                    ab_df.append(my_ab)
                    doi_df.append(my_di)
                    db_df.append("WEB OF SCIENCE")
                    
                    my_pt = []
                    my_au = []
                    my_ti = []
                    my_so = []
                    my_de = []
                    my_ab = []
                    my_c1 = []
                    my_py = []
                    my_di = []
                    my_cr = []
                    my_tc = []
                    my_nr = []
                    bibliography_file.write(f"DB WEB OF SCIENCE\n")
                    bibliography_file.write('ER\n\n')
                if line.startswith('ER') and 'scopus' in str(file):
                    
                    # PT
                    for item in my_pt:
                        bibliography_file.write(str(item))
                    # AU
                    for item in my_au:
                        bibliography_file.write(str(item))
                    
                    # TI
                    for item in my_ti:
                        bibliography_file.write(str(item))
                    
                    # SO
                    for item in my_so:
                        bibliography_file.write(str(item))
                    
                    # DE
                    final_list = []
                    for i in my_de:
                        final_list.append(i.strip())
                        
                    final_list = "; ".join(final_list)
                    bibliography_file.write("DE "f"{final_list}\n")
                    
                    #for item in my_de:
                    #    bibliography_file.write(str(item))
                    
                    # AB
                    for item in my_ab:
                        bibliography_file.write(str(item))
                    
                    # C1 
                    for item in my_c1:
                       bibliography_file.write(str(item))
                       
                    # CR
                    my_cr = ";".join(my_cr)
                    my_cr = my_cr.split(";")
                    count_cr = 0
                    #print(f'\n CITED REFERENCES {count_cr}')
                    for item in my_cr:
                        if count_cr == 0:
                            bibliography_file.write(f"CR {item}")
                            count_cr +=1
                            #print(item)
                        if count_cr > 0:
                            bibliography_file.write(f"   {item}")
                            count_cr+=1
                    nr.append(count_cr)
                    
                    # NR 
                    bibliography_file.write(f'NR {count_cr}\n')
                    
                    # TC
                    for item in my_tc:
                       bibliography_file.write(str(item))
                    
                    #PY
                    for item in my_py:
                       bibliography_file.write(str(item))
                    
                    # DI
                    for item in my_di:
                       bibliography_file.write(str(item))
                  
                    title_df.append(my_ti)
                    authors_df.append(my_au)                    
                    year_df.append(my_py)
                    ab_df.append(my_ab)
                    doi_df.append(my_di)
                    db_df.append("SCOPUS")

                    my_pt = []
                    my_au = []
                    my_ti = []
                    my_so = []
                    my_de = []
                    my_ab = []
                    my_c1 = []
                    my_py = []
                    my_di = []
                    my_cr = []
                    my_tc = []
                    bibliography_file.write(f"DB SCOPUS\n")
                    bibliography_file.write('ER\n\n')
                    
                if line.startswith('ER') and 'scielo' in str(file):
                    # PT
                    for item in my_pt:
                        bibliography_file.write(str(item))
                    # AU
                    for item in my_au:
                        bibliography_file.write(str(item))
                    
                    # TI
                    for item in my_ti:
                        bibliography_file.write(str(item))
                    
                    # SO
                    for item in my_so:
                        bibliography_file.write(str(item))
                    
                    # DE
                    for item in my_de:
                        bibliography_file.write(str(item))
                    
                    # AB
                    for item in my_ab:
                        bibliography_file.write(str(item))
                    
                    # C1 
                    for item in my_c1:
                       bibliography_file.write(str(item))
                       
                    # CR
                    for item in my_cr:
                       bibliography_file.write(str(item))
                       
                    # NR 
                    for item in my_nr:
                       bibliography_file.write(str(item))
                       
                    # TC
                    for item in my_tc:
                       bibliography_file.write(str(item))
                    
                    #PY
                    for item in my_py:
                       bibliography_file.write(str(item))
                    
                    # DI
                    for item in my_di:
                       bibliography_file.write(str(item))

                    title_df.append(my_ti)
                    authors_df.append(my_au)                    
                    year_df.append(my_py)
                    ab_df.append(my_ab)
                    doi_df.append(my_di)
                    db_df.append("SCIELO")
                    
                    my_pt = []
                    my_au = []
                    my_ti = []
                    my_so = []
                    my_de = []
                    my_ab = []
                    my_c1 = []
                    my_py = []
                    my_di = []
                    my_cr = []
                    my_tc = []
                    my_nr = []

                    bibliography_file.write(f"DB SCIELO\n")
                    bibliography_file.write('ER\n\n')

                # if line == None or line.startswith('EF'):
                #    bibliography_file.write('EF\n')
                # você pode escrever manualmente o EF ou quando acabar de rodar a
                # lista
    #df = pd.concat([df_wos, df_scopus, df_scielo], sort = False)
    df = pd.DataFrame({
                        'TITLE': title_df,
                        'AUTHORS': authors_df,
                        'YEAR': year_df,
                        'ABSTRACT': ab_df,
                        'DOI': doi_df,
                        'FROM': db_df
                    })
   
    df.to_excel('./new_data/levantamento_bases.xlsx', index=False)
    return (n_authors, years, types, tc, nr)


def check_doi(file):
    
    set_doi = set()
    set_ti = set()
    line_di = ''
    line_ti = ''
    doi = ''
    ti = ''

    for line_number, line in enumerate(file.readlines()):
        
        if line.startswith('DI'):
            doi = re.sub('DI ', '', line)
            line_di = line_number
            
        if line.startswith("TI"):
            ti = re.sub('TI ', '', line)
            line_ti = line_number
        
            file.seek(0)
            # Begin reading the file from the beginning again
            for new_number, new_line in enumerate(file.readlines()):
                if new_number != line_di and new_line.startswith('DI'):
                    if doi in new_line:
                        set_doi.add(doi)
                        break
                
                if new_number != line_ti and new_line.startswith('TI'):
                    if ti in new_line:
                        set_ti.add(ti)
                        break
                    
    #print("THE DOIS: \n")
    #print(", ".join(str(element) for element in set_doi))
    #print("----------------------")    
    return (set_doi, set_ti)  

def find_duplicates(file, bibliography_file, bibliography_content, begin_ref, line_number):
    try:
        with open('new_data/joined_bib.txt', 'r', encoding='utf-8') as bib:

            bibliography_content = bib.read()
            # Process the content as needed
            excerto = bibliography_content[begin_ref:line_number]
            if check_doi(excerto, bibliography_content) == 1:
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
                        line_number = count
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

def preprocess_tolist(file):
    list_title = []
    list_address = []
    list_language = []
    list_id = []
    list_year = []
    list_type = []
    list_ab = []
    list_keywords = []
    
    for linha in file.readlines():
                    
        if linha.startswith('TI'):
            line = re.sub("TI ", "", linha)
            #f1 = re.search(r"(?![TI ])(\w+)", str(linha))
            list_title.append(line)
    
        if linha.startswith('DI'):
            line = re.sub("DI ", "", linha)
            #f1 = re.search(r"(?![DI ]).+", str(linha))
            list_id.append(line)
            
        if linha.startswith('C1'):
            line = re.sub("C1 ", "", linha)
            #f1 = re.search(r"(?![C1 ]).+", str(linha))
            list_address.append(line)
     
        if linha.startswith('LA'):
            #f1 = re.search(r"(?![LA ])(\w+)", str(linha))
            list_language.append(line) 
            
        if linha.startswith('PY'):
            line = re.sub("PY ", "", linha)
            #f1 = re.search(r"(?![PY ])(\w+)", str(linha))
            list_year.append(line)
            
        if linha.startswith('DT'):
            line - re.sub("DT ", "", linha)
            #f1 = re.search(r"(?![DT ])(\w+)", str(linha))
            list_type.append(line)
            
        if linha.startswith('DE'):
            #f1 = re.search(r"(?![DE ])(\w+)", str(linha))
            #key = f1.partition(";")
            line = re.sub("DE ", "", linha)
            list_keywords.append(line)
            
        if linha.startswith('AB'):  ## PROBLEMA AQUI QUE NÃO PEGA TODAS AS LINHAS PROVAVELMENTE
            #f1 = re.search(r"(?![AB ]).+", str(linha))
            line = re.sub("AB ", "", linha)
            list_ab.append(line)
        
        if linha.startswith('EF'):
                break
            
    return (list_ab, list_keywords, list_language, list_address, list_type)

def transf_to_ris(filepaths):

    # Extract the titles of the references
#count = 0
    for filepath in filepaths:
          # Open the RIS file
        with open(filepath, 'r', encoding='utf-8') as f:
            # Parse the RIS file
            records = rispy.load(f)
              
        for record in records:
            id = record.get('id', '')
            title = record.get('title', '')
            authors = record.get('authors', [])
            abstract = record.get('abstract', '')
            keywords = record.get('keywords', [])
            year = record.get('year', '')
            journal_name = record.get('journal_name', '')
            df = df.append({
                'id': id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'keywords': keywords,
                'year': year,
                'source': journal_name
                }, ignore_index=True)
