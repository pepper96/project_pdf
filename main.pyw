import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

# Separador de PDF
def selecionar_pdf(label_pdf):
    global arquivo_pdf_sep
    # Seleciona o arquivo PDF
    arquivo_pdf_sep = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    
    if arquivo_pdf_sep:
        # Salva o caminho completo, mas exibe apenas o nome do arquivo
        nome_arquivo = os.path.basename(arquivo_pdf_sep)
        label_pdf.configure(text=f"Arquivo selecionado: {nome_arquivo}")  # Exibe apenas o nome do arquivo
    
    return arquivo_pdf_sep  # Retorna o caminho completo para uso posterior

def selecionar_pasta(label_pasta):
    global pasta_destino
    pasta_destino = filedialog.askdirectory()
    if pasta_destino:
        label_pasta.configure(text=f"Pasta selecionada: {pasta_destino}")
    return pasta_destino

def separar_paginas_pdf(arquivo_pdf_sep, pasta_destino, label_pdf, label_pasta):
    if not arquivo_pdf_sep or not pasta_destino:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF e a pasta de destino.")
        return
    try:
        leitor = PdfReader(arquivo_pdf_sep)
        for i, pagina in enumerate(leitor.pages):
            escritor = PdfWriter()
            escritor.add_page(pagina)
            arquivo_pagina = os.path.join(
                pasta_destino, f"{os.path.basename(arquivo_pdf_sep).replace('.pdf', '')}_pagina_{i + 1}.pdf"
            )
            with open(arquivo_pagina, "wb") as saida:
                escritor.write(saida)
        messagebox.showinfo("Sucesso", "Páginas separadas com sucesso!")
        label_pasta.configure(text="")
        label_pdf.configure(text="")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao separar páginas: {e}")

def tela_separar_pdf(parent, mostrar_menu):
    frame = ctk.CTkFrame(parent)
    label_titulo = ctk.CTkLabel(frame, text="Separar Páginas de PDF", font=("Arial", 20, "bold"))
    label_titulo.pack(pady=10)

    btn_selecionar_pdf = ctk.CTkButton(frame, text="Selecionar Arquivo PDF", command=lambda: selecionar_pdf(label_pdf))
    btn_selecionar_pdf.pack(pady=10)

    label_pdf = ctk.CTkLabel(frame, text="")
    label_pdf.pack(pady=5)

    btn_selecionar_pasta = ctk.CTkButton(frame, text="Selecionar Pasta de Destino", command=lambda: selecionar_pasta(label_pasta))
    btn_selecionar_pasta.pack(pady=10)

    label_pasta = ctk.CTkLabel(frame, text="")
    label_pasta.pack(pady=5)

    btn_executar = ctk.CTkButton(
        frame,
        text="Separar Páginas",
        command=lambda: separar_paginas_pdf(
            arquivo_pdf_sep,
            pasta_destino,
            #label_pdf.cget("text").split(": ")[-1],
            #label_pasta.cget("text").split(": ")[-1],
            label_pdf,
            label_pasta,
        ),
    )
    btn_executar.pack(pady=30)

    btn_voltar_menu = ctk.CTkButton(
        frame,
        text="Voltar",
        command=mostrar_menu,
        fg_color="red",
        text_color="white",
        width=10
    )
    btn_voltar_menu.place(relx=0.05, rely=0.9)

    return frame

# Lista global para armazenar os caminhos completos dos arquivos
arquivos_completos = []


# Função para selecionar os arquivos
def selecionar_arquivos(lista_arquivos):
    arquivos = filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
    if arquivos:
        for arquivo in arquivos:
            nome_arquivo = os.path.basename(arquivo)  # Extrai o nome do arquivo
            arquivos_completos.append(arquivo)  # Armazena o caminho completo
            lista_arquivos.insert(tk.END, nome_arquivo)  # Adiciona o nome do arquivo na listbox



