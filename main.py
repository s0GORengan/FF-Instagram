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

# Menampilkan hasil dalam format tabel
def display_results(non_followers):
    table = PrettyTable()
    table.field_names = ["No", "Username"]
    
    for index, user in enumerate(non_followers, start=1):
        table.add_row([index, user])
    
    print(table)

# Main
def main():
    # Load data
    followers_data = load_data('connections/followers_and_following/followers_1.json')  
    following_data = load_data('connections/followers_and_following/following.json')  

    # Dapatkan username
    followers = get_usernames(followers_data)
    following = get_usernames(following_data['relationships_following'])

    # Temukan non-followers
    non_followers = find_non_followers(followers, following)

    # Tampilkan hasil
    print("\nDaftar orang yang tidak mengikuti Anda tetapi Anda mengikutinya:")
    display_results(non_followers)

    # Pilihan untuk menyimpan output
    save_choice = input("\nSimpan output ke file? (csv/txt/tidak): ").strip().lower()
    if save_choice in ['csv', 'txt']:
        save_output(non_followers, save_choice)
    else:
        print("Output tidak disimpan.")

if __name__ == "__main__":
    main()