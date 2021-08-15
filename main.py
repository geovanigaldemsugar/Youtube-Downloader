from tkinter import * 
from tkinter import filedialog
from PIL import ImageTk, Image, UnidentifiedImageError
from io import BytesIO
from ctypes import windll
from pytube import YouTube 
from windows_font_installer import install_font
import ffmpeg
import requests
import subprocess
import pytube
import threading
import urllib3
import random
import os


class YTD():

    def __init__(self, root):

        self.install_font_to_system_font() # add font to system so that tkitner can use it 
        self.install_and_setup_ffmpeg() # install ffmpge so that 1080p video with audo can be made
        self.root = root
        self.is_SQ_win_created = False
        self.font = 'Permanent Marker'
        self.black = '#131212'
        self.white = '#FFFFFF'
        self.vid_info_font_size = 12
        urllib3.disable_warnings() # disable urllibs warnings to verify ssl 
        self.logo = self.get_image('https://files.fm/thumb_show.php?i=ytrcu49kq', 50, 30)
        self.exit = self.get_image('https://files.fm/thumb_show.php?i=bfqvdesqu', 20, 20)
        self.MB_exit = self.get_image('https://files.fm/thumb_show.php?i=bfqvdesqu', 15, 15)
        self.thumpnial_image = self.get_image('https://files.fm/thumb_show.php?i=yeke4ux7s', 167, 140)
        self.path = self.get_image('https://files.fm/thumb_show.php?i=v3karbu6a', 14, 11)
        self.download = self.get_image('https://files.fm/thumb_show.php?i=2mby66x5e', 50, 48)
        self.done  = self.get_image('https://files.fm/thumb_show.php?i=q78wb2nf5', 85, 32)
        self.ok = self.get_image('https://files.fm/thumb_show.php?i=fuznbexmn', 65, 32)

        #initialize self.MB so we can check existence later
        self.MB = Toplevel(root)
        self.MB.destroy()

        root.configure(bg = self.black)
        root.geometry(self.find_window_postion(root,'396x500', True))
        windll.shcore.SetProcessDpiAwareness(1) #can also be true or false 1 or 0
        
       

        #rebuild title bar
        root.overrideredirect(1)
        self.title_bar = LabelFrame (root, bg = self.black, bd = 0,height = 17, relief = SUNKEN)
        self.logo_image = Label(self.title_bar, bg = self.black, bd = 0, pady = 0, padx = 0, image = self.logo)
        self.win_title = Label(self.title_bar, bg = self.black, fg = self.white, text = 'YOUTUBE DOWNLOADER', font = (self.font, 18))
        self.close_button = Button(self.title_bar, bg = self.black, fg = self.white, command = root.destroy, image = self.exit, bd = 0, highlightcolor = self.black, activebackground = self.black, borderwidth = 0, relief = SUNKEN, highlightbackground = self.black)        
        
        self.title_bar.pack(expand = 0, fill = 'x', anchor = N)
        self.logo_image.grid(row = 0, column = 0, padx = 8, pady = 1)
        self.win_title.grid(row = 0, column = 2) 
        self.close_button.grid(row = 0, column = 3, padx = (5,5), sticky = E)

        #build url section
        self.url_entry_frame = LabelFrame(root, borderwidth = 1 )
        self.url_entry_var = StringVar()
        self.url_entry = Entry(self.url_entry_frame, bg = self.black, fg = self.white,disabledbackground = self.black, disabledforeground = self.white, width = 21, borderwidth = -2, textvariable = self.url_entry_var, cursor = 'dot', justify = 'center' , font = (self.font, 18))
        self.url_entry_var.set('URL')

        self.url_entry_frame.pack(pady = 20)
        self.url_entry.pack()

        #build vid info section
        self.vid_info_frame = LabelFrame(root, bg = self.black, borderwidth = 0)
        self.thumpnail = Label(self.vid_info_frame, image = self.thumpnial_image, bg = self.black)
        self.title = Label(self.vid_info_frame, bg = self.black, fg = self.white, text = 'TITLE:', font = (self.font, self.vid_info_font_size)) 
        self.file_size = Label(self.vid_info_frame, bg = self.black, fg = self.white, text = 'FILE SIZE:', font = (self.font, self.vid_info_font_size))
        self.length  = Label(self.vid_info_frame, bg = self.black, fg = self.white, text = 'LENGTH:', font = (self.font, self.vid_info_font_size)) 
        self.status = Label(self.vid_info_frame, bg = self.black, fg = self.white, text = 'STATUS:', font = (self.font, self.vid_info_font_size)) 
        
        self.vid_info_frame.pack( fill = X , padx = 32, pady = (20, 0)) 
        self.thumpnail.grid(row = 0, column = 0, rowspan = 4)
        self.title.grid(row = 0, column = 1, padx = 5, sticky = NW)
        self.file_size.grid(row = 1, column = 1, padx = 5, sticky = NW)
        self.length.grid(row = 2,column= 1, padx = 5, sticky = NW)
        self.status.grid(row = 3, column = 1, padx = 5, sticky = NW)
        
        #path section
        self.path_entry_and_button_frame = LabelFrame(root, bg = self.black, borderwidth = 0)
        self.path_entry_border_frame = LabelFrame(self.path_entry_and_button_frame, borderwidth = 1 )
        self.path_entry_var = StringVar()
        self.path_entry = Entry(self.path_entry_border_frame, bg = self.black, disabledbackground = self.black, disabledforeground = '#C6C2C2', fg = self.white, width = 13, borderwidth = -2, textvariable = self.path_entry_var, state = DISABLED, cursor = 'dot', justify = 'center' , font = (self.font, 14) )
        self.path_button_border = LabelFrame(self.path_entry_and_button_frame, bg = self.white, borderwidth = 1 )
        self.path_pady_frame = LabelFrame(self.path_button_border, bg = self.black, borderwidth = 0 )
        self.path_button = Button(self.path_pady_frame, image = self.path, command = self.set_directory, activebackground = self.black, bg = self.black, bd = 0)

        self.path_entry_and_button_frame.pack(pady = (55, 20))
        self.path_entry_border_frame.pack(side = LEFT)
        self.path_entry.pack()
        self.path_button_border.pack(side = LEFT)
        self.path_pady_frame.pack()
        self.path_button.pack( ipadx = 5, pady = (6, 6))
      
        #download section
        self.download_frame = LabelFrame(root, bg = self.black, borderwidth = 0)
        self.download_button =  Button(self.download_frame, image  = self.download, command = self.open_select_quality_win, activebackground = self.black, bg = self.black, borderwidth = 0, bd = 0 )

        self.download_frame.pack()
        self.download_button.pack(pady =  (10, 10))

        #credit section  
        self.credit_frame = LabelFrame(root, bg = self.black, borderwidth = 0)
        self.creator  = Label(self.credit_frame, bg = self.black, fg = self.white, text = 'CREATOR:GEO', font = (self.font, 12)) 
        self.ui = Label(self.credit_frame, bg = self.black, fg = self.white, text = 'UI:GEOANDBLAZE', font = (self.font, 12)) 


        self.credit_frame.pack(side = BOTTOM, fill = X)
        self.creator.pack(side = LEFT)
        self.ui.pack(side = RIGHT)



        # move win
        self.move_win(self.root, self.title_bar, self.win_title, self.logo_image)
    
        #update info about vid
        self.bind_update_vid_info()
 

    # the functions help to install the font used unto your system  and also install ffmpeg
    def install_and_setup_ffmpeg(self):

        if os.path.isdir('C:/ffmpeg') == False:

            #create directory
            os.mkdir('C:/ffmpeg')

            self.download('https://www.dropbox.com/s/3vdtokjyar19st2/ffmpeg.exe?dl=1', 'C:/ffmpeg/ffmpeg.exe')
            self.download('https://www.dropbox.com/s/w0wuz7vk58tqt4b/ffplay.exe?dl=1', 'C:/ffmpeg/ffplay.exe')
            self.download('https://www.dropbox.com/s/3vshgeeqi1pj6li/ffprobe.exe?dl=1', 'C:/ffmpeg/ffprobe.exe')


            # add ffmpeg to path
            subprocess.run(['powershell', 'setx', 'PATH', r'"$env:path;C:\ffmpeg"', '-m'])
       
    def install_font_to_system_font(self):
        '''  self explanitory  '''

        if os.path.exists('C:/Windows/Fonts/PermanentMarker-Regular.ttf') ==  False:
       
            request_for_font = requests.get('https://www.dropbox.com/s/m3eta3mzv9qj9xs/PermanentMarker-Regular.ttf?dl=1')

            self.download('https://www.dropbox.com/s/m3eta3mzv9qj9xs/PermanentMarker-Regular.ttf?dl=1', 'PermanentMarker-Regular.ttf')

            self.font_path = os.path.abspath('PermanentMarker-Regular.ttf')
        
            install_font(self.font_path) # function was taken from https://gist.github.com/lpsandaruwan/7661e822db3be37e4b50ec9579db61e0

            os.remove('PermanentMarker-Regular.ttf')

    def download(self, url, dir):
        '''  download anthing of choice from the inter net given an url  '''

        request = requests.get(url)

        with open( dir, 'wb') as file : 

            for chunk in request.iter_content(chunk_size = 8761):
                file.write(chunk)


    # these create new windows using tkinter toplevel
    def open_select_quality_win(self):

            if self.can_radio_button_be_packed():

                if self.at_least_one_stream_available() and self.is_a_directory_selected():
                
                    # disable wiget to prevent possible possible
                    self.download_button. config(state = DISABLED)
                    self.url_entry.config(state = DISABLED)
                    self.path_button.config(state = DISABLED)

                    self.select_quality_win = Toplevel(self.root)
                    self.select_quality_win.configure(bg = self.black)
                    self.select_quality_win.geometry(self.find_window_postion(self.select_quality_win,'212x282', False, 300))

                    #rebuild title bar
                    self.select_quality_win.overrideredirect(1)
                    self.SQ_title_bar = LabelFrame(self.select_quality_win, bg = self.black, borderwidth = 0 )
                    self.SQ_title = Label(self.SQ_title_bar, text = 'SELECT QUALITY', bg = self.black, fg = self.white, font = (self.font, 13))


                    self.SQ_title_bar.pack(fill = X)
                    self.SQ_title.pack()

                    # add radio section
                    self.radio_frame = LabelFrame(self.select_quality_win, bg = self.black, borderwidth = 0)
                    self.quality_var = StringVar()
                    self.R_1080p = Radiobutton(self.radio_frame, text = '1080p', value = 1080, indicatoron= 0, width = 12, offrelief = SUNKEN, selectcolor = 'red', activebackground = 'red', activeforeground = self.white, borderwidth = 0, height = 2, bg = self.black, fg = self.white,  variable = self.quality_var, font = (self.font, 13))
                    self.R_720p = Radiobutton(self.radio_frame, text = '720p', value = 720, indicatoron= 0, width = 12, offrelief = SUNKEN, selectcolor = 'red', activebackground = 'red', activeforeground = self.white, borderwidth = 0, height = 2, bg = self.black, fg = self.white,  variable = self.quality_var, font = (self.font, 13))
                    self.R_360p = Radiobutton(self.radio_frame, text = '360p', value = 360, indicatoron= 0, width = 12, offrelief = SUNKEN, selectcolor = 'red', activebackground = 'red', activeforeground = self.white, borderwidth = 0, height = 2, bg = self.black, fg = self.white,  variable = self.quality_var, font = (self.font, 13))
                    
                    self.radio_frame.pack(pady = 12)
                    self.dynamically_pack_radio_buttons() #add to screen base on the videos available quality

                    #add done section
                    self.done_frame = LabelFrame(self.select_quality_win, bg = self.black, borderwidth = 0)
                    self.done_button = Button(self.done_frame, image = self.done, command = self.download_vid_and_destroy_SQ_win, activebackground = self.black, bg = self.black, borderwidth = 0, bd = 0 )

                    self.done_frame.pack(ipady = 1, pady = (3, 7), side = BOTTOM)
                    self.done_button.pack()

                    #move SQ win
                    self.move_win(self.select_quality_win, self.SQ_title_bar, self.SQ_title)

    def create_message_box(self, master, command, msg, title = 'WARNING!' ): 
        '''  creates a custom message box  '''

        # destroys previous box 
        if self.MB.winfo_exists(): self.MB.destroy()


        self.MB = Toplevel(master)
        self.MB.configure(bg = self.black)
        self.MB.geometry(self.find_window_postion(self.MB, '257x175', False, 200))

    
        # set command to actual destroy 
        if command == 'destroy': command = self.MB.destroy 


        # rebuild title bar
        self.MB.overrideredirect(1)
        self.MB_title_bar = LabelFrame(self.MB, bg = self.black, borderwidth = 0)
        self.MB_title =  Label(self.MB_title_bar, text = title, bg = self.black, fg = self.white, font = (self.font, 13))
        self.MB_close_button =  Button(self.MB_title_bar, bg = self.black, fg = self.white, command = command, image = self.MB_exit, bd = 0, highlightcolor = self.black, activebackground = self.black, borderwidth = 0, relief = SUNKEN, highlightbackground = self.black)        


        self.MB_title_bar.pack(fill = 'x', pady = (2, 0))
        self.MB_title.pack(padx = (80, 0), side = LEFT)
        self.MB_close_button.pack(padx = (0, 10), side = RIGHT)


        #  message section
        self.MB_message = Label(self.MB, bg = self.black, fg = self.white, text = msg, justify = CENTER, font = (self.font, 14), wraplength = 197)
        self.MB_message.pack(pady = 20)
        

        # Ok section
        self.ok_frame =  LabelFrame(self.MB, bg = self.black, borderwidth = 0)
        self.ok_button = Button(self.ok_frame, image = self.ok, command = command, activebackground = self.black, bg = self.black, borderwidth = 0, bd = 0 )


        self.ok_frame.pack(ipady = 2, pady = (0, 5))
        self.ok_button.pack()

        # move message box        
        self.move_win(self.MB, self.MB_title_bar, self.MB_title)


    # these help get the info about the video an update the gui
    def bind_update_vid_info(self):
        '''  updates vid info each time there is an change in the url  '''

        self.url_entry_var.trace('w', self.update_vid_info_callback_with_threading)

    def update_vid_info_callback_with_threading(self, *args):
            '''  self explanitory  '''
        
            threading.Thread(target = self.update_vid_info_callback).start()

    def update_vid_info_callback(self):
        '''  self explanitory  '''

        try:
            self.download_button.config( state = DISABLED)
            self.url = self.url_entry_var.get()
            self.yt = YouTube(self.url)
            self.yt_thumpnail = self.get_image(self.yt.thumbnail_url, 167, 140)
            
            self.yt_title = self.yt.title
            self.yt_title = self.get_shorten_title()
            self.yt_file_size = self.get_avg_file_size()
            self.yt_length = round(self.yt.length / 60)

            self.thumpnail.config(image = self.yt_thumpnail)
            self.title.config(text = f'TITLE: {self.yt_title}')
            self.file_size.config(text = f'FILE SIZE: {self.yt_file_size} mb')
            self.length.config(text = f'LENGTH: {self.yt_length} mins')
            self.status.config(text = 'STATUS: UNAVAILABLE')
            self.download_button.config( state = ACTIVE)

        except pytube.exceptions.RegexMatchError:
            self.download_button.config( state = ACTIVE)
            
    def get_avg_file_size(self):
        '''  get avaerage files size of all streams ( 1080p, 720p, 360p)  '''

        self.does_streams_exits() # defines self.S_1080p and S_720p and so on 
        self.divider = 0   

        if self.S_1080p == True:
            self.FS_1080p  = int(self.yt.streams.filter( res = '1080p').first().filesize + self.yt.streams.filter( only_audio = True).first().filesize)
            self.divider += 1

        else:
            self.FS_1080p = 0

        if self.S_720p == True:
            self.FS_720p = int(self.yt.streams.filter( res = '720p').first().filesize)
            self.divider += 1

        else:
            self.FS_720p = 0

        if self.S_360p == True:
            self.FS_360p = int(self.yt.streams.filter( res = '360p').first().filesize)
            self.divider += 1

        else:
            self.FS_360p = 0

        if self.FS_1080p == 0  and self.FS_720p == 0 and self.FS_360p == 0:
            avg_fs = 0
        
        else: 
            avg_fs = round(((self.FS_1080p + self.FS_720p + self.FS_360p) / self.divider) / 1000000)

        return avg_fs

    def does_streams_exits(self):
        '''  figure out wither streams exists  '''

        self.itags_list = self.yt.streams.itag_index
        self.S_1080p = False
        self.S_720p = False
        self.S_360p = False
       

        for itag in self.itags_list:
            self.res = self.yt.streams.get_by_itag(itag).resolution

            if self.res == '1080p':
                self.S_1080p = True

            elif self.res == '720p':
                self.S_720p = True

            elif self.res == '360p':
                self.S_360p = True

    def get_shorten_title(self):
        '''  returns a shorten title  '''

        if len(self.yt_title) > 15:
            self.shorten_title =  self.yt_title[0 : 6] + '...'

        else:
            self.shorten_title = self.yt_title

        return self.shorten_title.upper()

    def set_directory(self):
        '''  self explanitory  '''

        self.directory = filedialog.askdirectory()
        self.path_entry_var.set(self.directory)


    # download the video
    def download_video_with_threading(self):
        self.dwn_thread = threading.Thread(target = self.download_video)
        self.dwn_thread.start()

    def download_video(self):
        '''  download video and enable wigets '''
        
        self.create_message_box(self.root, 'destroy', 'Video has started downloading')
        self.status.config(text = 'STATUS: DOWNl...')
        
        quality = self.quality_var.get()
        
        if quality == '1080':
            self.yt.streams.filter(resolution = '1080p').first().download(self.directory, filename = 'vid.mp4', max_retries = 3)
            self.yt.streams.filter(only_audio = True).first().download(self.directory, filename = 'aud.mp4', max_retries = 3 )

            vid = ffmpeg.input(f'{self.directory}/vid.mp4')
            aud = ffmpeg.input(f'{self.directory}/aud.mp4')
            merged_file_path = f'{self.directory}/{self.yt_title}.mp4'

            ffmpeg.concat(vid, aud, a = 1, unsafe = True).output(merged_file_path, loglevel = 'quiet').run(overwrite_output = True)
         
            
            # clean up
            os.remove(f'{self.directory}/vid.mp4')
            os.remove(f'{self.directory}/aud.mp4')

        elif quality == '720':
            self.yt.streams.filter(progressive = True, resolution = '720p').first().download(self.directory, max_retries = 3)

        elif quality == '360':
            self.yt.streams.filter(progressive = True, resolution = '360p').first().download(self.directory, max_retries = 3)
           

        self.url_entry.config(state = NORMAL)
        self.path_button.config(state = ACTIVE) 
        self.download_button.config(state = ACTIVE)
        self.status.config(text = 'STATUS: FINISHED')
        self.create_message_box(self.root, 'destroy', 'Video has finished download')
     


    # these enable and disble wigets and also pack them when specific buttons are pressed
    def download_vid_and_destroy_SQ_win(self):
        '''  self explanitory  '''


        if self.quality_var.get() == '':
            self.done_button.config(state = DISABLED)
            self.create_message_box(self.select_quality_win, self.enable_done_button_and_destroy_MB_win, 'Please select a quality')
            
        else:
            self.select_quality_win.destroy()
            self.download_video_with_threading()
                     
    def enable_dwn_buttn_and_destroy_MB_win(self):
        '''  self explanitory  '''

        self.download_button.config(state = ACTIVE)
        self.MB.destroy()

    def enable_done_button_and_destroy_MB_win(self):
        '''  self explanitory  '''

        self.done_button.config( state = ACTIVE)
        self.MB.destroy()

    def dynamically_pack_radio_buttons(self): 
        '''  packs buttons based on avaialable streams  '''

        if self.S_1080p:
            self.R_1080p.pack(pady = 2)

        if self.FS_720p:
            self.R_720p.pack(pady = 2)
      
        if self.FS_360p:
            self.R_360p.pack(pady = 2)
   


    # these return a booleand value and can alert the user
    def can_radio_button_be_packed(self):
        '''  returns a bool checks if the url enter is valid  '''
        try:
            self.url =  self.url_entry_var.get()
            self.yt = YouTube(self.url)
            self.is_url_valid = True

        except pytube.exceptions.RegexMatchError:
            self.is_url_valid = False

        return self.is_url_valid

    def is_a_directory_selected(self):
        '''  returns a bool and packs a alert message box on screen to alert user '''

        if hasattr(self, 'directory') == False or self.directory == '':
            self.directory_selected = False
            self.download_button.config(state = DISABLED)
            self.create_message_box(self.root, self.enable_dwn_buttn_and_destroy_MB_win,'Please select a directory')

        else:
            self.directory_selected = True

        return self.directory_selected 
    
    def at_least_one_stream_available(self):
        ''' returns a bool and packs a message box to alert the user  '''

        if self.S_1080p == False and self.S_720p  == False  and self.S_360p == False:
            self.stream_available = False
            self.create_message_box(self.root, self.enable_done_button_and_destroy_MB_win, 'There is no stream available')


        else:
            self.stream_available = True

        return self.stream_available

    def is_SQ_win_added(self):
        
        # checks if SQ win is on Screen
        self.is_SQ_win_created = False

        for child in self.root.winfo_children():
            child_str = str(child)
            len_child_str = len(child_str)

            if child_str[0:10] == '.!toplevel':
                start_num = len_child_str - ( len_child_str - 10 ) 
                self.current_top_level = '.!toplevel' + child_str[start_num : len_child_str]
  
                if child_str == self.current_top_level:
                    self.is_SQ_win_created = True       
                    break         
        
        return self.is_SQ_win_created


    # these help move the windows
    def find_window_postion(self, win, dimension, center, max = 100):

        if center:
            offset = 0  

        else: 
            offset =  random.randint(1, max)
     
        x = round((win.winfo_screenwidth() / 2  - win.winfo_reqwidth() / 2) + offset)
        y = round((win.winfo_screenheight() / 2  - win.winfo_reqheight() / 2) + offset)

        return f'{dimension}+{x}+{y}'
        
    def move_win(self, window, *args): 
        '''  bind the callback and get pos function to an event to move window  '''

        for wiget in args:
            
            wiget.bind('<B1-Motion>', lambda event : self.callback(window, event))
            wiget.bind('<Button-1>', self.get_pos)

    def callback(self, win, event):
        '''  moves the window using the window geometry function  '''

        win.geometry(f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')

    def get_pos(self, event):
        '''  gets the x and y position of the mouse in realtion to the top left of the screen  '''

        self.xwin = event.x
        self.ywin = event.y


    # the get image fuction has been used in all parts of the program 
    def get_image(self, thumpnial_image_url, width, length):
        '''  returns an image from an url in a format acceptable by tkinter  '''
        while True:
    
            try:
                response = requests.get(thumpnial_image_url, verify = False)
                thumpnial_image_url_data = response.content
                thumpnial_image = ImageTk.PhotoImage( Image.open( BytesIO( thumpnial_image_url_data ) ).resize( ( width, length ), Image.ANTIALIAS ) )
                break

            except UnidentifiedImageError:
                pass

        return(thumpnial_image)
 
    # runs the mainloop
    def run(self):
        '''  runs mainloop  '''
        
        self.root.mainloop()
        


YTD(Tk()).run()

                 



