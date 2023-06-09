from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import pyautogui as pa
from tkinter import ttk
from klase import *

root = Tk()
root.title('Restorani')

def update_listbox():
    lb.delete(0,END)
    [lb.insert(END,i) for i in R.lista_listbox()]

lb=Listbox(root)
lb.grid(row=0,column=0,rowspan=3)
update_listbox()

def racun():
    selected_indices = lb.curselection()
    if selected_indices:
        choice = pa.confirm('Da li želite da izdate racun?', buttons=['Da', 'Ne'])
        if choice == 'Da':
            selected_index = selected_indices[0]
            selected_item = lb.get(selected_index)
            selected_values = selected_item.split('-')
            if len(selected_values) != 5:
                messagebox.showwarning("Napomena", "Selektovana stavka nema validne vrednosti.")
            else:
                br_porudzbine = selected_values[0]
                datum_porudzbine = '-'.join(selected_values[1:4])
                cena = selected_values[4]
                R.lista_racun(br_porudzbine, datum_porudzbine, cena)
                t = Toplevel()
                t1 = Label(t, text='Racun uspesno izdat')
                t1.pack()
    else:
        choice = pa.confirm('Da li želite da izdate racun?', buttons=['Da', 'Ne'])
        if choice == 'Da':
            messagebox.showwarning("Napomena", "Nijedna stavka nije selektovana.")

b = Button(root, text='Izdaj racun', command=lambda:racun())
b.grid(row=4, column=0, rowspan=3)

menubar=Menu(root)
dodaj_menu=Menu(menubar,tearoff=0)
dodaj_menu.add_command(label='Dodaj novu porudzbinu',command=lambda:open_nova_porudzbina())
menubar.add_cascade(label='Dodaj',menu=dodaj_menu)
grafici=Menu(menubar,tearoff=0)
grafici.add_command(label='Top 5 Jela',command=lambda:piechart())
grafici.add_command(label='Najvise Porudzbina po Restoranu',command=lambda:barchart())
menubar.add_cascade(label='Grafik',menu=grafici)

def update_listbox1():
    lb1.delete(0,END)
    [lb1.insert(END,i) for i in R.lista_listbox1()]

def open_nova_porudzbina():
    global lb1
    global e1
    global e2
    global e3
    t = Toplevel(root)
    lb1 = Listbox(t, height=10, width=50)
    lb1.grid(row=0, column=0, rowspan=8)

    l1 = Label(t, text='Ime i prezime')
    l1.grid(row=0, column=1, columnspan=1)
    e1 = Entry(t)
    e1.grid(row=1, column=1, columnspan=1)

    l2 = Label(t, text='Adresa')
    l2.grid(row=2, column=1, columnspan=1)
    e2 = Entry(t)
    e2.grid(row=3, column=1, columnspan=1)

    current_timestamp = datetime.now().strftime('%Y-%m-%d')
    l3 = Label(t, text='Datum-automatski')
    l3.grid(row=4, column=1, columnspan=1)
    e3 = Entry(t)
    e3.insert(END, current_timestamp)
    e3.grid(row=5, column=1, columnspan=1)
    t2=Label(t,text="")
    t2.grid(row=7,column=1,columnspan=1)
    def handle_choice(choice):
        if choice == 'Da':
            t2.configure(text='Nova Porudžbina uspešno dodata')
            nova_porudzbina1()
        elif choice == 'Ne':
            t.destroy()

    b1 = Button(t, text='Dodaj', command=lambda: handle_choice(pa.confirm('Da li sigurno želite da dodate novu porudžbinu?', buttons=['Da', 'Ne'])))
    b1.grid(row=6, column=1, columnspan=1)
    update_listbox1()

  
def nova_porudzbina1():
    selected_indices = lb1.curselection()
    if selected_indices:
        selected_index = selected_indices[0]
        selected_item = lb1.get(selected_index)
        selected_values = selected_item.split('-')
        if len(selected_values) < 5:
            messagebox.showwarning("Napomena", "Selektovana stavka nema validne vrednosti.")
        elif e1.get()=='' or e2.get()=='':
            pa.alert('Polja nisu popunjena. Molimo popunite oba polja')
        else:
            datum_porudzbine = datetime.strptime(e3.get(), '%Y-%m-%d').date()
            R.nova_porudzbina(e1.get(), e2.get(), e3.get(), int(selected_values[3]), int(selected_values[4]))
            update_listbox()
    else:
        messagebox.showwarning("Napomena", "Nijedna stavka nije selektovana.")



