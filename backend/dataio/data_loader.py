import pandas as pd
import os


# create a class AnimeDataLoader with constructor that take original_csv and processed_csv as parameters
class AnimeDataLoader:
    def __init__(self, original_csv: str):
        self.original_csv = original_csv

    def load_and_process(self) -> pd.DataFrame:
        try:
            # Try to read the original CSV file
            df = pd.read_csv(self.original_csv, encoding="utf-8", on_bad_lines="skip")
            required_cols = {"Name", "Genre", "Synopsis"}
            # Check which required columns are present and which are missing
            missing_cols = required_cols - set(df.columns)
            if missing_cols:
                missing_list = ", ".join(sorted(missing_cols))
                raise ValueError(
                    f"CSV file is missing required column(s): {missing_list}"
                )
            # create a new  column 'combined_info' by concatenating 'Name', 'Genre', and 'synopsis' columns
            # The value should look lke Title: <Name> Overview: <synopsis> Genres: <Genre>
            df["combined_info"] = (
                "Title: "
                + df["Name"].astype(str)
                + " Overview: "
                + df["Synopsis"].astype(str)
                + " Genres: "
                + df["Genre"].astype(str)
            )
            # convert combined_info to CSV and save to processed_csv. Index should be False and encoding should be 'utf-8'
            processed_csv = os.path.join("data", "anime_processed.csv")
            df[["combined_info"]].to_csv(
                processed_csv, index=False, encoding="utf-8"
            )
        except FileNotFoundError:
            # raise exception
            raise FileNotFoundError(f"The file {self.original_csv} was not found.")
        except pd.errors.EmptyDataError:
            # raise exception
            raise ValueError(f"The file {self.original_csv} is empty.")
        # return the processed csv
        return processed_csv