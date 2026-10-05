// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.DelayButton {
 id: control
 implicitWidth: Math.max(100, implicitContentWidth + leftPadding + rightPadding)
 implicitHeight: Math.max(40, implicitContentHeight + topPadding + bottomPadding)
 padding: Material.padding; spacing: Material.spacing; hoverEnabled: true
 contentItem: ButtonContent { control: control }
 background: Surface {
  highlighted: control.checked; hovered: control.hovered; pressed: control.down; focused: control.visualFocus
  Rectangle { anchors.bottom: parent.bottom; width: parent.width*control.progress; height: Material.meterHeight; radius: height/2; color: Material.accent }
 }
}
