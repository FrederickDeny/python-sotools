#!/bin/env python3

import os
import sys

from sotools.dl_cache import _cache_libraries, Flags, get_generator

DEFAULT_CACHE = "/etc/ld.so.cache"

if __name__ == '__main__':
    target_cache = DEFAULT_CACHE

    if len(sys.argv) >= 2:
        target_cache = sys.argv[1]

    try:
        with open(target_cache, 'rb') as cache_file:
            cache_data = cache_file.read()
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    libs = _cache_libraries(cache_data)
    print(f"{len(libs)} libs found in cache `{target_cache}'")

    for library in libs:
        hwcap_entry_string = f" hwcap: \"{library.hwcaps}\"" if library.hwcaps else ""
        description = ",".join(
            filter(None,
                   [Flags.description(library.flags), hwcap_entry_string]))
        print(f"\t{library.key} ({description}) => {library.value}")

    generator = get_generator(cache_data)
    if generator:
        print(f"Cache generated by: {generator}")

    sys.exit(0)
