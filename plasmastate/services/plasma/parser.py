
from io import TextIOWrapper
import re
HEADER_RE = re.compile(r"\[([^\[\]]*)\]")

GroupMap = dict[tuple[str, ...], dict[str, str]]
class AppletSrcParser:
 
    def parse(self,outfile: TextIOWrapper) -> GroupMap:
        groups: GroupMap = {(): {}}
        current: tuple = ()
        for raw_line in outfile.readlines():
            line = raw_line.strip("\n")
            if not line.strip():
                continue
            if line.startswith("["):
                current = tuple(HEADER_RE.findall(line))
                groups.setdefault(current, {})
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                groups.setdefault(current, {})[key] = value
        return groups
    