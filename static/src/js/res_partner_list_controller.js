/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useBus, useService } from "@web/core/utils/hooks";
import { MergeContactsModal } from "./merge_contacts_modal";

export class ContactsListController extends ListController {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
        this.notification = useService("notification");
        useBus(this.env.bus, "reload_contacts", this.reloadContacts);
    }

    async showMergeModal() {
        const ids = await this.getSelectedResIds();

        if (ids.length < 2) {
            this.notification.add("Please select at least two partners to merge.", { // Используем сервис notification
                title: "Error",
                type: "danger",
                sticky: false,
            });
            return;
        }

        this.dialogService.add(MergeContactsModal, {selectedIds: ids, });

    }

    reloadContacts() {
        this.model.load();
    }

}

registry.category("views").add("button_in_contacts", {
    model: "res.partner",  // Применяем только для контактов
    ...listView,
    Controller: ContactsListController,
    buttonTemplate: "button_contacts.ListView.Buttons",  // Используем тот же шаблон кнопки
});
