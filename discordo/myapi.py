import os
import time
import webbrowser


def api_key():

    with open(os.path.join(os.path.dirname(__file__), "data.sec"), "r") as f:
        key = f.readlines()[0][:-1]
    return key
    # """
    # Set the API key to use for the API calls.
    # """
    # while True:
    #     cas = input("Modifier ou récupérer l'api? (m pour modifier) ")
    #     match cas:
    #         case "m":
    #             url="https://developer.riotgames.com/"
    #             webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    #             webbrowser.get('chrome').open(url)
    #             key = input("Entrez la clé: ")
    #             if len(key) > 0:
    #                 with open(os.path.join(os.path.dirname(__file__), "data.sec"), "w") as f:
    #                     f.write(key)
    #                 return key   
    #             else:
    #                 print("Erreur : la clé est vide")
    #                 continue 
    #         case _:
    #             time.sleep(5)
    #             with open(os.path.join(os.path.dirname(__file__), "data.sec"), "r") as f:
    #                 key = f.read()
    #             return key