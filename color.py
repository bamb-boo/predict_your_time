import hashlib
import tkinter as tk
import random 
import time
file="accuracy.txt"
colors = ["#B0EBB6", "#B2ECC7", "#B5EDC9", "#B7EDCB", "#BAEECE", "#BCEED0", 
    "#BFEFD2", "#C1F0D4", "#C4F0D6", "#C6F1D9", "#C9F1DB", "#CBF2DD", 
    "#CEF3DF", "#D0F3E1", "#D3F4E4", "#D5F4E6", "#D8F5E8", "#DAF6EA", 
    "#DDF6EC", "#DFF7EE", "#E2F7F0", "#E4F8F2", "#E7F8F4", "#E9F9F6", 
    "#ECF9F9", "#EEFAFB", "#F1FAFD", "#F3FBFF", "#F4FCFE", "#F5FCFC", 
    "#F5FBFA", "#F6FBFA", "#F7FCFA", "#F8FCFB", "#F9FDFC", "#FAFCFC", 
    "#FDFDFD", "#EFFCF0"
]

number=0
fade_duration=0
start=0
restart_done=False
secret="do_uk_the_muffin_man"

def color_on(): #initial green flash without fade 
    global start
    label.config(text="", bg="#ADEBB3")
    start=time.perf_counter()

def color_change(number): #fade+size decrease
    global fade_duration
    if number<len(colors):
        current=400-(number*10.8108)
        label.place(relx=0.5, rely=0.5, anchor="center", width=current, height=current)
        label.config(bg=colors[number])
        root.after(10, lambda: color_change(number+1))
    else:
        color_off()

def color_off(): #color's done, match-time text
    global pressed, done, actual
    end=time.perf_counter()
    actual=end-start
    pressed=False
    label.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
    label.config(bg="#FFFFFF", fg="#121212", text="try to match the time by holding the space key!")
    done=True

def spacedown(event): #registers keypress and begins timer
    global userstart, pressed, done, attempt
    if not done or attempt:
        return
    if not pressed:
        pressed=True
        userstart=time.perf_counter()
        label.config(bg="#ADEBB3", text="")

def spaceup(event): #registers keyremoval, stops time, calculates accuracy and outputs
    global pressed, done, randtime, attempt, restart_done, accuracy
    if not done or attempt:
        return
    
    if pressed:
        pressed=False
        attempt=True
        restart_done=True
        userduration=round(time.perf_counter()-userstart, 2)

        accuracy=round((userduration/(actual))*100, 2)
        if accuracy > 100:
            correct_acc = accuracy-100
            accuracy=100-correct_acc

        results=(
            f"target {round(actual, 2)}s \n"
            f"your time {round(userduration, 2)}s \n"
            f"accuracy {round(accuracy, 2)}% \n"
            f"click r to restart"
            )
        label.config(bg="#121212", fg="#10B981", text=results)
        
        scores=[]
        lines=[]
        tampered=False
        cntnt=""
        try:
            with open(file, "r") as f:
                cntnt=f.read()
                if "hash" in cntnt:
                    scpart, svhash=cntnt.split("hash", 1)
                    check=hashlib.sha256((scpart+secret).encode()).hexdigest()
                    if check==svhash.strip():
                        for i in scpart.split("\n"):
                            cleaned=i.strip().replace("%", "")
                            if cleaned:
                                if ". " in cleaned:
                                    cleaned=cleaned.split(". ")[1]
                            scores.append(float(cleaned))
                    else:
                        tampered=True
                        print("yo cheater. all ur results have been removed rofl. beginning from start :skull")
                
        except FileNotFoundError:
            pass

        if not tampered:
            scores.append(accuracy)
        else:
            scores=[accuracy]
        scores.sort(reverse=True)


        for i, s in enumerate(scores):
            lines.append(f"{i+1}. {s}%")
        data="\n".join(lines)
        tamper=hashlib.sha256((data+secret).encode()).hexdigest()
        
        with open(file, "w") as f:
            f.write(data+"\nhash\n"+tamper)

def three():
    label.config(text="3")

def two():
    label.config(text="2")

def one():
    label.config(text="1")

def begin(): #to begin code, restart functionality
    global randtime, total, pressed, done, userstart, attempt, totaltime, restart_done, userduration
    actual=0
    randtime=round(random.uniform(1.0, 4.0),2)
    fade = (len(colors)-1)*10
    totaltime=fade/1000+randtime
    userstart=0.0
    userduration=0.0
    pressed=True
    done=False
    restart_done=False
    attempt=False
    total=int(((4.4+randtime)*1000))
    total=3600+int(randtime*1000)+fade

    label.config(text="determine the length of the flash", bg="#FFFFFF", fg="#000000")
    root.after(1500, three)
    root.after(2500, two)
    root.after(3500, one)
    root.after(4500, color_on)
    root.after(4500+int(randtime*1000), lambda:color_change(number))

def restart(event): #restart
    global done, restart_done
    if done and restart_done:
        begin()
    if not restart_done:
        return

root=tk.Tk()
root.geometry("400x400")
label=tk.Label(root)
label.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
root.bind("<KeyPress-space>", spacedown)
root.bind("<KeyRelease-space>", spaceup)
root.bind("<KeyPress-r>", restart)

begin()
root.mainloop()
