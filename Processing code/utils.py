import pandas as pd 
import numpy as np
import os 

def check_create_directory(path: str) -> None:
    # Check if a directory exist otherwise create one.
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
    else:
        print(f"Directory already exists: {path}")

def transform_icc_data(combined_data: pd.DataFrame, response: str, column: str, max_size: int, return_df: bool) -> pd.DataFrame:
    # Take dataframe and convert in a way that we can calculate ICC scores. Similar to converting long format to wide format.
    
    # Process through dataset and save values.
    icc_data = {}
    for i in combined_data[column].unique():
        values = combined_data[combined_data[column] == i][response].values
        icc_data[i] = list(values)

    # Check whether all of them are same size otherwise add NaN values at the end.
    for i in icc_data.keys():
        if len(icc_data[i]) < max_size:
            icc_data[i].extend([np.nan] * (max_size - len(icc_data[i])))

    if return_df:
        return pd.DataFrame(icc_data).T
    else:
        return icc_data


def save_icc_data(data: pd.DataFrame, save_loc: str, cols: list, names: list, image_col: str, max_size: int, return_df: bool) -> pd.DataFrame:
    # Save all icc data given data and columns.
    icc_data = []
    for i in range(len(cols)):
        icc_data.append(transform_icc_data(data, cols[i],image_col,max_size, return_df))
        icc_data[i].to_csv(os.path.join(save_loc, f"icc_{names[i]}.csv"),index = False)

    if return_df:
        return icc_data

# Simple function to call groupby average for multiple columns
def groupby_average(data: pd.DataFrame, group_col: str, target_cols: list) -> pd.DataFrame:
    return data.groupby(group_col)[target_cols].mean().reset_index()

def get_duration(data: pd.DataFrame):
    # Get duration of one study
    return data["data.duration"].str.replace(",", ".").astype(float) / 1000

def attention_check(data: pd.DataFrame, attention_check_images: list, target: str) -> dict:
    # Check how many attention check images was correctly selected.
    attention_result = {}
    unique_ids = data.session.unique()
    if not attention_check_images:
        attention_check_images = ["attention_check_1.png","attention_check_2.png","attention_check_3.png","attention_check_4.png","attention_check_5.png"]
    
    for i in unique_ids:
        temp_data = data[data["session"] == i]
        temp_data = temp_data[temp_data["data.img_idx"].isin(attention_check_images)]
        temp_data["attention_value"] = [int(i.split("_")[-1].split(".")[0]) for i in temp_data["data.img_idx"]]
        attention_result[i] = []
        for j in range(len(temp_data)):
            attention_result[i].append(temp_data[target].iloc[j] == temp_data[target].iloc[j] == temp_data["attention_value"].iloc[j])

    return attention_result

def get_overall_duration(data: pd.DataFrame) -> dict:
    # Get how long it take for participants to finish study
    unique_ids = data.session.unique()
    duration_result = {}
    for i in unique_ids:
        temp_data = data[data["session"] == i]
        start_session = pd.to_datetime(temp_data["data.timestamp"].iloc[0], format='%Y-%m-%dT%H:%M:%S.%fZ')
        end_session = pd.to_datetime(temp_data["data.timestamp"].iloc[-1], format='%Y-%m-%dT%H:%M:%S.%fZ')
        duration_result[i] = (end_session - start_session).total_seconds() / 60
    return duration_result

def check_experiment_finished(data: pd.DataFrame) -> dict:
    # Check whether participants finished the experiment or not. 
    unique_ids = data.session.unique()
    experiment_finish = {}
    for i in unique_ids:
        temp_data = data[data.session == i]
        temp_data = temp_data[temp_data["data.sender"] == "Experiment End"]
        
        if len(temp_data) >= 1: # Fix this!!!1
            experiment_finish[i] = True
        elif len(temp_data) == 0:
            experiment_finish[i] = False
        else:
            experiment_finish[i] = "??"
    
    return experiment_finish

