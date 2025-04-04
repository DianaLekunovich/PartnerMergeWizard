/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useBus, useService } from "@web/core/utils/hooks";
import { useState, onRendered } from "@odoo/owl";
import { MergeContactsModal } from "./merge_contacts_modal";

export class ContactsListController extends ListController {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
        this.notification = useService("notification");
        this.state = useState({ showMergeButton: false });
        this.state = useState({ showFindSimilarButton: false });

        useBus(this.env.bus, "reload_contacts", this.reloadContacts);
        onRendered(() => {
            this.updateMergeButton(); // Check selection after each render
            this.updateFindSimilarButton();
        });
    }

    async updateFindSimilarButton() {
        const selectedIds = await this.getSelectedResIds();
        this.state.showFindSimilarButton = selectedIds.length == 1;
    }

    async updateMergeButton() {
        const selectedIds = await this.getSelectedResIds();
        this.state.showMergeButton = selectedIds.length >= 2;
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

    async findSimilarContacts() {
        const selectedIds = await this.getSelectedResIds();
        if (selectedIds.length !== 1) {
            this.notification.add("Please select only one contact to find similar.", {
                title: "Error",
                type: "danger",
                sticky: false,
            });
            return;
        }

        try {
            const similarContacts = await this.rpc("/partner/find_similar", { partner_id: selectedIds[0] });
            this.actionService.doAction({
                name: "Similar Contacts",
                type: "ir.actions.act_window",
                res_model: "partner.similar.wizard",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: { default_partner_ids: similarContacts },
            });
        } catch (error) {
            this.notification.add("Error finding similar contacts.", {
                title: "Error",
                type: "danger",
                sticky: false,
            });
        }
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
