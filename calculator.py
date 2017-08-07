import math
try:
    from Tkinter import *  # python 2.x
except ImportError:
    from tkinter import *  # python 3.x


class Calculator(Frame):

    digits = [str(i) for i in range(10)] + ["."]
    operators = ["+", "-", "*", "/", "1/x", "+/-", "sin", "cos", "tan", "y^x", "%", "e^x", "log"]
    others = ["C", "ENTER", "AC", "pi", "SWAP", "POP"]
    font1 = "Verdana 11"    
    font2 = "Verdana 16" 
    buttons = dict()
    operationPressed = False
    stack = []  
    isAnErrorHappened = False
    errorMessages = {"stackError": "Error: not enough args in stack",
                     "divisionByZero": "Error: division by zero ",
                     "domainError": "Error: cannot complete calculation",
                     "overflow": "Error: oveflow"}

    def __init__(self, master):
        Frame.__init__(self, master)
        master.wm_title("RPN Calculator v1.0")
        master.resizable(width=False, height=False)
        self.pack()
        self.create_widgets()
        self.bind_keys(master)

    def create_widgets(self):
        self.onDisplay = StringVar()
        self.onDisplay.set("")
        self.onStackDisplay = StringVar()
        self.onStackDisplay.set("[  ]")
        self.isDegrees = BooleanVar()
        self.isDegrees.set(True)

        self.display = Label(self,
                             textvariable=self.onDisplay,
                             font=self.font2,
                             bg="white",
                             borderwidth=5,
                             relief="groove",
                             width=48,
                             height=2,
                             anchor=E)


        self.stackLabel = Label(self,
                                text="Stack:",
                                font=self.font1,
                                width=8,
                                anchor=W,
                                height=2)

        self.stackDisplay = Label(self,
                                  textvariable=self.onStackDisplay,
                                  font=self.font1,
                                  fg="royal blue",
                                  width=32,
                                  anchor=W,
                                  height=2)


        for digit in self.digits:
            self.buttons[digit] = Button(self,
                                         text=digit,
                                         font=self.font1,
                                         command=lambda d=digit: self.add_to_display(d),
                                         width=8,
                                         height=2)

        for operator in self.operators:
            self.buttons[operator] = Button(self,
                                            text=operator,
                                            font=self.font1,
                                            command=lambda o=operator: self.perform_operation(o),
                                            width=8,
                                            height=2)

        for other in self.others:
            if other == "ENTER":
                command = self.press_ENTER
            elif other == "AC":
                command = self.press_AC
            elif other == "C":
                command = self.press_C
            elif other == "pi":
                command = self.press_PI
            elif other == "POP":
                command = self.press_POP
            elif other == "SWAP":
                command = self.press_SWAP 


            self.buttons[other] = Button(self,
                                       text=other,
                                       font=self.font1,
                                       command=command,
                                       width=8,
                                       height=2)

        self.degreesRadioButton = Radiobutton(self,
                                              text="DEG",
                                              width=8,
                                              height=2,
                                              variable=self.isDegrees,
                                              value=True
                                              )


        self.radiansRadioButton = Radiobutton(self,
                                              text="RAD",
                                              width=8,
                                              height=2,
                                              variable=self.isDegrees,
                                              value=False
                                              )
        self.render_layout()

    def render_layout(self):

        self.display.grid(row=0, column=0, columnspan=6, sticky=W)
        self.stackLabel.grid(row=1, column=0, sticky=W)        
        self.stackDisplay.grid(row=1, column=1, columnspan=3, sticky=W)

        self.buttons["AC"].grid(row=2, column=0, sticky=W)
        self.buttons["C"].grid(row=2, column=1, sticky=W)
        self.buttons["ENTER"].grid(row=6, column=3, sticky=W)
        self.buttons["POP"].grid(row=1, column=4, sticky=W)
        self.buttons["SWAP"].grid(row=1, column=5, sticky=W)

        self.buttons["."].grid(row=6, column=1, sticky=W)
        self.buttons["0"].grid(row=6, column=0, sticky=W)       
        self.buttons["1"].grid(row=5, column=0, sticky=W)
        self.buttons["2"].grid(row=5, column=1, sticky=W)
        self.buttons["3"].grid(row=5, column=2, sticky=W)
        self.buttons["4"].grid(row=4, column=0, sticky=W)
        self.buttons["5"].grid(row=4, column=1, sticky=W)
        self.buttons["6"].grid(row=4, column=2, sticky=W)
        self.buttons["7"].grid(row=3, column=0, sticky=W)
        self.buttons["8"].grid(row=3, column=1, sticky=W)
        self.buttons["9"].grid(row=3, column=2, sticky=W)

        self.buttons["*"].grid(row=2, column=3, sticky=W)
        self.buttons["/"].grid(row=3, column=3, sticky=W)
        self.buttons["+"].grid(row=4, column=3, sticky=W)
        self.buttons["-"].grid(row=5, column=3, sticky=W)
        self.buttons["1/x"].grid(row=4, column=4, sticky=W)
        self.buttons["+/-"].grid(row=6, column=2, sticky=W)
        self.buttons["%"].grid(row=2, column=2, sticky=W)
        self.buttons["y^x"].grid(row=5, column=4, sticky=W)
        self.buttons["sin"].grid(row=2, column=5, sticky=W)
        self.buttons["cos"].grid(row=3, column=5, sticky=W)
        self.buttons["tan"].grid(row=4, column=5, sticky=W)
        self.buttons["pi"].grid(row=5, column=5, sticky=W)
        self.buttons["e^x"].grid(row=2, column=4, sticky=W)
        self.buttons["log"].grid(row=3, column=4, sticky=W)

        self.degreesRadioButton.grid(row=6, column=4, sticky=W)
        self.radiansRadioButton.grid(row=6, column=5, sticky=W)

    def bind_keys(self, master):
        for digit in self.digits:
            master.bind(digit, self.add_to_display)

        master.bind(".", self.add_to_display)
        master.bind("<Return>", self.press_ENTER)

        master.bind("+", self.perform_operation)
        master.bind("-", self.perform_operation)
        master.bind("*", self.perform_operation)
        master.bind("/", self.perform_operation)
        master.bind("%", self.perform_operation)
        master.bind("<BackSpace>", self.press_DELETE)

    def add_to_display(self, value):
        
        if self.isAnErrorHappened:
            self.press_C()

        if self.operationPressed:
            self.press_ENTER()
            self.press_C()

        if isinstance(value, Event): # Input via keyboard rather than clicking on app
            value = value.char
        if not(value == "." and value in self.onDisplay.get()): 
            self.onDisplay.set(self.onDisplay.get() + value)

        self.operationPressed = False
        self.isAnErrorHappened = False

    def press_DELETE(self, event=None):
        if self.onDisplay.get() not in self.errorMessages.values():
            self.onDisplay.set(self.onDisplay.get()[:-1])
        else:
            self.press_C()

    def press_SWAP(self):
        if self.onDisplay.get() and len(self.stack) > 0:
            b, self.stack[-1] = self.stack[-1], self.onDisplay.get(), 
            self.onDisplay.set(b)
            self.refresh_stack_display()

    def press_POP(self):
        if len(self.stack) > 0:
            self.stack.pop()
            self.refresh_stack_display()

    def press_C(self):
        self.onDisplay.set("")

    def press_PI(self):
        self.press_ENTER()
        self.onDisplay.set("{}".format(math.pi))

    def refresh_stack_display(self):
        self.onStackDisplay.set("[ {} ]".format(", ".join(self.stack[::-1])))

    def press_ENTER(self, event=None):
        if self.onDisplay.get() and self.onDisplay.get() not in self.errorMessages.values():
            self.stack.append(self.onDisplay.get())
            self.press_C()
            self.refresh_stack_display()            

    def press_AC(self):
        self.stack = []
        self.press_C()
        self.refresh_stack_display()

    def perform_operation(self, operator):
        if self.onDisplay.get() in self.errorMessages.values():
            return
        try:
            if isinstance(operator, Event): # Input via keyboard rather than clicking on app
                operator = operator.char

            if operator in ["+", "-", "*", "/", "y^x", "%"]:
                if self.onDisplay.get():
                    x = float(self.onDisplay.get())
                    y = float(self.stack.pop())
                else:
                    x = float(self.stack.pop())
                    y = float(self.stack.pop())

                if operator == "+":
                    self.onDisplay.set("{}".format(round(y + x, 10)))
                elif operator == "-":
                    self.onDisplay.set("{}".format(round(y - x, 10)))
                elif operator == "*":
                    self.onDisplay.set("{}".format(round(y * x, 10)))
                elif operator == "/":
                    self.onDisplay.set("{}".format(round(y / x, 10)))
                elif operator == "y^x":
                    self.onDisplay.set("{}".format(round(y**x, 10))) 
                elif operator == "%":
                    self.onDisplay.set("{}".format(round(x/100.0 * y, 10)))                           
            else:
                if self.onDisplay.get():
                    x = float(self.onDisplay.get())
                else:
                    x = float(self.stack.pop())

                if operator == "1/x":
                    self.onDisplay.set("{}".format(round(x**-1, 10)))
                elif operator == "+/-":
                    self.onDisplay.set("{}".format(round(-x, 10)))
                elif operator == "sin":
                    conversionFactor = math.pi/180 if self.isDegrees.get() else 1
                    self.onDisplay.set("{}".format(round(math.sin(conversionFactor * x), 10)))
                elif operator == "cos":
                    conversionFactor = math.pi/180 if self.isDegrees.get() else 1
                    self.onDisplay.set("{}".format(round(math.cos(conversionFactor * x), 10)))  
                elif operator == "tan":
                    conversionFactor = math.pi/180 if self.isDegrees.get() else 1
                    self.onDisplay.set("{}".format(round(math.tan(conversionFactor * x), 10)))
                elif operator == "e^x":
                    self.onDisplay.set("{}".format(round(math.exp(x), 10)))
                elif operator == "log":
                    self.onDisplay.set("{}".format(round(math.log(x), 10)))

            self.operationPressed = True
            self.isAnErrorHappened = False
            self.refresh_stack_display()
        except IndexError:  # There isn't enough args in the stack to do the operation
            self.press_ENTER()
            self.onDisplay.set(self.errorMessages["stackError"])
            self.isAnErrorHappened = True
            self.refresh_stack_display()
        except ZeroDivisionError:  # Division by zero
            self.onDisplay.set(self.errorMessages["divisionByZero"])
            self.isAnErrorHappened = True
            self.refresh_stack_display()
        except ValueError:
            self.onDisplay.set(self.errorMessages["domainError"])
            self.isAnErrorHappened = True
            self.refresh_stack_display()
        except OverflowError:
            self.onDisplay.set(self.errorMessages["overflow"])
            self.isAnErrorHappened = True
            self.refresh_stack_display()

if __name__ == "__main__":
    root = Tk()
    app = Calculator(root)
    app.mainloop()
