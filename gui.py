# gui.py
import tkinter as tk
from analyzer import analyze

def on_check():
    pw = entry.get()
    res = analyze(pw)
    out_text.config(state="normal")
    out_text.delete("1.0", tk.END)
    out_text.insert(tk.END, f"Entropy (bits): {res['entropy_bits']}\n")
    out_text.insert(tk.END, f"Score: {res['score']} / 100 ({res['category']})\n\n")
    if res['suggestions']:
        out_text.insert(tk.END, "Suggestions:\n")
        for s in res['suggestions']:
            out_text.insert(tk.END, f" - {s}\n")
    out_text.config(state="disabled")

root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("420x300")

tk.Label(root, text="Enter password:").pack(pady=(10,0))
entry = tk.Entry(root, show="*", width=40)
entry.pack(pady=5)

tk.Button(root, text="Check Strength", command=on_check).pack(pady=5)

out_text = tk.Text(root, height=10, width=50, state="disabled")
out_text.pack(padx=10, pady=10)

root.mainloop()
