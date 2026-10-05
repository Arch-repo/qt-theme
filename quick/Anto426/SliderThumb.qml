// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
Rectangle {
 property var control
 property real position: 0
 property bool focused: false
 implicitWidth: Material.thumbSize; implicitHeight: Material.thumbSize
 radius: width/2; color: Material.foreground
 border.width: 1; border.color: focused ? Material.accent : Material.border
 x: control.leftPadding + (control.horizontal ? position*(control.availableWidth-width) : (control.availableWidth-width)/2)
 y: control.topPadding + (control.horizontal ? (control.availableHeight-height)/2 : position*(control.availableHeight-height))
}
