from ctypes import windll
from pynput import keyboard
from PIL import ImageGrab
import tkinter as tk
import io
import win32clipboard
import ctypes
from time import sleep

# Variáveis globais para armazenar as coordenadas da área selecionada
x_start, y_start, x_end, y_end = 0, 0, 0, 0 

ctypes.windll.shcore.SetProcessDpiAwareness(1)
user_quit = False

# Função que inicia a seleção da área
def select_area():
    # Criar a janela tkinter sem bordas e em fullscreen
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.25)  # Transparência para visualizar a tela
    root.configure(background='black')

    root.focus_force()
    root.lift()
    root.attributes('-topmost', True)

    canvas = tk.Canvas(root, cursor="cross", bg="gray", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Função que captura o ponto inicial do retângulo
    def on_mouse_down(event):
        global x_start, y_start
        x_start, y_start = event.x, event.y

    # Função que atualiza o retângulo durante a seleção
    def on_mouse_drag(event):
        global x_end, y_end
        x_end, y_end = event.x, event.y
        canvas.delete("rect")  # Limpa o retângulo anterior
        canvas.create_rectangle(x_start, y_start, x_end, y_end, outline='red', width=2, tag="rect")

    # Função que finaliza a seleção e tira o print
    def on_mouse_release(event):
        global x_start, y_start, x_end, y_end
        x_end, y_end = event.x, event.y
        root.quit()  # Fecha a janela de seleção

    def on_escape(e):
        global user_quit
        user_quit = True
        root.quit()

    # Bind de eventos do mouse
    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)
    root.bind("<Escape>", on_escape)

    # Executa a janela
    root.mainloop()

    if user_quit:
        return (0, 0, 0, 0, root)
    
    # Retorna as coordenadas da área selecionada
    return (x_start, y_start, x_end, y_end, root)

# Função que tira um print screen da área selecionada
def take_screenshot_of_area():

    area = select_area()
    x_start, y_start, x_end, y_end, root = area

    if x_start == x_end and y_start == y_end:
        global user_quit
        user_quit = False
        root.destroy()
        return
    
    # Seleciona a área
    x_start, y_start, x_end, y_end, root = area

    # Obtenha o fator de escala de DPI da tela
    dpi_scale = root.winfo_fpixels('1i') / 96

    root.attributes('-alpha', 0)

    # Ajusta as coordenadas com base na escala do DPI
    x_start = int(x_start + dpi_scale + 1)
    y_start = int(y_start + dpi_scale + 1)
    x_end = int(x_end + dpi_scale - 2)
    y_end = int(y_end + dpi_scale - 2)

    # print(x_start, x_end, '\n', y_start, y_end)

    # Certifica-se de que os valores são positivos
    if x_start > x_end:
        x_start, x_end = x_end, x_start

    if y_start > y_end:
        y_start, y_end = y_end, y_start


    # Captura a tela inteira e recorta a área selecionada
    screenshot = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))

    # root.clipboard_clear()  # Limpa o clipboard

    image_to_clipboard(screenshot)
    root.destroy()


def image_to_clipboard(image):
    output = io.BytesIO()
    # Converte a imagem para o formato BMP e descarta os primeiros 14 bytes (cabeçalho BMP)
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    
    # Copia o DIB para o clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

# Função chamada quando uma tecla é pressionada
def on_press(key):
    try:
        if key == keyboard.Key.print_screen:
            take_screenshot_of_area()
    except AttributeError:
        pass

# Configura o listener do teclado
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