def execute_query(query, naziv_fajla, kolone):    
    R.get_sql(query)
    R.export_excel(naziv_fajla, kolone)
    

t3=Label(root,text="")
t3.grid(row=3,column=1,columnspan=2)

def export_selected():
    izabrana_vrednost = izabrana_opcija.get()
    choice=pa.confirm('Da li zelite da eksportujete fajl: {}'.format(export_filename()), buttons=['Da', 'Ne'])
    if choice=='Da':
        if izabrana_vrednost == 1:
            t3.configure(text='Nazivi restorana+jela+cene fajl uspesno eksportovan')
            execute_query('''
                SELECT r.naziv_restorana, r.adresa, j.jelo, j.cena
                FROM Restorani r, Jelovnici j
                WHERE r.id_restoran = j.id_restoran
                ''', 'nazivi_restorana_jela_cene.xlsx', ["naziv_restorana", "adresa", "jelo", "cena"])
        elif izabrana_vrednost == 2:
            t3.configure(text='Najprodavanije-jelo fajl uspesno eksportovan')
            execute_query('''
                SELECT p.id_jela, j.jelo, r.naziv_restorana
                FROM Porudzbina p
                JOIN Jelovnici j ON p.id_jela = j.id_jela
                JOIN Restorani r ON p.id_restoran = r.id_restoran
                GROUP BY p.id_jela, j.jelo, r.naziv_restorana
                ORDER BY COUNT(*) DESC
                LIMIT 1;
                ''', 'najprodavanije_jelo.xlsx', ["id_jela", "jelo", "naziv_restorana"])
        elif izabrana_vrednost == 3:
            t3.configure(text='Porudzbine+jela+cene+datumi fajl uspesno eksportovan')
            execute_query('''
                SELECT p.br_porudzbine, j.jelo, j.cena, p.datum_porudzbine
                FROM Porudzbina p, Jelovnici j
                WHERE p.id_jela = j.id_jela
                ''', 'porudzbine_jela_datumi.xlsx', ["br_porudzbine", "jelo","cena", "datum_porudzbine"])
        else:
            pa.alert('Nijedna opcija nije izabrana. Molimo izaberite opciju')
            l4=Label(text='Nijedna opcija nije izabrana.')
            l4.grid(row=3,column=1,columnspan=2)

t3 = Label(root, text="")
t3.grid(row=3, column=1, columnspan=2)

izabrana_opcija = IntVar(value=0)

b1 = Radiobutton(root, text='Nazivi restorana+jela+cene', variable=izabrana_opcija, value=1)
b1.grid(row=0, column=1, columnspan=2)

b2 = Radiobutton(root, text='Najprodavanije-jelo', variable=izabrana_opcija, value=2)
b2.grid(row=1, column=1, columnspan=2)

b3 = Radiobutton(root, text='Porudzbine+jela+cene+datumi', variable=izabrana_opcija, value=3)
b3.grid(row=2, column=1, columnspan=2)

def handle_choice1(choice):
        if choice == 'Da':
            t3.configure(text='Fajl uspesno eksportovan')
            export_selected()

def export_filename():
    izabrana_vrednost = izabrana_opcija.get()
    if izabrana_vrednost == 1:
        return 'nazivi_restorana_jela_cene.xlsx'
    elif izabrana_vrednost == 2:
        return 'najprodavanije_jelo.xlsx'
    elif izabrana_vrednost == 3:
        return 'porudzbine_jela_datumi.xlsx'

export_button = Button(root, text='Export', command=lambda: export_selected())
export_button.grid(row=4, column=1, columnspan=2)


def piechart():
    t=Toplevel(root)
    month_var = StringVar()
    month_dropdown = ttk.Combobox(t, textvariable=month_var, values=[str(i) for i in range(1, 13)])
    month_dropdown.set("Izaberi Mesec")
    month_dropdown.grid(row=0, column=0)

    generate_button = Button(t, text="Izaberi", command=lambda:R.jela_piechart(month_var.get()))
    generate_button.grid(row=1, column=0)

def barchart():
    t=Toplevel(root)
    mesec_var=StringVar()
    mesec_dropdown=ttk.Combobox(t,textvariable=mesec_var,values=[str(i) for i in range(1,13)])
    mesec_dropdown.set('Izaberi Mesec')
    mesec_dropdown.grid(row=0,column=0)

    bt=Button(t,text='Izaberi',command=lambda:R.br_porudzbina(mesec_var.get()))
    bt.grid(row=1,column=0)

root.config(menu=menubar)
mainloop()
