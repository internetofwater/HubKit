export interface TransformConfig {
    settings:TransformConfigSetting | string;
}


export interface TransformConfigSetting{
    [key: string]: string | boolean | number;
}
