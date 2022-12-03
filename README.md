# CSGO Chat Autotranslator

This software reads the console log output of csgo, which can be written to a seperate file using the console command `con_logfile <filename>`. Where `<filename>` will then exist inside the csgo installation folder.

Press the "Open CS:GO Console Log File" button and input the ABSOLUTE path to your console logfile.
The Program will read the logfile and use the google translate API to translate the message. It will then get displayed inside this Software, along with a timestamp of when the message was read, a message type (team or all chat), who sent it (steam profile name) and details about the translated laguanges. You can use pretty much any target language supported by google translate.