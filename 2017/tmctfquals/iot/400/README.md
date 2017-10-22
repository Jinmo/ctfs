## IOT/OSINT/SCADA 400

In data.pcapng, there are Philips Hue API logs which changed saturation of 3 lights and turned it off.

I extracted JSON requests and listed saturation values of 3 lights, and XOR-ed each other. 3 values to 1 value.

Surprisingly, It printed flags.

## Codes

- codes/lights.json: Dissection information exported from wireshark, in JSON format.
- codes/lights.py: It decodes saturation values and prints the flag.
- codes/image.png: ? not used.