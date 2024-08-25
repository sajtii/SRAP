import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import sys
import threading
import time
import requests
from PIL import Image, ImageTk
import io
from pypresence import Presence
from tkinter import font
import webbrowser


config = configparser.ConfigParser()
config.read('config.ini')

settings = None
sdpra = None


#UI for settings, obviously
class Settings:
    def __init__(self, master):
        self.master = master
        self.master.title("Settings")
        self.master.geometry(f'350x375+{(self.master.winfo_screenwidth()  - 350) // 2}+{(self.master.winfo_screenheight() - 375) // 2}')
        self.master.resizable(False, False)
        
        
        self.icon_i = ImageTk.PhotoImage(Image.open('assets/settings.png'))
        self.master.iconphoto(False, self.icon_i)
        
    
        self.ra_username = tk.Label(self.master, text="RA Username")
        self.ra_username.place(x=10, y=10)
        self.ra_username_entry = tk.Entry(self.master)
        self.ra_username_entry.place(width=320, x=10, y=35)
        self.ra_username_entry.insert(0, config.get('RA', 'username'))
            
        self.ra_apikey = tk.Label(self.master, text="RA API Key")
        self.ra_apikey.place(x=10, y=65)
        self.ra_apikey_entry = tk.Entry(self.master)
        self.ra_apikey_entry.place(width=320, x=10, y=90)
        self.ra_apikey_entry.insert(0, config.get('RA', 'apikey'))

        self.dc_clientid = tk.Label(self.master, text="Discord Application ID")
        self.dc_clientid.place(x=10, y=120)
        self.dc_clientid_entry = tk.Entry(self.master)
        self.dc_clientid_entry.place(width=320, x=10, y=145)
        self.dc_clientid_entry.insert(0, config.get('DC', 'clientid'))

        self.dc_bottoken = tk.Label(self.master, text="Discord Bot Token")
        self.dc_bottoken.place(x=10, y=175)
        self.dc_bottoken_entry = tk.Entry(self.master)
        self.dc_bottoken_entry.place(width=320, x=10, y=200)
        self.dc_bottoken_entry.insert(0, config.get('DC', 'bottoken'))
    
    
        self.profile = tk.BooleanVar()
        self.profile.set(config.get('BT', 'profile') == '1')
        self.profile_chb = ttk.Checkbutton(self.master, text="Enable RA profile button", variable=self.profile)   
        self.profile_chb.place(x=10, y=230)
    
    
        self.gamepage = tk.BooleanVar()
        self.gamepage.set(config.get('BT', 'gamepage') == '1')
        self.showgp_chb = ttk.Checkbutton(self.master, text="Enable current game button", variable=self.gamepage)
        self.showgp_chb.place(x=10, y=255)

        self.entry_var = tk.StringVar()
        self.sync_interval = tk.Label(self.master, text="Update interval in seconds")
        def validate_numeric(P):       
            return P.isdigit() or P == ''
        self.vcmd = self.sync_interval.register(validate_numeric)
        self.sync_interval.place(x=10, y=285)
        self.sync_interval_entry = tk.Entry(self.master, textvariable=self.entry_var, validate="key", validatecommand=(self.vcmd, '%P'))
        self.sync_interval_entry.place(width=50, relx=0.5, y=285)
        self.sync_interval_entry.insert(0, config.get('SYNC', 'interval'))
    
        self.stwanted = tk.BooleanVar()
        self.stwanted.set(config.get('ST', 'dontshow') == '1')
        self.stwanted_chb = ttk.Checkbutton(self.master, text="Do not show this window again at next startup", variable=self.stwanted)
        self.stwanted_chb.place(x=10, y=315)


        def save():
            config['RA']['username'] = self.ra_username_entry.get()
            config['RA']['apikey'] = self.ra_apikey_entry.get()
            config['DC']['clientid'] = self.dc_clientid_entry.get()
            config['DC']['bottoken'] = self.dc_bottoken_entry.get()
            config['BT']['profile'] = '1' if self.profile.get() else '0'
            config['BT']['gamepage'] = '1' if self.gamepage.get() else '0'
            config['ST']['dontshow'] = '1' if self.stwanted.get() else '0'
            config['ST']['needed'] = '0'
            config['SYNC']['interval'] = self.sync_interval_entry.get()
            
    
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print('Settings saved!')
            run_sdpra()

        self.save_b = ttk.Button(self.master, text="Save and Start", command=save)
        self.save_b.place(relx=0.5, y=345, anchor='n')
    
    def close(self):
        self.master.destroy()


