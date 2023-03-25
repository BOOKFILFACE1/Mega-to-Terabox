from mega import Mega
import requests
import wget
from progress.bar import Bar

# Configuración de la cuenta de Mega
mega = Mega()
email = 'tu_email_de_mega'
password = 'tu_contraseña_de_mega'

# Iniciar sesión en Mega
print('Iniciando sesión en Mega...')
m = mega.login(email, password)
print('Sesión iniciada correctamente')

# Configuración de la cuenta de Terabox
t_email = 'tu_email_de_terabox'
t_password = 'tu_contraseña_de_terabox'

# Iniciar sesión en Terabox
print('Iniciando sesión en Terabox...')
session = requests.Session()
login_data = {'email': t_email, 'password': t_password}
response = session.post('https://app.terabox.com/login', data=login_data)
if response.status_code != 200:
    print('Error al iniciar sesión en Terabox')
    exit()
print('Sesión iniciada correctamente')

# Pedir al usuario los archivos a transferir
print('Archivos disponibles en Mega:')
files = m.get_files()
for i, f in enumerate(files):
    print(f'{i+1}. {f["name"]}')
selection = input('Ingrese los números de los archivos a transferir separados por comas: ')
file_numbers = list(map(int, selection.split(',')))
files_to_transfer = [files[n-1] for n in file_numbers]

# Transferir los archivos
print('Iniciando transferencia de archivos...')
for f in files_to_transfer:
    print(f'Transfiriendo {f["name"]}...')
    url = m.get_download_link(f)
    filename = wget.download(url)
    with open(filename, 'rb') as file:
        file_data = file.read()
    file_size = len(file_data)
    upload_url = f'https://app.terabox.com/upload/{f["name"]}'
    headers = {'Content-Type': 'application/octet-stream', 'Content-Length': str(file_size)}
    response = session.post(upload_url, headers=headers, data=file_data)
    if response.status_code != 200:
        print(f'Error al transferir {f["name"]}')
    else:
        print(f'{f["name"]} transferido correctamente')

print('Transferencia de archivos finalizada')
