/** @odoo-module **/
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MergeContactsModal extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.notification = useService("notification");
        this.state = useState({
            selectedPartners: [],
            mainPartnerId: null,
        });
        this.modalRef = useRef("mergeContactsModal");  // Create ref
        this.loadSelectedPartners();
    }

    async loadSelectedPartners() {
        console.log(this.props.action.params.selectedIds);
        const selectedIds = this.props.action.params.selectedIds;
        if (!selectedIds || selectedIds.length < 2) {
            this.notification.add( "Select at least two contacts to merge.", {  // Use notification service
                title: "Error",
                type: "danger",
            });
            return;
        }
        console.log(selectedIds);

        try {
        const partners = await this.orm.read("res.partner", selectedIds, ["name", "email", "phone", "street"]);
        this.state.selectedPartners = partners;
        if (partners.length > 0) {
            const firstPartner = partners[0];
        }
        this.state.mainPartnerId = partners[0]?.id;
         } catch (error) {
                this.notification.add("Error loading partners.", {
                    title: "Error",
                    type: "danger",
                });
         }
    }

    async mergeContacts() {
        try {
            // Подготовка данных
            const partnerIds = this.props.action.params.selectedIds;
            const mainPartnerId = this.state.mainPartnerId;

            // Вызов контроллера
            const result = await this.rpc("/partner/merge", {
                partner_ids: partnerIds,
                main_partner_id: mainPartnerId,
            });

            console.log("Controller result:", result);

            if (result.success) {
                this.notification.add(result.message, {
                    title: "Success",
                    type: "success",
                });
                this.closeModal();
            } else {
                this.notification.add(result.message, {
                    title: "Error",
                    type: "danger",
                });
            }
        } catch (error) {
            console.error("Error calling controller:", error);
            this.notification.add("An unexpected error occurred.", {
                title: "Error",
                type: "danger",
            });
        }
    }

    async closeModal() {
        setTimeout(() => {
            console.log("closeModal called, this.modalRef.el:", this.modalRef.el);
            if (this.modalRef.el) {
                const modal = this.modalRef.el.closest('.modal');
                if (modal) {
                    modal.classList.remove('show');
                    modal.style.display = 'none';
                    this.state.selectedPartners = [];
                    this.state.mainPartnerId = null;
                }
            } else {
                console.error("this.modalRef.el is undefined in closeModal");
            }
        }, 100);
    }

}

MergeContactsModal.props = {
    params: { type: Object, required: true },
};
MergeContactsModal.template = "PartnerMergeWizard.MergeContactsModal";
registry.category("actions").add("merge_contacts_modal", MergeContactsModal);
