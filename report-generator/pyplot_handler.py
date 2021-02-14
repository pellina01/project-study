class chart:
    from matplotlib import pyplot as plt
    from matplotlib import dates as mpl_dates
    import traceback

    def __init__(self, measurement, dbase):
        self.dbase = dbase
        self.measurement = measurement
        self.image_link = '/home/ubuntu/project-study/report-generator/images/no_data.png'
        self.generated = False
        self.plt.style.use('seaborn')

    def generate_plot(self, frm, to):
        try:
            self.time, self.amplitude = self.dbase.query(frm, to)
            print(self.measurement, self.time, self.amplitude)
            if len(self.time) > 0:
                self.plt.plot_date(self.time, self.amplitude)
                self.plt.xlabel('time')
                self.plt.ylabel('{} value'.format(self.measurement))
                self.plt.title(self.measurement)
                self.plt.tight_layout()
                self.plt.savefig(
                    '/home/ubuntu/project-study/report-generator/images/{}.png'.format(self.measurement))
                self.image_link = '/home/ubuntu/project-study/report-generator/images/{}.png'.format(
                    self.measurement)
            else:
                self.image_link = '/home/ubuntu/project-study/report-generator/images/no_data.png'

        except Exception as e:
            print(e)
            print(self.traceback.format_exc())
            self.image_link = '/home/ubuntu/project-study/report-generator/images/no_data.png'
        finally:
            self.generated = True

    def retrieve_plot_dir(self):
        if self.generated:
            self.generated = False
            return self.image_link

