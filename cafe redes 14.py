# BY CAMERON BADMAN


import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import sqlite3
from functools import partial
import tkinter as tkr
import datetime
import csv
import os
import tempfile
import reportlab
from reportlab.pdfgen import canvas as cancan
from tkinter import messagebox
#declarations
expression =""
changeray11 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, ".", "X"]
connection = sqlite3.connect("cafe database.db")
cursor = connection.cursor()
state = 1
category = []
query = "SELECT distinct category from Products"   
for record in cursor.execute(query):
    record =''.join(record)
    category.append(record)
buttoniden = []
amountchanges = 0
byocstate = "No"
defaultoptionray = []
defaultoptionrayidentiofier = 0
adfunctionstate = 0
categoricaloption = ""
optionselected = "default"
totalglobalprice = []
globalitems = []
pricetotal = 0
priceidentifier = 0
totalcolate = []
frequency = 0
color1 = "#585f68"
color2 = "#192a4f"
backupdatabase =[[],[],[],[],[],[]]
tablequery = 0
printtest = [[],[],[],[]]
totalpriceadd = 0



   
 
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #creates frames
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, CafeHomePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        #sets the start page
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#353537")
        self.controller = controller
        global test, test1
        #check that each item has a default settting in the foodoptions database
        query = """SELECT products.Name, products.category
                  FROM products
                  where not exists( select*
                                  from foodoptions
                                  where products.Name = foodoptions.food
                                  and foodoptions.options = "Default" and foodoptions.category != "Hot Drinks")"""
        for food, category in cursor.execute(query):
           
          if category == "Hot Drinks":
              #hot drinks runs on the coffe sys, not a the universal categorical system that everything else runs on 
            pass
          else:
            defaultoptionray.append([category, food, "Default", "0"])
            #append variables to a array for them to be set into the table
        for items in defaultoptionray:
            #items without a current default option are given one
          cursor.execute("INSERT INTO foodoptions (category, food, options, Price) VALUES (?,?,?,?)", items)
          connection.commit()

                                    
        def clear(n):
            #the clear function used universaly to 2 layer frame (menaFrame, recieptframe)
            list = n.place_slaves()
            for l in list:
                #destroys the frames
                l.destroy()
        def addclear(n, priceidentifier):
            #clears information in a 4th layer from in the reciet frame, allowing for dynamic deletion
          global expression, totalglobalprice, globalitems
          #resets the variables to zero for the items to not clutter
          totalglobalprice[priceidentifier] = 0
          globalitems[priceidentifier] = 0
          #refresh items
          globaltotallabel.config(text =str(sum(totalglobalprice)))
          totalglobalpricesum = sum(totalglobalprice)
          globaltotallabel.config(text =str(totalglobalpricesum))
          #destroying the frame
          n.destroy()

        def addfunc(Name, addfuncstate, price):
            #addfunc is run through both the categorical options, and the coffe frame for effieciency
                global amounts, categoricaloption, optionselected, totalglobalprice, pricetotal, priceidentifier, expression, globalitems
                #getting variables ready to be added to the frames
                frame1123 = LabelFrame(frame, text=Name, width=60, height=1, bg = color1, fg = "white")
                frame1123.pack(anchor=NW, pady=3)
                totalglobalprice.append(price)
                totalglobalpricesum = sum(totalglobalprice)
                globaltotallabel.config(text =str(totalglobalpricesum))
                globalitems.append(Name)
                print(globalitems)
                print (totalglobalprice)
                #activates if the system recieves a funcstate of 0 which is coffee sys
                if addfuncstate == 0:
                  message_W=Label(frame1123, text="byoc:   " + byocstate, bg = color1, fg = "white")
                  message_W.pack(anchor=NW)
                  message_W=Label(frame1123, text="Extras:", bg = color1, fg = "white")
                  message_W.pack(anchor=NW)
                  message_W=Label(frame1123, text="vanila:    " + str(amounts[0]), bg = color1, fg = "white")
                  message_W.pack(anchor=NW, padx = 10)
                  message_W=Label(frame1123, text="Hazelnut:  " + str(amounts[1]), bg = color1, fg = "white")
                  message_W.pack(anchor=NW, padx = 10)
                  message_W=Label(frame1123, text="caramel:   " + str(amounts[2]), bg = color1, fg = "white")
                  message_W.pack(anchor=NW, padx = 10)
                  message_W=Label(frame1123, text="extrashot: " + str(amounts[3]), bg = color1, fg = "white")
                  message_W.pack(anchor=NW, padx = 10)
                  message_W=Button(frame1123, text="X", width = 60, bg = "RED", fg = color1, command = partial(addclear, frame1123, priceidentifier))
                  message_W.pack(anchor=SW)
                # activates if the system gets a funcstate input of 1 which is categorical sys
                else:
                  message_W=Label(frame1123, text="Extra:", bg = color1, fg = "white")
                  message_W.pack(anchor=NW)
                  message_W=Label(frame1123, text=optionselected
                                  , bg = color1, fg = "white")
                  message_W.pack(anchor=NW)
                  message_W=Button(frame1123, text="X", width = 60, bg = "RED", fg = "white", command = partial(addclear, frame1123, priceidentifier))
                  message_W.pack(anchor=E)
                priceidentifier = priceidentifier + 1
                #floats the sum to creat the change messure, also to allow for negative numbers
                try:
                  amountchanges =  float(expression) - float(sum(totalglobalprice))
                  changegivenlabel.config(text = amountchanges)
                except:
                  changegivenlabel.config(text = "Invalid")
                
        #creates the buttons form a perspective category, this method was used to create pliability in the program                         
        def creation(cat, bg, fg):          
            clearob = partial(clear, menaFrame)
            clearob()
            menaFrame.config(bg = bg)
            #preparing the program for usage
            category = "'" + cat + "'"
            #query for the sysem button colors (easily manipulated in the database)
            query = """select products.ID, products.Name, products.Category, products.Price, buttoncolors.fg, buttoncolors.bg
            from products, buttoncolors
            where products.category = buttoncolors.corres and products.Category = """ + category + """ 
            order by products.ID"""
            col = 30
            row = 50
        #dynamicly creates the buttons, in a loop to keep them neatly inside the frame
            for record in cursor.execute(query):
                ID, Name, cat, price, fg, bg = record
                names = Button(menaFrame, text = Name + " - $"  + str(price), fg = fg, bg = bg, width = 19, height = 2, command = partial(change, cat, Name, price))
                names.place (y = row, x = col)
                buttoniden.append(names)
                

                if col == 320:
                    col = 30
                    row = row + 100

                else:
                    col = col + 145
        #changes the options screen dependant on category in the system
        def change(cat, Name, price):
            global baseprice, name
            if cat == "Hot Drinks":
                command = partial(Hotdrinks, Name, price,cat)
                command()
            else:
                command = partial(categoricaloptions, Name, price, cat)
                command()
        # the cateogorical system uses a food options table in the datbase   
        def categoricaloptions(Name, baseprice, cat):
            global baseprices, optionselected, totalglobalprice, pricetotal
            baseprices = baseprice
            print (baseprice)
            #clear frame
            clearob = partial(clear, optionFrame)
            clearob()
            print (pricetotal)
            print (pricetotal)
            #add button leading to the addfunc with a partial command to allow for dynamic usage
            
            buttonidentites = []
            IDentity = 0
            y = 100
            #calculates price
            def priice():
               global priices, baseprices, cat, pricetotal
               pricetotal = priices + baseprices
               total.config(text = "Total:  " + str(pricetotal))
            #sets the default choice to a the select color and sets the color to the new color when pressed
            def choices(ID, option, price, name):
              global priices, optionselected
              if name == "default":
                buttonidentites[ID].config (bg = "#adff2f", fg = "black")
                optionselected = str(option)
              else:
                pass
              priices = price
              for buttons in buttonidentites:
                buttons.config(bg = "#0000a5", fg = "white")
              buttonidentites[ID].config (bg = "#adff2f", fg = "black")
              optionselected = str(option)
              
              priice()
            print (pricetotal)
            addingbut = Button(optionFrame, text ="Add", width = 8, height = 1, font=('Helvetica', 20, 'bold'), bg = "#0000a5", fg = "white", anchor = NW, command= lambda: addfunc(Name, 1, baseprices))
            addingbut.place (x = 415, y = 912)
            
               
               

          
            
            for optionss in cursor.execute("""select options, price, category
                                          from foodoptions
                                          where food = """ + "'" + str(Name) + "'" + "and category =" "'" + str(cat) + "'"):
                option, price, category = optionss
                option =  ''.join(option)
                if option == "Default":
                  addingbut = Button(optionFrame, text = option, width = 20, height = 2, font=('Helvetica', 15, 'bold'), bg = "#adff2f", fg = "black", command = partial(choices, IDentity, option, price, option))
                  addingbut.place (x = 10, y = y)
                  optionselected = str(option)
                else:
                  addingbut = Button(optionFrame, text = option, width = 20, height = 2, font=('Helvetica', 15, 'bold'), bg = "#0000a5", fg = "white", command = partial(choices, IDentity, option, price, option))
                  addingbut.place (x = 10, y = y)
                  optionselected = str(option)
                y = y + 100
                buttonidentites.append(addingbut)
                IDentity = IDentity + 1
            
            options = Label(optionFrame, text = "Options:  " + Name , bd = 0, width = 35, height = 1, anchor = NW, bg = color1, fg = "white", font=('Helvetica', 20, 'bold'))
            options.place (x = 0, y = 0)
            extraoptions = Label(optionFrame, text = "Extra Options:" ,bd = 1, width = 20, height = 1, anchor = NW, bg = color1, fg = "white", font=('Helvetica', 20, 'bold'))
            extraoptions.place (x = 0, y = 50)
            total = Label(optionFrame, text ="Total:  " + str(baseprice), width = 15, height = 1, font=('Helvetica', 20, 'bold'), bg = "#0000a5", fg = "white")
            total.place (x = 15, y = 912)
            


        def Hotdrinks(Name, baseprice, cat):
            global status, amounts, byocTRIG, sizep, totalprice
            amounts = [0,0,0,0]
            extras = ["vanilla","Hazelnut","Caramel","Extrashot"]
            sizep = 0
            byocTRIG = 0
            clearob = partial(clear, optionFrame)
            clearob()
            status = 1
            
            
            def byoc():
                global status, byocTRIG, byocstate
                
                if status == 0:                    
                    BYOCButton.config (text="BYOC",  bg = color2, fg = "white")
                    status = 1
                    byocTRIG = - 0.5
                    byocstate = "No"
                else:   
                    BYOCButton.config (text="Stock",bg = "#adff2f", fg = "black")
                    status = 0
                    byocTRIG = 0
                    byocstate = "Yes"
                totalpriceitem()
                                
            def negativeam (n, i):
                nn = extras.index(n)
                amounts[nn] = amounts[nn] + 1
                bname = (button_identities[i])
                bname.config(text = amounts[nn])
                totalpriceitem()
                

            def positiveam (n, i):
                nn = extras.index(n)
                if amounts[nn] == 0:
                    pass
                else:
                    amounts[nn] = amounts[nn] - 1
                    
                bname = (button_identities[i])
                bname.config(text = amounts[nn])
                totalpriceitem()
                
            def sizefunc(n):
                global sizep
                sizes = [0, 0.5, 1]
                for buttons in button_identities1:
                    buttons.config (bg = color2, fg = "white")
                    button_identities1[n].config (bg = "#adff2f", fg = "black")
                sizep =  sizes[n]
                totalpriceitem()
            itemsy = 10
            reciept_identities = []
            
                        
            
            

            total = Label(optionFrame, text ="", width = 15, height = 1, font=('Helvetica', 20, 'bold'), bg = color2, fg = "white")
            total.place (x = 15, y = 912)
            def totalpriceitem():
               global byocTRIG, itempricetotal, amounts, sizep, amountchanges, pricetotal
               pricetotal = (baseprice + sizep + 0.5*sum(amounts) - byocTRIG)
               total.config(text = "Item Price:  $" + str(pricetotal))
            totalpriceitem()
        
            addingbut = Button(optionFrame, text ="Add", width = 8, height = 1, font=('Helvetica', 20, 'bold'), bg = color2, fg = "white", anchor = NW, command=partial (addfunc, Name, 0, pricetotal))
            addingbut.place (x = 415, y = 912)
            options = Label(optionFrame, text = "Options:" + Name ,bd = 0, width = 35, height = 1, anchor = NW, bg = color1, fg = "white", font=('Helvetica', 20, 'bold'))
            options.place (x = 0, y = 0)
            
            extraoptions = Label(optionFrame, text = "Extra Options:" ,bd = 1, width = 20, height = 1, anchor = NW, bg = color1, fg = "white", font=('Helvetica', 20, 'bold'))
            extraoptions.place (x = 0, y = 50)            
            BYOCButton = Button(optionFrame, text ="BYOC", width = 8, height = 1, font=('Helvetica', 20, 'bold'), bg = color2, fg = "white", anchor = NW, command=byoc)
            BYOCButton.place (x = 5 , y = 100)
            amounts = [0,0,0,0]
            
            yaxe1 = 185
            yaxe2 = 160
            yaxe3 = 5
            am = 0
            idenity = 0
            button_identities = []
            button_identities1 = []
            for extra in extras:
                negative = Button(optionFrame, text = "-1", relief = FLAT, width = 0, height = 0, font=('Helvetica', 25, 'bold'), bg = color2, fg = "white", command = partial(positiveam, extra, idenity ))
                negative.place(x = 5 , y = yaxe1)

                extra1 = Label(optionFrame, text = extra + ":", width = 10, height = 0, font=('Helvetica', 10, 'bold'), bg = color2, fg = "white")
                extra1.place(x = 5 , y = yaxe2)

                amount = Button(optionFrame, text = "+1", relief = FLAT, width = 0, height = 0, font=('Helvetica', 25, 'bold'), bg = color2, fg = "white", command = partial(negativeam, extra, idenity))
                amount.place(x = 195 , y = yaxe1)

                lvl = Label(optionFrame, text = amounts[0], width = 5, height = 0, font=('Helvetica', 25, 'bold'), bg = color2, fg = "white")
                lvl.place(x = 75 , y = yaxe1)
                idenity = idenity + 1

                button_identities.append(lvl)

                yaxe1 = yaxe1 + 95
                yaxe2 = yaxe2 + 95
                am = am + 1
            idenity = 0
            sizes = ["Small", "Medium", "Large"]
            
            for size in sizes:
                sizebut = Button(optionFrame, text = size, width = 7, height = 0, font=('Helvetica', 15, 'bold'), bg = color2,  relief = FLAT, fg = "white", command = partial(sizefunc, idenity))
                sizebut.place(x = yaxe3 , y = 540)
                yaxe3 = yaxe3 + 95
                button_identities1.append(sizebut)
                idenity = idenity + 1
            button_identities1[0].config (bg = "#adff2f", fg = "black")

        menaFrame = Frame(self, parent, width=458, height=971, bg=color1, highlightthickness=0.5, highlightbackground="#7A8663")
        menaFrame.place(y=10, x=109)

        optionFrame = Frame(self, parent, width=564, height=971, bg = color1, highlightthickness=0.5, highlightbackground="#7A8663")
        optionFrame.place(y=10, x=575)

        recieptFrame = Frame(self, parent, width=589, height=934, bg = color1, highlightthickness=0.5, highlightbackground="#7A8663")
        recieptFrame.place(y=10, x=1148)
        
        canvas1 = Canvas(self, width=125, height=971,highlightthickness=0, bg = color1)
        canvas1.place(x = 0, y = 10)
        
        scrollframe1 = Frame(recieptFrame, width=526, height=300, highlightthickness=0.5, highlightbackground="#7A8663", bg =color1)
        scrollframe1.place(x = 10, y = 10)
        scrollframe1.pack_propagate(0)
        
        canvas = Canvas(scrollframe1, bg = "#8b92ac", highlightthickness=0.5, highlightbackground="#8b92ac")
        canvas.pack(fill=BOTH, expand=True)
        frame = Frame(canvas, bg="#8b92ac")

        canvas.update_idletasks()
        canvas_frame = canvas.create_window((0,0), anchor='nw', window = frame)

        vsb = Scrollbar(canvas, orient="vertical", command = canvas.yview)
        vsb.pack(anchor=E, expand=True, fill="y")    

        def FrameWidth(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width = canvas_width)

        def OnFrameConfigure(event):
            canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand = vsb.set)

        frame.bind('<Configure>', OnFrameConfigure)
        canvas.bind('<Configure>', FrameWidth)

        changeFrame = Frame(recieptFrame, width=258, height=450, highlightthickness=0.5, highlightbackground="#7A8663", bg =color2)
        changeFrame.place(x = 10, y = 350)

        
        changeframey = 35
        changeframex = 5
        
        
        changelabel = Label(changeFrame, width=33, height=1, highlightthickness=0.5, highlightbackground="white", bg ="white", fg = "black")
        changelabel.place(x = 5, y = 10)
        changegivenlabel = Label(changeFrame, text=amountchanges, width=5, height=1, highlightthickness=0.5, font=('Helvetica', 20, 'bold'), highlightbackground="white", bg =color2, fg = "white")
        changegivenlabel.place(x = 5, y = 400)

        dynamictotalprice = Frame(recieptFrame, width=258, height=450, highlightthickness=0.5, highlightbackground="#7A8663", bg =color2)
        dynamictotalprice.place(x = 280, y = 350)

        globaltotallabel1 = Label(dynamictotalprice, text="Final Price:", anchor = W, width=8, font=('Helvetica', 15, 'bold'), bg =color2, fg = "white")
        globaltotallabel1.place(x = 10, y = 10)
        
        globaltotallabel = Label(dynamictotalprice, text=str(sum(totalglobalprice)), anchor = W, width=8, font=('Helvetica', 15, 'bold'), bg =color2, fg = "white")
        globaltotallabel.place(x = 10, y = 50)

        corfirmframe = Frame(recieptFrame, width=526, height=115, highlightthickness=0.5, highlightbackground="#7A8663", bg =color2)
        corfirmframe.place(x = 10, y = 810)
        def confirmorder(printiden):
          global totalglobalprice, globalitems, totalcolate, frequency, priceidentifier, pricetotal
          order = ["Confirm Order:", "print and Confirm Order"]
             
          
          totalcolate = []
          pdf_file = 'reciept.pdf'
          can = cancan.Canvas(pdf_file)
          YY = 770
          filename = tempfile.mktemp("text.txt")
          file = open(filename, "w")
          if totalglobalprice== []:
            pass
            print("1")
          else:
             MsgBox = tk.messagebox.askquestion (order[int(printiden)],icon = 'warning')
             if MsgBox == 'yes':
                currentDT = datetime.datetime.now()
                for totalglobalprice, globalitems in zip(totalglobalprice, globalitems):
                  if globalitems == 0:
                    pass
                  else:
                      
                    totalcolate.append([globalitems, totalglobalprice, currentDT.strftime("%Y/%m/%d"), currentDT.strftime("%H:%M:%S")])
                    file.write(globalitems + "|"+ str(totalglobalprice) + "|" + str(currentDT.strftime("%Y/%m/%d")) + "\n")
                
                
                if printiden == "1":
                    file.close()
                    os.startfile(filename, "print")
                else:
                    pass

                for colate in totalcolate:
                    cursor.execute("INSERT INTO confirmedpurchases (Item, Price, Date, Time) VALUES (?,?,?,?);", colate)
                    connection.commit()

                can.showPage()
                can.save()
                  
                list = frame.pack_slaves()
                for l in list:
                    l.destroy()
                totalglobalprice = []
                value = 0
                for values in totalglobalprice:
                  totalglobalprice[value] = 0
                  value = value + 1
                  
                globalitems = []
                priceidentifier = 0
                globaltotallabel.config(text =str(sum(totalglobalprice)))
             else:
                 pass
                     
          

              
          


        confirmorder1 = Button(corfirmframe, bd = 1, bg =color1, fg = "white", width = 25, text = "Print and Confirm Order:", anchor = W, font=('Helvetica', 15, 'bold'), relief="solid", command = partial(confirmorder, "1"))
        confirmorder1.place(x = 10, y = 60)

        confirmorder = Button(corfirmframe, bd = 1, bg =color1, fg = "white", width = 25, text = "Confirm Order:", anchor = W, font=('Helvetica', 15, 'bold'), relief="solid", command = partial(confirmorder, "0"))
        confirmorder.place(x = 10, y = 10)

        
        
        

        def calcchange(n):
           global expression, totalprice
           if n == "X":
            expression = expression[:-1]
           else:
               expression = expression + str(n) 
           changelabel.config(text = expression)
           amountchanges = 0
           if expression == "":
              changegivenlabel.config(text = "Invalid") 
           else:
              amountchanges =  float(expression ) - float(sum(totalglobalprice))
              if amountchanges < 0:
                changegivenlabel.config(text = "Invalid")
              else:
                changegivenlabel.config(text = amountchanges)
           
        for numberals in changeray11:
             changebutton = Button(changeFrame, text = numberals,bd = 3, width = 3, height = 0, font=('Helvetica', 25, 'bold'), bg = color1, fg = "white",command = partial(calcchange, numberals), highlightthickness=0.5, highlightbackground="#7A8663")
             changebutton.place(x = changeframex , y = changeframey)
             
             

             if changeframex == 175:
                changeframey = changeframey + 85
                changeframex = 5
             else:
                changeframex = changeframex + 85
 
        maincatx = 0
        maincaty = 0
        query = """SELECT distinct (products.Category), programcolors.fg, programcolors.bg
        from products, programcolors
        where products.category = programcolors.corres
        order by programcolors.ID desc"""
        for record in cursor.execute(query):
            category, fg, background = record
            
            categorybutton = Button(canvas1, text = category,bd = 3, width = 12, relief = "flat", height = 2, font=('Helvetica', 13, 'bold'), bg=background, fg=fg,
                                    command = partial(creation, category, background, fg))                                                                                                                                    
            categorybutton.place(x =0 , y = maincaty)
            maincaty = maincaty + 50
            partial(creation, "Food", "#FFFFFF")
        button = tk.Button(self, text="Return To HomeScreen", command=lambda: controller.show_frame("CafeHomePage"), bg = color2, width = 20, height = 2, fg = "white")
        button.place(x=1535, y=945)
          
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#353537")
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        
        Smalll = Button(self, text = "S",bd = 3, width = 2, height = 1)
        Smalll.place(x=0, y=0)

        button = tk.Button(self, text="""Return To Home Screen""",
                           command=lambda: controller.show_frame("PageOne"))
        button.place()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#353537")
        self.controller = controller

        
          
        
        
class CafeHomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#353537")
        self.controller = controller
        label = tk.Label(self, text="Cafe Main Menu", font=controller.title_font, width = 200, anchor = W)
        label.place (y = 10, x = 0)
        
        button11 = Button(self, text="Corinda Cafe", height = 38, width = 60, bg = color1, fg ="white", font=('Helvetica', 15, 'bold'),
                           command=lambda: controller.show_frame("StartPage"))
        button11.place(x = 10, y = 55)
        
        tablenameray = ["Products", "Confirmedpurchases", "Buttoncolors", "Foodoptions", "Programcolors"]
        tableray = ["SELECT * FROM Products", "SELECT * FROM confirmedpurchases order by id asc", "SELECT * FROM buttoncolors", "SELECT * FROM foodoptions", "SELECT * FROM programcolors"]
        insert = ["INSERT INTO Products VALUES (?, ?, ?, ?)", "INSERT INTO confirmedpurchases VALUES (?, ?, ?, ?, ?)", "INSERT INTO buttoncolors (?, ?, ?)", "INSERT INTO foodoptions VALUES (?, ?, ?, ?)", "INSERT INTO programcolors VALUES (?, ?, ?, ?)"]
        storingray = []
        def tranfertoexcel(n):
            for items in cursor.execute(tableray[n]):
                storingray.append(items)
                with open(tablenameray[n] + '.csv', 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerows(storingray)
            os.startfile(tablenameray[n] + '.csv')
            storingray.clear()
            
       
        def reload(n):
            showALL2 = "DELETE FROM " + tablenameray[n]
            cursor.execute(showALL2)
            connection.commit()           
                
            with open(tablenameray[n] + '.csv', 'r', newline='') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                   newdata = row
                   cursor.execute(insert[n], newdata)
                   connection.commit()
        def phyprint():
            for Record in cursor.execute("select * from Products"):
                ID, Name, category, Price = Record                       
                printtest[0].append(ID)
                printtest[1].append(Name)
                printtest[2].append(category)
                printtest[3].append(Price)                           
            filename = tempfile.mktemp(".txt")
            open (filename , "w").write (str(printtest))
            os.startfile(filename, "print")

        
         

        
        buttonum = 0
        yaxiss = 55
        for objects in tablenameray: 
          firstButton = Button(self, text = "Excel Create: " + objects, bg = color1, fg = "white", font=('Helvetica', 15, 'bold'), width = 35, height = 4, command = partial(tranfertoexcel, buttonum))
          firstButton.place(x = 760, y = yaxiss)

          firstButton = Button(self, text = "Reload Data of " + objects, bg = color2, fg = "white", font=('Helvetica', 15, 'bold'), width = 35, height = 4, command = partial(reload, buttonum))
          firstButton.place(x = 1240, y = yaxiss)
          buttonum = buttonum + 1
          yaxiss = yaxiss + 150

        firstButton = Button(self, text = "print", bg = color2, fg = "white", font=('Helvetica', 15, 'bold'), width = 35, height = 4, command = phyprint)
        firstButton.place(x = 1240, y = yaxiss)




if __name__ == "__main__":
    app = SampleApp()
    #255.255.248.0
    

    
    
    app.geometry("1718x985+10+10")
    app.mainloop()
