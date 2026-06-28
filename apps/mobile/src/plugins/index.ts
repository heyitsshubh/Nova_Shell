import { pluginManager } from './PluginManager';
import { BatteryPlugin } from './BatteryPlugin';
import { FlashlightPlugin } from './FlashlightPlugin';

// Register all local device plugins
pluginManager.register(new BatteryPlugin());
pluginManager.register(new FlashlightPlugin());
// Add more local plugins here like FlashlightPlugin, StoragePlugin, etc.

export { pluginManager };
