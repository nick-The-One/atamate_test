## Installation
Using Python 3.10.8
Reqiures poetry version 1.2.0 or newer for development (linters) and running tests \[TBD\]. Have no external dependecies otherwise.  
`poetry install`

## Notes
* I went a bit overboard with comments in hopes to better illustrate my thinking
* Entire thing can be converted to MessageReader class if needed and initialized with set message options
* `_handle_message` returns error string in case of invalid message and not interrupts execution since this branch of behaviour wasn't desribed in test
* `handle_message` with a single `print` statement is used due to requirement to produce printed output, and handling that in the parsing function would require even more logic to already complicated function