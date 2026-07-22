from typing import TypeAlias, Any


GroupPath: TypeAlias = tuple[str, ...]
GroupValues: TypeAlias = dict[str, str]
Groups: TypeAlias = dict[GroupPath, GroupValues]
from .model import Applet, Panel
from .plasmaconstants import PanelFormFactor, PanelLocation


from dataclasses import asdict


class PlasmaAnalyzer:
    def build_tree(
        self,
        groups: Groups,
        prefix: GroupPath,
        exclude_top: set[str] | None = None,
    ) -> dict[str, Any]:

        exclude_top = exclude_top or set()
        tree = {}

        for path, kv in groups.items():
            if path[: len(prefix)] != prefix or not kv:
                continue

            remainder = path[len(prefix) :]

            if remainder and remainder[0] in exclude_top:
                continue

            if not remainder:
                tree.update(kv)
                continue

            node = tree

            for seg in remainder:
                node = node.setdefault(seg, {})

            node.update(kv)

        return tree

    def get_applet_ids(self, groups: dict, cid: str) -> List[str]:
        ids = {
            p[3]
            for p in groups
            if len(p) >= 4
            and p[0] == "Containments"
            and p[1] == cid
            and p[2] == "Applets"
        }
        return sorted(ids, key=int)

    def build_applet(
        self,
        groups: Groups,
        prefix: GroupPath,
        aid: str,
    ) -> Applet:

        own = groups.get(prefix, {})

        return Applet(
            id=int(aid),
            plugin=own.get("plugin", ""),
            configuration=self.build_tree(groups, prefix),
        )

    def get_containment_ids(self, groups: Groups) -> list[str]:
        return sorted(
            {p[1] for p in groups if len(p) == 2 and p[0] == "Containments"}, key=int
        )

    def get_nested_applet_ids(
        self,
        groups: Groups,
        cid: str,
        aid: str,
    ) -> list[str]:

        ids = {
            path[5]
            for path in groups
            if (
                len(path) >= 6
                and path[0] == "Containments"
                and path[1] == cid
                and path[2] == "Applets"
                and path[3] == aid
                and path[4] == "Applets"
            )
        }
        
        return sorted(ids, key=int)

    def build_panels(self, groups: Groups) -> list[Panel]:

        panels = []

        for cid in self.get_containment_ids(groups):
            info = groups.get(("Containments", cid), {})

            if info.get("plugin") != "org.kde.panel":
                continue
            
            panel = self.build_panel(groups, cid)

            if panel is not None:
                panels.append(panel)

        return panels

    def build_nested_applets(
    self,
    groups: Groups,
    cid: str,
    aid: str,
    children: list[str],
) -> list[Applet]:

        result = []

        for child in children:
            applet = self.build_applet(
            groups,
            (
                "Containments",
                cid,
                "Applets",
                aid,
                "Applets",
                child,
            ),
            aid=int(child),
        )


            result.append(applet)

        return result

    def build_panel(self, groups: Groups, cid: str) -> Panel:

        info = groups.get(("Containments", cid), {})

        applets: list[Applet] = []

        for aid in self.get_applet_ids(groups, cid):
            applet = self.build_applet(
                groups, ("Containments", cid, "Applets", aid), int(aid)
            )
            children = self.get_nested_applet_ids(groups, cid, aid)
            if children:
                applet.contained_applets = self.build_nested_applets(
                    groups, cid, aid, children=children
                )

            applets.append(applet)

        properties = self.build_tree(
            groups,
            ("Containments", cid),
            exclude_top={"Applets"},
        )
        return Panel(
            id=int(cid),
            plugin=info.get("plugin", ""),
            properties=properties,
            applets=applets,
            screen=int(info["lastScreen"]) if "lastScreen" in info else None,
            location=PanelLocation.from_value(int(info.get("location"))),
            formfactor=PanelFormFactor.from_value(int(info.get("formfactor"))),
        )
    def get_child_applet_ids(
    self,
    groups: Groups,
    containment_id: str,
    parent_id: str,
) -> list[str]:

        prefix = (
        "Containments",
        containment_id,
        "Applets",
        parent_id,
        "Applets",
    )

        result = []

        for path in groups:
            if path[:len(prefix)] == prefix:
                if len(path) == len(prefix) + 1:
                    result.append(path[-1])

        return sorted(result, key=int)

    def full_panel_dump(self, groups: Groups):
        panels = self.build_panels(groups)
        dict_list = [asdict(panel) for panel in panels]
        result = dict()
        result["panels"] = dict_list
        return result
