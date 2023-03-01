import os
import sys
import shutil

class Gen():
    def __init__(self):
        self.error_code = {
            1:'Inicio deve ser um número menor que fim',
            2:'Valores devem ser diferentes',
            3:'Intervalos inválidos',
            4:'Intervalos inválidos'
        }
        
    def parse(self,string,listStartEnd):
        self.substrings = []

        for i in range(len(listStartEnd)):
            self.substrings.append((string[listStartEnd[i][0]-1:listStartEnd[i][1]],listStartEnd[i][2]))
        return self.substrings

    def create_substring_file(self,path,message):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        f = open(path,"w+")
        f.write(message)
        f.close()

    def remove_substrings_folder(self,path):
        # Try to remove the tree; if it fails, throw an error using try...except.
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


if(__name__ == "__main__"):
    p = Gen()
    #p.parse("string1string2string3string4string5",[(8, 14), (15, 21), (22, 28), (29, 35), (1, 7)])
    #p.remove_substrings_folder('Arquivos_de_Texto')
            