import os
import pandas as pd
import ast

def preprocess_data(file_path):
    # 파일이 비어있는지 확인
    if os.path.getsize(file_path) == 0:
        print(f"Warning: {file_path} is an empty file. Skipping preprocessing.")
        return None

    try:
        # CSV 파일 읽어들이기 (파싱 오류 행 건너뛰기)
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except pd.errors.EmptyDataError:
        print(f"Warning: {file_path} has no columns to parse. Returning an empty DataFrame.")
        return pd.DataFrame()  # 빈 데이터프레임 반환

    # 아티스트 이름의 불필요한 공백 제거
    df['artist'] = df['artist'].str.strip()

    # genre 정보 전처리
    def process_genres(genre_str):
        try:
            genres = ast.literal_eval(genre_str)
            return str(genres)
        except (SyntaxError, ValueError):
            # 형식이 잘못된 경우, 빈 리스트 반환
            return str([])

    df['genres'] = df['genres'].apply(process_genres)

    return df

# 입력 폴더와 출력 폴더 설정
input_folder = "output"
output_folder = "preprocessed_output"

# 출력 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 입력 폴더의 모든 파일 처리
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        preprocessed_df = preprocess_data(file_path)
        
        if preprocessed_df is not None and not preprocessed_df.empty:
            # 전처리된 데이터가 비어있지 않은 경우에만 출력 폴더에 저장
            preprocessed_df.to_csv(os.path.join(output_folder, file_name), index=False)