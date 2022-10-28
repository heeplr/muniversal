
## Quick and dirty json data to munin


1. symlink muniversal.py to /etc/munin/plugins/name_plot
2. create /etc/muniversal.json
3. restart munin


# Example

Solar charge controller data in ```/var/log/solar.json``` where each line looks like this:

```
{"V_bat": 13.54, "V_solar": 16.68, "I_charge": 6.3, "P_charge": 85.30199999999999, "ctrl_temp": 48, "charge_mode": "lead_agm1" }
```

Create symlink:
```
ln -s muniversal.py /etc/munin/plugins/sensors_solar
```

Possible muniversal.json:

```json
{
  "sensors": {
    "solar": {
      "logfile": "/var/log/solar.json",
      "config": {
        "graph_title": "Solar Controller",
        "graph_category": "sensors",
        "graph_info": "Solar Panels + Batteries",
        "graph_scale": "no",
        "bat_voltage.label": "Battery Voltage (V)",
        "bat_voltage.type": "GAUGE",
        "solar_voltage.label": "Solar Voltage (V)",
        "solar_voltage.type": "GAUGE",
        "charge_current.label": "Charge Current (A)",
        "charge_current.type": "GAUGE",
        "charge_power.label": "Charge Power (W)",
        "charge_power.type": "GAUGE",
        "temp_ctrl.label": "Controller Temp"
      },
      "valuemap": {
        "V_bat": "bat_voltage",
        "V_solar": "solar_voltage",
        "I_charge": "charge_current",
        "P_charge": "charge_power",
        "ctrl_temp": "temp_ctrl"
      }
    }
  }
}
```

* '''logfile''' contains one or more json streams
* '''config''' contains munin config
* '''valuemap''' contains one dict per logfile to map json stream keys to munin values
