// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
import QtQuick.Controls.impl 2.15 as Impl
Impl.IconLabel {
 property var control
 text: control.text
 font: control.font
 icon: control.icon
 display: control.display
 spacing: control.spacing
 mirrored: control.mirrored
 color: !control.enabled ? Material.muted : control.highlighted ? Material.selectedForeground : Material.foreground
}
