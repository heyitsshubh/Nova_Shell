import { Linking } from 'react-native';
import { BasePlugin, PluginConfig } from './PluginManager';

export class OpenAppPlugin implements BasePlugin {
  config: PluginConfig = {
    name: 'OpenAppPlugin',
    description: 'Opens external applications installed on the device (like WhatsApp, Settings, etc.).',
    permissions: []
  };

  async execute(params: Record<string, any>): Promise<any> {
    const appName = params.appName?.toLowerCase();
    if (!appName) {
      throw new Error('App name is required');
    }

    // Mapping of common app names to their URL schemes
    const appSchemes: Record<string, string> = {
      'whatsapp': 'whatsapp://app',
      'settings': 'app-settings:',
      'youtube': 'youtube://',
      'instagram': 'instagram://',
      'twitter': 'twitter://',
      'mail': 'mailto:'
    };

    const scheme = appSchemes[appName];

    if (!scheme) {
      return { status: 'error', message: `I don't know how to open ${appName} yet.` };
    }

    try {
      const supported = await Linking.canOpenURL(scheme);
      if (supported) {
        await Linking.openURL(scheme);
        return { status: 'success', app: appName, message: `Opened ${appName}` };
      } else {
        return { status: 'error', app: appName, message: `${appName} is not installed or cannot be opened.` };
      }
    } catch (error) {
      return { status: 'error', app: appName, message: `Failed to open ${appName}.` };
    }
  }
}
