import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scienceplots
plt.style.use(['science', 'nature'])
df = pd.read_csv('outputs/ambient_all.csv', parse_dates=['datetime'])

fig, axs = plt.subplots(2,1, sharex=True, figsize = (12,6), dpi = 170)
fig.subplots_adjust(hspace=0)
axs[0].plot(df.datetime, df.pressure, label = 'Presión [mbar]')
axs[1].plot(df.datetime, df.temperature, label = 'Temperatura [°C]')
axs[0].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axs[0].xaxis.set_major_locator(mdates.HourLocator(byhour=12))
axs[0].grid(axis = 'x', which = 'minor')
axs[1].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axs[1].xaxis.set_major_locator(mdates.HourLocator(byhour=12))
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
axs[1].grid(axis = 'x', which = 'minor')
axs[0].grid(axis = 'y')
axs[1].grid(axis = 'y')
axs[0].set_ylabel('Presión [mbar]', fontsize = 14)
axs[1].set_ylabel('Temperatura [°C]', fontsize = 14)
axs[1].set_xlabel('Día', fontsize =14)
axs[0].set_title('Serie Ambient Weather', fontsize = 18)
plt.show()