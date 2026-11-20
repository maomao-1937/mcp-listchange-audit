# Verification

Run `python -m unittest discover -s tests -v` from this folder. The 5 unit tests cover refresh ordering, missing refresh, malformed input, and clean traces. The README command is also run by the controller before release. CI is configured for Windows and Ubuntu using Python 3.11.
