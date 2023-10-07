#PortWhisper

PortWhisper is a Python-based graphical user interface (GUI) application that allows users to perform two main network tasks:

## Scan Ports
- Users can enter an IP address and a range of ports (e.g., 80-100) to scan.
- They can select a scan type (TCP, UDP, or HTTP) from the settings.
- Clicking the "Scan starten" button initiates the port scanning process.
- Results are displayed in real-time, indicating whether each scanned port is open, closed, or unresponsive.

## Ping
- Users can enter an IP address in the "Ping-Adresse" field.
- Clicking the "Ping starten" button sends a ping request to the specified IP address.
- The response, if received, is displayed as "Antwort von [IP address]: [ping output]".
- If there is no response or the request times out, it displays "Nicht möglich".
- Users can cancel an ongoing ping request using the "Ping Anfrage abbrechen" button.

## Additional Features
- The application uses the tkinter library for the graphical interface.
- Tabs are used to separate the "Scan Ports" and "Ping" functionalities.
- Users can configure the scan type (TCP, UDP, or HTTP) in the "Einstellungen" tab.
- The application provides real-time feedback in the "Scan Ports" tab with color-coded labels for open, closed, and unresponsive ports.

This tool simplifies the process of network port scanning and ping testing, making it accessible to users through an intuitive graphical interface.
