import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import eslintConfigPrettier from 'eslint-config-prettier'
import globals from 'globals'

export default [
  { ignores: ['dist/**', 'node_modules/**', 'public/**'] },
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      // Nama komponen satu kata (mis. HomeView) sengaja dipakai di proyek ini
      'vue/multi-word-component-names': 'off',
      // Variabel tak terpakai jadi peringatan, bukan error
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_', caughtErrorsIgnorePattern: '^_' }],
    },
  },
  // Matikan aturan ESLint yang bentrok dengan Prettier (harus paling akhir)
  eslintConfigPrettier,
]
