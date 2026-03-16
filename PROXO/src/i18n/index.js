import { createI18n } from 'vue-i18n'
import id from './id'
import en from './en'

const i18n = createI18n({
  legacy: false,
  locale: 'id',
  fallbackLocale: 'en',
  messages: { id, en }
})

export default i18n