def remover_arquivo():
    selecionado = lista_arquivos.curselection()  # Obtém o índice do item selecionado
    if selecionado:
        indice = selecionado[0]
        nome_arquivo = lista_arquivos.get(indice)  # Obtém o nome do arquivo selecionado
        print(f"Removendo: {nome_arquivo}")  # Linha de depuração

        # Encontre o caminho completo a partir do nome do arquivo
        caminho_completo = next((arquivo for arquivo in arquivos_completos if os.path.basename(arquivo) == nome_arquivo), None)
        
        if caminho_completo:
            arquivos_completos.remove(caminho_completo)  # Remove o caminho completo da lista global
            lista_arquivos.delete(indice)  # Remove o arquivo da listbox



# Função para selecionar a pasta de arquivos para unir
def selecionar_pasta_unir(label_pasta_unir):
    pasta = filedialog.askdirectory()
    if pasta:
        label_pasta_unir.configure(text=f"Pasta selecionada: {pasta}")
        # Limpa a lista de arquivos e a lista de arquivos no textbox antes de adicionar novos
        arquivos_completos.clear()
        lista_arquivos.delete(0, tk.END)
        for arquivo in os.listdir(pasta):
            if arquivo.endswith('.pdf'):
                caminho_completo = os.path.join(pasta, arquivo)
                arquivos_completos.append(caminho_completo)  # Armazena o caminho completo
                nome_arquivo = os.path.basename(arquivo)  # Exibe apenas o nome do arquivo
                lista_arquivos.insert(tk.END, nome_arquivo)  # Adiciona na listbox



# Função para unir os arquivos PDF selecionados
def unir_pdfs(label_pasta_uniao):
    global arquivos_completos  # Referenciando corretamente as variáveis globais
    if len(arquivos_completos) < 2:
        messagebox.showerror("Erro", "Por favor, selecione pelo menos dois arquivos PDF.")
        return

    try:
        escritor = PdfWriter()
        for arquivo in arquivos_completos:
            leitor = PdfReader(arquivo)
            for pagina in leitor.pages:
                escritor.add_page(pagina)

        arquivo_saida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo_saida:
            with open(arquivo_saida, "wb") as saida:
                escritor.write(saida)
            messagebox.showinfo("Sucesso", "Arquivos PDF unidos com sucesso!")

            # Limpa a listagem de arquivos e a pasta
            arquivos_completos.clear()
            lista_arquivos.delete(0, tk.END)

            # Apaga o texto da label de pasta
            label_pasta_uniao.configure(text="")

            arquivos_completos = []  # Redefinir a lista de arquivos

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao unir os arquivos: {e}")






# Função para exibir a interface para unir PDFs
def tela_unir_pdf(parent, mostrar_menu):
    global lista_arquivos,label_pasta_uniao
    frame = ctk.CTkFrame(parent)

    label_titulo = ctk.CTkLabel(frame, text="Unir Arquivos PDF", font=("Arial", 20, "bold"))
    label_titulo.pack(pady=10)

    btn_selecionar_arquivos = ctk.CTkButton(frame, text="Selecionar Arquivos PDF", command=lambda: selecionar_arquivos(lista_arquivos))
    btn_selecionar_arquivos.pack(pady=5)

    # Lista para exibir os arquivos selecionados
    lista_arquivos = tk.Listbox(frame, height=10, width=50, selectmode=tk.SINGLE)
    lista_arquivos.pack(pady=10)

    btn_remover_arquivo = ctk.CTkButton(frame, text="Remover Arquivo Selecionado", command=remover_arquivo)
    btn_remover_arquivo.pack(pady=5)

    btn_selecionar_pasta = ctk.CTkButton(frame, text="Selecionar Pasta com PDFs", command=lambda: selecionar_pasta_unir(label_pasta_uniao))
    btn_selecionar_pasta.pack(pady=5)

    label_pasta_uniao = ctk.CTkLabel(frame, text="")
    label_pasta_uniao.pack(pady=5)

    btn_executar = ctk.CTkButton(frame, text="Unir Arquivos", command=lambda: unir_pdfs(label_pasta_uniao))
    btn_executar.pack(pady=15)

    btn_voltar_menu = ctk.CTkButton(
        frame,
        text="Voltar",
        command=mostrar_menu,
        fg_color="red",
        text_color="white",
        width=10
    )
    btn_voltar_menu.place(relx=0.05, rely=0.9)

    return frame


