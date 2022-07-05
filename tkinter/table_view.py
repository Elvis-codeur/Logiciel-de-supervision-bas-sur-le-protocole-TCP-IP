
from tkinter import *
from tkinter import ttk

ws = Tk()

ws.title("Table view")
ws.geometry("500x500")
ws["bg"] = "#AC99F2"




game_frame = Frame(ws)
game_frame.pack()


# Scrooll Bar
game_scroll = Scrollbar(game_frame)
game_scroll.pack(side = RIGHT,fill= Y)



my_game = ttk.Treeview(game_frame,
                        yscrollcommand=game_scroll.set,
                        )




game_scroll.config(command=my_game.yview)
game_scroll.config(command = my_game.xview)

my_game.pack()

columns = ("Player_id","player_name","player_rank","player_states","player_city")
m_header = ("","Id","Name","Rank","States","States")
my_game["columns"] = columns 

my_game.column("#0",width=0,stretch=0)

for i in columns:
    my_game.column(i,anchor = CENTER,width = 80)


for a, b in zip(columns,m_header):
    my_game.heading(a,text = b,anchor=CENTER)


for i in range(30):
    my_game.insert(parent="",index="end",iid = i,text = "",values=("{}".format(i),"Ninja","101","Oklahoma","Moore"))


my_game.pack()

ws.mainloop()