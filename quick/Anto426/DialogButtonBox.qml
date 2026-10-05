// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.DialogButtonBox {
 id: control
 implicitWidth: contentWidth + leftPadding + rightPadding
 implicitHeight: 40 + topPadding + bottomPadding
 spacing: Material.spacing; padding: Material.spacing
 delegate: Button { width: Math.max(80, implicitWidth) }
 contentItem: ListView { model: control.contentModel; spacing: control.spacing; orientation: ListView.Horizontal; boundsBehavior: Flickable.StopAtBounds; snapMode: ListView.SnapToItem }
}
