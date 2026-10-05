// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.RadioDelegate {
 id: control
 implicitWidth: Math.max(implicitContentWidth + leftPadding + rightPadding, implicitIndicatorWidth + leftPadding + rightPadding)
 implicitHeight: Math.max(36, implicitContentHeight + topPadding + bottomPadding)
 padding: Material.spacing; spacing: Material.spacing; hoverEnabled: true
 indicator: ToggleIndicator { control: control; kind: "radio" }
 contentItem: ControlText { control: control }
 background: Surface { flat: true; hovered: control.hovered; focused: control.visualFocus }
}
