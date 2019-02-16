# dtm
Smart datetime objects

## dt objects
The main thing dtm exports is the 'dt' object. It wraps a standard Python
datetime object so that we can effectively add functionality to the
datetime class.

We wrap datetime rather than inheriting from it because we ran into issues
with the inheritance strategy.

The recommended method of import is:

    from dtm import dt

### constructor
The dt object constructor will accept several argument schemes

#### no arguments

        myobj = dt()
        
Create a dt object containing the current date and time. Effectively the same as

        myobj = datetime().now()
