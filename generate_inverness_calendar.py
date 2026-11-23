from datetime import date, timedelta
from zoneinfo import ZoneInfo

from astral import LocationInfo
from astral.sun import sun

tz = ZoneInfo("Europe/London")

city = LocationInfo(
    "Inverness",
    "Scotland",
    "Europe/London",
    57.4778,
    -4.2247
)

START_DATE = date(2026, 11, 24)
END_DATE = date(2050, 12, 31)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "PRODID:-//George Inverness Sun Calendar//EN",
    "X-WR-CALNAME:Inverness Sunrise & Sunset"
]

current = START_DATE

while current <= END_DATE:

    s = sun(city.observer, date=current, tzinfo=tz)

    sunrise = s["sunrise"]
    sunset = s["sunset"]

    sunrise_start = sunrise - timedelta(minutes=10)
    sunset_start = sunset - timedelta(minutes=10)

    lines.extend([
        "BEGIN:VEVENT",
        f"DTSTART;TZID=Europe/London:{sunrise_start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID=Europe/London:{sunrise.strftime('%Y%m%dT%H%M%S')}",
        "SUMMARY:Sunrise",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "END:VEVENT"
    ])

    lines.extend([
        "BEGIN:VEVENT",
        f"DTSTART;TZID=Europe/London:{sunset_start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID=Europe/London:{sunset.strftime('%Y%m%dT%H%M%S')}",
        "SUMMARY:Sunset",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "END:VEVENT"
    ])

    current += timedelta(days=1)

lines.append("END:VCALENDAR")

with open("inverness-sunrise.ics", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Calendar created")