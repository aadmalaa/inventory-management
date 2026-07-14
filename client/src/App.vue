<template>
  <div class="app-shell" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <aside class="sidebar">
      <div class="logo">
        <h1>{{ t('nav.companyName') }}</h1>
        <span class="subtitle">{{ t('nav.subtitle') }}</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" :class="{ active: $route.path === '/' }" :title="t('nav.overview')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>
        <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }" :title="t('nav.inventory')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }" :title="t('nav.orders')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect><line x1="9" y1="12" x2="15" y2="12"></line><line x1="9" y1="16" x2="15" y2="16"></line></svg>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>
        <router-link to="/spending" :class="{ active: $route.path === '/spending' }" :title="t('nav.finance')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>
        <router-link to="/demand" :class="{ active: $route.path === '/demand' }" :title="t('nav.demandForecast')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }" :title="t('nav.reports')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>
      </nav>
      <button
        class="sidebar-toggle"
        @click="toggleSidebar"
        :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        aria-label="Toggle sidebar"
      >
        <!-- chevrons-left; CSS rotates it 180deg when collapsed so it points right -->
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="11 17 6 12 11 7"></polyline><polyline points="18 17 13 12 18 7"></polyline></svg>
      </button>
      <div class="sidebar-footer">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>
    <div class="main-area">
      <FilterBar />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Large-screen sidebar collapse (user toggle; <1024px auto-collapse stays pure CSS).
    // localStorage only stores strings, so compare against 'true' - anything else
    // (null, garbage) falls back to expanded.
    const sidebarCollapsed = ref(localStorage.getItem('sidebar-collapsed') === 'true')

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebar-collapsed', String(sidebarCollapsed.value))
    }

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      showProfileDetails,
      showTasks,
      sidebarCollapsed,
      toggleSidebar,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
:root {
  /* Color - surfaces */
  --color-bg: #f8fafc;            /* page background (body) */
  --color-surface: #ffffff;       /* cards, sidebar, tables */
  --color-hover: #f1f5f9;         /* hover fills */

  /* Color - borders */
  --color-border: #e2e8f0;
  --color-border-strong: #cbd5e1; /* inputs, hovered cards */

  /* Color - text */
  --color-text: #0f172a;
  --color-text-secondary: #334155;
  --color-text-muted: #64748b;

  /* Color - brand/accent */
  --color-primary: #2563eb;
  --color-primary-soft: #eff6ff;  /* active nav tint */

  /* Color - status */
  --color-success: #059669;
  --color-warning: #ea580c;
  --color-danger: #dc2626;
  --color-info: #2563eb;

  /* Color - badge tints (existing badge pairs) */
  --tint-success-bg: #d1fae5;  --tint-success-text: #065f46;
  --tint-warning-bg: #fed7aa;  --tint-warning-text: #92400e;
  --tint-danger-bg: #fecaca;   --tint-danger-text: #991b1b;
  --tint-info-bg: #dbeafe;     --tint-info-text: #1e40af;

  /* Spacing - 4px/8px scale (rem, 16px base) */
  --space-1: 0.25rem;  /* 4px  */
  --space-2: 0.5rem;   /* 8px  */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.5rem;   /* 24px */
  --space-6: 2rem;     /* 32px */
  --space-7: 3rem;     /* 48px */

  /* Layout */
  --sidebar-width: 240px;
  --sidebar-width-collapsed: 64px;

  /* Radius & shadow */
  --radius-sm: 6px;    /* buttons, badges, nav links */
  --radius-md: 10px;   /* cards, dropdowns */
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--color-bg);
  /* was #1e293b (slate-800, off-ramp): snapped to the secondary text token */
  color: var(--color-text-secondary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-shell {
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: var(--space-4) var(--space-3);
  z-index: 100;
  transition: width 0.2s ease; /* smooth user-toggled collapse */
}

.logo {
  /* stacks vertically now (was a horizontal baseline row in the old top nav) */
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: 0 var(--space-3);
}

.logo h1 {
  font-size: 1.063rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
  /* long company names (e.g. JA locale) truncate instead of wrapping;
     also keeps the h1 contained in the collapsed icon rail */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  /* required for ellipsis when .logo uses align-items: center (collapsed rail):
     centering makes flex children shrink-to-content, so an unconstrained h1
     would take its intrinsic width and bleed past the 64px sidebar */
  max-width: 100%;
}

.logo .subtitle {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-top: var(--space-5);
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.15s ease;
}

.sidebar-nav a svg {
  flex-shrink: 0; /* long labels must never squash the icon */
}

.sidebar-nav a:hover {
  color: var(--color-text);
  background: var(--color-hover);
}

.sidebar-nav a.active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  box-shadow: inset 2px 0 0 var(--color-primary); /* left indicator replaces the old bottom underline */
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  margin-top: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: none;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--color-text-muted);
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s ease;
}

.sidebar-toggle:hover {
  color: var(--color-text);
  background: var(--color-hover);
}

