import { TransformConfig } from "../interfaces/transformconfig"

export const TRANSFORM_CONFIG_SETTINGS: TransformConfig = 
    { 
        settings:{
            source:"",
            data_structure:"One Sensor per row",
            type:"Excel",	
            file:"transform_config.json",
            thing_name_column:"",
            thing_description_column:"",
            thing_lng_column:"",
            thing_lat_column:"",
        },
        Things:{

            fields:[
                // {
                //     type:"single",
                //     mapped_to:"name",
                //     field_source_type:"text",
                //     field_name:"Alternate Well Name",
                //     sheet:"Test Data",
                //     value_type:"sheet",
                //     value:"A2",
                //     data_source:"sheet"
                // },
                // {
                //     type:"single",
                //     mapped_to:"description",
                //     field_source_type:"text",
                //     field_name:"Geological Description",
                //     sheet:"Test Data",
                //     value_type:"sheet",
                //     value:"O2",
                //     data_source:"sheet"
                // },
                ],
            name_of_thing:"",
            description:"",
        },
                Locations:{
                    iot:"",
                    location_name:"",
                    lat:"",
                    lng:"",
                },
                Datastreams:{
                }

        
    }


