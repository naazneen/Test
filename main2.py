# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:26:10 2020

@author: AMD
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 20:08:37 2020

@author: AMD
"""

from threading import Thread
from datetime import datetime
class ThreadR(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return









import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import sys
import os
import comtypes.client
from tkinter import ttk
#import iter1




# Import libraries
from pydub import AudioSegment
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave
from google.cloud import storage
from pydub import AudioSegment
from pydub.utils import make_chunks
filepath = "D:/Fiverr/Projects/SpeechtoNotes/chunks/"     #Input audio file path
output_filepath = "D:/Fiverr/Projects/SpeechtoNotes/Transcripts/" #Final transcript path
bucketname = "audio-files-bucket-fiverr" #Name of the bucket created in the step before






class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1200x530")
        #self.wm_iconbitmap('test.ico')
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.S2T = tk.Frame(master = self.container)
        self.S2T.grid_configure(row = 1, column = 0)
        self.Title = tk.Label(self.container, justify=tk.CENTER ,text="Speech to Text",font=('Candara',35),bg = '#cccccc',fg = 'black')
        self.Title.grid(row= 0,column=0,columnspan = 2)
        self.uploadbtn = tk.Button(master = self.S2T ,text = "Upload File", font=('Candara',16),bg = 'white',fg = 'black',command = lambda : self.asktoopen(self.S2T))
        self.uploadbtn.grid(row = 0,column=0,padx = 13,pady=10)
        #filename = tk.StringVar()
        self.uploadedfile = tk.Label(self.S2T, text = "", font=('Candara',15),bg = 'white',width = 40)
        self.uploadedfile.grid(row=0,column = 1,padx = 15,pady=10)
        self.languagelbl = tk.Label(self.S2T,text = "Language", font=('Candara',15),bg = 'white')
        self.languagelbl.grid(row=0,column = 2)
        self.languagevar = tk.StringVar(self.S2T)
        self.languagevar.set("English")
        self.languageoption = ttk.Combobox(self.S2T,textvariable=self.languagevar,font=('Candara',14),background = 'white',foreground = 'black')
        self.languageoption.grid(row = 0,column = 3 )
        self.languageoption['values'] = ("english","hindi")
        self.dobtn = tk.Button(self.S2T,text = "Upload and translate",command = lambda : self.process( self.uploadedfile['text']))
        self.dobtn.grid(row = 0,column = 5, columnspan = 2)
        self.progressBar = ttk.Progressbar(self.S2T, orient="horizontal", length=900,mode="determinate")
        self.progressBar.grid(column = 0, row = 1, pady=10,columnspan = 4)
        
        #uploadedfile.configure(text = fname,)
        self.ScrollBar = tk.Scrollbar(self.S2T)
        self.ftext = tk.Text(self.S2T,width = 90,height = 10, yscrollcommand = self.ScrollBar.set,font=('Candara',14),bg = 'white',fg = 'black')
        self.ftext.insert(tk.INSERT,"Upload File first")
        self.ScrollBar.config(command = self.ftext.yview)
        self.ScrollBar.grid(row=2,column =5,sticky=tk.N+tk.S+tk.W)
        self.ftext.grid(row=2,column=0,padx = 15,pady=10,columnspan = 4)
        self.Downloadbtn1 = tk.Button(self.S2T,justify = tk.CENTER, text = "Save as Word",command = lambda : self.saveasword(parent,fname),font=('Candara',18),bg = 'white',fg = 'black')
        self.Downloadbtn1.grid(row = 3,column = 0,padx = 15,pady=10,columnspan =2)
        self.Downloadbtn2 = tk.Button(self.S2T, text = "Save as PDF",command = lambda : self.saveaspdf(parent,fname),font=('Candara',18),bg = 'white',fg = 'black')
        self.Downloadbtn2.grid(row = 3,column = 2,padx = 15,pady=10,columnspan = 2)
        self.puncts = tk.Frame(self.S2T)
        self.puncts.grid(row=2,column=6, rowspan = 4)
        
        self.phead = tk.Label(self.puncts,text="Click Punctuation to insert",font=('Candara',14),bg = 'white',fg = 'black')
        self.phead.grid(row=0,column=0,sticky = tk.N,padx=15,pady=10)
        self.p1 = tk.Button(self.puncts,text = "Full stop - '.'",font=('Candara',10),bg = 'white',fg = 'black')
        self.p1.grid(row=1,column = 0,padx=5,pady=2,sticky = tk.W)
        self.p2 = tk.Button(self.puncts,text = "Comma - ','",font=('Candara',10),bg = 'white',fg = 'black')
        self.p2.grid(row=2,column = 0,padx=5,pady=2,sticky = tk.W)
        self.p3 = tk.Button(self.puncts,text = "Hiphen - '-'",font=('Candara',10),bg = 'white',fg = 'black')
        self.p3.grid(row=3,column = 0,padx=5,pady=2,sticky = tk.W)
        self.p4 = tk.Button(self.puncts,text = "Exclamation - '!'",font=('Candara',10),bg = 'white',fg = 'black')
        self.p4.grid(row=4,column = 0,padx=5,pady=2,sticky = tk.W)
        self.p5 = tk.Button(self.puncts,text = "Question Mark - '?'",font=('Candara',10),bg = 'white',fg = 'black')
        self.p5.grid(row=5,column = 0,padx=5,pady=2,sticky = tk.W)
        
        
        
    
    def saveasword(self,parent,fname):
        try :
            #directory = os.getcwd() 
            tx = fname+".docx"
            f = open(tx,"w+")
            text = "XYZ"
            t = ''.join(text)
            f.write(str(t))
            f.close()
            print ("saved in directory")
            savedin = tk.Label(parent, text = "saved in "+tx)
            savedin.grid(row = 4,column = 1, columnspan = 2)
        except :
            pass

    def saveaspdf(self,parent,fname):
        
        from docx2pdf import convert
        
        #convert("input.docx")
        print (tx)
        convert(tx, tx+".pdf")
        #convert("my_docx_folder/")
        #pdfkit.from_string('MicroPyramid', 'micro.pdf')
        
    def process(self,fname):
        """
        #parent.children[ftext].config(text = "file uploaded text")
        ScrollBar = tk.Scrollbar(parent)
        ftext = tk.Text(parent,width = 90, height = 10, yscrollcommand=ScrollBar.set,font=('Candara',14),bg = 'white',fg = 'black')
        ftext.grid(row=2,column=0,padx = 15,pady=10,columnspan = 4)
        ftext.insert(tk.INSERT,"Wait for the file to be processed")
        """
        texttd = ThreadR(target = self.SpeechToText,args = (self.fname,))
        texttd.daemon = True
        texttd.start()
        textcontain = texttd.join()
        self.ftext.insert(tk.INSERT,textcontain)
        self.ScrollBar.config(command = self.ftext.yview)
        self.ScrollBar.grid(row=2,column =5,sticky=tk.N+tk.S+tk.W)
        #ftext.insert(0,"file text will be shown here")
        """
        Downloadbtn1 = tk.Button(parent, text = "Save as Word",command = lambda : self.saveasword(parent,fname),font=('Candara',18),bg = 'white',fg = 'black')
        Downloadbtn1.grid(row = 3,column = 0,padx = 15,pady=10,columnspan = 2)
        Downloadbtn2 = tk.Button(parent, text = "Save as PDF",command = lambda : self.saveaspdf(parent,fname),font=('Candara',18),bg = 'white',fg = 'black')
        Downloadbtn2.grid(row = 3,column = 2,padx = 15,pady=10,columnspan = 2)
        """
      
        
    def asktoopen(self,parent):
        print ("prev called")
        print ("called")
        self.fname = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wave files","*.wav"),("all files","*.*")))
        #print (parent.children())
        self.uploadedfile['text'] =  self.fname
        self.uploadedfile.grid(row=0,column = 1,padx = 15,pady=10)
        #self.process(parent,fname)
        


    def upload_blob(self,bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
    
        blob.upload_from_filename(source_file_name)
        
    
    def delete_blob(self,blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucketname)
        blob = bucket.blob(blob_name)
        blob.delete()
        
        
    def google_transcribe(self,audio_file_name):
    
        gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
        transcript = ''
        
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri=gcs_uri)
    
        config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')
    
        # Detects speech in the audio file
        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout=10000)
    
        for result in response.results:
            transcript += result.alternatives[0].transcript
        
        #delete_blob(bucket_name, destination_blob_name)
        return transcript
    
    
    def write_transcripts(self,transcript_filename,transcript):
        f= open(output_filepath + transcript_filename,"w+")
        f.write(transcript)
        f.close()
        
    def finalrun(self,filepath):
        for audio_file_name in os.listdir(filepath):
            transcript = self.google_transcribe(audio_file_name)
            transcript_filename = audio_file_name.split('.')[0] + '.txt'
            self.write_transcripts(transcript_filename,transcript)
    
    #filepath = os.path.join(os.getcwd()+'\\'+'chunks')       
    
    def makingchunks(self,fname,ftype,length):
        try:
            os.mkdir(filepath)
            print (os.getcwd())
        except:
            pass
        os.chdir(filepath)
        print (os.getcwd())
        myaudio = AudioSegment.from_file(fname , ftype) 
        chunk_length_ms = 80000 # pydub calculates in millisec
        chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
        for i, chunk in enumerate(chunks):
            chunk_name = "chunk{0}.wav".format(i)
            print ("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")
            chunk.export(filepath + "\chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
            #filename = 'chunk'+str(i)+'.wav'
            #print ()
            #filepath = os.path.realpath(path) + "\chunks\\"+filename
        return(os.getcwd())
            #finalrun("D:\Fiverr\Projects\SpeechtoNotes\chunks")
    
    def SpeechToText(self,file):
        print ("called me")
        #progressBar = ttk.Progressbar(app.S2T, orient="horizontal", length=900,mode="determinate")
        #progressBar.grid(column = 0, row = 1, pady=10,columnspan = 4)
        print("trying to set pbar")
        self.progressBar['maximum'] = 100
        self.progressBar["value"] = 5
        print ("before update")
        self.progressBar.update()
        t = []
        t2 = []
        td =[]
        filepath = self.makingchunks(file,"wav",20)
        #filepath = 'D:\Fiverr\Projects\SpeechtoNotes\chunks'
        i = 0
        print("before loop")
        for audio_file_name in os.listdir(filepath):
            bucket_name = bucketname
            source_file_name = filepath + '\\' +audio_file_name
            destination_blob_name = audio_file_name
            #print(source_file_name)
            t.append(ThreadR(target = self.upload_blob , args=(bucket_name, source_file_name, destination_blob_name,)))
            t2.append(ThreadR(target = self.google_transcribe,args = (audio_file_name,)))
            print("Upload Started =", datetime.now().strftime("%H:%M:%S"))
            t[i].start()
            #upload_blob(bucket_name, source_file_name, destination_blob_name)
            print ('uploaded')
            i += 1   
        filetexts = '' 
        #tup = threading.Thread(target = self.progressBar.update,args=())
        print ("all upload started")
        #pt = int(100/len(t))
        #rem = 100%len(t)
        #print("trying to set pbar",pt,rem)
        #self.progressBar['maximum'] = 100
        #self.progressBar["value"] = 5
        #print ("before update")
        #tup.start()
        print("sett")
        #tup.join()
        print ("before another loop")
        for i in range(len(t)):
            try:
                t[i].join()
                #self.progressBar["value"] = i*pt
                #self.progressBar.update()
                #self.progressBar["value"] = 0
                print("Trans started =", datetime.now().strftime("%H:%M:%S"))
                t2[i].start()
            except:
                print ("reload")
                return -1
        #self.progressBar["value"] = 100
        print("Upload finished =", datetime.now().strftime("%H:%M:%S"))
        print("Current Time =", datetime.now().strftime("%H:%M:%S"))
        for j in range(len(t2)):
            filetexts += t2[j].join()
            td.append(Thread(target = self.delete_blob,args = ("chunk{0}.wav".format(j),)))
            td[j].daemon = True
            td[j].start()
        print (filetexts)
        print("Finished Time =", datetime.now().strftime("%H:%M:%S"))
        return (filetexts)
    #td = 
"""
r = SpeechToText() 
if r == -1:
    print ("error")
else:
    print ("success")
"""
#makingchunks("D:\Stack\phrases.wav","wav",20)
        










        
              
app = Main()
app.mainloop() 