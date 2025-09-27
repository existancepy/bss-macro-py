# Todo

- Let the users save config profiles and simply change between them
- After the macro is stopped, have it send a final report, which is like the hourly report, but using info from the start to finish of the macro
- Add a goo toggle (uses goo settings from existing settings), so it uses goo when collecting from that field

Traceback (most recent call last):
File "/Users/loganlatham/Downloads/bss-macro-Logan/src/modules/macro.py", line 3129, in hourlyReportBackgroundOnce
hourlyReportData = self.hourlyReport.generateHourlyReport(self.setdat)
File "/Users/loganlatham/Downloads/bss-macro-Logan/src/modules/submacros/hourlyReport.py", line 404, in generateHourlyReport
buffQuantity = self.buffDetector.getBuffsWithImage(self.hourBuffs)
File "/Users/loganlatham/Downloads/bss-macro-Logan/src/modules/submacros/hourlyReport.py", line 173, in getBuffsWithImage
if float(val) > float(maxFinalBuffValue):
ValueError: could not convert string to float: '.4.'