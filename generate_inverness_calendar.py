from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from astral import LocationInfo
from astral.sun import sun

tz = ZoneInfo("Europe/London")

city = LocationInfo(
    "Inverness",
    "Scotland",
    "Europe/London",
    57.4778,
    -4.2247,
)

START_DATE = date(2026, 11, 24)
END_DATE = date(2028, 12, 31)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "PRODID:-//George Inverness Sun Calendar//EN",
    "X-WR-CALNAME:Inverness Sunrise & Sunset",
    "X-WR-TIMEZONE:Europe/London",
    "",
    "BEGIN:VTIMEZONE",
    "TZID:Europe/London",
    "X-LIC-LOCATION:Europe/London",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:+0000",
    "TZOFFSETTO:+0100",
    "TZNAME:BST",
    "DTSTART:19810329T010000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0000",
    "TZNAME:GMT",
    "DTSTART:19961027T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
    "END:STANDARD",
    "END:VTIMEZONE",
]

dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

current = START_DATE

while current <= END_DATE:

    s = sun(city.observer, date=current, tzinfo=tz)

    sunrise = s["sunrise"]
    sunset = s["sunset"]

    sunrise_start = sunrise - timedelta(minutes=10)
    sunset_start = sunset - timedelta(minutes=10)

    lines.extend([
        "BEGIN:VEVENT",
        f"UID:sunrise-{current.isoformat()}@grumblesuk.github.io",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;TZID=Europe/London:{sunrise_start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID=Europe/London:{sunrise.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:Sunrise ({sunrise.strftime('%H:%M')})",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "END:VEVENT",
    ])

    lines.extend([
        "BEGIN:VEVENT",
        f"UID:sunset-{current.isoformat()}@grumblesuk.github.io",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;TZID=Europe/London:{sunset_start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID=Europe/London:{sunset.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:Sunset ({sunset.strftime('%H:%M')})",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "END:VEVENT",
    ])

    current += timedelta(days=1)

lines.append("END:VCALENDAR")

with open("inverness-sunrise.ics", "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\r\n".join(lines))

print("Calendar created successfully.")