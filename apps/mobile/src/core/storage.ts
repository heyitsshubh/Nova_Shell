import { MMKV } from 'react-native-mmkv';

export const storage = new MMKV({
  id: 'novashell-storage',
  encryptionKey: 'secure-encryption-key-for-production' // TODO: In production, derive this securely
});