def exclude_images(data: pd.DataFrame) -> pd.DataFrame:
    # Exclude Attention check, baseline and practice images
    attention_check_images = ["attention_check_1.png","attention_check_2.png","attention_check_3.png","attention_check_4.png","attention_check_5.png"]
    baseline_images = ['living room_31.png','living room_40.png','living room_70.png', 
                        'office room_4.png','office room_46.png','office room_64.png',
                        "restaurant_4.png", "restaurant_28.png", "restaurant_48.png"]
    practice_image = ["living room_0.png", "office room_24.png", "restaurant_80.png"]
    data = data[~data["data.img_idx"].isin(attention_check_images)]
    data = data[~data["data.img_idx"].isin(baseline_images)]
    data = data[~data["data.img_idx"].isin(practice_image)]
    return data

def practice_ratings(data: pd.DataFrame) -> pd.DataFrame:
    # Get practice image ratings
    practice_image = ["living room_0.png", "office room_24.png", "restaurant_80.png"]
    practice_data = data[data["data.img_idx_practice"].isin(practice_image)]
    practice_data = drop_duplicate_images(practice_data, "data.img_idx_practice")
    return practice_data

def baseline_ratings(data: pd.DataFrame) -> pd.DataFrame:
    # Get baseline image ratings    
    baseline_images = ['living room_31.png','living room_40.png','living room_70.png', 
                        'office room_4.png','office room_46.png','office room_64.png',
                        "restaurant_4.png", "restaurant_28.png", "restaurant_48.png"]

    baseline_data = data[data["data.img_idx"].isin(baseline_images)]
    baseline_data = drop_duplicate_images(baseline_data, "data.img_idx")
    return baseline_data

def drop_duplicate_images(data: pd.DataFrame, column: str) -> pd.DataFrame:
    # Drops duplicate images in the data. We do this because LabJs data returns multiple images with the same data.
    return pd.concat([group.drop_duplicates(subset=[column]) for _, group in data.groupby("session")]).reset_index(drop=True)

def n_image_completed(data: pd.DataFrame) -> dict:
    # Calculate number of images completed for all participants. This was used to check whether participants rated all images.
    unique_ids = data.session.unique()
    n_images = {}
    for i in unique_ids:
        n_images[i] = len(data[data.session == i])

    return n_images

def process_data(loc: str, target:str ) -> pd.DataFrame:
    # Read data from individual study
    data = pd.read_csv(loc, delimiter=";")
    # Get prolific IDs in the study
    prolific_ids = get_prolific_ids(data)
    # Get excluded participants ids
    excluded_ids = missing_participants_ids()
    # Remove participants if they are in excluded ids.
    for i in prolific_ids.keys():
        if i in excluded_ids:
            data = data[data["session"] != prolific_ids[i]]

    # Filter TEST responses created by the authors for testing the study.
    data = filter_data_by_the_index(data, prolific_ids)

    # Get prolific ids again
    prolific_ids = get_prolific_ids(data)

    # Select only not NA values in the data
    data = data[data[target].notna()]
    # Select only Not NA values in practice images
    practice_data = data[data["data.img_idx_practice"].notna()]
    data = data[data["data.img_idx"].notna()]

    # Transform "data.img_idx" so it only has name of the image not the whole directory
    data["data.img_idx"] = [i.split("\\")[-1] for i in data["data.img_idx"]]
    # To do the same transfromation for practice images
    practice_data["data.img_idx_practice"] = [i.split("\\")[-1] for i in practice_data["data.img_idx_practice"]]
    # Drop duplicate images in the data
    data = drop_duplicate_images(data, "data.img_idx")
    # Remove sessions with with no data.
    removed_sessions = ["session_787",
                        "session_44",
                        "session_41"]
    data = data[~data["session"].isin(removed_sessions)]
    practice_data = practice_data[~practice_data["session"].isin(removed_sessions)]
    
    # Get baseline data
    baseline_data = baseline_ratings(data)
    # Get baseline practice data
    practice_data = practice_ratings(practice_data)
    # Get attention check data
    attention_data = attention_check(data, None, target)
    # Exclude baseline, practice and attention check images
    data = exclude_images(data)

    return data, prolific_ids, baseline_data, practice_data, attention_data


