## 1.0.0 ...

 * Added CHANGELOG.md to dtm project.
 * Move version info from ./version.py to ./dtm/verinfo.py and update
   setup.py, ./dtm/__init__.py, and ./tests/test_1_dt.py to use it from
   there.
 * Remove ./version.py from the project
 * Minor updates to README.md: future plans, tweaks for accuracy

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
