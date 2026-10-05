// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.MenuItem {
 id: control
 implicitWidth: 180; implicitHeight: 40
 padding: Material.padding; leftPadding: padding + 22; rightPadding: padding + 18
 spacing: Material.spacing; hoverEnabled: true
 contentItem: ButtonContent { control: control }
 background: Surface { highlighted: control.highlighted; pressed: control.down; flat: true }
 indicator: Text { text: control.checked ? "✓" : ""; color: control.highlighted ? Material.selectedForeground : Material.foreground; x: control.padding; y: (control.height-height)/2 }
 arrow: Text { visible: control.subMenu; text: control.mirrored ? "‹" : "›"; color: control.highlighted ? Material.selectedForeground : Material.foreground; x: control.width-width-control.padding; y: (control.height-height)/2 }
}
