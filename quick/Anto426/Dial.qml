// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.Dial {
 id: control
 implicitWidth: 100; implicitHeight: 100
 background: Surface { radius: Math.min(width,height)/2; focused: control.visualFocus }
 handle: Rectangle {
  width: Material.thumbSize; height: width; radius: width/2; color: Material.accent
  x: (control.width-width)/2; y: Material.spacing
  transform: Rotation { origin.x: width/2; origin.y: control.height/2 - Material.spacing; angle: control.angle }
 }
}
