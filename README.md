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

Provide your own data
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

Fit Result
Model: (Model(gaussian, prefix='g_') + Model(exponential, prefix='b_'))

Fit Statistics
fitting method	leastsq
# function evals	1816
# data points	192
# variables	5
chi-square	0.08854927
reduced chi-square	4.7353e-04
Akaike info crit.	-1464.88477
Bayesian info crit.	-1448.59729
R-squared	0.99430169
Parameters
name	value	standard error	relative error	initial value	min	max	vary	expression
b_amplitude	5.1617e-15	9.3508e-15	(181.16%)	4.448869288486065e-33	-inf	inf	True	
b_decay	-1.47171725	0.08725824	(5.93%)	-0.6143451556512216	-inf	inf	True	
g_amplitude	0.40679699	0.00335422	(0.82%)	0.9256999870107145	0.00000000	inf	True	
g_center	44.6127722	0.00129809	(0.00%)	44.61536254241184	43.0000000	45.5000000	True	
g_sigma	0.18233135	0.00143627	(0.79%)	0.3693008637856311	1.0000e-04	inf	True	
g_fwhm	0.42935752	0.00338216	(0.79%)	0.8696370600596799	-inf	inf	False	2.3548200*g_sigma
g_height	0.89007470	0.00561758	(0.63%)	1.000000049126323	-inf	inf	False	0.3989423*g_amplitude/max(1e-15, g_sigma)
Correlations (unreported values are < 0.100)
Parameter1	Parameter 2	Correlation
b_amplitude	b_decay	-0.9999
g_amplitude	g_sigma	+0.6944
b_amplitude	g_amplitude	-0.2829
b_decay	g_amplitude	+0.2731
b_decay	g_center	-0.1926
b_amplitude	g_center	+0.1908
b_amplitude	g_sigma	-0.1646
b_decay	g_sigma	+0.1576
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


# References

[Varun Jain, Mark C. Biesinger, Matthew R. Linford (2018). The Gaussian-Lorentzian Sum, Product, and Convolution (Voigt) functions in the context of peak fitting X-ray photoelectron spectroscopy (XPS) narrow scans. Applied Surface Science, Volume 447, 31 July 2018, Pages 548-553](https://doi.org/10.1016/j.apsusc.2018.03.190)

# Contact
amvro23@gmail.com