.sidebar-toggle svg {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.main-area {
  /* margin, not flex: keeps the body as the only scroll container */
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.2s ease; /* tracks the sidebar's width transition */
}

/* User-toggled collapse (large screens). Twin of the <1024px media query below -
   class selectors can't share a rule with @media, so keep the two blocks in sync. */
.app-shell.sidebar-collapsed .sidebar {
  width: var(--sidebar-width-collapsed);
  padding: var(--space-4) var(--space-2);
}

.app-shell.sidebar-collapsed .nav-label,
.app-shell.sidebar-collapsed .logo .subtitle {
  display: none;
}

.app-shell.sidebar-collapsed .logo {
  padding: 0;
  align-items: center;
}

.app-shell.sidebar-collapsed .sidebar-nav a {
  justify-content: center;
  padding: var(--space-2);
}

.app-shell.sidebar-collapsed .sidebar-toggle {
  justify-content: center;
  padding: var(--space-2);
}

/* chevrons-left flips to point right = "expand" affordance */
.app-shell.sidebar-collapsed .sidebar-toggle svg {
  transform: rotate(180deg);
}

/* Footer triggers at 64px: keep only the globe icon / avatar. Targets
   LanguageSwitcher/ProfileMenu markup classes from the global block (CSS-only,
   no component logic changes). .chevron only exists on the trigger buttons. */
.app-shell.sidebar-collapsed .sidebar-footer .language-label,
.app-shell.sidebar-collapsed .sidebar-footer .profile-name,
.app-shell.sidebar-collapsed .sidebar-footer .chevron {
  display: none;
}

.app-shell.sidebar-collapsed .sidebar-footer .language-button,
.app-shell.sidebar-collapsed .sidebar-footer .profile-button {
  justify-content: center;
  /* space-1, not space-2: the 32px avatar + 1px borders must fit the 48px inner rail */
  padding: var(--space-1);
}

.app-shell.sidebar-collapsed .main-area {
  margin-left: var(--sidebar-width-collapsed);
}

.main-content {
  flex: 1;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  padding: var(--space-5) var(--space-6);
}

/* Below 1024px the sidebar collapses to a pure-CSS icon rail (no JS toggle) */
@media (max-width: 1023px) {
  .sidebar {
    width: var(--sidebar-width-collapsed);
    padding: var(--space-4) var(--space-2);
  }

  .sidebar .nav-label,
  .sidebar .logo .subtitle {
    display: none;
  }

  .sidebar .logo {
    padding: 0;
    align-items: center;
  }

  .sidebar-nav a {
    justify-content: center;
    padding: var(--space-2);
  }

  /* Rail is forced below 1024px regardless of user preference - hide the toggle */
  .sidebar-toggle {
    display: none;
  }

  /* Twin of the .app-shell.sidebar-collapsed footer rules above */
  .sidebar-footer .language-label,
  .sidebar-footer .profile-name,
  .sidebar-footer .chevron {
    display: none;
  }

  .sidebar-footer .language-button,
  .sidebar-footer .profile-button {
    justify-content: center;
    padding: var(--space-1);
  }

  .main-area {
    margin-left: var(--sidebar-width-collapsed);
  }
}

.page-header {
  margin-bottom: var(--space-5);
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-1); /* was 0.375rem (6px): snapped down to the 4px scale */
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--color-text-muted);
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5); /* was 1.25rem (20px): snapped up to match card spacing */
  margin-bottom: var(--space-5);
}

.stat-card {
  background: var(--color-surface);
  padding: var(--space-5); /* was 1.25rem (20px): snapped up to match .card padding */
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-2); /* was 0.625rem (10px): snapped down to the 8px step */
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: var(--color-warning);
}

.stat-card.success .stat-value {
  color: var(--color-success);
}

.stat-card.danger .stat-value {
  color: var(--color-danger);
}

.stat-card.info .stat-value {
  color: var(--color-info);
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--space-5); /* was 1.25rem (20px): snapped up to the 24px step */
  margin-bottom: var(--space-5);
  transition: box-shadow 0.15s ease, border-color 0.15s ease;
}

.card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3); /* was 0.875rem (14px): snapped down to the 12px step */
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

th {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  font-weight: 600;
  /* was #475569 (slate-600, off-ramp): snapped to the muted text token */
  color: var(--color-text-muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: var(--space-2) var(--space-3);
  border-top: 1px solid var(--color-hover); /* #f1f5f9 doubles as the hairline row divider */
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--color-bg); /* row hover reuses the page-bg tint (#f8fafc) */
}

.badge {
  display: inline-block;
  padding: var(--space-1) var(--space-3); /* was 0.313rem (5px) vertical: snapped down to 4px */
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: var(--tint-success-bg);
  color: var(--tint-success-text);
}

.badge.warning {
  background: var(--tint-warning-bg);
  color: var(--tint-warning-text);
}

.badge.danger {
  background: var(--tint-danger-bg);
  color: var(--tint-danger-text);
}

.badge.info {
  background: var(--tint-info-bg);
  color: var(--tint-info-text);
}

.badge.increasing {
  background: var(--tint-success-bg);
  color: var(--tint-success-text);
}

.badge.decreasing {
  background: var(--tint-danger-bg);
  color: var(--tint-danger-text);
}

.badge.stable {
  /* indigo pair has no token equivalent - left as-is */
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: var(--tint-danger-bg);
  color: var(--tint-danger-text);
}

.badge.medium {
  background: var(--tint-warning-bg);
  color: var(--tint-warning-text);
}

.badge.low {
  background: var(--tint-info-bg);
  color: var(--tint-info-text);
}

.loading {
  text-align: center;
  padding: var(--space-7);
  color: var(--color-text-muted);
  font-size: 0.938rem;
}

.error {
  /* red-50 surface has no token equivalent - left as-is */
  background: #fef2f2;
  border: 1px solid var(--tint-danger-bg);
  color: var(--tint-danger-text);
  padding: var(--space-4);
  border-radius: 8px;
  margin: var(--space-4) 0;
  font-size: 0.938rem;
}
</style>
