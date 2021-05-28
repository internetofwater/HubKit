import { FieldComponent } from "./fieldcomponent";

export interface FieldModel {
    model:string;
    param:string;
    field_name: string;
    field_label: string;
    field_help: string;
    field_order: number;
    config_field_name: string;
    field_placeholder: string;
    is_editable: boolean;
    is_custom: boolean;
    is_required: boolean;
    is_listed: boolean;
    component:FieldComponent;
  }