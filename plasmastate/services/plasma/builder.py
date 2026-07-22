from .model import Panel

class PlasmaBuilder:
    def build(self,groups) -> list[Panel]:
        panels = []
        containment_ids = {p[1] for p in groups if len(p) == 2 and p[0] == "Containments"}
        for cid in sorted(containment_ids, key=int):
            info = groups.get(("Containments", cid), {})
            if info.get("plugin") != "org.kde.panel":
                continue

            widgets = []
            for aid in self.get_applet_ids(groups, cid):
                entry = self.describe_applet(groups, cid, aid)
                cfg_direct = groups.get(("Containments", cid, "Applets", aid, "Configuration"), {})
                systray_id = cfg_direct.get("SystrayContainmentId")
                if systray_id:
                    entry["systray_widgets"] = [
                        self.describe_applet(groups, systray_id, said)
                        for said in self.get_applet_ids(groups, systray_id)
                    ]
                widgets.append(entry)

            properties = self.build_tree(groups, ("Containments", cid), exclude_top={"Applets"})

            panels.append({
                "id": cid,
                "screen": info.get("lastScreen"),
                "location": LOCATIONS.get(info.get("location", ""), "unbekannt"),
                "location_raw": info.get("location"),
                "formfactor": FORMFACTORS.get(info.get("formfactor", ""), "unbekannt"),
                "formfactor_raw": info.get("formfactor"),
                "properties": properties,
                "widgets": widgets,
            })


