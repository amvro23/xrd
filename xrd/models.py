import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import ExponentialModel, GaussianModel, LorentzianModel, VoigtModel
from xrd.data import x as default_x, y as default_y

class Scherrer:
    def __init__(self, instrument_fwhm=0.0, shape_factor=0.9, wavelength_A=1.54178,
                 x_2theta_deg=None, intensity=None):
        """
        Scherrer analysis on an XRD peak.
        instrument_fwhm : instrumental FWHM (deg 2θ)
        shape_factor    : K (≈0.9)
        wavelength_A    : X-ray wavelength in Å (Cu Kα = 1.54178 Å)
        x_2theta_deg    : optional array-like (deg). If None, uses .data defaults
        intensity       : optional array-like (a.u.). If None, uses .data defaults
        """
        self.instrument_fwhm = float(instrument_fwhm)
        self.shape_factor = float(shape_factor)
        self.wavelength_A = float(wavelength_A)

        # Load defaults immediately (and allow overrides)
        if x_2theta_deg is None or intensity is None:
            self.set_input(default_x, default_y)
        else:
            self.set_input(x_2theta_deg, intensity)

        # Sensible initial zoom (centered around the max, ±1.25°)
        xpeak = self.x[np.argmax(self.y)]
        self.zoom_area(lower=max(self.x.min(), xpeak - 1.25),
                       upper=min(self.x.max(), xpeak + 1.25))

    def set_input(self, x_2theta_deg=default_x, intensity=default_y):
        """x_2theta_deg (deg), intensity (a.u.) — defaults from .data"""
        self.x = np.asarray(x_2theta_deg, float)
        self.y = np.asarray(intensity, float)

    def xrd_initial_plot(self):
        plt.plot(self.x, self.y, "k-", lw=1)
        plt.xlabel("2θ (deg)")
        plt.ylabel("Intensity (a.u.)")
        plt.title("Initial XRD plot")
        plt.show()

    def zoom_area(self, lower=43.0, upper=45.5):
        self.lower_lim, self.upper_lim = float(lower), float(upper)
        m = (self.x >= self.lower_lim) & (self.x <= self.upper_lim)
        self.xtest = self.x[m]
        yseg = self.y[m]
        # guard against flat or empty segments
        if self.xtest.size == 0:
            raise ValueError("zoom_area bounds exclude all data points.")
        rng = yseg.max() - yseg.min()
        self.ytest = (yseg - yseg.min()) / (rng if rng > 0 else 1.0)

    def _fit_peak(self, model_cls, prefix):
        x, y = self.xtest, self.ytest

        bkg = ExponentialModel(prefix='b_')
        peak = model_cls(prefix=f'{prefix}_')
        pars = bkg.guess(y, x=x)
        pars.update(peak.make_params())

        # moment-based seeds
        mean = np.sum(x*y) / np.sum(y)
        var = np.sum(y*(x-mean)**2) / np.sum(y)
        sigma = max(1e-4, float(np.sqrt(max(var, 0.0))))
        height = float(y.max())

        pars[f'{prefix}_center'].set(value=mean, min=self.lower_lim, max=self.upper_lim)

        if isinstance(peak, GaussianModel):
            pars[f'{prefix}_sigma'].set(value=sigma, min=1e-4)
            pars[f'{prefix}_amplitude'].set(value=height * sigma * np.sqrt(2*np.pi), min=0)
        elif isinstance(peak, LorentzianModel):
            # lmfit LorentzianModel also uses 'sigma' (HWHM)
            pars[f'{prefix}_sigma'].set(value=sigma, min=1e-4)
            pars[f'{prefix}_amplitude'].set(value=height * np.pi * sigma, min=0)
        else:  # Voigt
            pars[f'{prefix}_sigma'].set(value=sigma, min=1e-4)
            pars[f'{prefix}_gamma'].set(value=sigma, min=1e-4)
            pars[f'{prefix}_amplitude'].set(value=height * sigma * np.sqrt(2*np.pi), min=0)

        mod = peak + bkg
        out = mod.fit(y, pars, x=x)
        comps = out.eval_components(x=x)
        return out, comps

    @staticmethod
    def _deconvolve_fwhm(meas_fwhm, inst_fwhm, shape='gaussian'):
        """Return sample FWHM (deg) after instrument correction."""
        meas = max(1e-12, float(meas_fwhm))
        inst = max(0.0, float(inst_fwhm))
        if shape == 'gaussian':
            val2 = meas*meas - inst*inst
            return np.sqrt(val2) if val2 > 0 else meas
        elif shape == 'lorentzian':
            return max(1e-12, meas - inst)
        elif shape == 'voigt':
            # pragmatic: prefer gaussian-like subtraction; fallback to linear
            val2 = meas*meas - inst*inst
            return np.sqrt(val2) if val2 > 0 else max(1e-12, meas - inst)
        return meas

    def _scherrer_nm(self, fwhm_deg, center_deg, shape_hint='gaussian'):
        beta_deg = self._deconvolve_fwhm(fwhm_deg, self.instrument_fwhm, shape_hint)
        beta_rad = np.deg2rad(beta_deg)
        theta_rad = np.deg2rad(center_deg/2.0)
        D_nm = (self.shape_factor * self.wavelength_A) / (beta_rad * np.cos(theta_rad)) / 10.0
        return D_nm

    def fit_voigt(self):
        out, comps = self._fit_peak(VoigtModel, 'v')
        fwhm = out.params['v_fwhm'].value
        center = out.params['v_center'].value
        D = self._scherrer_nm(fwhm, center, 'voigt')
        self._plot_result(out, comps, 'v_', 'Voigt', D)
        return D, out

    def fit_gaussian(self):
        out, comps = self._fit_peak(GaussianModel, 'g')
        fwhm = out.params['g_fwhm'].value
        center = out.params['g_center'].value
        D = self._scherrer_nm(fwhm, center, 'gaussian')
        self._plot_result(out, comps, 'g_', 'Gaussian', D)
        return D, out

    def fit_lorentzian(self):
        out, comps = self._fit_peak(LorentzianModel, 'l')
        fwhm = out.params['l_fwhm'].value
        center = out.params['l_center'].value
        D = self._scherrer_nm(fwhm, center, 'lorentzian')
        self._plot_result(out, comps, 'l_', 'Lorentzian', D)
        return D, out

    def _plot_result(self, out, comps, key, label, D_nm):
        x, y = self.xtest, self.ytest
        fitted = out.best_fit
        resid = y - fitted

        fig, axs = plt.subplots(nrows=2, dpi=100, figsize=(6,6))
        axs[0].plot(x, y, '-', label='data')
        axs[0].plot(x, comps[key], label=label)
        axs[0].plot(x, fitted, '--', label='total fit')
        axs[0].fill_between(x, 0, comps[key], alpha=0.3)
        axs[0].set_xlabel('2θ (deg)')
        axs[0].set_ylabel('Intensity (a.u.)')
        axs[0].legend(loc='best')
        r2 = getattr(out, "rsquared", np.nan)
        axs[0].text(x.mean(), y.max()*0.8, f'R² = {r2:.4f}\nD ≈ {D_nm:.0f} nm')

        axs[1].plot(x, resid, '.', label='residuals')
        axs[1].axhline(0, ls=':', c='k', alpha=0.6)
        axs[1].set_xlabel('2θ (deg)')
        axs[1].set_ylabel('Residuals')
        axs[1].legend(loc='best')
        fig.tight_layout()
        plt.show()


def _metrics(y, yhat, n_params):
    resid = y - yhat
    n = y.size
    sse = np.sum(resid**2)
    rmse = np.sqrt(sse / n)
    # R^2 vs mean of y
    r2 = 1.0 - sse / np.sum((y - y.mean())**2)
    # AIC/BIC for non-linear LS
    aic = n * np.log(sse / n) + 2 * n_params
    bic = n * np.log(sse / n) + np.log(n) * n_params
    return {"R2": r2, "RMSE": rmse, "AIC": aic, "BIC": bic}

def compare_models(s: Scherrer):
    results = []
    for name, fit_fn, shape in [
        ("Gaussian",   s.fit_gaussian,   "gaussian"),
        ("Lorentzian", s.fit_lorentzian, "lorentzian"),
        ("Voigt",      s.fit_voigt,      "voigt"),
    ]:
        D_nm, out = fit_fn()
        m = _metrics(s.ytest, out.best_fit, out.nvarys)
        m.update({"model": name, "D_nm": D_nm})
        results.append(m)
    # sort by BIC (or AIC)
    results.sort(key=lambda d: d["BIC"])
    return results
