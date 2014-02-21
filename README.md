# Testing out APIs

# 1.
```python
  import pandas as pd
  df = pd.util.testing.makeDataFrame()
  with dplyr(df) as res:
      group_by(A, B)
      summarize(total=sum(C))
      arrange(desc(D))

  # manager.operations => [group_by(A,B), summarize(total=sum(C)), arrange(desc(D))]
```
