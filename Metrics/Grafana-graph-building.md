# Graph building with Prometheus

## Query tab
* a basic `metric_name` is sufficient 
  * don't need to do `sum(metric_name[5m])` or `metric_name{label1="value",label2="value2"}`

## Transform tab
* Say we want to group by (time, name, platform) - and we have 10 different prometheus labels
    * **Important Notes**:
        1. The order of transforms matter
            * Drag & drop to re-arrange
        2. Press the eye (hide/view) to see the effect
        3. Use the table view to check there's a Time columm & correct values

1. **Labels to Fields** - keep the "Value field name" __EMPTY__
2. **Merge** - must go second
3. **Group by** - must go third
    * Select Time - Groupby
    * Select Name - Groupby
    * Select Platform - Groupby
    * Select Value - Total
    * Leave the others "Ignored" (check the table should only have 4 columns)
4. **Sort by** - must go fourth
