/**
 * app.js
 * Shared utilities used across every JobTrack page:
 *   - JWT token storage (localStorage)
 *   - authenticated fetch() wrapper with automatic access-token refresh
 *   - small UI helpers (alerts, status badges, date formatting)
 *
 * Authentication model:
 *   JobTrack's pages are rendered by Django (no JS framework), but all data
 *   comes from the DRF JSON API. On login/register, the API returns a JWT
 *   access + refresh token pair which is stored in localStorage. Every
 *   subsequent API call attaches "Authorization: Bearer <access_token>".
 *   If a request comes back 401, we try to refresh the access token once
 *   using the refresh token; if that also fails, the user is sent back to
 *   the login page.
 */

const JobTrack = (() => {
  const ACCESS_KEY = "jobtrack_access_token";
  const REFRESH_KEY = "jobtrack_refresh_token";
  const USER_KEY = "jobtrack_user";

  function getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  }

  function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  }

  function getCurrentUser() {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  }

  function setSession({ access, refresh, user }) {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
    if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function clearSession() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
  }

  function isLoggedIn() {
    return !!getAccessToken();
  }

  /** Redirect to /login/ if there is no access token. Call at the top of every protected page. */
  function requireAuth() {
    if (!isLoggedIn()) {
      window.location.href = "/login/";
      return false;
    }
    return true;
  }

  async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return false;
    try {
      const res = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      setSession({ access: data.access });
      return true;
    } catch (err) {
      return false;
    }
  }

  /**
   * Authenticated fetch wrapper.
   * Usage: JobTrack.apiFetch('/api/applications/', { method: 'GET' })
   * Automatically JSON-encodes `body` objects and parses JSON responses.
   */
  async function apiFetch(url, options = {}) {
    const opts = { ...options };
    opts.headers = { ...(options.headers || {}) };

    if (opts.body && typeof opts.body !== "string") {
      opts.body = JSON.stringify(opts.body);
      opts.headers["Content-Type"] = "application/json";
    }

    const access = getAccessToken();
    if (access) {
      opts.headers["Authorization"] = `Bearer ${access}`;
    }

    let response = await fetch(url, opts);

    if (response.status === 401 && getRefreshToken()) {
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        opts.headers["Authorization"] = `Bearer ${getAccessToken()}`;
        response = await fetch(url, opts);
      }
    }

    if (response.status === 401) {
      clearSession();
      window.location.href = "/login/";
      throw new Error("Session expired. Please log in again.");
    }

    let data = null;
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      data = await response.json().catch(() => null);
    }

    if (!response.ok) {
      const error = new Error((data && (data.detail || JSON.stringify(data.errors))) || "Request failed.");
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  }

  function logout() {
    const refresh = getRefreshToken();
    if (refresh) {
      // Best-effort server-side logout; ignore failures.
      fetch("/api/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getAccessToken()}`,
        },
        body: JSON.stringify({ refresh }),
      }).catch(() => {});
    }
    clearSession();
    window.location.href = "/login/";
  }

  /** Stores a one-time message to show after a redirect (e.g. "Application added successfully"). */
  function setFlash(message, type = "success") {
    sessionStorage.setItem("jobtrack_flash", JSON.stringify({ message, type }));
  }

  /** Reads and clears the flash message, rendering it into the given container if present. */
  function consumeFlash(containerId) {
    const raw = sessionStorage.getItem("jobtrack_flash");
    if (!raw) return;
    sessionStorage.removeItem("jobtrack_flash");
    try {
      const { message, type } = JSON.parse(raw);
      showAlert(containerId, message, type);
    } catch (err) { /* ignore malformed flash data */ }
  }

  function showAlert(containerId, message, type = "danger") {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
  }

  function clearAlert(containerId) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = "";
  }

  /** Renders DRF field errors (e.g. {"job_title": ["Job title is required."]}) as a readable list. */
  function formatErrors(errorData) {
    if (!errorData) return "Something went wrong. Please try again.";
    if (typeof errorData === "string") return errorData;
    if (errorData.detail && !errorData.errors) return errorData.detail;

    const errors = errorData.errors || errorData;
    const messages = [];
    for (const field in errors) {
      const value = errors[field];
      const text = Array.isArray(value) ? value.join(" ") : value;
      messages.push(`<strong>${field}:</strong> ${text}`);
    }
    return messages.length ? messages.join("<br>") : "Something went wrong. Please try again.";
  }

  const STATUS_BADGES = {
    Applied: "badge-status-applied",
    Shortlisted: "badge-status-shortlisted",
    Interview: "badge-status-interview",
    Selected: "badge-status-selected",
    Rejected: "badge-status-rejected",
    Withdrawn: "badge-status-withdrawn",
  };

  function statusBadge(status) {
    const cls = STATUS_BADGES[status] || "bg-secondary";
    return `<span class="badge status-badge ${cls}">${status}</span>`;
  }

  const PRIORITY_BADGES = {
    Low: "bg-secondary-subtle text-secondary-emphasis",
    Medium: "bg-info-subtle text-info-emphasis",
    High: "bg-danger-subtle text-danger-emphasis",
  };

  function priorityBadge(priority) {
    const cls = PRIORITY_BADGES[priority] || "bg-secondary";
    return `<span class="badge ${cls}">${priority}</span>`;
  }

  function formatDate(value) {
    if (!value) return "-";
    const d = new Date(value + "T00:00:00");
    if (isNaN(d)) return value;
    return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
  }

  function formatTime(value) {
    if (!value) return "-";
    const [h, m] = value.split(":");
    const d = new Date();
    d.setHours(parseInt(h, 10), parseInt(m, 10));
    return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
  }

  function formatCurrency(value) {
    if (value === null || value === undefined || value === "") return "-";
    return "₹" + Number(value).toLocaleString(undefined, { maximumFractionDigits: 0 });
  }

  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function initNavbar() {
    const user = getCurrentUser();
    const nameEl = document.getElementById("navbarUserName");
    if (nameEl && user) nameEl.textContent = user.full_name;

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });

    // Highlight the active nav link based on the current path.
    const path = window.location.pathname;
    document.querySelectorAll(".navbar-nav .nav-link[data-nav]").forEach((link) => {
      const target = link.getAttribute("data-nav");
      if (target === "/" ? path === "/" : path.startsWith(target)) {
        link.classList.add("active");
      }
    });
  }

  return {
    getAccessToken,
    getRefreshToken,
    getCurrentUser,
    setSession,
    clearSession,
    isLoggedIn,
    requireAuth,
    apiFetch,
    logout,
    showAlert,
    clearAlert,
    setFlash,
    consumeFlash,
    formatErrors,
    statusBadge,
    priorityBadge,
    formatDate,
    formatTime,
    formatCurrency,
    escapeHtml,
    initNavbar,
  };
})();

document.addEventListener("DOMContentLoaded", () => {
  JobTrack.initNavbar();
});