# Função para exibir a interface para unir PDFs
def tela_unir_pdf(parent, mostrar_menu):
    global lista_arquivos
    frame = ctk.CTkFrame(parent)

    label_titulo = ctk.CTkLabel(frame, text="Unir Arquivos PDF", font=("Arial", 20, "bold"))
    label_titulo.pack(pady=10)

    btn_selecionar_arquivos = ctk.CTkButton(frame, text="Selecionar Arquivos PDF", command=lambda: selecionar_arquivos(lista_arquivos))
    btn_selecionar_arquivos.pack(pady=5)

    # Lista para exibir os arquivos selecionados
    lista_arquivos = tk.Listbox(frame, height=10, width=50, selectmode=tk.SINGLE)
    lista_arquivos.pack(pady=10)

    btn_remover_arquivo = ctk.CTkButton(
        frame,
        text="x",  # Texto com o "X"
        width=5,   # Largura do botão
        height=5,  # Altura do botão
        fg_color="red",  # Cor de fundo vermelha
        text_color="white",  # Cor do texto (branco)
        command=remover_arquivo  # Comando para remover o arquivo
    )

    # Posicionamento do botão Remover Arquivo ao lado da Listbox, na mesma altura
    btn_remover_arquivo.place(
        x=lista_arquivos.winfo_x() + lista_arquivos.winfo_width() + 110,  # Posição X ao lado da Listbox
        y=lista_arquivos.winfo_y() + lista_arquivos.winfo_width() + 95,  # Mesma altura do topo da Listbox
    )

    btn_selecionar_pasta = ctk.CTkButton(frame, text="Selecionar Pasta", command=lambda: selecionar_pasta_unir(label_pasta_uniao))
    btn_selecionar_pasta.pack(pady=5)

    label_pasta_uniao = ctk.CTkLabel(frame, text="")
    label_pasta_uniao.pack(pady=5)

    btn_executar = ctk.CTkButton(frame, text="Unir Arquivos", command=lambda: unir_pdfs(label_pasta_uniao))
    btn_executar.pack(pady=15)

    btn_voltar_menu = ctk.CTkButton(
        frame,
        text="Voltar",
        command=mostrar_menu,
        fg_color="red",
        text_color="white",
        width=10
    )
    btn_voltar_menu.place(relx=0.05, rely=0.9)

    return frame


def tela_menu_principal(parent, mostrar_separar_pdf, mostrar_unir_pdf):
    frame = ctk.CTkFrame(parent)

    label_menu = ctk.CTkLabel(frame, text="Menu Principal", font=("Arial", 20, "bold"))
    label_menu.pack(pady=20)

    btn_ir_para_pdf = ctk.CTkButton(frame, text="Separar Páginas de PDF", command=mostrar_separar_pdf)
    btn_ir_para_pdf.pack(pady=20)

    btn_ir_para_unir_pdf = ctk.CTkButton(frame, text="Unir Arquivos PDF", command=mostrar_unir_pdf)
    btn_ir_para_unir_pdf.pack(pady=20)

    return frame


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Tratamento PDF")
root.geometry("500x400")
root.resizable(False, False) 

def mostrar_frame(frame):
    frame.tkraise()

def fechar_janela():
    root.quit()

root.protocol("WM_DELETE_WINDOW", fechar_janela)

frame_menu = tela_menu_principal(root, lambda: mostrar_frame(frame_pdf), lambda: mostrar_frame(frame_unir_pdf))
frame_pdf = tela_separar_pdf(root, lambda: mostrar_frame(frame_menu))
frame_unir_pdf = tela_unir_pdf(root, lambda: mostrar_frame(frame_menu))

for frame in (frame_menu, frame_pdf, frame_unir_pdf):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

mostrar_frame(frame_menu)

root.mainloop()
