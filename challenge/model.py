import pandas as pd
from typing import Tuple, Union, List
import numpy as np
from datetime import datetime


class DelayModel:

    def __init__(
        self
    ):
        self._model = None  # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        # Convert 'Fecha-I' and 'Fecha-O' to datetime
        data['Fecha-I'] = pd.to_datetime(data['Fecha-I'])
        data['Fecha-O'] = pd.to_datetime(data['Fecha-O'])

        # Create 'high_season' feature
        data['high_season'] = 0
        data.loc[(data['Fecha-I'].dt.month == 12) &
                 (data['Fecha-I'].dt.day >= 15), 'high_season'] = 1
        data.loc[(data['Fecha-I'].dt.month == 1) |
                 (data['Fecha-I'].dt.month == 2), 'high_season'] = 1
        data.loc[(data['Fecha-I'].dt.month == 3) &
                 (data['Fecha-I'].dt.day <= 3), 'high_season'] = 1
        data.loc[(data['Fecha-I'].dt.month == 7) & (data['Fecha-I'].dt.day >=
                                                    15) & (data['Fecha-I'].dt.day <= 31), 'high_season'] = 1
        data.loc[(data['Fecha-I'].dt.month == 9) & (data['Fecha-I'].dt.day >=
                                                    11) & (data['Fecha-I'].dt.day <= 30), 'high_season'] = 1

        # Create 'min_diff' feature
        data['min_diff'] = (data['Fecha-O'] - data['Fecha-I']
                            ).dt.total_seconds() / 60

        # Create 'period_day' feature
        data['period_day'] = 'noche'
        data.loc[(data['Fecha-I'].dt.hour >= 5) &
                 (data['Fecha-I'].dt.hour < 12), 'period_day'] = 'mañana'
        data.loc[(data['Fecha-I'].dt.hour >= 12) &
                 (data['Fecha-I'].dt.hour < 19), 'period_day'] = 'tarde'

        # Create 'delay' feature
        data['delay'] = 0
        data.loc[data['min_diff'] > 15, 'delay'] = 1

        # Drop columns that are no longer needed
        drop_cols = ['Vlo-I', 'Ori-I', 'Des-I', 'Emp-I',
                     'Vlo-O', 'Ori-O', 'Des-O', 'Emp-O',
                     'AÑO',  'SIGLAORI']
        data.drop(drop_cols, axis=1, inplace=True)

        # Convert categorical variables into dummy variables
        categorical_cols = ['TIPOVUELO', 'OPERA', 'period_day', 'MES']
        data = pd.get_dummies(data, columns=categorical_cols)

        if target_column:
            target = data[target_column]
            data.drop([target_column], axis=1, inplace=True)
            return data, target

        return data

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        return
