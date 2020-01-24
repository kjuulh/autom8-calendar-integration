__version__ = '0.1.0'

import pendulum

from autom8_calendar_integration.calendar import Calendar


def start():
    cal = Calendar()
    print(cal.get_workhours_for_date(pendulum.now()))
