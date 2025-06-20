import tkinter as tk
from tkinter import ttk
import speech_recognition as sr

# Language to subjects mapping
language_subjects = {
    "English": ["Math", "Science", "English Grammar"],
    "Hindi": ["गणित", "विज्ञान", "हिंदी व्याकरण"],
    "Telugu": ["గణితం", "సైన్స్", "తెలుగు వ్యాకరణం"],
    "Kannada": ["ಗಣಿತ", "ವಿಜ್ಞಾನ", "ಕನ್ನಡ ವ್ಯಾಕರಣ"],
    "Tamil": ["கணிதம்", "அறிவு", "தமிழ் இலக்கணம்"]
}

# Subject content mapping
subject_contents = {
    "Math": {
        "5-10": "Learn basic addition, subtraction, multiplication, and division.",
        "11-15": "Explore algebra, geometry, and basic calculus.",
        "16-18": "Advanced topics in calculus, trigonometry, and statistics."
    },
    "Science": {
        "5-10": "Explore plants, animals, and basic experiments.",
        "11-15": "Learn about physics, chemistry, and biology.",
        "16-18": "Study advanced topics in physics, chemistry, and environmental science."
    },
    "English Grammar": {
        "5-10": "Practice nouns, verbs, tenses, and sentence formation.",
        "11-15": "Learn about advanced tenses, parts of speech, and complex sentence structures.",
        "16-18": "Master writing essays, research papers, and advanced grammar."
    },
    "गणित": {
        "5-10": "जोड़, घटाव, गुणा और भाग सीखें।",
        "11-15": "बीजगणित, रेखागणित और गणना के बारे में जानें।",
        "16-18": "कैल्कुलस, त्रिकोणमिति और सांख्यिकी में उन्नत विषय।"
    },
    "विज्ञान": {
        "5-10": "पौधे, जानवर और प्रयोगों का अध्ययन करें।",
        "11-15": "भौतिकी, रसायन विज्ञान और जीवविज्ञान सीखें।",
        "16-18": "भौतिकी, रसायन विज्ञान और पर्यावरण विज्ञान के उन्नत विषय पढ़ें।"
    },
    "हिंदी व्याकरण": {
        "5-10": "संज्ञा, क्रिया, काल और वाक्य रचना।",
        "11-15": "विस्तृत वाक्य रचनाएं और काव्यशास्त्र अध्ययन करें।",
        "16-18": "व्याकरण के जटिल नियमों का अध्ययन करें।"
    },
    "గణితం": {
        "5-10": "అడ్డిషన్, సబ్ట్రాక్షన్, మల్టిప్లికేషన్ మరియు డివిజన్ నేర్చుకోండి.",
        "11-15": "బీజగణితం, రేఖాగణితం మరియు కేల్కులస్ గురించి తెలుసుకోండి.",
        "16-18": "అధిక రేటింగ్‌లు, ట్రిగోనోమెట్రీ మరియు గణాంకాలు."
    },
    "సైన్స్": {
        "5-10": "చెట్లు, జంతువులు మరియు ప్రాథమిక ప్రయోగాలు తెలుసుకోండి.",
        "11-15": "భౌతిక శాస్త్రం, రసాయన శాస్త్రం మరియు జీవశాస్త్రం తెలుసుకోండి.",
        "16-18": "భౌతిక శాస్త్రం, రసాయన శాస్త్రం మరియు పర్యావరణ శాస్త్రం గురించి తెలుసుకోండి."
    },
    "తెలుగు వ్యాకరణం": {
        "5-10": "నామవాచకాలు, క్రియలు మరియు వాక్య నిర్మాణం అభ్యసించండి.",
        "11-15": "జనరల్ వ్యాకరణం మరియు కవిత్వం సాధన.",
        "16-18": "పరిష్కరణ వ్యాకరణం మరియు విశ్లేషణ."
    },
    "ಗಣಿತ": {
        "5-10": "ಜೋಡಣೆ, ಕಡಿತ, ಗುಣಾಕಾರ ಮತ್ತು ಭಾಗಾಕಾರವನ್ನು ಕಲಿಯಿರಿ.",
        "11-15": "ಬೀಜಗಣಿತ, ರೇಖಾಗಣಿತ ಮತ್ತು ಕೇಲ್ಕುಲಸ್ ಕುರಿತಂತೆ ತಿಳಿದುಕೊಳ್ಳಿ.",
        "16-18": "ಅಭ್ಯಾಸ ಕಲಿಕೆಗೆ ಉನ್ನತ ಮಟ್ಟದಲ್ಲಿ ಕೇಲ್ಕುಲಸ್, ಟ್ರಿಗೋನೋಮೆಟ್ರಿ ಮತ್ತು ಗಣಿತ ಸಂಶೋಧನೆ."
    },
    "ವಿಜ್ಞಾನ": {
        "5-10": "ಸಸ್ಯಗಳು, ಪ್ರಾಣಿಗಳು ಮತ್ತು ಪ್ರಯೋಗಗಳ ಅರಿವು.",
        "11-15": "ಭೌತಶಾಸ್ತ್ರ, ರಾಸಾಯನಶಾಸ್ತ್ರ ಮತ್ತು ಜೀವಶಾಸ್ತ್ರವನ್ನು ತಿಳಿದುಕೊಳ್ಳಿ.",
        "16-18": "ಭೌತಶಾಸ್ತ್ರ, ರಾಸಾಯನಶಾಸ್ತ್ರ ಮತ್ತು ಪರಿಸರ ವಿಜ್ಞಾನದಲ್ಲಿ ಉನ್ನತ ವಿಷಯಗಳು."
    },
    "ಕನ್ನಡ ವ್ಯಾಕರಣ": {
        "5-10": "ನಾಮಪದ, ಕ್ರಿಯಾಪದ ಮತ್ತು ವಾಕ್ಯ ರಚನೆ.",
        "11-15": "ವಿಶಿಷ್ಟ ವಾಕ್ಯ ರಚನೆ ಮತ್ತು ಕವಿತ್ವ.",
        "16-18": "ಅಧಿಕ ಜಟಿಲತೆಗಳಾದ ವಾಕ್ಯರಚನೆ ಅಧ್ಯಯನ."
    },
    "கணிதம்": {
        "5-10": "கூட்டல், கழித்தல், பெருக்கல், வகுத்தல் கற்போம்.",
        "11-15": "பீஜகணிதம், வரைகணிதம் மற்றும் காஸ்குலஸ் பற்றி அறிந்துகொள்ளுங்கள்.",
        "16-18": "மேம்பட்ட கணிதம் மற்றும் கணித ஆராய்ச்சி."
    },
    "அறிவு": {
        "5-10": "மரங்கள், விலங்குகள் மற்றும் அடிப்படை அறிவியல்.",
        "11-15": "புவியியல், வேதியியல் மற்றும் உயிரியல் கற்றுக்கொள்ளுங்கள்.",
        "16-18": "புவியியல், வேதியியல் மற்றும் சுற்றுச்சூழல் அறிவியல் படிக்கவும்."
    },
    "தமிழ் இலக்கணம்": {
        "5-10": "பெயர்ச்சொல், வினைச்சொல், காலங்கள் மற்றும் வாக்கியங்கள்.",
        "11-15": "முன்னணி தமிழ் இலக்கணம் மற்றும் கவிதைகள்.",
        "16-18": "ஆதிக இலகண்முறை படிப்புகளுக்கு முன்பதிவுகள்."
    }
}

class LanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Based Learning with Voice")
        self.root.geometry("650x550")
        self.root.configure(bg="#F9F9F9")

        self.age_label = tk.Label(root, text="Enter Your Age:", font=("Arial", 12), bg="#F9F9F9")
        self.age_label.pack(pady=10)

        self.age_entry = tk.Entry(root, font=("Arial", 12), width=10)
        self.age_entry.pack()

        self.age_voice_btn = tk.Button(root, text="🎙 Speak Age", command=self.speak_age, bg="#A5D6A7")
        self.age_voice_btn.pack(pady=5)

        self.lang_label = tk.Label(root, text="Choose a Language:", font=("Arial", 12), bg="#F9F9F9")
        self.lang_label.pack(pady=10)

        self.lang_combo = ttk.Combobox(root, values=list(language_subjects.keys()), state="readonly", font=("Arial", 12))
        self.lang_combo.pack()

        self.lang_voice_btn = tk.Button(root, text="🎙 Speak Language", command=self.speak_language, bg="#90CAF9")
        self.lang_voice_btn.pack(pady=5)

        self.lang_combo.bind("<<ComboboxSelected>>", self.show_subjects)

        self.subject_frame = tk.Frame(root, bg="#F9F9F9")
        self.subject_frame.pack(pady=10)

        self.content_label = tk.Label(root, text="", font=("Arial", 11), wraplength=600, justify="left", bg="#F9F9F9", fg="#444")
        self.content_label.pack(pady=10)

    def speak_age(self):
        age = self.recognize_voice(prompt="Say your age")
        if age and age.isdigit():
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, age)

    def speak_language(self):
        lang = self.recognize_voice(prompt="Say your language")
        if lang:
            for option in language_subjects.keys():
                if lang.lower() in option.lower():
                    self.lang_combo.set(option)
                    self.show_subjects(None)
                    break

    def recognize_voice(self, prompt="Speak now"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(prompt)
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print("Recognized:", text)
                return text.strip()
            except Exception as e:
                print("Error:", e)
                return ""

    def show_subjects(self, event):
        for widget in self.subject_frame.winfo_children():
            widget.destroy()

        selected_lang = self.lang_combo.get()
        age = self.age_entry.get()

        if not age.isdigit() or not (5 <= int(age) <= 18):
            self.content_label.config(text="Please enter a valid age between 5 and 18.")
            return

        subjects = language_subjects.get(selected_lang, [])
        tk.Label(self.subject_frame, text="Recommended Subjects:", font=("Arial", 12, "bold"), bg="#F9F9F9").pack()

        for subj in subjects:
            btn = tk.Button(self.subject_frame, text=subj, font=("Arial", 11), bg="#E3F2FD", fg="black",
                            command=lambda s=subj: self.show_content(s))
            btn.pack(pady=5, ipadx=10)

    def show_content(self, subject):
        age = self.age_entry.get()
        if age.isdigit():
            age_range = self.get_age_range(int(age))
            content = subject_contents.get(subject, {}).get(age_range, "Content coming soon!")
        else:
            content = "Please enter a valid age between 5 and 18."
        self.content_label.config(text=content)

    def get_age_range(self, age):
        if 5 <= age <= 10:
            return "5-10"
        elif 11 <= age <= 15:
            return "11-15"
        elif 16 <= age <= 18:
            return "16-18"
        return "5-10"  # Default case

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageApp(root)
    root.mainloop()
