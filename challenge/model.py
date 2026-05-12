import pandas as pd
from typing import Tuple, Union, List
import numpy as np
from challenge.utils import (is_high_season, get_period_day, get_min_diff , top_10_features)
import xgboost as xgb
from sklearn.model_selection import train_test_split

class DelayModel:

    def __init__(self):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame] :
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
        data = data.copy(Deep=True)
        
        if 'Fecha-I' in data.columns and 'Fecha-O' in data.columns:
            data['high_season'] = data.apply(lambda x: is_high_season(x['Fecha-I']), axis=1)
            data['period_day'] = data.apply(lambda x: get_period_day(x['Fecha-I']), axis=1)
            data['min_diff'] = data.apply(lambda x: get_min_diff(x), axis=1)
            data['delay'] = np.where(data['min_diff'] > 15, 1, 0)
    
        # One-hot encode
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)
    
        # Rellenar features faltantes con 0
        for col in top_10_features:
            if col not in features.columns:
                features[col] = 0
                
        # Seleccionar top 10 features
        features = features[top_10_features]
    
        if target_column:
            target = data[[target_column]]
            return features, target
    
        return features
        


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
        # Se usan los mismos parámetros que se usaron para entrenar el modelo en el notebook de exploración
        x_train, _, y_train, _ = train_test_split(
            features, 
            target, 
            test_size=0.33, 
            random_state=42
        )

        n_y0 = len(y_train[y_train.iloc[:, 0] == 0])
        n_y1 = len(y_train[y_train.iloc[:, 0] == 1])
        scale = n_y0 / n_y1

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale)
        self._model.fit(x_train, y_train.iloc[:, 0])


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
        if self._model is None:
            raise ValueError("Modelo no entrenado. Por favor, llama a fit() antes de predict().")
        
        return self._model.predict(features).tolist()