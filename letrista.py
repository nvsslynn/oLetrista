import re
import os, time
from rich.console import Console
import pyautogui as pag

class InexistentLyrics(Exception):
    pass

def load_lrc(path):
    padrao = re.compile(r'\[(\d+):(\d+)\.(\d+)\](.*)')
    if not os.path.exists(path):
        raise InexistentLyrics("File does not exist")
    
    linhas = []
    with open(path, 'r', encoding='utf-8') as file:
        for linha in file:
            match = padrao.match(linha.strip())
            if match:
                minu = int(match.group(1))
                secs = int(match.group(2))
                cents = int(match.group(3))

                stamp = secs+(cents/100)
                stamp += (minu*60)
                linhas.append(
                    (stamp, match.group(4))
                )
    
    return linhas

def display_lyrics(lyrics:list):
    console = Console()
    altura = console.height  # altura do terminal em linhas

    anterior = 0
    for linha in lyrics:
        wait = max(0, linha[0]-anterior)
        time.sleep(wait)
        console.clear()
        
        # empurra o texto pro meio vertical
        margem = (altura // 2) - 1
        console.print("\n" * margem)
        console.print("♪ {} ♪".format(linha[1]), style="bold cyan", justify="center")
        
        anterior = linha[0]
    time.sleep(4)

def load_by_name(name:str):
    n = name.lower().replace(" ", "_")+".lrc"
    print("Carregando '{}'...".format(n))
    return load_lrc("letras/"+n)

if __name__ == "__main__":
    video = input("Você tem um video aberto no YouTube? (s/n) > ")
    lrcs = load_by_name(input("Nome da música (precisa estar na pasta de letras) > "))
    time.sleep(5)
    if video.lower() == "s": pag.press("k")

    display_lyrics(lrcs)