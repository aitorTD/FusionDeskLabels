import tkinter as tk
from tkinter import filedialog, messagebox
import os
import csv
from fpdf import FPDF

def select_file(label):
    """Selecciona un archivo CSV y actualiza la etiqueta correspondiente."""
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        label.config(text=file_path)

def wrap_text(pdf, text, max_width):
    """Divide el texto en líneas si es más largo que el ancho permitido."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if pdf.get_string_width(current_line + " " + word) <= max_width:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def generate_pdf():
    """Genera un PDF con tarjetas basadas en los CSV seleccionados."""
    passwords_file_path = passwords_label.cget("text")
    names_file_path = names_label.cget("text")

    if not os.path.isfile(passwords_file_path):
        messagebox.showerror("Error", "Por favor, selecciona un archivo CSV de contraseñas válido.")
        return
    if not os.path.isfile(names_file_path):
        messagebox.showerror("Error", "Por favor, selecciona un archivo CSV de nombres válido.")
        return

    pdf_name = pdf_name_entry.get().strip()
    if not pdf_name:
        pdf_name = "labels"

    output_path = os.path.join(os.path.expanduser("~/Downloads"), pdf_name + ".pdf")
    CARD_WIDTH = 105
    MIN_CARD_HEIGHT = 65
    MARGIN_LEFT = 0
    MARGIN_TOP = 0
    INTERNAL_MARGIN = 1
    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297
    MARGIN_HORIZONTAL = 0
    MARGIN_VERTICAL = 0

    pdf = FPDF(format='A4', unit='mm')
    pdf.set_auto_page_break(auto=False)

    try:
        pdf.add_page()

        # Leer los nombres y almacenarlos en un diccionario
        with open(names_file_path, newline='', encoding='utf-8') as names_file:
            names_reader = csv.reader(names_file)
            names_dict = {row[1].strip(): (row[0].strip(), row[4].strip()) for row in names_reader}

        # Leer las contraseñas y generar las tarjetas
        with open(passwords_file_path, newline='', encoding='utf-8') as passwords_file:
            passwords_reader = csv.DictReader(passwords_file)

            x = MARGIN_LEFT
            y = MARGIN_TOP

            for row in passwords_reader:
                candidate_id = row['CandidateID']
                name, exam_date = names_dict.get(candidate_id, ("Nombre no encontrado", "Fecha no encontrada"))

                pdf.set_font("Arial", size=15, style='B')

                # Calcular líneas y alturas dinámicas
                name_lines = wrap_text(pdf, name, CARD_WIDTH - 1 * INTERNAL_MARGIN)
                line_height = 9
                name_height = len(name_lines) * line_height
                card_height = max(MIN_CARD_HEIGHT, name_height + 5 * line_height)

                # Comprobar si la tarjeta cabe en la página
                if y + card_height > PAGE_HEIGHT - MARGIN_TOP:
                    pdf.add_page()
                    x = MARGIN_LEFT
                    y = MARGIN_TOP

                # Dibuja la tarjeta
                pdf.set_draw_color(0, 0, 0)
                pdf.rect(x, y, CARD_WIDTH, card_height)

                # Escribir contenido dentro de la tarjeta
                text_x = x + INTERNAL_MARGIN
                text_y = y + INTERNAL_MARGIN
                pdf.set_xy(text_x, text_y)
                pdf.cell(w=0, h=line_height, txt=f"ID: {candidate_id}", ln=1)

                pdf.set_font("Arial", size=12, style='B')
                for i, line in enumerate(name_lines):
                    pdf.set_xy(text_x, text_y + (i + 1) * line_height)
                    pdf.cell(w=0, h=line_height, txt=line, ln=1)

                pdf.set_font("Arial", size=11)
                pdf.set_xy(text_x, text_y + name_height + line_height)
                pdf.cell(w=0, h=line_height, txt=f"User: {row['Username']}", ln=1)
                pdf.set_xy(text_x, text_y + name_height + 2 * line_height)
                pdf.cell(w=0, h=line_height, txt=f"Pass: {row['Password']}", ln=1)
                pdf.set_xy(text_x, text_y + name_height + 3 * line_height)
                pdf.cell(w=0, h=line_height, txt=f"Pin: {row['Pincode']}", ln=1)

                # Agregar la fecha del examen cerca del margen derecho
                date_x = x + CARD_WIDTH - INTERNAL_MARGIN - pdf.get_string_width(f"{exam_date}")
                pdf.set_xy(date_x, text_y + name_height + 4 * line_height)
                pdf.cell(w=0, h=line_height, txt=f"{exam_date}", ln=1)

                x += CARD_WIDTH + MARGIN_HORIZONTAL

                if x + CARD_WIDTH > PAGE_WIDTH - MARGIN_LEFT:
                    x = MARGIN_LEFT
                    y += card_height + MARGIN_VERTICAL

        pdf.output(output_path)
        success_label.config(text=f"✅ PDF generado en {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al generar el PDF:\n{e}")

# Interfaz gráfica
root = tk.Tk()
root.title("Generador de Tarjetas PDF")

frame_files = tk.LabelFrame(root, text="Archivos CSV", padx=10, pady=10)
frame_files.pack(padx=10, pady=10, fill="x")

tk.Button(frame_files, text="Seleccionar CSV de contraseñas", command=lambda: select_file(passwords_label)).grid(row=0, column=0, padx=5, pady=5)
passwords_label = tk.Label(frame_files, text="(Ningún archivo seleccionado)", width=60, anchor="w")
passwords_label.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_files, text="Seleccionar CSV de nombres", command=lambda: select_file(names_label)).grid(row=1, column=0, padx=5, pady=5)
names_label = tk.Label(frame_files, text="(Ningún archivo seleccionado)", width=60, anchor="w")
names_label.grid(row=1, column=1, padx=5, pady=5)

frame_settings = tk.LabelFrame(root, text="Configuración", padx=10, pady=10)
frame_settings.pack(padx=10, pady=10, fill="x")

tk.Label(frame_settings, text="Nombre del PDF (sin .pdf):").grid(row=0, column=0, padx=5, pady=5)
pdf_name_entry = tk.Entry(frame_settings, width=40)
pdf_name_entry.grid(row=0, column=1, padx=5, pady=5)

generate_button = tk.Button(root, text="Generar PDF", command=generate_pdf)
generate_button.pack(pady=10)

success_label = tk.Label(root, text="", fg="green")
success_label.pack()

root.mainloop()
