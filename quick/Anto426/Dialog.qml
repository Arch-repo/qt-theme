// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.Dialog {
 id: control
 implicitWidth: Math.max(160, implicitContentWidth + leftPadding + rightPadding)
 implicitHeight: Math.max(implicitBackgroundHeight, implicitContentHeight + topPadding + bottomPadding + implicitHeaderHeight + implicitFooterHeight)
 padding: Material.padding; margins: Material.padding
 background: Surface { radius: Material.cardRadius; color: Material.popover }
 header: Text { text: control.title; visible: control.title; font: control.font; color: Material.foreground; padding: Material.padding }
 footer: DialogButtonBox { visible: count > 0; standardButtons: control.standardButtons }
}
