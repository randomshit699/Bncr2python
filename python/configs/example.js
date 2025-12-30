/**
* @author 小九九
* @name example
* @origin 小九九
* @team 小九九
* @version 1.0.0
* @description python插件配置页
* @public false
* @disable false
* @service true
* @priority 1
*/
const jsonSchema = {"type":"object","title":"jsonSchema示例","description":"描述文本","properties":{}};
const ConfigDB = new BncrPluginConfig(jsonSchema);
module.exports = {
    jsonSchema: jsonSchema,
    get: async () => {
        await ConfigDB.get();
        return ConfigDB.userConfig;
    },
};
