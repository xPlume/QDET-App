import pandas as pd
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
import os
import random

from tabulate import tabulate

from text2props.model import Text2PropsModel
from text2props.modules.estimators_from_text import (
    FeatureEngAndRegressionPipeline,
    FeatureEngAndRegressionEstimatorFromText,
)
from text2props.modules.feature_engineering import FeatureEngineeringModule
from text2props.modules.feature_engineering.components import LinguisticFeaturesComponent, ReadabilityFeaturesComponent
from text2props.modules.latent_traits_calibration import KnownParametersCalibrator
from text2props.modules.regression import RegressionModule
from text2props.modules.regression.components import SklearnRegressionComponent
from text2props.constants import DATA_PATH, WRONGNESS, QUESTION_DF_COLS, Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS


def data_preparation():
    # This is a custom method built to provide the data in the format expected by the models defined in text2props.

    raw_df = pd.read_csv(os.path.join(DATA_PATH, 'reading_comprehension_questions.csv'))
    print(f"[INFO] Length of the original dataset: {len(raw_df)}")

    # This is a dictionary that contains the "true" latent traits for the questions.
    wrongness_dictionary = {
        WRONGNESS: {
            q_id: 1-facility
            for q_id, facility in raw_df[['q_id', 'question_facility']].values
        }
    }
    print(f"[INFO] Number of questions in the wrongness dictionary: {len(wrongness_dictionary[WRONGNESS])}")

    def prepare_questions_df(input_df: pd.DataFrame):
        """ This is a method that maps from the format of the raw_df to the format needed by the library. """
        output_df = pd.DataFrame(columns=QUESTION_DF_COLS)
        # Unique ID of the question
        output_df[Q_ID] = input_df['q_id']
        # The full text needed as input is text of the reading passage + text of the question
        output_df[Q_TEXT] = input_df.apply(lambda r: f"Context:\n{r['text']}\n\nQuestion:\n{r['question']}", axis=1)
        # The texts of the correct answer options(s), as a list of str
        output_df[CORRECT_TEXTS] = input_df.apply(
            lambda r: [ [r['option_0'], r['option_1'], r['option_2'], r['option_3']][r['correct_answer']] ],
            axis=1
        )
        # The texts of the wrong answer option(s), as a list of str
        output_df[WRONG_TEXTS] = input_df.apply(
            lambda r: [
                x for idx, x in enumerate([r['option_0'], r['option_1'], r['option_2'], r['option_3']])
                if idx != r['correct_answer']
            ],
            axis=1
        )
        return output_df

    # Train/test split
    list_context_ids = list(raw_df['context_id'].unique())
    random.shuffle(list_context_ids)
    n_train_context_ids = int(len(list_context_ids) * 0.8)
    print(f"[INFO] Number training contexts: {n_train_context_ids}")
    train_df = raw_df[raw_df['context_id'].isin(list_context_ids[:n_train_context_ids])]
    print(f"[INFO] Length (n questions) of train_df: {len(train_df)}")
    test_df = raw_df[raw_df['context_id'].isin(list_context_ids[n_train_context_ids:])]
    print(f"[INFO] Length (n questions) of test_df: {len(test_df)}")

    # Convert DFs to the right format
    train_df = prepare_questions_df(train_df)
    print(f"[INFO] Length (n questions) of  (after conversion to text2props format): {len(train_df)}")
    test_df = prepare_questions_df(test_df)
    print(f"[INFO] Length (n questions) of test_df (after conversion to text2props format): {len(test_df)}")

    return wrongness_dictionary, train_df, test_df


if __name__ == '__main__':
	
	# Prepare data. This is custom for the given .csv()
	known_latent_traits, df_train, df_test = data_preparation()
	
	print("")
	print("")
	print("")
	print("")
	print("WRONGNESS_DICTIONARY")
	print(known_latent_traits)
	print("")
	print("")
	print("")
	
	# 1. Don't truncate column width (allows full text to show)
	pd.set_option('display.max_colwidth', None)

	# 2. Show all columns (don't use '...' in the middle of columns)
	pd.set_option('display.max_columns', None)
	
	# 3. Show all rows (don't use '...' in the middle of the dataset)
	pd.set_option('display.max_rows', None)
	
	# 4. Don't wrap the table to the next line (prevents breaking the table)
	pd.set_option('display.expand_frame_repr', False)
	
	print("--- TRAIN_DF CONTENT ---")
	print(df_train)
	#print(tabulate(df_train, headers='keys', tablefmt='grid'))
	
	print("")
	print("")
	print("")
	
	print("\n--- TEST_DF CONTENT ---")
	print(df_test)
	#print(tabulate(df_test, headers='keys', tablefmt='grid'))
	
# --- --- COLUMN REQUIREMENTS and DATA FORMAT --- ---

# --- For the known_latent_traits dictionary ---
# It is a nested dictionary. First key is the name of the latent trait (one of WRONGNESS, DIFFICULTY, DISCRIMINATION)
# The values are dictionaries (the keys are the question IDs, the values the latent traits).
# Note: wrongness = 1 - facility

# --- for df_train and df_test ---
# These are the dataframes which contain the text of the questions and the value of the latent trait.
# Needs colums QUESTION_DF_COLS = [Q_ID, Q_TEXT, CORRECT_TEXTS, WRONG_TEXTS] (from text2props.constants)

# --- For df_gte ---
# This is the dataset that contains the responses of individual students to the questions (not needed here).
# Needs columns ANSWERS_DF_COLS (from text2props.constants)

