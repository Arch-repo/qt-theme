// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.ScrollBar {
 id: control
 implicitWidth: horizontal ? 120 : 8; implicitHeight: horizontal ? 8 : 120
 padding: 2
 contentItem: Rectangle { radius: 3; color: control.pressed ? Material.accent : Material.muted; opacity: control.active ? .65 : .3 }
}
