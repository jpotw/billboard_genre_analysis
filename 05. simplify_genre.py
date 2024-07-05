import os
import pandas as pd
import ast

def simplify_genres(genres_str):
    if 'Need Manual Check' in genres_str:
        return None
    else:
        genres = ast.literal_eval(genres_str)
        for genre in genres:
            genre = genre.lower()
            if 'pop' in genre:
                return 'Pop'
            elif 'rock' in genre:
                return 'Rock'
            elif 'hip hop' in genre or 'rap' in genre:
                return 'Hip Hop'
            elif 'r&b' in genre:
                return 'R&B'
            elif 'electronic' in genre or 'edm' in genre or 'dance' in genre:
                return 'Electronic/Dance'
            elif 'country' in genre:
                return 'Country'
            elif 'jazz' in genre:
                return 'Jazz'
            elif 'reggae' in genre:
                return 'Reggae'
            elif 'latin' in genre:
                return 'Latin'
            elif 'classical' in genre:
                return 'Classical'
        return '기타'


# 입력 폴더 경로
input_folder = "output"

# 출력 폴더 경로
output_folder = "simplified_output"

# 출력 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 폴더 내의 모든 파일 가져오기
file_list = os.listdir(input_folder)

# 각 파일 처리
for file_name in file_list:
    if file_name.endswith(".csv"):
        # 파일 경로
        file_path = os.path.join(input_folder, file_name)
        
        # 파일 크기 확인
        if os.path.getsize(file_path) == 0:
            print(f"Skipping empty file: {file_name}")
            continue
        
        # CSV 파일 읽기
        df = pd.read_csv(file_path)
        
        # 'Need Manual Check'이 포함된 행 삭제
        # 장르 단순화
        df['simplified_genre'] = df['genres'].apply(simplify_genres)

        # 'Need Manual Check'이 포함된 행 삭제
        df = df[df['simplified_genre'].notnull()]
        
        # 새로운 파일 경로
        new_file_path = os.path.join(output_folder, file_name)
        
        # 수정된 데이터프레임 저장
        df.to_csv(new_file_path, index=False)

print("파일 수정 및 저장이 완료되었습니다.")