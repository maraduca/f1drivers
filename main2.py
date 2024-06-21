import tkinter as tk
from tkinter import PhotoImage, messagebox
import requests
from bs4 import BeautifulSoup


def extract_drivers_teams():
    url = 'https://www.formula1.com/en/teams'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        vector_links = soup.find_all('link', attrs={'as': 'image'})

        drivers_teams = []
        for i in range(0, len(vector_links), 4):
            team_link = vector_links[i]['href']
            team_name = team_link.split('/')[-1].replace('-logo.png', '').replace('-', ' ').title()

            driver1_link = vector_links[i+1]['href']
            driver1_parts = driver1_link.split('/')
            driver_name1 = driver1_parts[-2].split('_')[-1].replace('_', ' ')
            driver_name2 = driver1_parts[-2].split('_')[-2].replace('_', ' ')
            driver_name1 = f"{driver_name2} {driver_name1}"

            driver2_link = vector_links[i+2]['href']
            driver2_parts = driver2_link.split('/')
            driver_name3 = driver2_parts[-2].split('_')[-1].replace('_', ' ')
            driver_name4 = driver2_parts[-2].split('_')[-2].replace('_', ' ')
            driver_name2 = f"{driver_name4} {driver_name3}"

            team_image_url = vector_links[i]['href']
            driver1_image_url = vector_links[i+1]['href']
            driver2_image_url = vector_links[i+2]['href']

            drivers_teams.append({"team": team_name, "drivers": [driver_name1, driver_name2], "team_image": team_image_url, "driver1_image": driver1_image_url, "driver2_image": driver2_image_url})

        return drivers_teams
    else:
        print(f'Failed to retrieve page: {response.status_code}')
        return None
    
def get_red_bull_racing_info():
    
    url = "https://www.formula1.com/en/teams/red-bull-racing.html"

    response = requests.get(url)

 
    if response.status_code == 200:
  
        soup = BeautifulSoup(response.content, 'html.parser')

      
        title = soup.find('h1', class_='f1--xxs').text.strip()

        team_info = soup.find_all('div', class_='listing-item--team-info')
        details = [info.text.strip() for info in team_info]

    
        return {
            'title': title,
            'details': details
        }
    else:
        return None


def extract_tickets_info():
    url = 'https://tickets.formula1.com/en'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ticket_info = soup.find('div', class_='ticket-card__content')
        if ticket_info:
            return ticket_info.text.strip()
        else:
            return "Informații despre biletele la curse nu sunt disponibile în acest moment."
    else:
        print(f'Failed to retrieve page: {response.status_code}')
        return "Nu s-a putut accesa informațiile despre biletele la curse în acest moment."


def show_tickets_info():
    tickets_info = extract_tickets_info()
    messagebox.showinfo("Informații Bilete Formula 1", tickets_info)

def show_team_details(team_name):
    
    for item in drivers_teams:
        if item["team"] == team_name:
            team_details = f"Echipa: {item['team']}\n"
            team_details += f"Piloți: {', '.join(item['drivers'])}\n\n"
            team_details += "Detalii despre echipă:\n"
            
            team_details += "Istorie: Echipa cu sediul în (oraș/sediu), fondată în anul X, campioană mondială în anul Y.\n"

            return team_details

    return "Detalii despre echipă nedisponibile."

def show_drivers(event):
    
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        team_name = listbox.get(index) 

      
        for item in drivers_teams:
            if item["team"] in team_name: 
                drivers = ", ".join(item["drivers"])
                team_image_url = item["team_image"]
                driver1_image_url = item["driver1_image"]
                driver2_image_url = item["driver2_image"]
                
                show_drivers_window(item["team"], drivers, team_image_url, driver1_image_url, driver2_image_url)


def show_drivers_window(team_name, drivers, team_image_url, driver1_image_url, driver2_image_url):
   
    drivers_window = tk.Toplevel(root)
    drivers_window.title(f"Piloți pentru echipa {team_name}")

   
    screen_width = drivers_window.winfo_screenwidth()
    screen_height = drivers_window.winfo_screenheight()

    
    drivers_window.geometry(f"{screen_width}x{screen_height}+0+0")

    
    team_label = tk.Label(drivers_window, text=f"Echipa: {team_name}", font=("Helvetica", 16))
    team_label.pack(pady=10)

    
    team_image_data = requests.get(team_image_url).content
    team_photo = PhotoImage(data=team_image_data)
    team_image_label = tk.Label(drivers_window, image=team_photo)
    team_image_label.pack()

   
    drivers_label = tk.Label(drivers_window, text=f"Piloți: {drivers}", font=("Helvetica", 14))
    drivers_label.pack(pady=10)

    
    driver1_image_data = requests.get(driver1_image_url).content
    driver1_photo = PhotoImage(data=driver1_image_data)
    driver1_photo = driver1_photo.subsample(2, 2)  
    driver1_image_label = tk.Label(drivers_window, image=driver1_photo)
    driver1_image_label.pack(side=tk.LEFT, padx=20)

    driver2_image_data = requests.get(driver2_image_url).content
    driver2_photo = PhotoImage(data=driver2_image_data)
    driver2_photo = driver2_photo.subsample(2, 2) 
    driver2_image_label = tk.Label(drivers_window, image=driver2_photo)
    driver2_image_label.pack(side=tk.RIGHT, padx=20)

    
    team_details = show_team_details(team_name)
    team_details_label = tk.Label(drivers_window, text=team_details, font=("Helvetica", 12), justify=tk.LEFT)
    team_details_label.pack(pady=10)

   
    root.mainloop()


root = tk.Tk()
root.title("Piloți și Echipe Formula 1")


root.geometry("800x600")


listbox_frame = tk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


listbox = tk.Listbox(listbox_frame, width=100, height=25, font=("Helvetica", 12))
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


drivers_teams = extract_drivers_teams()
if drivers_teams:
    for item in drivers_teams:
        listbox.insert(tk.END, item['team']) 


listbox.bind("<ButtonRelease-1>", show_drivers)


tickets_button = tk.Button(root, text="Informații Bilete", font=("Helvetica", 12), command=show_tickets_info)
tickets_button.pack(pady=20)


root.mainloop()
