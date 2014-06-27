simplecache.py
==============
MIT Licenced.

A very simple python caching proxy for helping with debugging / testing / mocking access to slow remote services.  It caches the results as simple flat files, which it stores indefinitely.

This is often really useful when prototyping and debugging slow services.  If you want to use it in production (be careful!!) for anything, make sure it's only public facing with a good reverse proxy such as nginx in front of it, and it's probably a good idea to create a cron job or something to daily flush the cache.

usage:
------

python simpleserver.py <other_site>