#main window, don't ask me why I named it like this
class Sdpra:
    def __init__(self, master):
        self.master = master
        self.master.title("Sajti's RA Presence")
        self.master.geometry(f'550x200+{(self.master.winfo_screenwidth()  - 550) // 2}+{(self.master.winfo_screenheight() - 200) // 2}')
        self.master.resizable(False, False)
        
        
        self.master.configure(bg="#2b2b2b")
        self.style = ttk.Style()
        self.style.configure('.', background="#2b2b2b", foreground="white")
        
        self.settings_image = tk.PhotoImage(file='assets/settings.png')
        self.dc_dev_image = tk.PhotoImage(file='assets/dc_dev_off.png')
        self.ra_pfp = tk.PhotoImage(file='assets/ava_def.png')
        self.game_image = tk.PhotoImage(file='assets/def_gameimage.png')
        self.icon_i = ImageTk.PhotoImage(Image.open('assets/stinky.png'))
        
        self.master.iconphoto(False, self.icon_i)
        
        
        
        
        self.ra_profile_url = 'https:\\retroachievements.org'
        def open_ra_profile(event):
            webbrowser.open(self.ra_profile_url)
        self.ra_profile_image = ttk.Label(self.master, image=self.ra_pfp)
        self.ra_profile_image.place(x=10, y=10)
        self.ra_profile_image.bind("<Button-1>", open_ra_profile)
        
        self.dc_dev_url = 'https:\\discord.com'
        def open_dc_dev(event):
            webbrowser.open(self.dc_dev_url)
        self.dc_dev = ttk.Label(self.master, image=self.dc_dev_image)
        self.dc_dev.place(x=70, y=10)
        self.dc_dev.bind("<Button-1>", open_dc_dev)
        
        def settings_e(event):
            response = messagebox.askyesno("Sajti's RA Presence", "To open the settings, the app needs to be restarted. Do you wish to continue?")
            if response: 
                settings_needed()
        self.b_settings = ttk.Label(self.master, image=self.settings_image)
        self.b_settings.place(x=490, y=10)
        self.b_settings.bind("<Button-1>", settings_e)
        
        
        
        self.c_game_url = 'https:\\retroachievements.org'
        def open_c_game(event):
            webbrowser.open(self.c_game_url)
        self.c_game_image = ttk.Label(self.master, image=self.game_image)
        self.c_game_image.place(x=10, y=80)
        self.c_game_image.bind("<Button-1>", open_c_game)
        
        
        self.c_playing_frame = ttk.Frame(self.master, width=420, height=35)
        self.c_playing_frame.place(x=120, y=75)
        self.c_playing = ttk.Label(self.c_playing_frame, text="...")
        self.c_playing.place(x=0, y=0)
        
        
        self.c_game_name_frame = ttk.Frame(self.master, width=420, height=30)
        self.c_game_name_frame.place(x=120, y=110)
        self.c_game_name = ttk.Label(self.c_game_name_frame, text="...")
        self.c_game_name.place(x=0, y=0)
        
        self.c_game_frame = ttk.Frame(self.master, width=420, height=50)
        self.c_game_frame.place(x=120, y=140)
        self.c_game_details = ttk.Label(self.c_game_frame, text="...", wraplength=420, justify='left')
        self.c_game_details.place(x=0, y=0)
        
    def still_running(self):
            return self.master.winfo_exists()
        
        
        
def run_sdpra():
    global sdpra, settings
    if settings != None:
        settings.close()
        settings = None
    root = tk.Tk()
    sdpra = Sdpra(root)
    threading.Thread(target=syncing).start()
    root.mainloop()

def run_settings():
    global settings
    root = tk.Tk() 
    settings = Settings(root)
    root.mainloop() 
    
#function to restart the app and open the settings window
def settings_needed():
    config['ST']['needed'] = '1'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    os.execv(sys.executable, ['python'] + sys.argv)
    
def ra_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None



