// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.Slider {
 id: control
 implicitWidth: horizontal ? 180 : 36; implicitHeight: horizontal ? 36 : 180
 padding: Material.spacing
 background: Rectangle {
  x: control.leftPadding + (control.horizontal ? 0 : (control.availableWidth-width)/2)
  y: control.topPadding + (control.horizontal ? (control.availableHeight-height)/2 : 0)
  width: control.horizontal ? control.availableWidth : Material.meterHeight
  height: control.horizontal ? Material.meterHeight : control.availableHeight
  radius: Material.meterHeight/2; color: Material.border
  Rectangle {
   x: control.horizontal && control.mirrored ? parent.width-width : 0
   y: control.horizontal ? 0 : parent.height-height
   width: control.horizontal ? control.position * parent.width : parent.width
   height: control.horizontal ? parent.height : control.position * parent.height
   radius: parent.radius; color: Material.accent
  }
 }
 handle: Rectangle {
  x: control.leftPadding + (control.horizontal ? control.visualPosition * (control.availableWidth-width) : (control.availableWidth-width)/2)
  y: control.topPadding + (control.horizontal ? (control.availableHeight-height)/2 : control.visualPosition * (control.availableHeight-height))
  implicitWidth: Material.thumbSize; implicitHeight: Material.thumbSize
  radius: width/2; color: Material.foreground
  border.width: control.visualFocus ? 2 : 0; border.color: Material.accent
 }
}
