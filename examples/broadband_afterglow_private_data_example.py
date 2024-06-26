# What if your data is not public, or if you simulated it yourself.
# You can fit it with redback but now by loading the transient object yourself.
# This example also shows how to fit afterglow models to broadband data.
# In particular, the afterglow of GRB170817A, the GRB that accompanied the first binary neutron star merger

import redback
import pandas as pd

# load the data file
data = pd.read_csv('example_data/grb_afterglow.csv')
time_d = data['time'].values
flux_density = data['flux'].values
frequency = data['frequency'].values
flux_density_err = data['flux_err'].values

# we now load the afterglow transient object. We are using flux_density data here, so we need to use that data mode
data_mode = 'flux_density'

# set some other useful things as variables
name = '170817A'
redshift = 1e-2

afterglow = redback.transient.Afterglow(
    name=name, data_mode=data_mode, time=time_d,
    flux_density=flux_density, flux_density_err=flux_density_err, frequency=frequency)

# Now we have loaded the data up, we can plot it.
# We can pass keyword arguments here to not show, save the plot or change the aesthetics.
afterglow.plot_data()
afterglow.plot_multiband()

# now let's actually fit it with data. We will use all the data and a gaussiancore structured jet from afterglowpy.
# Note to make the example run quick, we will make some sampling sacrifices for speed and fix several parameters.

model = 'gaussiancore'

# use default priors and 'dynesty' sampler
sampler = 'dynesty'
priors = redback.priors.get_priors(model=model)

#fix the redshift
priors['redshift'] = redshift

# We are gonna fix some of the microphysical parameters for speed
priors['logn0'] = -2.6
priors['p'] = 2.16
priors['logepse'] = -1.25
priors['logepsb'] = -3.8
priors['ksin'] = 1.

model_kwargs = dict(frequency=frequency, output_format='flux_density')

# Fitting returns a afterglow result object, which can be used for plotting or doing further analysis.
result = redback.fit_model(transient=afterglow, model=model, sampler=sampler, model_kwargs=model_kwargs,
                           prior=priors, sample='rslice', nlive=500, resume=True)
# plot corner
result.plot_corner()

# plot multiband lightcurve.
# This will plot a panel for every unique frequency,
# along with the fitted lightcurve from a 100 random realisations randomly drawn from the prior.
# We can change other settings by passing in different keyword arguments here.
result.plot_multiband_lightcurve(random_models=100)
