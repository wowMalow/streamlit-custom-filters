# streamlit-custom-filters
Streamlit tools for interactive dataframes filtering

Also demo for publishing and deploy docs via github workflow

Example of usage:

```python
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
```
