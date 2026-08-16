import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import MainLayout from "@/layout/index.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: MainLayout,
    redirect: "/chat",
    children: [
      {
        path: "chat",
        name: "Chat",
        component: () => import("@/views/chat/index.vue"),
        meta: { title: "AI 烹饪问答" },
      },
      {
        path: "knowledge",
        name: "Knowledge",
        component: () => import("@/views/knowledge-base/RecipeBrowse.vue"),
        meta: { title: "菜谱与知识库" },
      },
      {
        path: "recommend",
        name: "Recommend",
        component: () => import("@/views/recommend/index.vue"),
        meta: { title: "今日吃什么" },
      },
      {
        path: "favorites",
        name: "Favorites",
        component: () => import("@/views/favorites/index.vue"),
        meta: { title: "我的收藏" },
      },
      {
        path: "manage",
        name: "Manage",
        component: () => import("@/views/recipe-manage/index.vue"),
        meta: { title: "菜谱知识管理" },
      },
      {
        path: "settings",
        name: "Settings",
        component: () => import("@/views/settings/index.vue"),
        meta: { title: "系统设置" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(), // Electron 中推荐使用 Hash 路由，避免刷新 404
  routes,
});

export default router;
