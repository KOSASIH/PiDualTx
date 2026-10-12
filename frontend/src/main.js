import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import { createI18n } from 'vue-i18n';
import en from './i18n/en';
import id from './i18n/id';

// Configure internationalization (i18n) - Cijoho Genesis
const messages = { en, id };

const i18n = createI18n({
  legacy: false,
  locale: 'en', // default language
  fallbackLocale: 'en',
  messages,
});

// Create Vue app - God-Chain ID 314159
const app = createApp(App);

app.use(store);
app.use(i18n);
app.mount('#app');
