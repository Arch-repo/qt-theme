// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.RangeSlider {
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
   x: control.horizontal ? Math.min(control.first.visualPosition,control.second.visualPosition)*parent.width : 0
   y: control.horizontal ? 0 : Math.min(control.first.visualPosition,control.second.visualPosition)*parent.height
   width: control.horizontal ? Math.abs(control.second.position-control.first.position)*parent.width : parent.width
   height: control.horizontal ? parent.height : Math.abs(control.second.position-control.first.position)*parent.height
   radius: Material.meterHeight/2; color: Material.accent
  }
 }
 first.handle: SliderThumb { control: control; position: control.first.visualPosition; focused: control.first.pressed || control.visualFocus }
 second.handle: SliderThumb { control: control; position: control.second.visualPosition; focused: control.second.pressed || control.visualFocus }
}
