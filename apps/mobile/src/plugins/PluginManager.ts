import { BatteryPlugin } from './BatteryPlugin';
import { FlashlightPlugin } from './FlashlightPlugin';
import { OpenAppPlugin } from './OpenAppPlugin';

export interface PluginConfig {
  name: string;
  description: string;
  permissions: string[];
}

export interface BasePlugin {
  config: PluginConfig;
  execute(params: Record<string, any>): Promise<any>;
}

class PluginManager {
  private plugins: Map<string, BasePlugin> = new Map();

  constructor() {
    this.register(new BatteryPlugin());
    this.register(new FlashlightPlugin());
    this.register(new OpenAppPlugin());
  }

  register(plugin: BasePlugin) {
    this.plugins.set(plugin.config.name, plugin);
  }

  getPlugin(name: string): BasePlugin | undefined {
    return this.plugins.get(name);
  }

  async executePlugin(name: string, params: Record<string, any>): Promise<any> {
    const plugin = this.plugins.get(name);
    if (!plugin) {
      throw new Error(`Plugin ${name} not found locally on the device.`);
    }
    
    // Permission validation could occur here before execution
    return await plugin.execute(params);
  }
}

export const pluginManager = new PluginManager();
