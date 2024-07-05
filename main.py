import pandas as pd
import flet as ft
from flet import FilePicker, FilePickerResultEvent
import os

usuario = os.getlogin()

def dividir_excel(excel_file, output_dir = f"C:\\Users\\{usuario}\\Downloads", linhas_por_arquivo=10000):
    df = pd.read_excel(excel_file)
    os.makedirs(output_dir, exist_ok=True)
    total_linhas = len(df)
    num_files = (total_linhas // linhas_por_arquivo) + int(total_linhas % linhas_por_arquivo != 0)
    for i in range(num_files):
        start_row = i * linhas_por_arquivo
        end_row = min((i +1) * linhas_por_arquivo, total_linhas)
        df_chunk = df.iloc[start_row:end_row]
        txt_data = df_chunk.to_csv(index=False, sep="\t")
        output_file = os.path.join(output_dir, f"Arquivo_{i + 1}.txt")
        with open (output_file, "w", encoding='utf-8') as f:
            f.write(txt_data)
def main(page: ft.Page):
    page.title = "Dividor Arquivos de Telefone"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def on_file_picked(e: FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            dividir_excel(file_path)
            file_label.value = f"Arquivo selecionado: {file_path}"
            page.update()

    file_picker = FilePicker(on_result=on_file_picked)
    file_label = ft.Text("Nenhum arquivo selecionado")

    select_file_button = ft.ElevatedButton(
        text="Selecionar arquivo Excel",
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"])
    )


    page.add(
        ft.Row(
            [
                select_file_button, file_label
            ], alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.overlay.append(file_picker)
    page.update()

ft.app(target=main)
