"""
Module with custom block of filter widgets
"""
from abc import ABC, abstractmethod

import streamlit as st
import pandas as pd
import numpy as np

from typing import List, Union, Tuple, Any, Optional


class Filter(ABC):
    def __init__(self, column: str, label: Optional[str] = None) -> None:
        """     
        :param column: name of column to be filtered
        :param label: text in filter label before column name
        """
        self.column = column
        self._label = label
        self._values: Union[List[str], Tuple[int|float]]
        
    def reset(self):
        self._values = None

    @abstractmethod
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters DataFrame
        
        :param df: pandas DataFrame
        :return: Filtered pandas DataFrame
        """
        pass

    @abstractmethod
    def display(self, df: pd.DataFrame) -> None:
        """
        Display DataFrame on page
        
        :param df: pandas DataFrame
        """
        pass

    @abstractmethod
    def _get_range(self, df: pd.DataFrame) -> Any:
        """Get min/max values of values in column"""
        pass


class CategoricalFilter(Filter):
    """
    Multiselect of categorical data
    """
    def __init__(self, column: str, label: Optional[str] = None) -> None:
        super().__init__(column, label)
        if label is None:
            self._label = "Select categories from"
    
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._values:
            return df[df[self.column].isin(self._values)]
        return df
    
    def _get_range(self, df: pd.DataFrame):
        return df[self.column].unique().tolist()
    
    def display(self, df: pd.DataFrame) -> None:
        options = self._get_range(df)
        selected = st.multiselect(f"{self._label} '{self.column}'", options=options)
        self._values = selected


class RangeFilter(Filter):
    """
    Min/max slider value selector
    """
    def __init__(self, column: str, label: Optional[str] = None) -> None:
        super().__init__(column, label)
        if label is None:
            self._label = "Select range for"
    
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._values is not None:
            return df[(df[self.column] >= self._values[0]) & (df[self.column] <= self._values[1])]
        return df
    
    def _get_range(self, df: pd.DataFrame):
        min_value, max_value = df[self.column].min(), df[self.column].max()
        if isinstance(min_value, np.float32):
            min_value = float(min_value)
            max_value = float(max_value)
        return min_value, max_value
    
    def display(self, df: pd.DataFrame) -> None:
        min_value, max_value = self._get_range(df)
        selected = st.slider(
            f"{self._label} {self.column}",
            min_value, max_value, (min_value, max_value)
        )
        self._values = selected


class GreaterFilter(RangeFilter):
    """
    Filter data by low threshold 
    """
    def __init__(self, column: str, label: Optional[str] = None) -> None:
        super().__init__(column, label)
        if label is None:
            self._label = "Enter minimum value of"
        self._values: Union[int, float]
    
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._values is not None:
            return df[df[self.column] >= self._values]
        return df
    
    def display(self, df: pd.DataFrame) -> None:
        min_value, max_value = self._get_range(df)
        selected = st.number_input(
            f"{self._label} {self.column}",
            min_value, max_value, value=min_value
        )
        self._values = selected


class LessFilter(RangeFilter):
    """
    Filter data by high threshold 
    """
    def __init__(self, column: str, label: Optional[str] = None) -> None:
        super().__init__(column, label)
        if label is None:
            self._label = "Enter minimum value of"
        self._value: Union[int, float]
    
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._value is not None:
            return df[df[self.column] <= self._value]
        return df
    
    def display(self, df: pd.DataFrame) -> None:
        min_value, max_value = self._get_range(df)
        selected = st.number_input(
            f"{self._label} {self.column}",
            min_value, max_value, value=max_value
        )
        self._value = selected


class DataFrameFilter:
    """
    Component that sets up filters block and 
    displays DataFrame 
    """
    def __init__(
        self, df: pd.DataFrame,
        filters: List[Filter],
        columns: int = 2,
        gap: str = "medium",
    ) -> None:
        """
        :param filters: List of filters instances
        :param columns: amount of columns in block
        :param gap: distance between columns, can be
            `small`, `medium` or `large`
        """
        self._check_columns_consistency(df, filters)
        self.df = df
        self.filters = filters
        self.columns = columns
        self.gap = gap
        
    def filter_df(self) -> pd.DataFrame:
        """Apply all filters for DataFrame"""
        filtered_df = self.df.copy()
        for filter in self.filters:
            filtered_df = filter.filter(filtered_df)
        return filtered_df

    def display_filters(self) -> None:
        """Renders the block of filters"""     
        for position, filter in enumerate(self.filters):
            counter = position % self.columns
            
            if counter == 0:
                col_list = st.columns(self.columns, gap=self.gap)
            
            with col_list[counter]:
                filter.display(self.df)
    
    def display_df(self, *args, **kwargs) -> None:
        """Renders the filtered dataframe in the main area.
        Supports the same functionality as `st.dataframe`
        """
        st.dataframe(self.filter_df(), *args, **kwargs)
    
    def _check_columns_consistency(self, df: pd.DataFrame, filters: List[Filter]):
        for filter in filters:
            assert filter.column in df.columns, f"{filter.column} missing in DataFrame. Must be one of {df.columns}"