#the heart and soul of this piece of software
def syncing():
    
    
    #loading values from config and setting up other variables
    username = config.get('RA', 'username')
    apikey = config.get('RA', 'apikey')
    appid = config.get('DC', 'clientid')
    bottoken = config.get('DC', 'bottoken')
    ra_profile = f"https://retroachievements.org/API/API_GetUserProfile.php?u={username}&y={apikey}&z={username}"
    dc_url = f'https://discord.com/api/v10/applications/{appid}'
    headers = {
        'Authorization': f'Bot {bottoken}',
        'Content-Type': 'application/json'
    }
    try:
        interval = int(config.get('SYNC', 'interval'))
        if interval < 20:
            sleeptime = 20
            config['SYNC']['interval'] = '20'
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
    except ValueError:
        sleeptime = 20
        config['SYNC']['interval'] = '20'
        with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
    if config.get('BT', 'profile') == '1':    
        button2 = {"label": f"{username}'s RA Page", "url": f"https://retroachievements.org/user/{username}"}  
    else:
        button2 = None
   
        
    onetime = True
    game_title_stored = None
    start_time = int(time.time())
               
    t_font = font.nametofont("TkDefaultFont").actual()['family']
      
    
    global sdpra
    sdpra.ra_profile_url = f"https://retroachievements.org/user/{username}"
    response = requests.get(dc_url, headers=headers)
    if response.status_code == 200:
        appinfo = response.json()
        sdpra.c_playing.configure(text=f"Playing {appinfo['name']}", font=(t_font, 12))
        sdpra.dc_dev_image = tk.PhotoImage(file="assets/dc_dev.png")
        sdpra.dc_dev.configure(image=sdpra.dc_dev_image)
        sdpra.dc_dev_url = f'https://discord.com/developers/applications/{appid}/information'
        RPC = Presence(appid)
        RPC.connect()
        print('Connected to Discord!')
    else:
        messagebox.showerror("Error!", "Something went wrong! Check your settings, particularly those related to Discord.")
        settings_needed()
   
    while sdpra.still_running():
           
        data = ra_data(ra_profile)
        if data != None:
            params = f"?z={username}&y={apikey}&i={data['LastGameID']}"
            ra_game = f"https://retroachievements.org/API/API_GetGame.php{params}"
            ra_game_data = ra_data(ra_game)
        else:
            messagebox.showerror("Error!", "Something went wrong! Check your settings, particularly those related to RetroAchievements.")
            settings_needed()
           
        if onetime == True:
            npfp = requests.get(f"https://media.retroachievements.org/UserPic/{username}.png")
            sdpra.ra_pfp=ImageTk.PhotoImage(Image.open(io.BytesIO(npfp.content)).resize((50,50), Image.LANCZOS))
            sdpra.ra_profile_image.configure(image=sdpra.ra_pfp)
            print('Connected to RetroAchievements!')
            onetime = False
            
                
            
        game_title = f"{ra_game_data['GameTitle']}"
        if game_title != game_title_stored:
            if config.get('BT', 'gamepage') == '1':
                button1 = {"label": "View on RetroAchievements", "url": f"https://retroachievements.org/game/{data['LastGameID']}"}
            else:
                button1 = None   
            buttons = [button1, button2]
            buttons_filtered = [d for d in buttons if d is not None]
            sdpra.c_game_name.configure(text=game_title, font=(t_font, 10))
            game_title_stored = game_title
            ngi = requests.get(f"https://media.retroachievements.org{ra_game_data['ImageIcon']}")
            sdpra.game_image=ImageTk.PhotoImage(Image.open(io.BytesIO(ngi.content)))
            sdpra.c_game_image.configure(image=sdpra.game_image)
            sdpra.c_game_url = f"https://retroachievements.org/game/{data['LastGameID']}"
        
        

                
                
        state = data["RichPresenceMsg"]
        sdpra.c_game_details.configure (text=state, font=(t_font, 10))
        
        RPC.update(
            state=data["RichPresenceMsg"],
            details=game_title,
            start=start_time,
            large_image=f"https://media.retroachievements.org{ra_game_data['ImageIcon']}",
            large_text=f"Released {ra_game_data['Released']}, Developed by {ra_game_data['Developer']}, Published by {ra_game_data['Publisher']}",
            small_image=config.get('CI', str(ra_game_data['ConsoleID'])),
            small_text=ra_game_data['ConsoleName'],
            buttons=buttons_filtered
        )
        
        print(f"Taking a {sleeptime} second nap.")
        time.sleep(sleeptime)
        
        
    
if __name__ == "__main__":
    if config.get('ST', 'dontshow') == '0' or config.get('ST', 'needed') == '1':
        run_settings()
    else:
        run_sdpra()
