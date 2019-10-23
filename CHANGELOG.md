## 1.2.0 ... 2019-10-23 18:53:52

 * Improve internal function _norm_loc_ize() by making it take a datetime
   rather than a timestamp and always use the dt internal self._tz.
 * Rearranged test files to allow for test_1_dt_internals.py.
 * Added test and code for method dt.datetime()
 * Updated tests and code for __str__ and __repr__ to make __str__ use
   format "%F %T %Z" and make __repr__ show the raw timestamp and timezone.
 * Wrote dt._fail() and replaced 'raise dt_error(<message>)' with
   dt._fail(<message>)
 * Added tests for internal helper functions.


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
