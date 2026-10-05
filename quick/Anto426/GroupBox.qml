// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.GroupBox {
 id: control
 implicitWidth: Math.max(implicitContentWidth + leftPadding + rightPadding, implicitLabelWidth + leftPadding + rightPadding)
 implicitHeight: implicitContentHeight + topPadding + bottomPadding
 padding: Material.padding; topPadding: padding + (title ? implicitLabelHeight + Material.spacing : 0)
 label: Text { x: control.leftPadding; y: control.padding; width: control.availableWidth; text: control.title; font: control.font; color: Material.foreground; elide: Text.ElideRight }
 background: Surface { radius: Material.cardRadius }
}
