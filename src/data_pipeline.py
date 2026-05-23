import pandas as pd
from extractors import extract_features_from_csv_file
from files import list_files_in_directory

if __name__ == "__main__":
    SAMPLING_RATE = 10000
    files_names = list_files_in_directory("data/raw")
    # print(files_names)

    features_list = []

    print("Main Extraction Loop Started!")
    for idx, file_name in enumerate(files_names):
        try:
            file_features = extract_features_from_csv_file(
                "data/raw" + "/" + file_name, SAMPLING_RATE=SAMPLING_RATE
            )

            features_list.append(file_features)
            print("-" * 34)
            print(f"Extracted features from {idx+1}/2618 files")
        except Exception as e:
            print(f"Error processing file ({idx+1}), with name of :{file_name}")
            continue
    print("Main Extraction Loop Finished!")
    df = pd.DataFrame(features_list)

    df.to_csv("data/processed/features.csv", index=False)
    print("features.csv created.")
