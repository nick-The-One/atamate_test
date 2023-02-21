## Installation
Using Python 3.10.8  
Reqiures poetry version 1.2.0 or newer for development (linters) and running tests. Have no external dependecies otherwise.  
`make init` — this will install poetry and setup venv with all dependencies  
`make test` will run tests in venv

## Notes
* I went a bit overboard with comments in hopes to better illustrate my thinking
* Used 99 char line limit from PEP8 instead of default 79 to make it slightly more readable
* Entire thing can be converted to MessageReader class if needed and initialized with set message options
* `_handle_message` returns error string in case of invalid message and not interrupts execution since this branch of behaviour wasn't desribed in test
* `handle_message` with a single `print` statement is used due to requirement to produce printed output, and handling that in the parsing function would require even more logic to already complicated function
* Might have gone too defensive, so for two failure states — bad readings count unpacking and malformed sensor reading — I couldn't come up with good tests