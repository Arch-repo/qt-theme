// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.Drawer {
 id: control
 implicitWidth: Math.max(180, implicitContentWidth + leftPadding + rightPadding)
 implicitHeight: implicitContentHeight + topPadding + bottomPadding
 padding: Material.padding
 background: Surface { radius: Material.cardRadius; color: Material.popover }
}
