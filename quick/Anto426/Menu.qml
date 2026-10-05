// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.Menu {
 id: control
 implicitWidth: Math.max(160, implicitContentWidth + leftPadding + rightPadding)
 implicitHeight: Math.max(implicitBackgroundHeight, implicitContentHeight + topPadding + bottomPadding)
 delegate: MenuItem {}
 padding: Material.padding; margins: Material.padding
 background: Surface { radius: Material.cardRadius; color: Material.popover }
 contentItem: ListView { implicitHeight: contentHeight; model: control.contentModel; interactive: false; clip: true }
}