def get_prolific_ids(data: pd.DataFrame) -> list:
    # Get Prolific IDS.
    unique_ids = data[data["data.ProlificID"].notna()]["data.ProlificID"].unique()
    ids = {data[data["data.ProlificID"] == i]["data.ProlificID"].unique().item():data[data["data.ProlificID"] == i]["session"].unique()[-1] for i in unique_ids}
    return ids

def filter_data_by_the_index(data: pd.DataFrame, prolific_ids: dict) -> pd.DataFrame:
    for i in prolific_ids.keys():
        if not i.startswith("TEST") and not i.startswith("test"):
            start_index = data[data["data.ProlificID"] == i].index[0].item()
            break

    return data[start_index:]

def process_demographic_data(loc: str) -> pd.DataFrame:
    # Load data
    data_demographic = pd.read_csv(loc)
    # Get IDs of excluded participants
    excluded_ids = missing_participants_ids()
    # Remove excluded participants and expired data
    data_demographic = data_demographic[~data_demographic["Participant id"].isin(excluded_ids)]
    data_demographic = data_demographic[data_demographic.Status == "APPROVED"]
    # Select columns that are relevant
    data_demographic = data_demographic[['Participant id', 'Time taken','Age', 'Sex',
        'Ethnicity simplified', 'Country of birth', 'Country of residence',
        'Nationality', 'Language', 'Student status', 'Employment status', 'Total approvals','Status']]
    data_demographic["Time taken"] = data_demographic["Time taken"] / 60
    return data_demographic

def missing_participants_ids(): # -> These are anonymized prolific IDs for both studies.
    return pd.read_csv('..\missing_ids.txt', sep=",", header=None)[0].tolist() 


def process_equivalence_data(baseline_data: pd.DataFrame, affective_response: str) -> pd.DataFrame:
    # Load and process data from Deniz et al. (2025)
    data_Deniz2025 = pd.read_csv(r"..\\Data for equivalence testing\Deniz2025_baseline.csv")
    data_Deniz2025 = data_Deniz2025[["image", "participant", "Negative_Positive.response", "Leave_Enter.response","Sleepy_Awake.response", "Tense_Relaxed.response"]]
    data_Deniz2025["participant"] = [f"P_{i}" for i in data_Deniz2025["participant"]]
    data_Deniz2025.rename(columns={"Negative_Positive.response": "valence", "Leave_Enter.response": "approach",
                               "Sleepy_Awake.response": "tense", "Tense_Relaxed.response": "energetic"}, inplace = True)
    data_Deniz2025["study"] = "Deniz2025"
    # Process the baseline data from IDEAS
    baseline_data.rename(columns={"data.valence":"valence","data.approach":"approach", 
                              "data.img_idx":"image", "session":"participant",
                              "data.tense":"tense", "data.energetic":"energetic"}, inplace = True)

    baseline_data["image"] = [i.split(".")[0] for i in baseline_data["image"]]
    baseline_data["study"] = "IDEAS"
    # If it is valence/approach studies save them 
    if affective_response == "valence":
        data_Deniz2025 = data_Deniz2025[["image", "participant","valence", "approach", "study"]]
        
        baseline_data = baseline_data[["participant","valence", "approach", "image", "study"]]

        pd.concat([baseline_data, data_Deniz2025], axis = 0).to_csv(r"..\\Data for equivalence testing\valence_approach_data.csv",index = False)
    # If it is tense/energetic studies save them 
    if affective_response == "tense":
        data_Deniz2025 = data_Deniz2025[["image", "participant","tense", "energetic", "study"]]
        baseline_data = baseline_data[["participant","tense", "energetic", "image", "study"]]

        pd.concat([baseline_data, data_Deniz2025], axis = 0).to_csv(r"..\\Data for equivalence testing\tense_energetic_data.csv", index = False)
