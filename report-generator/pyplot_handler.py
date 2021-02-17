class chart:
    from matplotlib import pyplot as plt
    from matplotlib import dates as mpl_dates
    import traceback

    def __init__(self, measurement, dbase):

        # self.plt = plt
        # self.mpl_dates = mpl_dates
        # self.traceback = traceback

        self.dbase = dbase
        self.measurement = measurement
        self.no_data = '/home/ubuntu/project-study/report-generator/static/images/no_data.png'
        self.image_link = self.no_data
        self.generated = False

    def generate_plot(self, frm, to):
        try:
            self.time, self.amplitude = self.dbase.query(frm, to)
            print(self.measurement, self.time, self.amplitude)
            if len(self.time) > 0:
                self.plt.style.use('seaborn')
                self.plt.figure().set_size_inches(2,1)
                self.plt.xlabel('time')
                self.plt.tight_layout()
                self.plt.ylabel('{} value'.format(self.measurement))
                self.plt.title(self.measurement)
                self.plt.plot_date(self.time, self.amplitude)
                self.plt.savefig(
                    '/home/ubuntu/project-study/report-generator/static/images/{}.png'.format(self.measurement), 
                    dpi=125)
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

