
import csv
from roster import Team

class UI():

    def Window(self, Players):    
        Teams = Team().Read_teams(Players)
        
        # Lets make window and gieve it a size
        window = Tk.Tk()
        window.configure(background='gray')
        window.geometry('600x400+500+300')
        window.title('LoL_Calculator')

        Team_list = []

        for item in Teams:
            Team_list.append(item)
        
        self.team1 = Tk.StringVar(window)
        self.team1.set(Team_list[0])
        self.team2 = Tk.StringVar(window)
        self.team2.set(Team_list[0])

        team1 = Tk.OptionMenu(window, self.team1, *Team_list)
        team2 = Tk.OptionMenu(window, self.team2, *Team_list)
        team1.pack()
        team2.pack()
	
        button1 = Tk.Button(window, text = 'Get Elo',
                            command=lambda: self.Output1(Teams))
        button1.pack()
        button2 = Tk.Button(window, text = 'Get Elo',
                            command=lambda: self.Output2(Teams))
        button2.pack()
        
        Tk.mainloop()

        return Teams
        
    def Output1(self, Teams):
	   print '{}'.format(Teams[self.team1.get()].Out(self.team1.get()))

    def Output2(self, Teams):
       print '{}'.format(Teams[self.team2.get()].Out(self.team2.get()))

UI().Window()


