import os
import pandas as pd
from collections import defaultdict

input_folder = "simplified_output"
output_file = "genre_scores.csv"
genre_list = ['Pop', 'Rock', 'Hip Hop', 'R&B', 'Electronic/Dance', 'Country', 'Jazz', 'Reggae', 'Latin', 'Classical', '기타']
all_scores = []

file_list = os.listdir(input_folder)

for file_name in file_list:
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        if os.path.getsize(file_path) == 0:
            print(f"Skipping empty file: {file_name}")
            continue
        
        date = file_name.split("_")[0]  
        df = pd.read_csv(file_path)
        genre_scores = defaultdict(int)
        
        for _, row in df.iterrows():
            if pd.isnull(row['rank']):  
                continue  
            
            genres = row['simplified_genre'].split(', ')
            score = 101 - int(row['rank'])
            
            for genre in genres:
                genre = genre.lower()  
                if 'pop' in genre:
                    genre_scores['Pop'] += score
                elif 'rock' in genre:
                    genre_scores['Rock'] += score
                elif 'hip hop' in genre or 'rap' in genre:
                    genre_scores['Hip Hop'] += score
                elif 'r&b' in genre:
                    genre_scores['R&B'] += score
                elif 'electronic' in genre or 'edm' in genre or 'dance' in genre:
                    genre_scores['Electronic/Dance'] += score
                elif 'country' in genre:
                    genre_scores['Country'] += score
                elif 'jazz' in genre:
                    genre_scores['Jazz'] += score
                elif 'reggae' in genre:
                    genre_scores['Reggae'] += score
                elif 'latin' in genre:
                    genre_scores['Latin'] += score
                elif 'classical' in genre:
                    genre_scores['Classical'] += score
                else:
                    genre_scores['기타'] += score
        
        scores = [date] + [genre_scores.get(genre, 0) for genre in genre_list]
        all_scores.append(scores)

result_df = pd.DataFrame(all_scores, columns=['date'] + genre_list)
result_df.to_csv(output_file, index=False)
print(f"Genre scores saved to {output_file}")