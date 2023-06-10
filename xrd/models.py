import numpy as np
import matplotlib.pyplot as plt
from xrd.data import x,y
from lmfit.models import ExponentialModel, GaussianModel, LorentzianModel, VoigtModel


class Scherrer(object):

     def __init__(self, instrument_defect = 0.0, shape_factor = 0.9, Cu_K_alpha = 1.54178):
        """Class for evaluating crystallite size using Scherrer equation.
        Parameters
        ----------
        instrument_defect  : float or integer, optional
             instrument_defect, by default 0.0
        shape_factor       : float, optional
             shape_factor, by default 0.9
        Cu_K_alpha         : float, optional
             wavelength (Cu_K_alpha), by default 1.54178
        """           
        self.instrument_defect = instrument_defect
        self.shape_factor = shape_factor
        self.Cu_K_alpha = Cu_K_alpha

     def set_input(self, x=x, y=y):
        """Set input parameters for Scherrer equation.
        Parameters
        ----------
        x  : 1d array of floats, optional
             eV of XRD diffractions
        y  : 1d array of floats, optional
             counts/s of XRD diffractions
        """             
        self.x = x
        self.y = y

     def xrd_initial_plot(self):
        """Plot initial XRD plot"""
        plt.plot(self.x, self.y, "k-", lw = 1)
        plt.xlabel("eV")
        plt.ylabel("counts/s")
        plt.title("Initial XRD plot")
        plt.show()

     def zoom_area(self, lower_lim = 43.0, upper_lim = 45.5):
        """Set input parameters to define the peak you want to test.
        Parameters
        ----------
        lower_lim  : float or integer, optional
        upper_lim  : float or integer, optional
        """          
        self.lower_lim = lower_lim
        self.upper_lim = upper_lim
        func = np.vectorize(lambda x: x>self.lower_lim and x<self.upper_lim)
        self.y1 = self.y[func(self.x)]
        self.xtest = self.x[func(self.x)]
        self.ytest = (self.y1-min(self.y1))/(max(self.y1)-min(self.y1))

     def xrd_zoom_area_plot(self):
        """Plot initial XRD plot"""
        plt.plot(self.xtest, self.ytest, "k-", lw = 1)
        plt.xlabel("2θ")
        plt.ylabel("Intensity m.u.")
        plt.title("XRD plot")
        plt.show()     

     def voigt(self):
        x = self.xtest
        y = self.ytest 
        exp_mod = ExponentialModel(prefix = 'exp_')
        pars = exp_mod.guess(y, x = x)
        voigt = VoigtModel(prefix = 'v_')
        pars.update(voigt.make_params())
        mean = sum(x * y) / sum(y)
        sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))
        pars['v_center'].set(value = mean, min = self.lower_lim, max = self.upper_lim)
        pars['v_sigma'].set(value = sigma)
        pars['v_amplitude'].set(value = max(y))
        mod = voigt + exp_mod
        init = mod.eval(pars, x = x)
        out = mod.fit(y, pars, x = x)
        comps = out.eval_components(x = x)
        residual_Voigt = y - comps['v_']
        print(out.fit_report(min_correl = 0.25))

        # Scherrer equation
        corr_fwhm = out.params['v_fwhm'] - self.instrument_defect
        angle_rad_2θ = x[comps['v_'].argmax()]
        angle_rad_θ = angle_rad_2θ/2
        corr_fwhm_rad = np.pi*corr_fwhm/180
        angle_rad_θ_rad = np.pi*angle_rad_θ/180
        cryst_size_A = self.Cu_K_alpha*self.shape_factor/corr_fwhm_rad/np.cos(angle_rad_θ_rad)
        cryst_size_nm = round(cryst_size_A/10, 0)
        print("Crystal size in nm with Voigt fitting: {:.0f}".format(cryst_size_nm))

        # plot the Voigt graph with the residuals
        fig, axs = plt.subplots(nrows = 2, dpi = 100)
        axs[0].plot(x, y, 'k-', label = 'data')
        axs[0].plot(x, comps['v_'], color = 'g', label = 'Voigt')
        axs[0].fill_between(x, comps['v_'].min(), comps['v_'], facecolor = 'g', alpha=0.5)
        axs[0].text(x.mean(), y[-1], "$R^2$ = {:.4f}".format(out.rsquared))
        axs[0].legend()
        axs[0].set_ylabel('Intensity a.u.')
        axs[0].set_xlabel('2θ')
        axs[1].plot(comps['v_'], residual_Voigt, ".", color = 'g', mfc = 'none', label = 'residuals') 
        axs[1].legend()
        axs[1].set_xticks([])
        axs[1].set_ylabel('residuals')
        axs[1].set_xlabel('fitted')
        axs[1].axhline(y=0.00, color = 'k', linestyle = ':', alpha = 0.5)
        fig.tight_layout()
        plt.show()

     def gauss(self):
        x = self.xtest
        y = self.ytest 
        exp_mod = ExponentialModel(prefix = 'exp_')
        pars = exp_mod.guess(y, x = x)
        gauss = GaussianModel(prefix = 'g_')
        pars.update(gauss.make_params())
        mean = sum(x * y) / sum(y)
        sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))
        # where max is the value of the peak
        pars['g_center'].set(value = mean, min = self.lower_lim, max = self.upper_lim)
        pars['g_sigma'].set(value = sigma)
        pars['g_amplitude'].set(value = max(y))
        mod = gauss + exp_mod
        init = mod.eval(pars, x = x)
        out = mod.fit(y, pars, x = x)
        comps = out.eval_components(x = x)
        residual_Gauss = y - comps['g_']
        print(out.fit_report(min_correl = 0.25))

        # Scherrer equation   
        corr_fwhm = out.params['g_fwhm'] - self.instrument_defect
        angle_rad_2θ = x[comps['g_'].argmax()]
        angle_rad_θ = angle_rad_2θ/2
        corr_fwhm_rad = np.pi*corr_fwhm/180
        angle_rad_θ_rad = np.pi*angle_rad_θ/180
        cryst_size_A = self.Cu_K_alpha*self.shape_factor/corr_fwhm_rad/np.cos(angle_rad_θ_rad)
        cryst_size_nm = round(cryst_size_A/10, 0)
        print("Crystal size in nm with Gaussian fitting: {:.0f}".format(cryst_size_nm))

        # plot the Gauss graph with the residuals
        fig, axs = plt.subplots(nrows = 2, dpi = 100)
        axs[0].plot(x, y, 'k-', label = 'data')
        axs[0].plot(x, comps['g_'], color = 'y', label = 'Gauss')
        axs[0].fill_between(x, comps['g_'].min(), comps['g_'], facecolor = 'y', alpha=0.5)
        axs[0].text(x.mean(), y[-1], "$R^2$ = {:.4f}".format(out.rsquared))
        axs[0].legend()
        axs[0].set_ylabel('Intensity a.u.')
        axs[0].set_xlabel('2θ')
        axs[1].plot(comps['g_'], residual_Gauss, '.', color = 'y', mfc = 'none', label = 'residuals')
        axs[1].legend()
        axs[1].set_xticks([])
        axs[1].axhline(y=0.00, color = 'y', linestyle = ':', alpha = 0.5)
        axs[1].set_ylabel('residuals')
        axs[1].set_xlabel('fitted')
        fig.tight_layout()
        plt.show()

     def lorentzian(self):
        x = self.xtest
        y = self.ytest 
        exp_mod = ExponentialModel(prefix = 'exp_')
        pars = exp_mod.guess(y, x = x)
        lorentzian = LorentzianModel(prefix = 'l_')
        pars.update(lorentzian.make_params())
        mean = sum(x * y) / sum(y)
        sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))
        pars['l_center'].set(value = mean, min = self.lower_lim, max = self.upper_lim)
        pars['l_sigma'].set(value = sigma)
        pars['l_amplitude'].set(value = max(y))
        mod = lorentzian + exp_mod
        init = mod.eval(pars, x = x)
        out = mod.fit(y, pars, x = x)
        comps = out.eval_components(x = x)
        residual_Lorentzian = y - comps['l_']
        print(out.fit_report(min_correl = 0.25))

        # Scherrer equation
        corr_fwhm = out.params['l_fwhm'] - self.instrument_defect
        angle_rad_2θ = x[comps['l_'].argmax()]
        angle_rad_θ = angle_rad_2θ/2
        corr_fwhm_rad = np.pi*corr_fwhm/180
        angle_rad_θ_rad = np.pi*angle_rad_θ/180
        cryst_size_A = self.Cu_K_alpha*self.shape_factor/corr_fwhm_rad/np.cos(angle_rad_θ_rad)
        cryst_size_nm = round(cryst_size_A/10, 0)
        print("Crystal size in nm with Lorentzian fitting: {:.0f}".format(cryst_size_nm))

        # plot the Lorentzian graph with the residuals
        fig, axs = plt.subplots(nrows = 2, dpi = 100)
        axs[0].plot(x, y, 'k-', label = 'data')
        axs[0].plot(x, comps['l_'], color = 'm', label = 'Lorentzian')
        axs[0].fill_between(x, comps['l_'].min(), comps['l_'], facecolor = 'm', alpha=0.5)
        axs[0].text(x.mean(), y[-1], "$R^2$ = {:.4f}".format(out.rsquared))
        axs[0].legend()
        axs[0].set_ylabel('Intensity a.u.')
        axs[0].set_xlabel('2θ')
        axs[1].plot(comps['l_'], residual_Lorentzian, '.', color = 'm', mfc = 'none', label = 'residuals')
        axs[1].legend()
        axs[1].set_xticks([])
        axs[1].axhline(y=0.00, color = 'k', linestyle = ':', alpha = 0.5)
        axs[1].set_ylabel('residuals')
        axs[1].set_xlabel('fitted')
        fig.tight_layout()
        plt.show()