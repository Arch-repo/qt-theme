// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.SpinBox {
 id: control
 implicitWidth: 160; implicitHeight: 40
 padding: Material.padding; leftPadding: padding + 24; rightPadding: padding + 24
 validator: IntValidator { bottom: Math.min(control.from,control.to); top: Math.max(control.from,control.to) }
 contentItem: T.TextField {
  text: control.textFromValue(control.value,control.locale); font: control.font
  color: Material.foreground; selectionColor: Material.accent; selectedTextColor: Material.selectedForeground
  horizontalAlignment: TextInput.AlignHCenter; verticalAlignment: TextInput.AlignVCenter
  readOnly: !control.editable; validator: control.validator; inputMethodHints: Qt.ImhFormattedNumbersOnly
 }
 background: Surface { focused: control.visualFocus }
 up.indicator: Text { text: "+"; width: 30; height: control.height; x: control.width-width; color: Material.foreground; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
 down.indicator: Text { text: "−"; width: 30; height: control.height; color: Material.foreground; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
}
