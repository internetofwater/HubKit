import { FieldComponent } from "./fieldcomponent";

export interface FieldModel {
    field_name: string;
    field_label: string;
    field_help: string;
    field_order: number;
    field_placeholder: string;
    is_editable: boolean;
    is_custom: boolean;
    is_required: boolean;
    is_listed: boolean;
    component:FieldComponent;
  }