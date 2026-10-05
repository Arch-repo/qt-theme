// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.ComboBox {
 id: control
 implicitWidth: 180; implicitHeight: 40
 padding: Material.padding; rightPadding: Material.padding + 22
 background: Surface { focused: control.visualFocus; pressed: control.down; hovered: control.hovered }
 indicator: Text { text: "⌄"; color: Material.foreground; x: control.width-width-control.padding; y: (control.height-height)/2; font.pixelSize: 18 }
 contentItem: T.TextField {
  text: control.editable ? control.editText : control.displayText
  enabled: control.editable; autoScroll: control.editable; readOnly: control.down
  inputMethodHints: control.inputMethodHints; validator: control.validator; selectByMouse: control.selectTextByMouse
  color: Material.foreground; selectionColor: Material.accent; selectedTextColor: Material.selectedForeground
  verticalAlignment: TextInput.AlignVCenter
 }
 delegate: ItemDelegate { width: control.width; text: control.textAt(index); highlighted: control.highlightedIndex === index }
 popup: Popup {
  y: control.height + 4; width: control.width
  implicitHeight: Math.min(contentItem.implicitHeight + topPadding + bottomPadding, 360)
  contentItem: ListView { clip: true; implicitHeight: contentHeight; model: control.delegateModel; currentIndex: control.highlightedIndex; highlightMoveDuration: 0 }
 }
}
