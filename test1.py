import zipfile
import json
#from pathlib import Path
from pandas.io.json import json_normalize

#df1=pd.json_normalize(data=json.loads(json1), record_path='Patient', meta=['Doctor id','Visit id'])
#Path = ('.')

response_file = None  
data = None 
with zipfile.ZipFile("./df.zip", "r") as z:
   for filename in z.namelist():  
      print(filename)  
      with z.open(filename) as f:  
         data = f.read()  
         response_file = json.loads(data)  

diarios_municipio = {}
n_mun = 0
diarios_exo = {}
mes_exo = {}
anos = {}

for item in response_file:
    municipio = item["municipio"]
    mes = item["mes"]
    ano = item['ano']
    if municipio in diarios_municipio:
        diarios_municipio[municipio] += 1
        diarios_exo[municipio] +=1
        #mes_exo[mes] +=1
    else:
        diarios_municipio[municipio] = 1
        n_mun += 1
        diarios_exo[municipio] = 1
        #mes_exo[mes] = 1
        
    if ano in anos:
        anos[ano] += 1
    else:
        anos[ano] = 1
        
        
print(diarios_municipio)
print(n_mun)
print(diarios_exo)
print(mes_exo)
print(anos)