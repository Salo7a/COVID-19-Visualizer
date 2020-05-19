import logging
import logging.handlers
import os
import shutil
import sys
import threading
import time
from datetime import datetime
from http.server import HTTPServer, CGIHTTPRequestHandler
from os import chdir, environ

import cv2
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pytz
import qtmodern.styles
import qtmodern.windows
import tzlocal
from PyQt5.QtCore import QUrl, QTimer, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from bubbly.bubbly import bubbleplot
import matplotlib.pyplot as plt

from DataDownload import GetLatest, UpdateData, GenerateDailyData, GetDailyData, GetSummary, GetData
from UI import Ui_MainWindow


def StartServer(path, port=8000):
    """Start a simple webserver serving path on port"""
    chdir(path)
    httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
    httpd.serve_forever()


def SetupLogging():
    handler = logging.handlers.WatchedFileHandler(
        environ.get("LOGFILE", "COVID19Stats.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)


def SafeDivide(x, y):
    if y == 0:
        return 0
    return (x / y)*100


class ApplicationWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        SetupLogging()
        self.setupUi(self)
        self.AddToLog("Starting Server Thread")
        self.port = 8000
        self.server = threading.Thread(name='daemon_server',
                                       target=StartServer,
                                       args=('.', self.port))
        self.server.setDaemon(True)  # Set as a daemon so it will be killed once the main thread is dead.
        self.server.start()
        self.Update.clicked.connect(self.UpdateHandler)
        self.Bubble.setChecked(True)
        self.Bubble.toggled.connect(lambda: self.SetCurrentPlot("Bubble"))
        self.Map.toggled.connect(lambda: self.SetCurrentPlot("Map"))
        self.BarCases.toggled.connect(lambda: self.SetCurrentPlot("BarCases"))
        self.BarDeaths.toggled.connect(lambda: self.SetCurrentPlot("BarDeaths"))
        self.EBubble.toggled.connect(lambda: self.SetCurrentPlot("EBubble"))
        self.Export.clicked.connect(self.ExportHandler)
        self.SummaryTimer = QTimer()
        self.SummaryTimer.setInterval(600000)
        self.SummaryTimer.timeout.connect(self.UpdateSummary)
        self.UpdateSummary()
        self.LatestCountries = []
        self.data = []
        self.Times = []
        self.TimesFormatted = []
        self.Timeline = []
        self.Summary = []
        self.Accumulated = []
        self.AccumulatedData = GetData()
        self.browser.setUrl(QUrl("http://localhost:8000/bubble.html"))
        self.data = GetDailyData()
        self.GenerateTimes()
        self.GenerateTimeline()
        self.GenerateAccumulated()
        self.show()

    @pyqtSlot(str)
    def ShowCountryPlot(self, country):
        self.AddToLog(f"Showing Plots For {country}", duration=5000)
        CountryData = self.Timeline[self.Timeline.country == country]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=CountryData['Date'], y=CountryData['deaths'],
                                 mode='lines+markers',
                                 name='Deaths'))
        fig.add_trace(go.Scatter(x=CountryData['Date'], y=CountryData['confirmed'],
                                 mode='lines+markers',
                                 name='Confirmed Cases'))
        fig.update_layout(title=f'Cases & Deaths Through Time in {country}',
                          xaxis_title='Date')

        fig.show()

    def GenerateLatest(self):
        """Generates Array of Latest COVID19 Statistics For All Countries"""
        latesttemp = []
        for country in self.data:
            if len(latesttemp) > 0 and latesttemp[-1][0] == country['country']:
                latesttemp[-1][1] += country['latest']['confirmed']
                latesttemp[-1][2] += country['latest']['deaths']
                latesttemp[-1][3] += country['latest']['recovered']
                continue
            temp = [country['country'], country['latest']['confirmed'], country['latest']['deaths'],
                    country['latest']['recovered']]
            latesttemp.append(temp)
        self.LatestCountries = pd.DataFrame(data=latesttemp, columns=['country', 'confirmed', 'deaths', 'recovered'])

    def GenerateBubbleGraph(self):
        """Generates Bubble Graph From Latest Data COVID19 Data"""
        figure = bubbleplot(dataset=self.Timeline, x_column='deaths', y_column='recovered',
                            bubble_column='country', time_column="date", size_column='confirmed', scale_bubble=4,
                            x_title="Number of Deaths", color_column="confirmed", y_title="Recoveries",
                            colorbar_title='New Cases', x_logscale=True, y_logscale=True,
                            colorscale='Viridis', title='COVID19')

        plotly.offline.plot(figure, filename='Bubble.html', include_plotlyjs='directory', auto_open=False)

    def GenerateDeathBubble(self):
        """Generates Death Rate Bubble Graph From Latest COVID19 Data"""
        figure = bubbleplot(dataset=self.Accumulated, x_column='recovered', y_column='confirmed',
                            bubble_column='country', time_column="date", size_column='DeathRate', scale_bubble=4,
                            x_title="Number of Recoveries", color_column="DeathRate",
                            y_title="Number of Confirmed Cases",
                            colorbar_title='Death Rate', x_logscale=True, y_logscale=True,
                            colorscale='Viridis', title='Country Death Rate')

        plotly.offline.plot(figure, filename='EBubble.html', include_plotlyjs='directory', auto_open=False)

    def GenerateMap(self):
        fig = px.choropleth(self.Timeline,  # Input Pandas DataFrame
                            locations="country",  # DataFrame column with locations
                            color="confirmed",  # DataFrame column with color values
                            hover_name="country",
                            hover_data=["confirmed", "deaths", "recovered"],
                            animation_frame="Date",
                            animation_group="country",
                            projection="miller",
                            locationmode='country names')
        plotly.offline.plot(fig, filename='Map.html', include_plotlyjs='directory', auto_open=False)

    def GenerateTimes(self):
        """Generates array containing all dates included in the dataset"""
        for item in self.data[0]["timelines"]["confirmed"]["timeline"]:
            datetime_object = datetime.strptime(item, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=pytz.utc).astimezone(
                tzlocal.get_localzone())
            time = datetime_object.strftime("%y%m%d")
            self.Times.append(time)
            self.TimesFormatted.append(item)

    def GenerateTimeline(self):
        """Generates All Countries Timeline Data"""
        timelinetemp = []
        for time, timekey in zip(self.Times, self.TimesFormatted):
            rtime = datetime.strptime(timekey, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=pytz.utc).astimezone(
                tzlocal.get_localzone())
            currentday = rtime.strftime("%d-%B-%y")
            rtime = rtime.strftime("%#m/%#d/%y")
            for country in self.data:
                if len(country['timelines']['recovered']['timeline']) == 0:
                    continue
                if len(timelinetemp) > 0 and timelinetemp[-1][0] == country['country']:
                    timelinetemp[-1][1] += country['timelines']['confirmed']['timeline'][timekey]
                    timelinetemp[-1][2] += country['timelines']['deaths']['timeline'][timekey]
                    timelinetemp[-1][3] += country['timelines']['recovered']['timeline'][rtime]
                else:
                    temp = [country['country'], country['timelines']['confirmed']['timeline'][timekey],
                            country['timelines']['deaths']['timeline'][timekey],
                            country['timelines']['recovered']['timeline'][rtime], int(time), currentday]
                    timelinetemp.append(temp)
        self.Timeline = pd.DataFrame(data=timelinetemp, columns=['country', 'confirmed', 'deaths',
                                                                 'recovered', 'date', 'Date'])

    def GenerateAccumulated(self):
        """Generates All Countries Accumulated Timeline"""
        timelinetemp = []
        for time, timekey in zip(self.Times, self.TimesFormatted):
            rtime = datetime.strptime(timekey, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=pytz.utc).astimezone(
                tzlocal.get_localzone())
            currentday = rtime.strftime("%d-%B-%y")
            rtime = rtime.strftime("%#m/%#d/%y")
            for country in self.AccumulatedData:
                if len(country['timelines']['recovered']['timeline']) == 0:
                    continue
                if len(timelinetemp) > 0 and timelinetemp[-1][0] == country['country']:
                    timelinetemp[-1][1] += country['timelines']['confirmed']['timeline'][timekey]
                    timelinetemp[-1][2] += country['timelines']['deaths']['timeline'][timekey]
                    timelinetemp[-1][3] += country['timelines']['recovered']['timeline'][rtime]
                    timelinetemp[-1][4] = SafeDivide(timelinetemp[-1][2], timelinetemp[-1][1])
                else:
                    temp = [country['country'], country['timelines']['confirmed']['timeline'][timekey],
                            country['timelines']['deaths']['timeline'][timekey],
                            country['timelines']['recovered']['timeline'][rtime],
                            SafeDivide(country['timelines']['deaths']['timeline'][timekey],
                            country['timelines']['confirmed']['timeline'][timekey]), currentday, int(time)]
                    timelinetemp.append(temp)
        self.Accumulated = pd.DataFrame(data=timelinetemp, columns=['country', 'confirmed', 'deaths',
                                                                    'recovered', 'DeathRate', 'Date', 'date'])

    def GenerateBarCases(self):
        CleanedCases = self.Timeline[self.Timeline.confirmed != 0]
        fig = px.bar(CleanedCases, x='country', y='confirmed', animation_frame="Date", animation_group="country",
                     hover_data=["confirmed", "deaths", "recovered"],
                     color_continuous_scale=plotly.express.colors.cyclical.IceFire)
        fig.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder': 'total descending'})
        plotly.offline.plot(fig, filename='BarCases.html', include_plotlyjs='directory', auto_open=False)

    def GenerateBarDeaths(self):
        CleanedDeaths = self.Timeline[self.Timeline.deaths != 0]
        fig = px.bar(CleanedDeaths, x='country', y='deaths', animation_frame="Date", animation_group="country",
                     hover_data=["confirmed", "deaths", "recovered"],
                     color_continuous_scale=plotly.express.colors.cyclical.IceFire)
        fig.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder': 'total descending'})
        plotly.offline.plot(fig, filename='BarDeaths.html', include_plotlyjs='directory', auto_open=False)

    def UpdateSummary(self):
        self.AddToLog("Updating Summary", duration=5000)
        self.Summary = GetSummary()
        self.Cases.setStyleSheet("QLabel { color : yellow; }")
        self.Cases.setText(f"{self.Summary['Global']['TotalConfirmed']:,}")
        self.CasesNew.setText(f"(+{self.Summary['Global']['NewConfirmed']:,})")
        self.Deaths.setStyleSheet("QLabel { color : red; }")
        self.Deaths.setText(f"{self.Summary['Global']['TotalDeaths']:,} ")
        self.DeathsNew.setText(f"(+{self.Summary['Global']['NewDeaths']:,})")
        self.Recovered.setStyleSheet("QLabel { color : green; }")
        self.Recovered.setText(f"{self.Summary['Global']['TotalRecovered']:,} ")
        self.RecoveredNew.setText(f"(+{self.Summary['Global']['NewRecovered']:,})")

    def UpdateHandler(self):
        self.UpdateThread = threading.Thread(target=self.UpdateAll)
        self.UpdateThread.start()

    def UpdateAll(self):
        self.Export.setDisabled(True)
        self.Update.setDisabled(True)
        self.AddToLog("Database Update Started")
        self.AddToLog("Downloading Data")
        UpdateData()
        self.AddToLog("Parsing Data")
        GenerateDailyData()
        self.UpdateSummary()
        self.AddToLog("Getting Data")
        self.data = GetDailyData()
        self.AddToLog("Generating Times")
        self.GenerateTimes()
        self.GenerateLatest()
        self.AddToLog("Generating Timeline")
        self.GenerateTimeline()
        self.AddToLog("Generating Accumulated Data Timeline")
        self.GenerateAccumulated()
        self.AddToLog("Generating Bubble Graph")
        self.GenerateBubbleGraph()
        self.AddToLog("Generating Cases Bar Chart")
        self.GenerateBarCases()
        self.AddToLog("Generating Deaths Bar Chart")
        self.GenerateBarDeaths()
        self.AddToLog("Generating Death Rate Bubble Graph")
        self.GenerateDeathBubble()
        self.AddToLog("Update Completed Successfully", duration=2000)
        self.Export.setDisabled(False)
        self.Update.setDisabled(False)

    def AddToLog(self, log, type=20, duration=100000):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(log, duration)
        llog = " " + time.ctime(time.time()) + " : " + log
        if type == 20:
            logging.info(llog)
        elif type == 30:
            logging.warning(llog)

    def SetCurrentPlot(self, plot):
        self.AddToLog(f"Switched to {plot}", duration=3000)
        self.browser.setUrl(QUrl(f"http://localhost:8000/{plot}.html"))
        if plot == "Map":
            self.channel = QWebChannel(self.browser.page())
            self.browser.page().setWebChannel(self.channel)
            self.channel.registerObject('backend', self)
            self.AddToLog("Created Web Channel", duration=3000)

    def ExportHandler(self):
        self.ExportThread = threading.Thread(target=self.VideoExport)
        self.ExportThread.start()

    def VideoExport(self):
        self.AddToLog("Video Export Starting")
        self.Export.setDisabled(True)
        self.Update.setDisabled(True)
        frames = len(self.Times)
        ImgPaths = []
        if self.Bubble.isChecked():
            i = 1
            dic = "Bubble"
            shutil.rmtree(dic, ignore_errors=True)
            os.mkdir(dic)
            for date in self.Times:
                frame = self.Timeline[self.Timeline.date == int(date)]
                fig = px.scatter(frame, x='deaths', y='recovered', color="confirmed", size_max=100,
                                 size='confirmed', text='country', color_continuous_scale=px.colors.sequential.Viridis,
                                 title='COVID19')
                fig.write_image(f"{dic}/{i:03d}.jpeg")
                self.AddToLog(f"Rendering Frame {i}/{frames}")
                ImgPaths.append(f"Bubble/{i:03d}.jpeg")
                i += 1
        elif self.Map.isChecked():
            i = 1
            dic = "Map"
            shutil.rmtree(dic, ignore_errors=True)
            os.mkdir(dic)
            for date in self.Times:
                frame = self.Timeline[self.Timeline.date == int(date)]
                fig = px.choropleth(frame,  # Input Pandas DataFrame
                                    locations="country",  # DataFrame column with locations
                                    color="confirmed",  # DataFrame column with color values
                                    hover_name="country",
                                    hover_data=["confirmed", "deaths", "recovered"],
                                    projection="miller",
                                    locationmode='country names')
                fig.write_image(f"{dic}/{i:03d}.jpeg")
                self.AddToLog(f"Rendering Frame {i}/{frames}")
                ImgPaths.append(f"{dic}/{i:03d}.jpeg")
                i += 1
        elif self.BarCases.isChecked():
            i = 1
            dic = "BarCases"
            shutil.rmtree(dic, ignore_errors=True)
            os.mkdir(dic)
            for date in self.Times:
                CleanedCases = self.Timeline[self.Timeline.confirmed != 0]
                frame = CleanedCases[CleanedCases.date == int(date)]
                fig = px.bar(frame, x='country', y='confirmed',
                             hover_data=["confirmed", "deaths", "recovered"],
                             color_continuous_scale=plotly.express.colors.cyclical.IceFire)
                fig.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder': 'total descending'})
                fig.write_image(f"{dic}/{i:03d}.jpeg")
                self.AddToLog(f"Rendering Frame {i}/{frames}")
                ImgPaths.append(f"{dic}/{i:03d}.jpeg")
                i += 1
        elif self.BarDeaths.isChecked():
            i = 1
            dic = "BarDeaths"
            shutil.rmtree(dic, ignore_errors=True)
            os.mkdir(dic)
            for date in self.Times:
                CleanedCases = self.Timeline[self.Timeline.deaths != 0]
                frame = CleanedCases[CleanedCases.date == int(date)]
                fig = px.bar(frame, x='country', y='deaths',
                             hover_data=["confirmed", "deaths", "recovered"],
                             color_continuous_scale=plotly.express.colors.cyclical.IceFire)
                fig.update_layout(xaxis_tickangle=-45, xaxis={'categoryorder': 'total descending'})
                fig.write_image(f"{dic}/{i:03d}.jpeg")
                self.AddToLog(f"Rendering Frame {i}/{frames}")
                ImgPaths.append(f"{dic}/{i:03d}.jpeg")
                i += 1
        elif self.EBubble.isChecked():
            i = 1
            dic = "DRBubble"
            shutil.rmtree(dic, ignore_errors=True)
            os.mkdir(dic)
            for date in self.Times:
                frame = self.Accumulated[self.Accumulated.date == int(date)]
                fig = px.scatter(frame, x='recovered', y='confirmed', color="DeathRate", size_max=100,
                                 size='DeathRate', text='country', color_continuous_scale=px.colors.sequential.Viridis,
                                 title='COVID19 Death Rate')
                fig.write_image(f"{dic}/{i:03d}.jpeg")
                self.AddToLog(f"Rendering Frame {i}/{frames}")
                ImgPaths.append(f"{dic}/{i:03d}.jpeg")
                i += 1
        self.AddToLog(f"Rendering Complete")
        Frames = []
        for im in ImgPaths:
            img = cv2.imread(im)
            height, width, layers = img.shape
            size = (width, height)

            # inserting the frames into an image array
            Frames.append(img)
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save", f"{dic}.avi", "Video Files (*.avi)", options=options)
        if fileName:
            out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(*'DIVX'), 4, size)
            self.AddToLog("Writing File")
            for f in Frames:
                # writing to a image array
                out.write(f)
            out.release()
            self.AddToLog("Video Exporting Complete", duration=5000)
        else:
            self.AddToLog("Video Exporting Canceled", duration=5000)
        shutil.rmtree(dic, ignore_errors=True)
        self.Export.setDisabled(False)
        self.Update.setDisabled(False)



# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.setWindowTitle("COVID19 Stats")
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(application)
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
