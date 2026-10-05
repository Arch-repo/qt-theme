// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.PageIndicator {
 id: control
 implicitWidth: implicitContentWidth + leftPadding + rightPadding; implicitHeight: 20
 padding: 4; spacing: Material.spacing
 delegate: Rectangle { implicitWidth: 8; implicitHeight: 8; radius: 4; color: index === control.currentIndex ? Material.accent : Material.border }
 contentItem: Row { spacing: control.spacing; Repeater { model: control.count; delegate: control.delegate } }
}
