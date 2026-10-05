// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
Rectangle {
 property var control
 property string kind: "check"
 readonly property bool selected: control.checked || (kind === "check" && control.checkState === Qt.PartiallyChecked)
 implicitWidth: kind === "switch" ? 41 : 22
 implicitHeight: kind === "switch" ? 23 : 22
 x: control.mirrored ? control.width - width - control.rightPadding : control.leftPadding
 y: control.topPadding + (control.availableHeight - height) / 2
 radius: kind === "check" ? 6 : height / 2
 color: selected ? Material.accent : Material.surface
 border.width: control.visualFocus ? 2 : selected ? 0 : 1
 border.color: control.visualFocus ? Material.accent : Material.border
 opacity: control.enabled ? 1 : 0.45
 Rectangle {
  visible: parent.kind === "switch" || (parent.kind === "radio" && parent.selected)
  width: parent.kind === "switch" ? 19 : 10; height: width; radius: width/2
  x: parent.kind === "switch" ? 2 + control.visualPosition * (parent.width - width - 4) : (parent.width-width)/2
  y: (parent.height-height)/2
  color: parent.kind === "switch" ? Material.foreground : Material.selectedForeground
  Behavior on x { enabled: !control.down; NumberAnimation { duration: 120; easing.type: Easing.OutCubic } }
 }
 Text {
  anchors.centerIn: parent
  visible: parent.kind === "check" && parent.selected
  text: control.checkState === Qt.PartiallyChecked ? "−" : "✓"
  font.pixelSize: 15; font.weight: Font.DemiBold
  color: Material.selectedForeground
 }
}
