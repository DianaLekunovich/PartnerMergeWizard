/** @odoo-module **/
import { Component, useState, useRef, onMounted, useEnv } from "@odoo/owl";
import { useService, useBus } from "@web/core/utils/hooks";
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
    this.modalRef = useRef("mergeContactsModal"); // Create ref
    this.env = useEnv();
    this.loadSelectedPartners();
  }

  async loadSelectedPartners() {
    const selectedIds = this.props.selectedIds;
    if (!selectedIds || selectedIds.length < 2) {
      this.notification.add("Select at least two contacts to merge.", {
        // Use notification service
        title: "Error",
        type: "danger",
      });
      return;
    }

    try {
      const partners = await this.orm.read("res.partner", selectedIds, [
        "name",
        "email",
        "phone",
        "street",
      ]);
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
      // Preparing data
      const partnerIds = this.props.selectedIds;
      const mainPartnerId = this.state.mainPartnerId;

      // Call controller
      const result = await this.rpc("/partner/merge", {
        partner_ids: partnerIds,
        main_partner_id: mainPartnerId,
      });

      if (result.type === "ir.actions.act_window") {
        const action = {
          name: "Choose Email",
          type: "ir.actions.act_window",
          res_model: "partner.merge.email.wizard",
          view_mode: "form",
          views: [[false, "form"]],
          target: "new",
          context: {
            default_partner_merge_wizard_id:
              result.context.default_partner_merge_wizard_id,
            partner_ids_to_archive: result.context.partner_ids_to_archive,
          },
        };
        this.actionService.doAction(action, {
          onClose: () => {
            this.env.bus.trigger("reload_contacts");
            this.closeModal();
          },
        });
      } else if (result.success) {
        this.notification.add(result.message, {
          title: "Success",
          type: "success",
        });
        this.env.bus.trigger("reload_contacts");
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
    if (this.modalRef.el) {
      const modal = this.modalRef.el.closest(".modal");
      if (modal) {
        modal.classList.remove("show");
        modal.style.display = "none";
        this.state.selectedPartners = [];
        this.state.mainPartnerId = null;
      }
    } else {
      console.error("this.modalRef.el is undefined in closeModal");
    }
  }
}

MergeContactsModal.props = {
  params: { type: Object, required: true },
};
MergeContactsModal.template = "PartnerMergeWizard.MergeContactsModal";
registry.category("actions").add("merge_contacts_modal", MergeContactsModal);
