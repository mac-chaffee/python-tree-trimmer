# Python Tree Trimmer

This repo contains a script to find tiny-but-popular Python packages that might not be necessary for their dependers to use.

For example, if a popular library like Django happened to have a sub-sub-sub-sub- dependency on some random library which is just a few lines of Python code, the dependency "tree" could be "trimmed" by finding whichever sub-dependency imports the dependency and just inlining the code.

Example: https://github.com/microlinkhq/metascraper/pull/449

The reasons for doing this are:

* increased security (less attack surface of random developers that could get hacked/bought out)
* decreased network overhead during pip installs
* encouraging a healthy relationship with dependencies (tiny dependencies are often more trouble than they're worth), something [other ecosystems](https://arstechnica.com/information-technology/2016/03/rage-quit-coder-unpublished-17-lines-of-javascript-and-broke-the-internet/) lack ;)
* Since this is not really a huge benefit in the grand scheme of things, the final reason is: my own education!

## Notes

* List of most popular packages came from https://hugovk.github.io/top-pypi-packages/ . I removed the JSON bits and only took the top ~2.3k.
* You'll need a github [Personal Access Token](https://github.com/settings/tokens) to be able to make over 60 API calls in an hour. Don't grant the token any permissions since you're just reading public repo metadata.
* Yes I know you could parallelize the HTTP requests, but I want to be a good citizen of the pypi API since it has no rate limits.
* A good chunk of repos don't have github repo links that the script could detect. About 250 don't have github links, and about 21 didn't return LoC metadata from github.
* Could the size of wheels be a good approximation for python LoC? Then we could remove the need to contact github.

## Output

Running this on Sep 26th found about 30 "tiny" packages, which I trimmed down (removed packages with tons of C/C++/html/js/other important code, removed deprecated/stub packages, etc.) to the following list:

* https://github.com/datamade/probableparsing only has 2357 python bytes
* https://github.com/yusugomori/barbar only has 3047 python bytes
* https://github.com/kittyandrew/telethon-tgcrypto only has 1039 python bytes
* https://github.com/MobileDynasty/pytest-env only has 2177 python bytes
* https://github.com/jstasiak/enum-compat only has 1346 python bytes
* https://github.com/yashtodi94/pytest-custom_exit_code only has 3804 python bytes
* https://github.com/tylerbakke/MarkupPy only has 1163 python bytes
* https://github.com/cldellow/parquet-metadata only has 2893 python bytes
* https://github.com/glyph/publication only has 2164 python bytes
* https://github.com/eugenekolo/pip-install only has 2891 python bytes
* https://github.com/vagrantism/libify only has 2663 python bytes
* https://github.com/bigsassy/pytest-pythonpath only has 3560 python bytes
* https://github.com/sobolevn/flake8-broken-line only has 3349 python bytes
* https://github.com/jcb91/jupyter_highlight_selected_word only has 1871 python bytes
* https://github.com/scipy/oldest-supported-numpy only has 37 python bytes
* https://github.com/satoshi03/slack-python-webhook only has 1694 python bytes

I think the fact that the list is so short is testament to the Python community's healthy relationship with dependencies. Or maybe that's incidental since dependency management is notoriously hard to do in Python so maybe people find it easier to write their own left-pad instead of figuring out which dep manager is in style now ;)
