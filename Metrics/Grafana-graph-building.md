# Graph building with Prometheus

## Query tab
* a basic `metric_name` is sufficient 
  * don't need to do `sum(metric_name[5m])` or `metric_name{label1="value",label2="value2"}`
### Wildcard by name
* `topk(10, {__name__=~".*name_to_search.*"})` 
  * searches using regex anything that matches `*name_to_search*`
  * Returns each of the lines as separate tables
  * this query only shows the top `10` lines

## Transform tab
* Say we want to group by (time, name, platform) - and we have 10 different prometheus labels
    * **Important Notes**:
        1. The order of transforms matter
            * Drag & drop to re-arrange
        2. Press the eye (hide/view) to see the effect
        3. Use the table view to check there's a Time columm & correct values

1. **Labels to Fields** - keep the `Value field name` __EMPTY__ - Important !!!!!
2. **Merge** - must go second
3. **Group by** - must go third
    * Select Time - Groupby
    * Select Name - Groupby
    * Select Platform - Groupby
    * Select Value - Total
    * Leave the others "Ignored" (check the table should only have 4 columns)
4. **Sort by** - must go fourth

# Dashboard Variables
* Get all values of tag by doing `label_values(algo)`
* Example Variable setting:
  * Name - `algo_name`  # usage `$algo_name` in graphs / text
  * Label - `Algo Name`
  * Description - `Some text`
  * Data Source - `Prometheus` or `database`
  * Refresh - `On dashboard Load`
  * Query - `label_values(algo)` or `SELECT algo FROM db.table`
  * Sort - `Alphabetical (case-insensitive)`

# Dashboard Styling
* Colour a table
 * Overrides 
   * Fields with matching regex `.*` (colour all cells) or `.*Failures.*` - to only colour those cells with Failures in it
   * Cell display Mode - `color background (solid)` 
   * Standard Options -> Color scheme -> Single Color -> Then pick the colour next to it
