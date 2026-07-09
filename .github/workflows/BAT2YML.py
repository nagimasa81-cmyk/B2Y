import tkinter as tk
from tkinter import filedialog
import zipfile
from pathlib import Path

bats = {}

def convert_bat(txt, name):
    steps=["      - name: Checkout repository\n        uses: actions/checkout@v4"]
    for line in txt.splitlines():
        l=line.strip()
        if not l or l.startswith('@echo') or l.lower()=='pause':
            continue
        steps.append(f"      - name: Command\n        shell: cmd\n        run: |\n          {l}")
    return f"name: {name}\n\non:\n  workflow_dispatch:\n\njobs:\n  build:\n    runs-on: windows-latest\n\n    steps:\n" + "\n".join(steps)

root=tk.Tk(); root.title('BAT2YML'); root.geometry('1000x600')
left=tk.Frame(root); left.pack(side='left',fill='y')
right=tk.Frame(root); right.pack(side='right',fill='both',expand=True)

lst=tk.Listbox(left,width=30); lst.pack(fill='both',expand=True)
text=tk.Text(right); text.pack(fill='both',expand=True)

def open_zip():
    f=filedialog.askopenfilename(filetypes=[('ZIP','*.zip')])
    if not f: return
    bats.clear(); lst.delete(0,'end')
    with zipfile.ZipFile(f) as z:
        for n in z.namelist():
            if n.lower().endswith('.bat'):
                bats[Path(n).name]=z.read(n).decode('utf-8','ignore')
                lst.insert('end',Path(n).name)

def sel(evt=None):
    if not lst.curselection(): return
    n=lst.get(lst.curselection()[0])
    text.delete('1.0','end')
    text.insert('1.0',convert_bat(bats[n],Path(n).stem))

lst.bind('<<ListboxSelect>>',sel)
tk.Button(left,text='ZIPを開く',command=open_zip).pack(fill='x')
root.mainloop()
