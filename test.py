string = ''' I've got that, Rayan. I'll add a meeting at 1 PM to your calendar for tomorrow.
===add_event===
&calendar.Event{
  Summary: Meeting at 1 PM
  Start: &calendar.EventDateTime{
    DateTime: tomorrow's date + "T13:00:00+00:00",
    TimeZone: "Europe/Bruxelles",
  },
  End: &calendar.EventDateTime{
    DateTime: tomorrow's date + "T14:00:00+00:00",
    TimeZone: "Europe/Bruxelles",
  },
}
'''
first_part = string.split("===add_event===")[0]
second_part = string.split("===add_event===")[1]
print(first_part)

print(second_part)