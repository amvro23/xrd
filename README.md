# xrd
A python package for calculating XRD crystallite (grain) size

[Install](#Install) / [Usage](#Usage) / [Gauss](#Gauss) / [Voigt](#Voigt) / [Lorentzian](#Lorentzian) / [References](#References) / [Contact](#Contact)

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

Create an instance. Default optional values are instrument_defect = 0.0, shape_factor = 0.9, Cu_K_alpha = 1.54178.
```Python
xrd = Scherrer()
```

Set inlet values for adsorption isotherm equations. Default parameter x represents the [eV] and optional parameter y represents the [counts/s].
```Python
isotherm.set_inlet()
```

Adjust the values of x and y parameters according to your xrd results (The model carries default values).
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
# Gauss
Choose the desired equation in order to fit the data and obtain the XRD crystallite (grain) size. Note that a fit analysis report alongside a residual plot is also printed.
```Python
xrd.gauss()
```
![Figure_1](https://github.com/amvro23/xrd/assets/91277572/e763eec4-a01d-4ec0-89d2-10051e3714f8)

```
[[Model]]
    (Model(gaussian, prefix='g_') + Model(exponential, prefix='exp_'))
[[Fit Statistics]]
    # fitting method   = leastsq
    # function evals   = 1833
    # data points      = 192
    # variables        = 5
    chi-square         = 0.08854927
    reduced chi-square = 4.7353e-04
    Akaike info crit   = -1464.88477
    Bayesian info crit = -1448.59729
    R-squared          = 0.99430169
[[Variables]]
    exp_amplitude:  5.1616e-15 +/- 9.3517e-15 (181.18%) (init = 4.448869e-33)
    exp_decay:     -1.47171669 +/- 0.08725847 (5.93%) (init = -0.6143452)
    g_amplitude:    0.40679699 +/- 0.00335422 (0.82%) (init = 1)
    g_center:       44.6127722 +/- 0.00129809 (0.00%) (init = 44.61536)
    g_sigma:        0.18233135 +/- 0.00143627 (0.79%) (init = 0.3693009)
    g_fwhm:         0.42935752 +/- 0.00338216 (0.79%) == '2.3548200*g_sigma'
    g_height:       0.89007471 +/- 0.00561759 (0.63%) == '0.3989423*g_amplitude/max(1e-15, g_sigma)'
[[Correlations]] (unreported correlations are < 0.250)
    C(exp_amplitude, exp_decay)   = -0.9999
    C(g_amplitude, g_sigma)       = +0.6944
    C(exp_amplitude, g_amplitude) = -0.2829
    C(exp_decay, g_amplitude)     = +0.2731
Crystal size in nm with Gaussian fitting: 20
```

# Voigt
You can also draw fair comparisons regarding the best fit on occasion since R squared is also printed with the plot.
```Python
xrd.voigt()
```

![Figure_2](https://github.com/amvro23/xrd/assets/91277572/e89f9cd1-8084-4f15-9cee-b6a6ba7468f5)

```
[[Model]]
    (Model(voigt, prefix='v_') + Model(exponential, prefix='exp_'))
[[Fit Statistics]]
    # fitting method   = leastsq
    # function evals   = 1284
    # data points      = 192
    # variables        = 5
    chi-square         = 0.03201933
    reduced chi-square = 1.7123e-04
    Akaike info crit   = -1660.19086
    Bayesian info crit = -1643.90338
    R-squared          = 0.99793950
[[Variables]]
    exp_amplitude:  1.8677e-26 +/- 8.7869e-26 (470.47%) (init = 4.448869e-33)
    exp_decay:     -0.80057479 +/- 0.06648062 (8.30%) (init = -0.6143452)
    v_amplitude:    0.53691781 +/- 0.00377304 (0.70%) (init = 1)
    v_center:       44.6143955 +/- 7.6836e-04 (0.00%) (init = 44.61536)
    v_sigma:        0.11663920 +/- 7.4103e-04 (0.64%) (init = 0.3693009)
    v_gamma:        0.11663920 +/- 7.4103e-04 (0.64%) == 'v_sigma'
    v_fwhm:         0.42005165 +/- 0.00266867 (0.64%) == '1.0692*v_gamma+sqrt(0.8664*v_gamma**2+5.545083*v_sigma**2)'
    v_height:       0.96073817 +/- 0.00387211 (0.40%) == '(v_amplitude/(max(1e-15, v_sigma*sqrt(2*pi))))*wofz((1j*v_gamma)/(max(1e-15, v_sigma*sqrt(2)))).real'
[[Correlations]] (unreported correlations are < 0.250)
    C(exp_amplitude, exp_decay)   = -1.0000
    C(v_amplitude, v_sigma)       = +0.8232
    C(exp_amplitude, v_amplitude) = -0.7420
    C(exp_decay, v_amplitude)     = +0.7388
    C(exp_amplitude, v_sigma)     = -0.5494
    C(exp_decay, v_sigma)         = +0.5465
Crystal size in nm with Voigt fitting: 20
```

# Lorentzian
```Python
xrd.lorentzian()
```
![Figure_3](https://github.com/amvro23/xrd/assets/91277572/7796a6a7-466d-4990-aff9-0a7df84831f8)

```
[[Model]]
    (Model(lorentzian, prefix='l_') + Model(exponential, prefix='exp_'))
[[Fit Statistics]]
    # fitting method   = leastsq
    # function evals   = 5965
    # data points      = 192
    # variables        = 5
    chi-square         = 0.08446267
    reduced chi-square = 4.5167e-04
    Akaike info crit   = -1473.95666
    Bayesian info crit = -1457.66918
    R-squared          = 0.99456467
[[Variables]]
    exp_amplitude:  1.4532e-84 +/- 7.2746e-83 (5005.89%) (init = 4.448869e-33)
    exp_decay:     -0.23895951 +/- 0.06247247 (26.14%) (init = -0.6143452)
    l_amplitude:    0.63690019 +/- 0.00522466 (0.82%) (init = 1)
    l_center:       44.6176801 +/- 0.00126901 (0.00%) (init = 44.61536)
    l_sigma:        0.19730233 +/- 0.00197555 (1.00%) (init = 0.3693009)
    l_fwhm:         0.39460467 +/- 0.00395110 (1.00%) == '2.0000000*l_sigma'
    l_height:       1.02751767 +/- 0.00622355 (0.61%) == '0.3183099*l_amplitude/max(1e-15, l_sigma)'
[[Correlations]] (unreported correlations are < 0.250)
    C(exp_amplitude, exp_decay)   = -1.0000
    C(l_amplitude, l_sigma)       = +0.7966
    C(exp_amplitude, l_amplitude) = -0.6326
    C(exp_decay, l_amplitude)     = +0.6321
    C(exp_amplitude, l_sigma)     = -0.4571
    C(exp_decay, l_sigma)         = +0.4566
    C(exp_amplitude, l_center)    = -0.3446
    C(exp_decay, l_center)        = +0.3443
Crystal size in nm with Lorentzian fitting: 22
```

# References

[Varun Jain, Mark C. Biesinger, Matthew R. Linford (2018). The Gaussian-Lorentzian Sum, Product, and Convolution (Voigt) functions in the context of peak fitting X-ray photoelectron spectroscopy (XPS) narrow scans. Applied Surface Science, Volume 447, 31 July 2018, Pages 548-553](https://doi.org/10.1016/j.apsusc.2018.03.190)

# Contact
amvro23@gmail.com
