import tkinter as tk
from tkinter import filedialog,messagebox
import threading
import moviepy.editor as mp
import speech_recognition as sr
import cv2
from googletrans import Translator
import sqlite3
class VideoCaptionGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Caption Generator")

        self.label = tk.Label(master, text="Select Video File:")
        self.label.pack()

        self.select_button = tk.Button(master, text="Select", command=self.select_video)
        self.select_button.pack()

        self.convert_button = tk.Button(master, text="Generate Captions", command=self.generate_captions)
        self.convert_button.pack()

        self.translator = Translator()

    def select_video(self):
        self.video_file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])

    def video_to_audio(self):
        video_clip = mp.VideoFileClip(self.video_file_path)
        audio_path = "audio_from_video.wav"
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        return audio_path

    def audio_to_text(self, audio_path):
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source , duration=None)
                text = recognizer.recognize_google(audio_data)
            return text
        except Exception as e:
            print("Error during audio-to-text conversation:", e)
            return ""

    def translate_text(self, text, source_lang='en', target_lang='mr'):
        translated_text = self.translator.translate(text, src=source_lang, dest=target_lang).text
        return translated_text

    def generate_captions(self):
        if hasattr(self, 'video_file_path'):
            threading.Thread(target=self.process_video).start()
        else:
            print("Please select a video file first.")

    def write_to_file(self, text):
        with open("translated_captions.txt", "a", encoding="utf-8") as file:
            file.write(text + "\n")
    def process_video(self):
        audio_path = self.video_to_audio()
        text = self.audio_to_text(audio_path)
        if text:
            print("Transcribed Text:", text)
            translated_text = self.translate_text(text)
            print("Translated Text:", translated_text)
            self.write_to_file(translated_text)
            self.display_video_with_captions(translated_text)
        else:
            print("No caption generated. Please check the audio file.")

    def display_video_with_captions(self, captions):
        cap = cv2.VideoCapture(self.video_file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.putText(frame, captions, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Video with Captions', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


def create_table():
    conn = sqlite3.connect('login_credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def open_video_generator():
    root.withdraw()  # Hide login window
    root_video = tk.Toplevel()  # Create new window for video caption generator
    #root.geometry("900x900")
    root_video.geometry("800x800")
    root_video.configure(bg="lightblue")
    app_video = VideoCaptionGeneratorApp(root_video)

#root = tk.Tk()
#app = VideoCaptionGeneratorApp(root)
class Login:
    def __init__(self, master):
        self.master = master
        master.title("Login System")
         
        self.label = tk.Label(master, text="Login Here!!!!!!!!",font=("Algerian",25,"bold"),bg="#fafad2",padx=10,pady=10)
        self.label.pack(side="top",pady=50)
        # Username label and entry
        self.label_username = tk.Label(master, text="Username:", font=("Times New Roman", 12, "bold"),padx=10, pady=5)
        self.label_username.pack()
        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=15)

        # Password label and entry
        self.label_password = tk.Label(master, text="Password:", font=("Times New Roman", 12, "bold"),padx=10, pady=5)
        self.label_password.pack()
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack(pady=15)


        # Login button
        self.button_login = tk.Button(master, text="Login", command=self.login, font=("Times New Roman", 12, "bold"),bg="#4633FF")
        self.button_login.pack(pady=15)

        # Register button
        self.button_register = tk.Button(master, text="Register", command=self.register, font=("Times New Roman", 12, "bold"),bg="#4633FF")
        self.button_register.pack(pady=15)

    def register(self):
       username = self.entry_username.get()
       password = self.entry_password.get()

       conn = sqlite3.connect('login_credentials.db')
       c = conn.cursor()
       try:
          c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
          conn.commit()
          messagebox.showinfo("Success", "Registration successful!")
       except sqlite3.IntegrityError:
          messagebox.showerror("Error", "Username already exists!")
          conn.close()
    def login(self):
          username =self.entry_username.get()
          password =self.entry_password.get()

          conn = sqlite3.connect('login_credentials.db')
          c = conn.cursor()
          c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
          result = c.fetchone()
          conn.close()

          if result:
            messagebox.showinfo("Success", "Login successful!")
            open_video_generator()
          else:
            messagebox.showerror("Error", "Invalid username or password")
root = tk.Tk()
app = Login(root)
#root.mainloop()
root.geometry("400x400")
root.configure(bg="#ffcccc")
root.mainloop()
