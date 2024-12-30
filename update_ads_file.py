import os
import requests
import shutil

# URLs base
ads_files_url = "http://naeu-o-dn.playblackdesert.com/UploadData/ads_files"
language_data_url_template = "https://naeu-o-dn.playblackdesert.com/UploadData/ads/languagedata_en/{}/languagedata_en.loc"

# Diretório local
destination_dir = r"C:\Pearlabyss\BlackDesert\ads"
destination_file = os.path.join(destination_dir, "languagedata_pt.loc")

def get_file_number():
    response = requests.get(ads_files_url)
    if response.status_code == 200:
        # Divide o conteúdo em linhas e procura pela linha específica
        lines = response.text.splitlines()
        for line in lines:
            if "languagedata_en.loc" in line:
                # Extraindo o número associado ao "languagedata_en.loc"
                parts = line.split()
                return parts[-1]  # O número deve ser o último elemento
    raise Exception("Não foi possível obter o número do arquivo.")

def download_file(file_number):
    url = language_data_url_template.format(file_number)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_file = os.path.join(destination_dir, "languagedata_en.loc")
        with open(temp_file, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        return temp_file
    else:
        raise Exception(f"Erro ao baixar o arquivo: {response.status_code}")

def replace_file(new_file):
    if os.path.exists(destination_file):
        os.remove(destination_file)
    shutil.move(new_file, destination_file)

def main():
    try:
        file_number = get_file_number()
        print(f"Número do arquivo obtido: {file_number}")
        
        new_file = download_file(file_number)
        print(f"Arquivo baixado: {new_file}")
        
        replace_file(new_file)
        print(f"Arquivo substituído com sucesso em: {destination_file}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
