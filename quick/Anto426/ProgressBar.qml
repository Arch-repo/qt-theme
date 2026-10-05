// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.ProgressBar {
 id: control
 implicitWidth: 180; implicitHeight: Material.meterHeight
 background: Rectangle { radius: height/2; color: Material.border }
 contentItem: Item {
  clip: true
  Rectangle {
   width: control.indeterminate ? parent.width * .3 : control.position * parent.width
   height: parent.height; radius: height/2; color: Material.accent
   NumberAnimation on x { running: control.indeterminate && control.visible; from: -width; to: control.width; duration: 1100; loops: Animation.Infinite }
  }
 }
}
