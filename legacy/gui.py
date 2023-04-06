from guizero import App, Text, TextBox, Box, PushButton

app = App(title="Log in")
open_message = Text(app, text="Welcome!", size=40, )
print(open_message)
Text(app, text="User ID: ",align="left", grid=[3,3])
instruct = Text(app, text="Please enter your ID number")
id_box = TextBox(app,instruct.disable(), width=25, align="left", grid=[3,4])
# app.set_full_screen()
app.display()
