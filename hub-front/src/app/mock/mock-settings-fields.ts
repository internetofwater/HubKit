
import { Field } from '../interfaces/field';

export const SETTINGS_FIELDS: Field[] = [
  { id: 11, 
    datavalue:'excel', 
    field:{
      "field_name": "data_source",
      "field_label": "Data Source",
      "field_help": "",
      "field_order": 1,
      "field_placeholder":"",
      "component": {
          "name": "select",
          "options": {
              "values": [
                  'Excel',
                  'CSV'
              ]
          },
          "group": "Settings"
      },
      "is_editable": true,
      "is_custom": false,
      "is_required": false,
      "is_listed": false
    },
   

  },
  { id: 12, 
    datavalue:'Test Thing', 
    field:{}
  },
  { 
    id: 13, 
    datavalue:'Test Thing', 
  field:{}
 }
];