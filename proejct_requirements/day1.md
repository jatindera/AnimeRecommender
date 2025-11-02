## 🎯 **Project Overview**

**Project Name:** `AnimeRecommenderSystem`
**Goal:** Build a system that can recommend anime shows based on their description, genre, and other information.
We will start small — by **loading, cleaning, and processing anime data** from a CSV file.

---

## 📁 **Step 1: Project Folder Structure**

Ask students to create the following folders and files:

```
AnimeRecommenderSystem/
│
├── src/
│   └── data_loader.py
│
├── data/
│   ├── anime_raw.csv        # Original input data (Sample file is available in data folder)
│   └── anime_processed.csv  # Will be created by the code
│
└── README.md
```

Explain:

* `src/` holds all the Python code.
* `data/` holds input/output files.
* `README.md` will explain the project.

---

## 🧠 **Step 2: Understanding What the Code Does**

Tell students this file (`data_loader.py`) is about:

> “Reading anime data from a CSV file, checking if important columns exist, combining some text into one column, and saving it into a new processed file.”

---

## 🧩 **Step 3: Requirements for `AnimeDataLoader` class**

Ask students to create the following **requirements one by one** (you’ll assign them gradually in class):

---

### ✅ **Requirement 1 — Create the Class**

* File: `src/data_loader.py`
* Create a class called `AnimeDataLoader`.
* The constructor (`__init__`) should take two parameters:

  * `original_csv`: the path to the raw CSV file
  * `processed_csv`: the path where processed CSV will be saved
* Save both parameters as class variables (`self.original_csv`, `self.processed_csv`).

📘 *Goal:* Learn to design a class that holds configuration data (file paths).

---

### ✅ **Requirement 2 — Create `load_and_process()` method**

This method will:

1. Read the CSV file.
2. Check that required columns are present.
3. Create a new column `combined_info`.
4. Save it to a new CSV file.

---

### ✅ **Requirement 3 — Read the CSV File**

Inside `load_and_process()`:

* Use **pandas** to read the CSV file with `encoding='utf-8'`.
* Use a `try...except` block to handle missing or empty files.
* If the file is missing, raise:

  ```python
  FileNotFoundError(f"The file {self.original_csv} was not found.")
  ```
* If the file is empty, raise:

  ```python
  ValueError(f"The file {self.original_csv} is empty.")
  ```

📘 *Goal:* Learn how to handle file errors safely.

---

### ✅ **Requirement 4 — Check for Required Columns**

* The CSV **must have** these columns:
  `"Name"`, `"Genre"`, and `"synopsis"`.
* If any of them are missing, raise an error like:

  ```
  CSV file is missing required column(s): synopsis
  ```

📘 *Goal:* Practice validating input data.

---

### ✅ **Requirement 5 — Create the Combined Column**

Once the file passes validation:

* Add a new column called `combined_info`.
* It should combine `Name`, `Genre`, and `synopsis` in this format:

  ```
  Title: <Name> Overview: <synopsis> Genres: <Genre>
  ```

Example:

| Name   | synopsis                               | Genre             | combined_info                                                                            |
| ------ | -------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------- |
| Naruto | A young ninja dreams to become Hokage. | Action, Adventure | Title: Naruto Overview: A young ninja dreams to become Hokage. Genres: Action, Adventure |

📘 *Goal:* Learn how to combine text columns into a new column.

---

### ✅ **Requirement 6 — Save the Processed File**

* Save only the `combined_info` column into the output CSV file.
* Use:

  ```python
  df[['combined_info']].to_csv(self.processed_csv, index=False, encoding='utf-8')
  ```
* Return the path of the processed CSV.

📘 *Goal:* Learn how to write processed data back to a file.

---

### ✅ **Requirement 7 — Test the Code**

In a Jupyter notebook or a separate test file (`test_data_loader.py`), write:

```python
from src.data_loader import AnimeDataLoader

loader = AnimeDataLoader("data/anime_raw.csv", "data/anime_processed.csv")
loader.load_and_process()
```

Check if:

* The new file is created.
* It has one column named `combined_info`.
* The content looks correct.

---

## 🌟 **Bonus Challenge (Optional for Advanced Students)**

* Print a message after successful processing.
* Count how many rows were processed.
* Display first 5 rows using `print(df.head())`.

---

## 🧾 **Learning Outcomes**

By completing this part:

* You will understand **modular programming** and **file handling**.
* You will know how to **validate input data** and **handle exceptions**.
* You will get familiar with **pandas** for basic data manipulation.


