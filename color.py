import tkinter as tk
import random 
import time

colors = ["#93C69A", "#99CDA2", "#9ED3A9", "#A4DAB1",
          "#A9E0B8", "#AFE7C0", "#B4EDC7", "#BAF4CF", "#BDF2C2",
          "#C2F3C6", "#C5F4CA", "#C9F4CE", "#CCF5D1", "#D0F6D5",
          "#D3F7D9", "#D7F8DD", "#DAF8E1", "#DEF9E1", "#EFFCF0"
]

number=0
def color_on():
    label.config(text="", bg="#ADEBB3")

def color_change(number):
    if number<len(colors):
        label.config(bg=colors[number])
        root.after(20, lambda: color_change(number+1))

def color_off():
    global pressed, done
    pressed=False
    label.config(bg="#FFFFFF", fg="#121212", text="try to match the time by holder the space key!")
    done=True

def spacedown(event):
    global userstart, pressed, done
    if not done:
        return
    if not pressed:
        pressed=True
        userstart=time.perf_counter()
        label.config(bg="#ADEBB3", text="")

def spaceup(event):
    global pressed, done, randtime
    if not done:
        return
    
    if pressed:
        pressed=False
        userduration=round(time.perf_counter()-userstart, 2)

        accuracy=round((userduration/(randtime+1+0.380))*100, 2)
        if accuracy > 100:
            correct_acc = accuracy-100
            accuracy=100-correct_acc

        results=(
            f"target {round(randtime+1+0.380, 2)}s \n"
            f"your time {round(userduration, 2)}s \n"
            f"accuracy {round(accuracy, 2)}% \n"
            f"click r to restart"
            )
        label.config(bg="#121212", fg="#10B981", text=results)

def three():
    label.config(text="3")

def two():
    label.config(text="2")

def one():
    label.config(text="1")

def begin():
    global randtime, total, pressed, done, userstart
    randtime=round(random.uniform(1.0, 4.0),2)
    userstart=0.0
    userduration=0.0
    pressed=True
    done=False
    total=int(((4.4+randtime)*1000))

    label.config(text="determine the length of the flash", bg="#FFFFFF", fg="#000000")
    root.after(1000, three)
    root.after(2000, two)
    root.after(2800, one)
    root.after(3600, color_on)
    root.after(3600+int(randtime*1000), lambda:color_change(number))
    root.after(total, color_off)

def restart(event):
    global done
    if done:
        begin()

root=tk.Tk()
root.geometry("400x400")
label=tk.Label(root)
label.pack(expand=True, fill="both")
root.bind("<KeyPress-space>", spacedown)
root.bind("<KeyRelease-space>", spaceup)
root.bind("<KeyPress-r>", restart)

begin()
root.mainloop()
