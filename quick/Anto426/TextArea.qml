// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.TextArea {
 id: control
 implicitWidth: 180
 implicitHeight: Math.max(80, contentHeight + topPadding + bottomPadding)
 padding: Material.padding
 color: Material.foreground; selectionColor: Material.accent; selectedTextColor: Material.selectedForeground
 placeholderTextColor: Material.muted; selectByMouse: true
 wrapMode: TextEdit.Wrap
 background: Surface { focused: control.activeFocus; hovered: control.hovered }
 Text {
  x: control.leftPadding; y: control.topPadding
  width: control.availableWidth; height: control.availableHeight
  text: control.placeholderText; font: control.font; color: control.placeholderTextColor
  verticalAlignment: Text.AlignTop
  visible: !control.length && !control.preeditText; elide: Text.ElideRight
 }
}
