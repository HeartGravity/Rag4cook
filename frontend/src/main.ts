import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "@/assets/styles/main.scss"; // 引入全局样式
import router from "./router";
import App from "./App.vue";

const app = createApp(App);

app.use(ElementPlus);
app.use(router);
app.mount("#app");
