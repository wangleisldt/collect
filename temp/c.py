import pandas as pd
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
print('System: {}'.format(sys.version))
for module in [pd, matplotlib,np]:
    print('Module {:10s} - version {}'.format(module.__name__, module.__version__))
df = pd.DataFrame({"Fecha inicio": ['2016-01-31', '2016-01-31', '2016-01-31', '2016-01-31', '2016-12-31', '2016-12-31',
                                    '2016-12-31', '2016-12-31', ],
                  "Delito": ["ABANDONO DE PERSONA","ABORTO","ABUSO DE AUTORIDAD","ABUSO DE CONFIANZA","VIOLACION",
                             "VIOLACION EQUIPARADA","VIOLACION TUMULTUARIA","VIOLENCIA FAMILIAR", ],
                  "No delitos": [19, 8, 112, 241, 40, 4, 1, 1397, ]
                   })
print(df)
df['date2'] = pd.to_datetime(df['Fecha inicio'], infer_datetime_format=True)
df['YearMonth'] = df['date2'].map(lambda x: '{}-{}'.format(x.year, x.month))
print('1---')
print(df)
print('2---')
print(df.groupby(['YearMonth', 'Delito'])['No delitos'].sum())
print('3---')
# pb 1
print(df.groupby(['YearMonth', 'Delito'])['No delitos'].sum().reset_index())

# pb 2
print('4---')
df = df.groupby(['YearMonth', 'Delito'])['No delitos'].sum()
print(df)

print('5---')
df = df.groupby('YearMonth').nlargest(3).reset_index(level=0,drop=True).reset_index()
print(df)

print('6--- Plotting df')
sns.barplot(data=df, x='YearMonth', y='No delitos', hue='Delito')

plt.show()