esphome:
  name: water-level-sensor
  comment: "3-level water tank sensor with stable logic (Low/Medium/Full/Empty)"

esp32:
  board: esp32dev
  framework:
    type: esp-idf

wifi:
  ssid: "Wifi-Deco"
  password: "1q2w3e4r"

logger:
  level: DEBUG   # enable detailed logs

api:
captive_portal:

# ------------------------
# Raw Tank Level Probes
# ------------------------
binary_sensor:
  - platform: gpio
    pin:
      number: 32
      mode: INPUT_PULLUP
    id: tank_low
    name: "Tank Low"
    device_class: moisture
    filters:
      - invert          # probe to GND when wet
      - delayed_on: 200ms
      - delayed_off: 2s

  - platform: gpio
    pin:
      number: 33
      mode: INPUT_PULLUP
    id: tank_medium
    name: "Tank Medium"
    device_class: moisture
    filters:
      - invert
      - delayed_on: 200ms
      - delayed_off: 2s

  - platform: gpio
    pin:
      number: 25
      mode: INPUT_PULLUP
    id: tank_full
    name: "Tank Full"
    device_class: moisture
    filters:
      - invert
      - delayed_on: 200ms
      - delayed_off: 2s

# ------------------------
# Derived Tank State
# ------------------------
sensor:
  - platform: template
    name: "Tank Status"
    id: tank_status
    update_interval: 2s
    accuracy_decimals: 0
    lambda: |-
      // Cascading logic: highest probe wet determines state
      if (id(tank_full).state) {
        ESP_LOGI("tank_status", "DEBUG: Tank FULL");
        return 3.0f;  // Full
      }
      if (id(tank_medium).state) {
        ESP_LOGI("tank_status", "DEBUG: Tank MEDIUM");
        return 2.0f;  // Medium
      }
      if (id(tank_low).state) {
        ESP_LOGI("tank_status", "DEBUG: Tank LOW");
        return 1.0f;  // Low
      }
      ESP_LOGI("tank_status", "DEBUG: Tank EMPTY");
      return 0.0f;    // Empty

text_sensor:
  - platform: template
    name: "Tank Level Text"
    update_interval: 2s
    lambda: |-
      if (id(tank_full).state) {
        return {"Full"};
      }
      if (id(tank_medium).state) {
        return {"Medium"};
      }
      if (id(tank_low).state) {
        return {"Low"};
      }
      return {"Empty"};
