// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import QtQuick.Templates 2.15 as T
T.SplitView {
 handle: Rectangle { implicitWidth: 6; implicitHeight: 6; color: T.SplitHandle.pressed ? Material.accent : Material.border }
}
