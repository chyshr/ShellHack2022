import json

import openai
from tkinter import *
from tkinter.ttk import Combobox

from twilio.rest import Client
import requests

# create a blank window
root = Tk()
root.geometry("750x280+390+300")
root.title(string="Greeting AI")
root.configure(bg='#F5C7A9')



def close_win():
    root.destroy()

label = Label(root, text="Greeting AI", font=("Times New Roman", 40, "bold"), bg="#D1512D", fg="#F5C7A9")

def font_style():
    label.config(font=('Helvetica bold', 26))


label.pack(fill=X)

label_1 = Label(root, text="Sender Name", font=("Times New Roman", 20), bg="#F5C7A9")
label_2 = Label(root, text="Topic", font=("Times New Roman", 20), bg="#F5C7A9")
entry_1 = Entry(root)
entry_2 = Entry(root)

label_1.place(x=220, y=95)
label_2.place(x=220, y=130)
entry_1.place(x=350, y=95)
entry_2.place(x=350, y=130)
loaded = False

def openNewWindow():
    name = entry_1.get()
    topic = entry_2.get()
    root.destroy()
    toSendPhone = []
    toSendPeople = []


    def loadContact():
        print("load contact")
        global loaded
        loaded = True

        def Enter():
            group = options.get()
            print("Enter")
            with open("./data/ContactsName.json", "r") as read_file:
                nameData = json.load(read_file)
            contactPhoneList = data[group]
            contactNameList = nameData[group]
            toSendPeople.extend(contactNameList)
            toSendPhone.extend(contactPhoneList)

            load_pop_window.destroy()

        load_pop_window = Tk()
        load_pop_window.configure(bg='#F5C7A9')
        load_pop_window.title(string="Greeting AI")
        load_pop_window.geometry("350x100+600+400")

        choose_frame = Frame(load_pop_window)
        choose_frame.configure(bg='#F5C7A9')
        choose_frame.pack(pady=15)

        choose_cat_label = Label(choose_frame, text="Choose Category", font=("Times New Roman", 14), bg="#F5C7A9")
        choose_cat_label.pack(side='left')

        options = StringVar(choose_frame)
        options.set("One")
        with open("./data/ContactsPhone.json", "r") as read_file:
            data = json.load(read_file)

        option_menu = Combobox(choose_frame, textvariable=options,
                               values=list(data.keys()))
        option_menu.pack(side='left', padx=5)

        Enter_but = Button(load_pop_window, font=("Times New Roman", 16), text="Enter", fg="#D1512D", command=Enter)
        Enter_but.pack()

        load_pop_window.mainloop()

    def addContact():
        toSendPhone.append(entry_receiver_num.get())
        toSendPeople.append(entry_receiver_name.get())
        print("add contact")

    def callApis():
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': topic,
            },
            headers={'api-key': '9cd02ccb-5141-4ac1-95fd-428791514083'}
        )
        myUrl = r.json()['output_url']
        print(myUrl)

        for phoneNum, sendName in zip(toSendPhone, toSendPeople):
            openai.api_key = "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"

            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="write a " + topic + " greeting for " + str(sendName),
                temperature=1,
                max_tokens=850,
                top_p=1,
                frequency_penalty=2,
                presence_penalty=2
            )
            print(response["choices"][0]["text"])

        # Twilio:
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
            account_sid = 'ACf6277af0745826c7d38a24101464d488'
            auth_token = '28dba7ccbe5e8cc3edf0a6079d8dcea1'
            client = Client(account_sid, auth_token)

        # Send MMS
            message = client.messages \
                .create(
                body=response["choices"][0]["text"] + "\n" + "From " + name,
                from_='+19853323754',
                media_url=[myUrl],
                to='+1' + str(phoneNum)
            )

            print(message.sid)

    def sendSth():
        if (entry_receiver_num.get() != ""):
            toSendPhone.append(entry_receiver_num.get())
            toSendPeople.append(entry_receiver_name.get())
        if len(toSendPeople) > 1:
            def Confirm():
                print("Confirm")
                with open("./data/ContactsPhone.json", "r") as read_file:
                        numdata = json.load(read_file)
                with open("./data/ContactsName.json", "r") as read_file:
                        namedata = json.load(read_file)
                numdata[enter_cat_entry.get()] = toSendPhone
                namedata[enter_cat_entry.get()] = toSendPeople
                with open("./data/ContactsPhone.json", "w") as write_file:
                    json.dump(numdata, write_file)
                with open("./data/ContactsName.json", "w") as write_file:
                    json.dump(namedata, write_file)
                callApis()
                send_pop_window.destroy()

            send_pop_window = Tk()
            send_pop_window.title(string="Greeting AI")
            send_pop_window.configure(bg='#F5C7A9')
            send_pop_window.geometry("350x100+600+400")
            enter_frame = Frame(send_pop_window)
            enter_frame.configure(bg='#F5C7A9')
            enter_frame.pack(pady=10)
            enter_cat_label = Label(enter_frame, text="Enter Category", font=("Times New Roman", 14), bg="#F5C7A9")
            enter_cat_label.pack(side='left')
            enter_cat_entry = Entry(enter_frame)
            enter_cat_entry.pack(side='left', padx=5)

            confirm_but = Button(send_pop_window, font=("Times New Roman", 16), fg="#D1512D", text="Confirm",
                                 command=Confirm)
            confirm_but.pack()

            send_pop_window.mainloop()
        else:
            callApis()
            # print("send sth")

    receiver_info_window = Tk()
    receiver_info_window.title(string="Greeting AI")
    receiver_info_window.configure(bg='#F5C7A9')
    receiver_info_window.geometry("600x450+470+230")

    receiver_info_label = Label(receiver_info_window, text="Greeting AI", font=("Times New Roman", 40, "bold"),
                                bg="#D1512D", fg="#F5C7A9")
    receiver_info_label.pack(fill=X)

    load_contact_but = Button(receiver_info_window, font=("Times New Roman", 20, "bold"), text="Load Contact",
                              fg="#D1512D", command=loadContact)
    load_contact_but.pack(pady=30)

    middle_frame = Frame(receiver_info_window)
    middle_frame.configure(bg='#F5C7A9')
    middle_frame.pack(pady=20)

    label_frame = Frame(middle_frame)
    label_frame.configure(bg='#F5C7A9')
    label_frame.pack(side='left')

    label_receiver_name = Label(label_frame, text="Receiver Name", font=("Times New Roman", 15), bg="#F5C7A9")
    label_receiver_num = Label(label_frame, text="Receiver Phone Number", font=("Times New Roman", 15), bg="#F5C7A9")

    label_receiver_name.pack(side='top')
    label_receiver_num.pack(side='top')

    entry_frame = Frame(middle_frame)
    entry_frame.configure(bg='#F5C7A9')
    entry_frame.pack(side='left', padx=10)

    entry_receiver_name = Entry(entry_frame)
    entry_receiver_num = Entry(entry_frame)

    entry_receiver_name.pack(side='top')
    entry_receiver_num.pack(side='top')

    add_contact_but = Button(receiver_info_window, font=("Times New Roman", 20, "bold"), text="Add To Contact",
                             fg="#D1512D", command=addContact)
    add_contact_but.pack(side='top')

    send_but = Button(receiver_info_window, font=("Times New Roman", 30, "bold"), text="SEND!", fg="#D1512D", width=8,
                      command=sendSth)
    send_but.pack(pady=50)

    receiver_info_window.mainloop()

button = Button(root, text="Continue", font=("Times New Roman", 20, "bold"), fg="#D1512D",
                command=openNewWindow)
button.place(x=325, y=190)
root.mainloop()


