// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.MenuBar {
 id: control
 implicitWidth: implicitContentWidth + leftPadding + rightPadding
 implicitHeight: implicitContentHeight + topPadding + bottomPadding
 padding: Material.spacing; spacing: Material.spacing
 delegate: MenuBarItem {}
 contentItem: ListView { model: control.contentModel; spacing: control.spacing; orientation: ListView.Horizontal; boundsBehavior: Flickable.StopAtBounds; implicitWidth: contentWidth; implicitHeight: 40; clip: true }
 background: Surface { flat: true }
}
