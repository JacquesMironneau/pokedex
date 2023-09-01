import pytesseract
import PIL
from time import sleep
import webbrowser

SCREEN_X = 1100
SCREEN_Y = 50
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 60
TESSERACT_PATH = r'C:\Users\jacqu\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
DEBUG = False
SLEEP_TIME = 2
POKEMON_LIST_FILE_PATH = r'C:\Users\jacqu\Downloads\pokemon.txt'

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def get_pokemon_list() -> dict:
    pokemon_list = {}
    with open(POKEMON_LIST_FILE_PATH, 'r') as f:
        for line in f:
            pokemon_list[line.strip()] = 0
    return pokemon_list

def screenGrab( rect ):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Handles a Linux installation with and older Pillow by falling-back
        to using XLib """
    global use_grab
    x, y, width, height = rect

    image = PIL.ImageGrab.grab( bbox=[ x, y, x+width, y+height ] )
   
    return image

if ( __name__ == "__main__" ):
    pokemons = get_pokemon_list()

    screen_rect = [ SCREEN_X, SCREEN_Y, WINDOW_WIDTH, WINDOW_HEIGHT ]
    prev_text = ''

    while True:
        image = screenGrab( screen_rect )              # Grab the area of the screen
        if ( DEBUG ):
            image.show()
        sleep(SLEEP_TIME)
        text  = pytesseract.image_to_string( image )   # OCR the image

        text = text.strip()
        if  len( text ) > 0 and (text != prev_text):
            prev_text = text

            text = ''.join(e for e in text if e.isalpha())
            print(f'filtered text: {text}')
            print(f'prev text: {prev_text}')
            if text in pokemons and pokemons[text] == 0:
                pokemons[text] += 1
                print(f'found {text} {pokemons[text]} times')
                webbrowser.open(f'https://www.pokepedia.fr/{text}')
