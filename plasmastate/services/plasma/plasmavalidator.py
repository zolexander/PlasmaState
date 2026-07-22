from .model import Panel,Applet
class PlasmaValidator:

    def validate_panel(self, panel: Panel) -> list[str]:
        errors = []

        if panel.plugin != "org.kde.panel":
            errors.append(f"Containment {panel.id} ist kein Panel.")

        if panel.location is None:
            errors.append(f"Panel {panel.id}: keine Position.")

        if panel.formfactor is None:
            errors.append(f"Panel {panel.id}: kein FormFactor.")
        
        for applet in panel.applets:
            errors += self.validate_applet(applet)
            
        return errors
    
    def validate_applet(self, applet: Applet) -> list[str]:
        errors = []

        if not applet.plugin:
            errors.append(f"Applet {applet.id}: Plugin fehlt.")
        if applet.contained_applets:
            for contained_applet in applet.contained_applets:
                errors +=self.validate_applet(contained_applet)
        return errors