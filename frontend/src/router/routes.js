import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import UserProfile from "@/pages/UserProfile.vue";
import Notifications from "@/pages/Notifications.vue";
import Icons from "@/pages/Icons.vue";
import Typography from "@/pages/Typography.vue";
import TransactionsList from "@/pages/TransactionsList.vue";
import RewardsList from "@/pages/RewardsList.vue";

import About from "@/pages/About.vue";
import Login from "@/auth/Login.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "profile",
        name: "profile",
        component: UserProfile,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "table-list",
        name: "table-list",
        component: TransactionsList,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "notifications",
        name: "notifications",
        component: Notifications
      },
      {
        path: "icons",
        name: "icons",
        component: Icons
      },
      {
        path: "typography",
        name: "typography",
        component: Typography
      },
      {
        path: "rewards",
        name: "rewards",
        component: RewardsList
      },
      {
        path: "about",
        name: "about",
        component: About
      },
      {
        path: "login",
        name: "login",
        component: Login
      }
    ]
  },
  { path: "*", component: NotFound }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
