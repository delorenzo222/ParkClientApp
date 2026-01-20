import customtkinter as ctk
import requests
import json

class ParkApp(ctk.CTk):
    def __init__(self, config_path="config.json"):
        super().__init__()

        # Laden der JSON Datei mit den Verlinkungen
        with open(config_path, 'r') as file:
            config = json.load(file)

            # API Basis-URL und Admin-URL
            self.base_api_url = config['urls']['base_api']
            self.admin_url = config['urls']['admin_api']

        # Client Fenster
        self.title("ParkAPI Desktop Client")
        self.geometry("1000x1200")

        # Titel
        self.label = ctk.CTkLabel(self, text="Parkplatz Management", font=("Arial", 22, "bold"))
        self.label.pack(pady=20)


        # Alle Daten laden
        self.all_button = ctk.CTkButton(self, text="Alle Parkplätze anzeigen", command=self.lade_alle_daten)
        self.all_button.pack(pady=10)


        # Einzelnen Parkplatz mit ID suchen
        self.label = ctk.CTkLabel(self, text="Information über bestimmten Parkplatz", font=("Arial", 20))
        self.label.pack()

        self.search_frame = ctk.CTkFrame(self) # Gruppierung für schöneres Layout
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.id_entry = ctk.CTkEntry(self.search_frame, placeholder_text="ID eingeben (z.B. 1)")
        self.id_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.search_button = ctk.CTkButton(self.search_frame, text="Suchen", width=100, command=self.suche_einzelnen_platz)
        self.search_button.pack(side="right", padx=10)




        # Verfügbare Parkplätze eines bestimmten Parkplatz ausgeben
        self.label = ctk.CTkLabel(self, text="Verfügbare Parkplätze bei bestimmter ID", font=("Arial", 20))
        self.label.pack()

        self.search_frame = ctk.CTkFrame(self) # Gruppierung für schöneres Layout
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.id_entry2 = ctk.CTkEntry(self.search_frame, placeholder_text="ID eingeben (z.B. 1)")
        self.id_entry2.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.search_button = ctk.CTkButton(self.search_frame, text="Suchen", width=100, command=self.freie_plaetze)
        self.search_button.pack(side="right", padx=10)




        # Neuen Parkplatz hinzufügen
        self.add_label = ctk.CTkLabel(self, text="Parkplatz hinzufügen", font=("Arial", 20))
        self.add_label.pack(pady=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name des Parkplatzes")
        self.name_entry.pack()

        self.city_entry = ctk.CTkEntry(self, placeholder_text="Ort des Parkplatzes")
        self.city_entry.pack()

        self.totalSpots_entry = ctk.CTkEntry(self, placeholder_text="Maximale Kapazität")
        self.totalSpots_entry.pack()

        self.add_button = ctk.CTkButton(self, text="Hinzufügen", fg_color="green", command=self.neuen_parkplatz_posten)
        self.add_button.pack()




        # Parkplatz löschen
        self.add_label = ctk.CTkLabel(self, text="Parkplatz löschen", font=("Arial", 20))
        self.add_label.pack(pady=20)

        self.search_frame = ctk.CTkFrame(self) # Gruppierung für schöneres Layout
        self.search_frame.pack()

        self.id_entry3 = ctk.CTkEntry(self.search_frame, placeholder_text="ID eingeben (z.B. 1)")
        self.id_entry3.pack()

        self.delete_button = ctk.CTkButton(
        self.search_frame, 
        text="Löschen", 
        fg_color="red",      # Rot signalisiert Löschen
        hover_color="darkred", 
        command=self.delete_parkplatz
        )
        self.delete_button.pack()

        # ERGEBNIS ANZEIGE
        self.result_box = ctk.CTkTextbox(self, width=450, height=250)
        self.result_box.pack(pady=20, padx=20)
        self.result_box.insert("0.0", "Willkommen! Bitte wählen Sie eine Aktion.")
        self.result_box.configure(state="disabled")

    def schreibe_in_box(self, text):
        """Hilfsfunktion zum sauberen Schreiben in die Box"""
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("end", text)
        self.result_box.configure(state="disabled")





    # Methode um alle Parkplätze abzurufen
    def lade_alle_daten(self):
        self.schreibe_in_box("Lade alle Parkplätze...")
        try:
            # /all
            response = requests.get(f"{self.base_api_url}/all", timeout=5)
            response.raise_for_status()
            parkplaetze = response.json()

            # Falls keine Parkplätze vorhanden sind
            if not parkplaetze:
                self.schreibe_in_box("Keine Parkplätze gefunden.")
            else:
                ausgabe = "VERFÜGBARE PARKPLÄTZE:\n" + "="*30 + "\n"
                for platz in parkplaetze:
                    ausgabe += f"ID: {platz['id']} | Name: {platz['name']}\n"
                self.schreibe_in_box(ausgabe)
        except Exception as e:
            self.schreibe_in_box(f"Fehler: {str(e)}")





    # Methode um nur den gewünschten Parkplatz abzurufen
    def suche_einzelnen_platz(self):
        p_id = self.id_entry.get().strip()
        if not p_id:
            self.schreibe_in_box("Fehler: Bitte eine ID eingeben!")
            return

        self.schreibe_in_box(f"Suche ID {p_id}...")
        try:
            # /{id}
            response = requests.get(f"{self.base_api_url}/{p_id}", timeout=5)
            
            # Erfolg
            if response.status_code == 200:
                platz = response.json()
                info = f"EINZELANSICHT:\n" + "="*30 + "\n"
                info += f"ID: {platz['id']}\nName: {platz['name']}\nKapazität: {platz['totalSpots']}"
                self.schreibe_in_box(info)
            # Fehler
            elif response.status_code == 404:
                self.schreibe_in_box(f"ID {p_id} wurde nicht gefunden.")
            else:
                self.schreibe_in_box(f"Server-Fehler: {response.status_code}")
        except Exception as e:
            self.schreibe_in_box(f"Verbindungsfehler: {str(e)}")






    # Methode um freie Plätze bei bestimmter ID zu ermitteln
    def freie_plaetze(self):
        p_id = self.id_entry2.get().strip()
        if not p_id:
            self.schreibe_in_box("Fehler: Bitte eine ID eingeben!")
            return
        
        self.schreibe_in_box(f"Suche ID {p_id}...")
        try:
            response = requests.get(f"{self.base_api_url}/{p_id}/free", timeout=5)

            # Erfolg
            if response.status_code == 200:
                platz = response.json()
                info = f"Freie Plätze bei {p_id}: {platz}"
                self.schreibe_in_box(info)
                
            # Fehler
            elif response.status_code == 404:
                self.schreibe_in_box(f"ID {p_id} wurde nicht gefunden.")
            else:
                self.schreibe_in_box(f"Server-Fehler: {response.status_code}")
        except Exception as e:
            self.schreibe_in_box(f"Verbindungsfehler: {str(e)}")

        




    # Methode um neuen Parkplatz hinzuzufügen
    def neuen_parkplatz_posten(self):
        # Daten aus UI holen
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        totalSpots = self.totalSpots_entry.get().strip()

        if not name or not city or not totalSpots:
            self.schreibe_in_box("Fehler: Alle Felder ausfüllen")
            return

        try:
            # Daten für die API vorbereiten
            daten_paket = {
                "name": name,
                "city": city,
                "totalSpots": int(totalSpots) 
            }

            # POST an das C# Backend senden
            response = requests.post(self.admin_url, json=daten_paket, timeout=5)

            if response.status_code in [200, 201]:
                self.schreibe_in_box(f"Erfolg: Parkplatz '{name}' wurde erstellt!")
                # Felder leeren
                self.name_entry.delete(0, "end")
                self.city_entry.delete(0, "end")
                self.totalSpots_entry.delete(0, "end")
                self.lade_alle_daten() # Liste direkt erneuern
            else:
                self.schreibe_in_box(f"API Fehler {response.status_code}: {response.text}")

        except ValueError:
            self.schreibe_in_box("Fehler: Anzahl muss eine Zahl sein!")
        except Exception as e:
            self.schreibe_in_box(f"Verbindungsfehler: {e}")
    





    # Methode um einen Parkplatz zu löschen
    def delete_parkplatz(self):

        p_id = self.id_entry3.get().strip()
    
        if not p_id:
            self.schreibe_in_box("Fehler: Bitte eine ID zum Löschen eingeben!")
            return

        # Sicherheitsabfrage (optional)
        self.schreibe_in_box(f"Versuche ID {p_id} zu löschen...")
    
        try:
            # requests.delete statt requests.get
            url = f"{self.admin_url}/{p_id}"
            response = requests.delete(url, timeout=5)

            if response.status_code == 200 or response.status_code == 204:
                self.schreibe_in_box(f"Erfolg: Parkhaus mit ID {p_id} wurde gelöscht.")
                self.id_entry.delete(0, 'end') # Eingabefeld leeren
            elif response.status_code == 404:
                self.schreibe_in_box(f"Fehler: ID {p_id} existiert nicht.")
            elif response.status_code == 401:
                self.schreibe_in_box("Fehler: Keine Berechtigung (Admin erforderlich).")
            else:
                self.schreibe_in_box(f"Server-Fehler: {response.status_code}")

        except Exception as e:
            self.schreibe_in_box(f"Verbindungsfehler: {str(e)}")



if __name__ == "__main__":
    app = ParkApp()
    app.mainloop()