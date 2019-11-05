## 1.4.1 ... 2019-11-05 18:10:55

 * Address and fix the diff-str bug.
 * Tests and payload for td object comparisons (==, !=, <, <=, >, >=)
 * Test and payload for td.days(), td.hours(), td.minutes(), td.seconds()
 * Test and payload for td.dhhmmss()
 * Test and payload for td.dhms()
 * Make dt and td comparison tests DRY
 * Reflect dt and td comparison tests
 * README.md improvements

## 1.4.0 ... 2019-11-01 20:25:32

 * Write tests and payload for class td (time delta), which represents a
   length of time.
 * Write tests and payload for dt.__add__() so that
    * <dt> + <int> => <dt>
    * <dt> + <td> => <dt>
    * <dt> + <timedelta> => <dt>
    * <int> + <dt> => <dt>
    * <td> + <dt> => <dt>
    * <timedelta> + <dt> => <dt>
    * <dt> + <dt> => TypeError
    * <dt> + <datetime> => TypeError
    * <datetime> + <dt> => TypeError
 * Write tests and [payload] for dt.__sub__() so that
    * <dt> - <dt> => <td>
    * <dt> - <datetime> => <td>
    * <datetime> - <dt> => <td>        (__rsub__)
    * <dt> - <int> => <dt>
    * <dt> - <td> => <dt>
    * <dt> - <timedelta> => <dt>
    * <int> - <dt> => TypeError        (__rsub__)
    * <td> - <dt> => TypeError         (__rsub__)
    * <timedelta> - <dt> => TypeError  (__rsub__)
 * Write tests and payload for td.__add__() so that
    * <td> + <td> => <td>
    * <td> + <timedelta> => <td>
    * <timedelta> + <td> => <td>
    * <td> + <int> => <td>
    * <int> + <td> => <td>
    * <td> + <dt> [== <dt>.__radd__] => <dt>
    * <td> + <datetime> => <dt>
    * <datetime> + <td> (__radd__) => <dt>
 * Write tests and payload for td.__sub__() so that
    * <td> - <td> => <td>
    * <td> - <timedelta> => <td>
    * <timedelta> - <td> => <td> (td.__rsub__)
    * <datetime> - <td> => <dt>  (td.__rsub__)
    * <td> - <int> => <td>
    * <int> - <td> => <td>
    * <td> - <dt> => TypeError   (dt.__sub__)
    * <td> - <datetime> => TypeError
 * Write tests and payload for td.__str__()
 * Complete test coverage


## 1.3.1 ... 2019-10-30 06:26:38

 * Put common test utility items in importable file dtm_test_utils.py and
   started using them instead of repeating them in each test file. Eg.,
   'dtu.pp' rather than 'pp'.
 * Wrote tests for payload code already in dtm/__main__.py.
 * Fixed up payload code to pass its tests.
 * Whitespace cleanup and typos.
 * Ensuring all tests call pytest.dbgfunc() so they are debuggable.
 * Reordered dtm commands in the source code.
 * Made improvements to the payload code for reporting raw timezones, a
   structured set of timezones, etc.
 * Addressed the "0 offset" bug that was causing .next_day() and
   .previous_day() to traceback when they got an argument of 0. Added tests
   that tickled the bug, then fixed the payload code to resolve it and
   satisfy the tests.
 * Wrote tests (and test helper code) for 'dtm calendar'.
 * Wrote payload code for 'dtm calendar'.
 * Made sure that 100% of payload code has test coverage.


## 1.3.0 ... 2019-10-26 13:51:20

 * Add test and code for dt.weekday_ceiling(), parametrize test for
   dt.weekday_floor().
 * Update tests for weekday_{ceiling,floor}() to check for
    * exception raised on invalid argument,
    * target input being a list.
 * Update weekday_{ceiling,floor}() to raise exception on invalid argument
   and handle the target input being a list of weekdays.
 * Add Quick Start section to README.md.
 * Add test and code for $DTM_FORMATS support for adding user-defined
   entries to the list of default parseable formats
 * Add test and code for $DTM_STR support to allow user to specify the
   format __str__() should use.


## 1.2.0 ... 2019-10-24 05:19:17

 * Improve internal function _norm_loc_ize() by making it take a datetime
   rather than a timestamp and always use the dt internal self._tz.
 * Rearranged test files to allow for test_1_dt_internals.py.
 * Added test and code for method dt.datetime()
 * Updated tests and code for __str__ and __repr__ to make __str__ use
   format "%F %T %Z" and make __repr__ show the raw timestamp and timezone.
 * Wrote dt._fail() and replaced 'raise dt_error(<message>)' with
   dt._fail(<message>)
 * Added tests for internal helper functions.
 * Tweaked some tests to address failures on travis.


## 1.1.0 ... 2019-10-22 07:27:57

 * Add tz arg support on input and output methods: test and functionality.
 * Add iso() method: tests and functionality.
 * Add tests that probe dst transitions, both entering and leaving on all
   input and output methods.
 * Make sure all methods have a descriptive comment.
 * Add __call__() method: tests and functionality.
 * Add __str__() method: tests and functionality.
 * Catch README.md up to the package functionality.
 * Add test_2_recipes.py for verifying timezone conversion recipes.
 * Move test_deployable() from test_1_dt.py to test_9_deploy.py so it runs
   last.
 * Replace ._dtobj and other members with ._utc and ._tz.
 * Internal: helper functions for next_day, previous_day, normalizing and
   localizing datetime objects.
 * Internal: define and use 'pp' for 'pytest.param' in test files.
 * Tests involving tz conversions that probe dst entry and exit
   > __call__.
 * Add dtm/__main__.py to git to provide command line functions for
   browsing the timezone database.
 * Add .travis.yml to institute CI for this project.


## 1.0.0 ... 2019-10-12 13:15:12

 * Added CHANGELOG.md to dtm project.
 * Move version info from ./version.py to ./dtm/version.py and update
   setup.py, ./dtm/__init__.py, and ./tests/test_1_dt.py to use it from
   there.
 * Remove ./version.py from the project
 * Minor updates to README.md: future plans, tweaks for accuracy
 * Add test_deployable() from tbx project

## 0.0.4 ... 2019.1012 05:42:52

 * Added version.py as the single point of truth for dtm version info and
   as an entry in py_modules in setup.py. This works. When it was not in
   py_modules, installation failed when setup.py tried to import version.
 * Added ability to query dtm version (dt().version() or dt.version()).
 * Added ISO format "%Y-%m-%dT%H:%M:%S" to default parseable date/time
   formats for the dt constructor. The source string may optionally have a
   final 'Z'. Added tests for this functionality.
 * Added support for dt(epoch=<number>). Added test for this.

## prehistory ... 2019.1006 15:22:44

 * Added setup.py to package
 * Exposed strptime() as a dtm static method
 * Support year, month, day, hour, minute, second members of dt object
 * Support and tests for various comparison operators on dt and datetime
   objects (<, >, ==, !=, <=, >=)
 * Add id names to parametrized tests
 * Add detailed descriptions of the major dt object methods
 * Describe what dtm adds to datetime
