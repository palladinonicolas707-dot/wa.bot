import sys
import time
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# Configurazione della tua API Key di Gemini
GOOGLE_API_KEY = "AQ.Ab8RN6LdGTkUc21NryTU6GG9XviPzDYIFvePszysXYeQxl7YTw"
genai.configure(api_key=GOOGLE_API_KEY)

# Configurazione del modello Gemini
modello = genai.GenerativeModel('gemini-3.6-flash')

# Inizializziamo il motore vocale e il Riconoscitore audio
motore = pyttsx3.init()
recognizer = sr.Recognizer()

def parla(testo):
    print(f"IA (Voce): {testo}")
    motore.say(testo)
    motore.runAndWait()

def ascolta_microfono():
    with sr.Microphone() as source:
        print("\n[In ascolto dal microfono... Parla ora!]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            testo_riconosciuto = recognizer.recognize_google(audio, language="it-IT")
            print( tu := f"Tu (Voce): {testo_riconosciuto}")
            return testo_riconosciuto.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Errore microfono: {e}")
            return ""

def avvia_assistente():
    print("==========================================")
    print("   ASSISTENTE ZTE VOCALE & GEMINI         ")
    print("==========================================")
    parla("Sistema vocale avviato. Pronuncia zte per risvegliarmi.")
    
    while True:
        # Ascoltiamo continuamente l'ambiente
        comando = ascolta_microfono()
        
        if "zte" in comando:
            parla("Dimmi creatore, ti ascolto!")
            
            while True:
                input_utente = ascolta_microfono()
                
                if not input_utente:
                    continue
                
                if "esci" in input_utente or "spegniti" in input_utente or "torna in background" in input_utente:
                    parla("Torno in background. Dimmi zte per richiamarmi.")
                    break
                
                try:
                    print(f"Invio a Gemini: {input_utente}")
                    risposta_api = modello.generate_content(input_utente)
                    testo_risposta = risposta_api.text
                    
                    print(f"Gemini: {testo_risposta}")
                    parla(testo_risposta)
                    
                except Exception as e:
                    parla("Scusa, c'è stato un problema di connessione con le mie API.")
                    print(f"Errore tecnico: {e}")
                    
        elif "spegni app" in comando:
            parla("Chiusura dell'applicazione in corso. Ciao!")
            sys.exit()

if __name__ == "__main__":
    avvia_assistente()
