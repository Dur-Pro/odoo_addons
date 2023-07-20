/** @odoo-module **/

import {
    MessageListController,
    MessageListModel,
    MessageListRenderer,
} from "./list_mixin.esm";
import ListController from "web.ListController";
import ListModel from "web.ListModel";
import ListRenderer from "web.ListRenderer";
import ListView from "web.ListView";
import viewRegistry from "web.view_registry";

const MailMessageUpdateListController = ListController.extend(MessageListController);

const MailMessageUpdateListModel = ListModel.extend(MessageListModel);

const MailMessageUpdateListRenderer = ListRenderer.extend(MessageListRenderer);

export const MailMessageUpdateListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: MailMessageUpdateListController,
        Model: MailMessageUpdateListModel,
        Renderer: MailMessageUpdateListRenderer,
    }),
});

viewRegistry.add("mail_messages_update_list", MailMessageUpdateListView);
