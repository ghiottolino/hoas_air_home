# HOAS Air-Home
Home Assistant integration to provide Maico air-home data to hoas retrieving data from the air-home web portal.

# Installation

1. Make sure the [HACS](https://github.com/custom-components/hacs) custom component is installed and working.
2. Search for `AirHome Home Assistant` and add it through HACS
3. Refresh home-assistant.

# Configuration

```
sensor:
  - platform: airhome
    scan_interval: 600
    cookie: YOUR_AIRHOME_COOKIE (example ASP.NET_SessionId=YYY)
    serial_number: YOUR_SERIAL_NUMBER (device number)
```
