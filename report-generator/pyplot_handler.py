class chart:
    import traceback

    def __init__(self, measurement, dbase, plt, mpl_dates):
        self.plt = plt
        self.mpl_dates = mpl_dates
        self.dbase = dbase
        self.measurement = measurement
        self.no_data = '/home/ubuntu/project-study/report-generator/static/images/no_data.png'
        self.image_link = self.no_data
        self.generated = False

    def generate_plot(self, frm, to):
        try:
            time, amplitude, frm_dt, to_dt = self.dbase.query(
                frm, to)
            self.time = self.mpl_dates.date2num(time)
            self.amplitude = self.mpl_dates.date2num(amplitude)
            frm_dt = self.mpl_dates.date2num([frm_dt])
            to_dt = self.mpl_dates.date2num([to_dt])
            print(self.measurement, self.time, self.amplitude)

            if len(self.time) > 0:
                self.plt.plot_date(
                    self.time, self.amplitude, linestyle="solid")
                self.plt.gcf().autofmt_xdate()
                self.plt.gca().set_xlim([frm_dt, to_dt])
                # self.plt.figure().set_size_inches(3, 2)
                self.plt.title(self.measurement)
                self.plt.ylabel('{} value'.format(self.measurement))
                self.plt.xlabel('time')
                # self.plt.tight_layout()
                self.plt.savefig(
                    '/home/ubuntu/project-study/report-generator/static/images/{}.png'.format(
                        self.measurement), dpi=70)
                self.image_link = '/home/ubuntu/project-study/report-generator/static/images/{}.png'.format(
                    self.measurement)
            else:
                self.image_link = self.no_data

        except Exception as e:
            print(e)
            print(self.traceback.format_exc())
            self.image_link = self.no_data
        finally:
            self.generated = True

    def retrieve_plot_dir(self):
        if self.generated:
            self.generated = False
            return self.image_link
        else:
            return self.no_data
