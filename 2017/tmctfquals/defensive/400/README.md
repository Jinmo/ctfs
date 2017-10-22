## Analysis - defensive 400

It was eternalblue + doublepulsar payload. Fortunately, [a decoder](https://github.com/countercept/doublepulsar-c2-traffic-decryptor) for traffic existed, but didn't work properly.

The cause is, it looks the packet with TCP chunks, but the actual data is transferred and decoded by SMB protocol in OS. Wireshark decodes this, but the script is not.

So I exported Packet Dissection summary with JSON format from wireshark, and decoded it through the routine in the repo.

### Codes

- codes/extract.py: Traffic decoder
- extractme2.json: Traffic data with JSON format (from Wireshark)
- codes/output: Dumped dll + exe. Two MZ headers in the file.
  - 1.dll: First MZ header. I don't know what it does.
  - 2.exe: Second MZ header. Windows binary compiled with Go language.
- codes/payload.exe
  - I analysed 2.exe and wrote solver for a routine that seemed to generate a flag, which checks a string.

codes/payload.exe gives the flag. It uses Z3Py.