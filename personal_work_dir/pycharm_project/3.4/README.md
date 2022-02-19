Just noting for myself that 3.3/csrf5.py has the code to interact
with the exploit server in these challenges programmatically.

I kept these as text because it was quicker to just use PortSwigger's exploit
server UI to update the exploit code than to do so programmatically.

Note for clickjacking 3, we found that the name parameter was vulnerable because it
is set as the innerHtml to an invisible html element 'feedbackResult'. So, we can
provide any html we want in the URL via the name param, and use that, paired with other
pre-filled data, as an exploit.
