# xrd
A python package for calculating XRD crystallite (grain) size

[Install](#Install) / [Usage](#Usage) /  [XRD](#XRD) / [References](#References) / [Contact](#Contact)

# Install
First, make sure you have a Python 3 environment installed.
To install from github:
```Python
pip install -e git+https://github.com/amvro23/xrd/#egg=xrd
```
Note: It might be useful to write "git+https://github.com/amvro23/xrd/#egg=xrd" if installing directly from a Python interpreter as # can be interpreted as a comment.

```Python
from xrd.models import Scherrer
```

Create an instance. Default optional values are instrument_defect = 0.0, shape_factor = 0.9, Cu_K_alpha = 1.54178.
```Python
xrd = Scherrer()
```

Set inlet values for adsorption isotherm equations. Default parameter x represents the [eV] and optional parameter y represents the [counts/s].
```Python
isotherm.set_inlet()
```

Adjust the values of x and y parameters according to your xrd results (The model carried default values).
```Python
path = "xrd.txt"
df = pd.read_csv(path, delimiter = '\t')
x = np.array(df['eV'])
y = np.array(df['counts/s'])
```

Select the desired peak (e.g., 2θ = 43 to 2θ = 45.5)
```Python
xrd.zoom_area(43, 45.5)
```

Choose the desired equation in order to fit the data. Note that a fit analysis report alongside a residual plot is also printed.
```Python
xrd.gauss()
```
![Figure_1](https://github.com/amvro23/xrd/assets/91277572/e763eec4-a01d-4ec0-89d2-10051e3714f8)

You can also draw fair comparison regarding the best fit on occasion since R squared is also printed with the plot
```Python
xrd.voigt()
```
![Figure_2](https://github.com/amvro23/xrd/assets/91277572/e89f9cd1-8084-4f15-9cee-b6a6ba7468f5)
