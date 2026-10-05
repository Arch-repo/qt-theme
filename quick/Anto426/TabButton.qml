// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.TabButton {
 id: control
 implicitWidth: Math.max(80, implicitContentWidth + leftPadding + rightPadding)
 implicitHeight: Math.max(40, implicitContentHeight + topPadding + bottomPadding)
 padding: Material.padding; spacing: Material.spacing; hoverEnabled: true
 contentItem: ButtonContent { control: control }
 background: Surface {
  highlighted: false
  pressed: control.down; hovered: control.hovered; focused: control.visualFocus
  flat: false
  color: control.checked ? Material.selectedSurface : highlighted ? Material.accent : pressed ? Material.selectedSurface : hovered ? Material.hoverSurface : flat ? "transparent" : Material.surface
  
 }
}
