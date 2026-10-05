// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.ScrollIndicator {
 id: control
 implicitWidth: horizontal ? 100 : 6; implicitHeight: horizontal ? 6 : 100
 contentItem: Rectangle { radius: 3; color: Material.muted; opacity: control.active ? .65 : 0 }
}
