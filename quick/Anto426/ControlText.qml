// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
Text {
 property var control
 text: control.text; font: control.font
 color: control.enabled ? Material.foreground : Material.muted
 verticalAlignment: Text.AlignVCenter
 elide: Text.ElideRight
 leftPadding: control.indicator && !control.mirrored ? control.indicator.width + control.spacing : 0
 rightPadding: control.indicator && control.mirrored ? control.indicator.width + control.spacing : 0
}
