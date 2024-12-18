import json
import pandas as pd
from prettytable import PrettyTable

# Memuat data dari file JSON
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Mendapatkan daftar username dari data
def get_usernames(data):
    return {item['string_list_data'][0]['value'] for item in data}

# Membandingkan followers dan following
def find_non_followers(followers, following):
    return following - followers

# Menyimpan output ke file
def save_output(non_followers, file_format):
    if file_format == 'csv':
        df = pd.DataFrame(non_followers, columns=['Non-Followers'])
        df.to_csv('non_followers.csv', index=False)
        print("Output saved to non_followers.csv")
    elif file_format == 'txt':
        with open('non_followers.txt', 'w') as file:
            for user in non_followers:
                file.write(f"{user}\n")
        print("Output saved to non_followers.txt")
    elif file_format == 'xlsx':
        df = pd.DataFrame(non_followers, columns=['Non-Followers'])
        df.to_excel('non_followers.xlsx', index=False)
        print("Output saved to non_followers.xlsx")

# Menampilkan hasil dalam format tabel
def display_results(non_followers):
    table = PrettyTable()
    table.field_names = ["No", "Username"]
    
    for index, user in enumerate(non_followers, start=1):
        table.add_row([index, user])
    
    print(table)

# Menampilkan statistik
def display_statistics(followers, following, non_followers):
    print("\n--- Statistik ---")
    print(f"Jumlah Followers: {len(followers)}")
    print(f"Jumlah Following: {len(following)}")
    print(f"Jumlah Non-Followers: {len(non_followers)}")

# Main
def main():
    # Pilih file JSON followers dan following
    followers_file = input("Masukkan path file followers (default: followers_1.json): ").strip() or 'connections/followers_and_following/followers_1.json'
    following_file = input("Masukkan path file following (default: following.json): ").strip() or 'connections/followers_and_following/following.json'

    # Load data
    followers_data = load_data(followers_file)  
    following_data = load_data(following_file)  

    # Dapatkan username
    followers = get_usernames(followers_data)
    following = get_usernames(following_data['relationships_following'])

    # Temukan non-followers
    non_followers = find_non_followers(followers, following)

    # Tampilkan statistik
    display_statistics(followers, following, non_followers)

    # Filter dengan keyword (opsional)
    keyword = input("\nFilter hasil dengan keyword (tekan Enter untuk skip): ").strip()
    if keyword:
        non_followers = {user for user in non_followers if keyword.lower() in user.lower()}

    # Tampilkan hasil
    print("\nDaftar orang yang tidak mengikuti Anda tetapi Anda mengikutinya:")
    display_results(non_followers)

    # Pilihan untuk menyimpan output
    save_choice = input("\nSimpan output ke file? (csv/txt/xlsx/tidak): ").strip().lower()
    if save_choice in ['csv', 'txt', 'xlsx']:
        save_output(non_followers, save_choice)
    else:
        print("Output tidak disimpan.")

if __name__ == "__main__":
    main()
