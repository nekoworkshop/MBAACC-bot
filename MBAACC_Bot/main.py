import time

from InputInjector import *

from MBAACC_Bot.processInjector import *


def main():

   injector = ProcessInjector()

   while True:
      injector.stageDataPrettyPrint()
      time.sleep(0.01)

if __name__ == "__main__": main()