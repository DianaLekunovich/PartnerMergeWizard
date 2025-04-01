/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useBus, useService } from "@web/core/utils/hooks";
import { MergeContactsModal } from "./merge_contacts_modal";

export class ContactsListController extends ListController {
    setup() {
        super.setup();
        this.actionService = useService("action");
    }

    async showMergeModal() {
        const ids2 = this.getSelectedResIds();
        const ids = await ids2;

        console.log(ids.length, ids2);
        if (ids.length < 2) {
            this.displayNotification({
                title: "Error",
                message: "Please select at least two partners to merge.1",
                type: "danger",
                sticky: false,
            });
            return;
        }

        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "merge_contacts_modal",
            params: { selectedIds: [...ids] },
        });
    }

}

registry.category("views").add("button_in_contacts", {
    model: "res.partner",  // Применяем только для контактов
    ...listView,
    Controller: ContactsListController,
    buttonTemplate: "button_contacts.ListView.Buttons",  // Используем тот же шаблон кнопки
});
