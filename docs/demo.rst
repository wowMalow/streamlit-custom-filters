Filters
==================================

.. automodule:: filters

Example of usage:

.. code:: python

   dataframe_filters = DataFrameFilter(
      df=sales_df,
      filters=[
         RangeFilter('source_count'),
         GreaterFilter('sales'),
         GreaterFilter('demand_ratio'),
         LessFilter('available_ratio'),
         CategoricalFilter('trend_category'),
      ],
      columns=3,
      gap="small",
   )

   dataframe_filters.display_filters()
   dataframe_filters.display_df(hide_index=True)


DataFrameFilter
```````````````````

.. autoclass:: DataFrameFilter
   :members: __init__, filter_df, display_filters, display_df



CategoricalFilter
```````````````````
.. autoclass:: CategoricalFilter
   :special-members: __init__
   :members: 



RangeFilter
```````````````````
.. autoclass:: RangeFilter
   :special-members: __init__
   :members: 



GreaterFilter
```````````````````
.. autoclass:: GreaterFilter
   :special-members: __init__
   :members: 



LessFilter
```````````````````
.. autoclass:: LessFilter
   :special-members: __init__
   :members: 