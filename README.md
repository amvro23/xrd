# xrd
A python package for calculating XRD crystallite (grain) size

[Install](#Install) / [Usage](#Usage) / [Quick_Start](#Quick_Start) / [fit_gaussian](#fit_gaussian) / [References](#References) / [Contact](#Contact)

# Install
First, make sure you have a Python 3 environment installed.
To install from github:
```Python
pip install -e git+https://github.com/amvro23/xrd/#egg=xrd
```
Note: It might be useful to write "git+https://github.com/amvro23/xrd/#egg=xrd" if installing directly from a Python interpreter as # can be interpreted as a comment.

# Usage
```Python
from xrd.models import Scherrer
```

# Quick_Start
By default, the class loads x, y from xrd.data and auto-zooms around the strongest peak:
Set inlet XRD values. Default parameter x represents the [eV] and optional parameter y represents the [counts/s].

```Python
xrd = Scherrer()           # uses default x,y from .data
xrd.xrd_initial_plot()     # optional: see the full scan
xrd.zoom_area(43.0, 45.5)  # choose a peak window in 2θ (deg)
D_nm, out = xrd.fit_gaussian()
```

<img width="580" height="453" alt="image" src="https://github.com/user-attachments/assets/8af9fc08-9f82-4857-8def-8d1044e319a2" />
<img width="590" height="590" alt="image" src="https://github.com/user-attachments/assets/640f1f92-24f2-49a9-8a0e-db6a5a93a953" />

Provide your own data in numpy arrays form
Your x must be 2θ (degrees) and y is intensity (a.u.):
```Python
your_x = x
your_y = y
xrd = Scherrer(x_2theta_deg=your_x, intensity=your_y)  # or xrd.set_input(x, y)
xrd.zoom_area(43.0, 45.5)
D_nm, out = xrd.fit_lorentzian()
```

Parameters
```Python
Scherrer(
    instrument_fwhm=0.0,   # instrumental FWHM in deg (2θ)
    shape_factor=0.9,      # K in Scherrer equation (≈0.9)
    wavelength_A=1.54178,  # λ in Å (Cu Kα)
    x_2theta_deg=None,     # optional x (2θ in deg); defaults to .data.x
    intensity=None         # optional y (a.u.); defaults to .data.y
)
```

Selecting a peak
```Python
xrd.zoom_area(lower=43.0, upper=45.5)
```

# fit_gaussian

Fit a Gaussian peak + background and compute D:

```Python
D_nm, out = xrd.fit_gaussian()

print(f"Crystallite size D = {D_nm:.2f} nm")

out
Crystallite size D = 20.01 nm
```

Compare models
```Python
s = Scherrer()
s.zoom_area(43.0, 45.5)
summary = compare_models(s)
for r in summary:
    print(f"{r['model']:10s}  R2={r['R2']:.4f}  RMSE={r['RMSE']:.4f}  "
          f"AIC={r['AIC']:.1f}  BIC={r['BIC']:.1f}  D≈{r['D_nm']:.1f} nm")
```
<img width="590" height="590" alt="image" src="https://github.com/user-attachments/assets/6003276f-e50a-4af0-b9dc-242c406566e2" />
<img width="590" height="590" alt="image" src="https://github.com/user-attachments/assets/41a75f94-8d6d-4855-a0e8-3ce353d39649" />
<img width="598" height="590" alt="image" src="https://github.com/user-attachments/assets/6a24d348-5b0d-4588-bd83-d617c8fc6482" />

<pre> ``` out Lorentzian R²=0.9946 RMSE=0.0210 AIC=-1474.0 BIC=-1457.7 D≈21.8 nm Gaussian R²=0.9943 RMSE=0.0215 AIC=-1464.9 BIC=-1448.6 D≈20.0 nm Voigt R²=0.9143 RMSE=0.0833 AIC=-944.4 BIC=-928.1 D≈11.6 nm ``` </pre>


# References

[Varun Jain, Mark C. Biesinger, Matthew R. Linford (2018). The Gaussian-Lorentzian Sum, Product, and Convolution (Voigt) functions in the context of peak fitting X-ray photoelectron spectroscopy (XPS) narrow scans. Applied Surface Science, Volume 447, 31 July 2018, Pages 548-553](https://doi.org/10.1016/j.apsusc.2018.03.190)

# Contact
amvro23@gmail.com
